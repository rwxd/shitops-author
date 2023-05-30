from author.logging import logger
from author.templates import template_podcast_from_blog_post, template_podcast_intro
from author.gpt import prompt_openai
from author.misc import remove_mermaid_diagrams_from_text
from google.cloud import texttospeech
from typing import Sequence, Literal
from pydub import AudioSegment
from dataclasses import dataclass, asdict
from pathlib import Path
import yaml
from tempfile import NamedTemporaryFile


@dataclass
class PodcastSinglePart:
    role: Literal['interviewer', 'engineer']
    text: str
    gender: Literal['male', 'female']


PodcastText = list[PodcastSinglePart]


def create_podcast_from_blog_post(
    post: str, filename: str, jingle: Path
) -> AudioSegment:
    logger.debug(f'Creating audio for blog post to path {filename}')
    intro_content = create_podcast_intro()
    with open('podcast_intro.txt', 'w') as f:
        f.write(intro_content)
    intro_audio = mp3_bytes_to_audio_segment(
        create_audio_from_text(intro_content, voice='en-US-Neural2-G')
    )
    post = remove_mermaid_diagrams_from_text(post)
    logger.debug(f'Prompting for podcast')
    podcast_prompt = template_podcast_from_blog_post.render(post=post)
    podcast_content = prompt_openai(podcast_prompt)
    with open(filename.replace('.mp3', '.txt'), 'w') as f:
        f.write(podcast_content)
    parsed_podcast_text = parse_podcast_content(podcast_content)
    with open('parsed_podcast_text.yaml', 'w') as f:
        _ = yaml.safe_dump([asdict(i) for i in parsed_podcast_text], f)
    jingle_audio = AudioSegment.from_mp3(str(jingle))
    tracks = create_podcast_main_track(parsed_podcast_text)
    audio = combine_audio_tracks(intro_audio, jingle_audio, tracks)
    return audio


def parse_podcast_content(content: str) -> PodcastText:
    parsed = yaml.safe_load(content)
    text: PodcastText = []
    for i in parsed:
        role = i['role']
        if role not in ['engineer', 'interviewer']:
            raise ValueError(f'Why is the role {role}')
        gender = i['gender']
        if gender not in ['male', 'female']:
            raise ValueError(f'We want male or female like voices not {gender}')
        text.append(PodcastSinglePart(role=role, text=i['text'], gender=gender))
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


def create_podcast_main_track(podcast: PodcastText) -> list[AudioSegment]:
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
        audio_bytes = create_audio_from_text(part.text, voice=voice)
        tracks.append(mp3_bytes_to_audio_segment(audio_bytes))
    return tracks


def combine_audio_tracks(
    intro: AudioSegment, jingle: AudioSegment, podcast: list[AudioSegment]
):
    logger.info(f'Combining intro, jingle and {len(podcast)} tracks')
    audio = intro + jingle
    logger.debug(f'Audio is {audio.duration_seconds} seconds long')
    logger.debug(f'Audio is {audio.duration_seconds} seconds long')
    for i in podcast:
        logger.debug(f'Audio is {audio.duration_seconds} seconds long')
        audio = audio + i
    logger.info(f'Created {audio.duration_seconds} seconds of audio')
    return audio


def create_audio_from_text(
    text: str,
    voice: str = 'en-US-Neural2-A',
    language_code: str = 'en-US',
    # gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    audio_encoding=texttospeech.AudioEncoding.MP3,
) -> bytes:
    logger.info(f'Creating audio for "{text}"')
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=audio_encoding)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )

    return response.audio_content


def list_languages():
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices()
    languages = unique_languages_from_voices(response.voices)

    print(f" Languages: {len(languages)} ".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="\n" if i % 5 == 4 else "")


def unique_languages_from_voices(voices: Sequence[texttospeech.Voice]):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set


def list_voices(language_code=None):
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")
