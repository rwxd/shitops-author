import typer
import yaml
from author.templates import template_blog_post
from author.logging import init_logger, logger
from author.words import get_random_words
from author.misc import remove_mermaid_diagrams_from_text
from author.gpt import Post, generate_post
import author.az_tts as az_tts
from author.audio import (
    create_podcast_text_from_blog_post,
    create_podcast_with_az_tts,
    create_podcast_intro,
)
from datetime import datetime
from datetime import UTC
from pathlib import Path
import openai
from pydub import AudioSegment
from dataclasses import asdict
from author.misc import insert_podcast_link_into_blog_post, upload_podcast_to_s3
from author.github import upload_blog_post_to_github

app = typer.Typer()


@app.command()
def create_post(
    openai_token: str = typer.Option(..., envvar="OPENAI_TOKEN"),
    github_token: str = typer.Option(..., envvar="BLOG_GITHUB_TOKEN"),
    s3_access_key: str = typer.Option(..., envvar="S3_ACCESS_KEY"),
    s3_secret_key: str = typer.Option(..., envvar="S3_SECRET_KEY"),
    debug: bool = typer.Option(False),
    topic: str = typer.Option("", help="Use a specific topic"),
    dest: Path = typer.Option(
        Path("./output"), help="Destination directory to render the template"
    ),
    podcast: bool = True,
    az_region: str = typer.Option("eastus"),
    az_subscription_key: str = typer.Option(..., envvar="AZ_SUBSCRIPTION_KEY"),
    interactive: bool = True,
):
    if debug:
        init_logger("DEBUG")
    else:
        init_logger("INFO")

    openai.api_key = openai_token

    random_words = get_random_words()
    logger.info(f"Using {len(random_words)} random words: {random_words}")

    if interactive:
        input(f"Continue with the words? <CR>")

    rendered_prompt = template_blog_post.render(
        date=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        topic=topic,
        random_words=random_words,
    )
    post = generate_post(rendered_prompt)

    logger.info(f"Generated blog post {post.filename}")

    if not podcast:
        exit(0)

    if interactive:
        input("Podcast creation? <CR>")

    jingle_audio: AudioSegment = AudioSegment.from_mp3(str(Path("jingle.mp3")))
    if not jingle_audio:
        raise ValueError(f"Could not load jingle.mp3")

    logger.info(f"Creating intro text")
    intro_text = create_podcast_intro()
    with open("podcast_intro.txt", "w") as f:
        f.write(intro_text)

    logger.info(f"Prompting for podcast")

    post_text = remove_mermaid_diagrams_from_text(post.content)
    podcast_text = create_podcast_text_from_blog_post(post_text)
    audio_filepath = dest.joinpath(post.filename.replace(".md", ".mp3"))

    az_tts.az_speech_subscription_key = az_subscription_key
    az_tts.az_service_region = az_region
    podcast_audio = create_podcast_with_az_tts(intro_text, jingle_audio, podcast_text)
    logger.info(f"Exporting podcast to {audio_filepath}")
    podcast_audio.export(str(audio_filepath), format="mp3")

    post.content = insert_podcast_link_into_blog_post(post.content, audio_filepath.name)
    upload_podcast_to_s3(audio_filepath, s3_access_key, s3_secret_key)
    upload_blog_post_to_github(github_token, post.filename, post.content)
