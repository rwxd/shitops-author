import typer
from author.templates import template_blog_post
from author.logging import init_logger, logger
from author.words import get_random_words
from author.misc import remove_mermaid_diagrams_from_text
from author.gpt import Post, generate_post
import author.az_tts as az_tts
from author.audio import (
    create_podcast_text_from_blog_post,
    create_podcast_with_az_tts,
    create_podcast_with_google_tts,
    mp3_bytes_to_audio_segment,
    create_podcast_intro,
)
from datetime import datetime
from datetime import UTC
from pathlib import Path
import openai
from pydub import AudioSegment
import os
from typing import Optional
from yaml import safe_load

app = typer.Typer()


@app.command()
def create_post(
    openai_token: str = typer.Option(..., envvar='OPENAI_TOKEN'),
    github_project: str = typer.Option('rwxd/shitops'),
    debug: bool = typer.Option(False),
    topic: str = typer.Option('', help='Use a specific topic'),
    dest: Path = typer.Option(..., help='Destination directory to render the template'),
    podcast: bool = True,
    google_service_account: Optional[Path] = typer.Option(
        ...,
        envvar='GOOGLE_SERVICE_ACCOUNT',
        help='Path to the google service account json',
    ),
    google_voice: bool = False,
    az_voice: bool = True,
    az_region: str = typer.Option('eastus'),
    az_subscription_key: str = typer.Option('', envvar='AZ_SUBSCRIPTION_KEY'),
):
    if debug:
        init_logger('DEBUG')
    else:
        init_logger('WARNING')

    if not dest.is_dir():
        raise ValueError(f'{dest} is not a directory')

    openai.api_key = openai_token

    random_words = get_random_words()
    logger.info(f'Using {len(random_words)} random words: {random_words}')

    rendered_prompt = template_blog_post.render(
        date=datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
        topic=topic,
        random_words=random_words,
    )
    post = generate_post(rendered_prompt)
    filepath = dest.joinpath(post.filename)
    with open(filepath, 'w') as f:
        logger.info(f'saving post to {post.filename}')
        f.write(post.content)

    logger.info(f'Saved file to "{filepath}"')

    if not podcast:
        exit(0)

    jingle_audio: AudioSegment = AudioSegment.from_mp3(str(Path('jingle.mp3')))
    if not jingle_audio:
        raise ValueError(f'Could not load jingle.mp3')

    logger.info(f'Creating intro text')
    intro_text = create_podcast_intro()
    with open('podcast_intro.txt', 'w') as f:
        f.write(intro_text)

    logger.debug(f'Prompting for podcast')

    post_text = remove_mermaid_diagrams_from_text(post.content)
    podcast_text = create_podcast_text_from_blog_post(post_text)

    audio_filepath = str(filepath).replace('.md', '.mp3')

    if google_voice:
        if not google_service_account or not google_service_account.exists():
            raise ValueError(f'{google_service_account} does not exist')

        logger.debug(f'Using google service account {google_service_account}')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(google_service_account)

        podcast_audio = create_podcast_with_google_tts(
            intro_text, jingle_audio, podcast_text
        )
        podcast_audio.export(str(audio_filepath), format='mp3')
    else:
        az_tts.az_speech_subscription_key = az_subscription_key
        az_tts.az_service_region = az_region
        if az_tts.az_speech_subscription_key == '':
            raise ValueError(
                f'AZ_SUBSCRIPTION_KEY is not set, please set it or use --az-subscription-key'
            )

        podcast_audio = create_podcast_with_az_tts(
            intro_text, jingle_audio, podcast_text
        )
        logger.info(f'Exporting podcast to {audio_filepath}')
        podcast_audio.export(str(audio_filepath), format='mp3')
