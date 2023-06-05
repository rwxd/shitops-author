from author.logging import logger
from author.templates import template_podcast_from_blog_post, template_podcast_intro
from author.gpt import prompt_openai
from typing import Literal
from pydub import AudioSegment
from dataclasses import dataclass, asdict
import yaml
from tempfile import NamedTemporaryFile
import author.google_tts as google_tts
import author.az_tts as az_tts


@dataclass
class PodcastSinglePart:
    role: Literal['interviewer', 'engineer']
    text: str
    gender: Literal['male', 'female']


PodcastText = list[PodcastSinglePart]


def parse_podcast_content(content: str) -> PodcastText:
    parsed = yaml.safe_load(content)
    text: PodcastText = []
    for i in parsed:
        role = i['role'].lower()
        if role not in ['engineer', 'interviewer']:
            raise ValueError(f'Why is the role {role}')
        gender = i['gender'].lower()
        if gender not in ['male', 'female']:
            raise ValueError(f'We want male or female like voices not {gender}')
        text.append(PodcastSinglePart(role=role, text=i['text'], gender=gender))
    for role in ['interviewer', 'engineer']:
        for i in text:
            role_gender = ''
            if i.role == role:
                if role_gender == '':
                    role_gender = i.gender
                else:
                    if role_gender != i.gender:
                        raise ValueError(
                            f'Role {role} has multiple genders for voice {role_gender} and {i.gender}'
                        )
    logger.debug(text)
    return text


def mp3_bytes_to_audio_segment(input: bytes) -> AudioSegment:
    with NamedTemporaryFile(mode='wb') as f:
        f.write(input)
        return AudioSegment.from_mp3(f.name)


def create_podcast_intro() -> str:
    logger.info(f'Creating the podcast intro')
    intro_prompt = template_podcast_intro.render()
    return prompt_openai(intro_prompt)


def create_podcast_text_from_blog_post(text: str) -> PodcastText:
    podcast_prompt = template_podcast_from_blog_post.render(post=text)
    podcast_content = prompt_openai(podcast_prompt)
    parsed_podcast_text = parse_podcast_content(podcast_content)
    with open('parsed_podcast_text.yaml', 'w') as f:
        _ = yaml.safe_dump([asdict(i) for i in parsed_podcast_text], f)
    return parsed_podcast_text


def create_podcast_with_google_tts(
    intro_text: str, jingle: AudioSegment, podcast: PodcastText
) -> AudioSegment:
    logger.info(f'Creating podcast with google TTS')
    intro_audio = mp3_bytes_to_audio_segment(
        google_tts.create_audio_from_text(intro_text, voice='en-US-Neural2-G')
    )
    tracks: list[AudioSegment] = []
    for part in podcast:
        role = part.role
        gender = part.gender
        voice = 'en-US-Neural2-G'
        if role == 'engineer' and gender == 'male':
            voice = 'en-US-Neural2-J'
        elif role == 'engineer' and gender == 'female':
            voice = 'en-US-Neural2-E'
        elif role == 'interviewer' and gender == 'male':
            voice = 'en-US-Neural2-I'
        elif role == 'interviewer' and gender == 'female':
            voice = 'en-US-Neural2-H'
        logger.info(f'Creating audio for {role} with voice {voice}')
        audio_bytes = google_tts.create_audio_from_text(part.text, voice=voice)
        tracks.append(mp3_bytes_to_audio_segment(audio_bytes))
    return combine_audio_tracks_to_podcast(intro_audio, jingle, tracks)


def create_podcast_with_az_tts(
    intro_text: str, jingle: AudioSegment, podcast: PodcastText
) -> AudioSegment:
    logger.info(f'Creating podcast with azure TTS')
    intro_audio = mp3_bytes_to_audio_segment(
        az_tts.create_audio_from_text(intro_text, voice='en-US-JennyNeural')
    )
    tracks: list[AudioSegment] = []
    for part in podcast:
        role = part.role
        gender = part.gender
        voice = ''
        style = 'default'
        if role == 'engineer' and gender == 'male':
            voice = 'en-US-DavisNeural'
            style = 'chat'
        elif role == 'engineer' and gender == 'female':
            voice = 'en-US-AriaNeural'
            style = 'chat'
        elif role == 'interviewer' and gender == 'male':
            voice = 'en-US-GuyNeural'
            style = 'default'
        elif role == 'interviewer' and gender == 'female':
            voice = 'en-US-JennyNeural'
            style = 'chat'
        if voice == '':
            raise ValueError('No voice found for {role} & {gender}')
        logger.info(f'Creating audio for {role} with voice {voice}')
        audio_bytes = az_tts.create_audio_from_text(part.text, voice=voice, style=style)
        tracks.append(mp3_bytes_to_audio_segment(audio_bytes))
    return combine_audio_tracks_to_podcast(intro_audio, jingle, tracks)


def combine_audio_tracks_to_podcast(
    intro: AudioSegment, jingle: AudioSegment, podcast: list[AudioSegment]
) -> AudioSegment:
    logger.info(f'Combining intro, jingle and {len(podcast)} tracks')
    audio = intro + jingle
    logger.debug(f'Audio is {audio.duration_seconds} seconds long')
    logger.debug(f'Audio is {audio.duration_seconds} seconds long')
    for i in podcast:
        logger.debug(f'Audio is {audio.duration_seconds} seconds long')
        audio = audio + i
    audio = audio + jingle
    logger.info(f'Created {audio.duration_seconds} seconds of audio')
    return audio
