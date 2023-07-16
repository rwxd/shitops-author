# from google.cloud import texttospeech
# from author.logging import logger
# from typing import Sequence
#
#
# def create_audio_from_text(
#     text: str,
#     voice: str = 'en-US-Neural2-A',
#     language_code: str = 'en-US',
#     # gender=texttospeech.SsmlVoiceGender.NEUTRAL,
#     audio_encoding=texttospeech.AudioEncoding.MP3,
# ) -> bytes:
#     logger.debug(f'Creating audio for "{text}"')
#     client = texttospeech.TextToSpeechClient()
#     synthesis_input = texttospeech.SynthesisInput(text=text)
#     voice_params = texttospeech.VoiceSelectionParams(
#         language_code=language_code, name=voice
#     )
#     audio_config = texttospeech.AudioConfig(audio_encoding=audio_encoding)
#     response = client.synthesize_speech(
#         input=synthesis_input, voice=voice_params, audio_config=audio_config
#     )
#
#     return response.audio_content
#
#
# def list_languages():
#     client = texttospeech.TextToSpeechClient()
#     response = client.list_voices()
#     languages = unique_languages_from_voices(response.voices)
#
#     print(f" Languages: {len(languages)} ".center(60, "-"))
#     for i, language in enumerate(sorted(languages)):
#         print(f"{language:>10}", end="\n" if i % 5 == 4 else "")
#
#
# def unique_languages_from_voices(voices: Sequence[texttospeech.Voice]):
#     language_set = set()
#     for voice in voices:
#         for language_code in voice.language_codes:
#             language_set.add(language_code)
#     return language_set
#
#
# def list_voices(language_code=None):
#     client = texttospeech.TextToSpeechClient()
#     response = client.list_voices(language_code=language_code)
#     voices = sorted(response.voices, key=lambda voice: voice.name)
#
#     print(f" Voices: {len(voices)} ".center(60, "-"))
#     for voice in voices:
#         languages = ", ".join(voice.language_codes)
#         name = voice.name
#         gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
#         rate = voice.natural_sample_rate_hertz
#         print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")
