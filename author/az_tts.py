from os import walk
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
from author.logging import logger
from author.templates import template_az_speech_ssml
from author.logging import logger

az_speech_subscription_key = ""
az_service_region = ""
az_speech_token = ""


def create_audio_from_text(
    text: str,
    voice: str,
    format: speechsdk.SpeechSynthesisOutputFormat = speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateMonoMp3,
    style: str = "default",
    language: str = "en-US",
) -> bytes:
    """
    Set the voice name, refer to https://aka.ms/speech/voices/neural for full list.
    """
    logger.debug(f'Creating audio for "{text}"')
    speech_config = speechsdk.SpeechConfig(
        subscription=az_speech_subscription_key,
        region=az_service_region,
    )
    speech_config.speech_synthesis_voice_name = voice
    speech_config.set_speech_synthesis_output_format(format)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    ssml = template_az_speech_ssml.render(
        text=text,
        language=language,
        style=style,
        voice=voice,
    )

    logger.debug(f"Using ssmml: {ssml}")

    result = speech_synthesizer.speak_ssml(ssml=ssml)
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data

    logger.error(
        f"Error synthesizing audio for text, {result.cancellation_details.error_details}"
    )
    raise RuntimeError(f'Error synthesizing audio for text "{text}"')
