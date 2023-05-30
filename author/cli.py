import typer
from author.templates import template_blog_post
from author.logging import init_logger, logger
from author.gpt import generate_post, Post, Post
from author.words import get_random_words
from author.audio import (
    create_podcast_from_blog_post,
)
from author.misc import get_filename_of_post
from datetime import datetime
from datetime import UTC
from pathlib import Path
import openai
import os

app = typer.Typer()


@app.command()
def create_post(
    openai_token: str = typer.Option(..., envvar='OPENAI_TOKEN'),
    github_project: str = typer.Option('rwxd/shitops'),
    debug: bool = typer.Option(False),
    topic: str = typer.Option('', help='Use a specific topic'),
    dest: Path = typer.Option(..., help='Destination directory to render the template'),
    google_service_account: Path = typer.Option(
        ...,
        envvar='GOOGLE_SERVICE_ACCOUNT',
        help='Path to the google service account json',
    ),
):
    if debug:
        init_logger('DEBUG')
    else:
        init_logger('WARNING')

    if not dest.is_dir():
        raise ValueError(f'{dest} is not a directory')

    if not google_service_account.exists():
        raise ValueError(f'{google_service_account} does not exist')
    logger.debug(f'Using google service account {google_service_account}')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(google_service_account)

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

    podcast = create_podcast_from_blog_post(
        post.content,
        get_filename_of_post(post.content, '.mp3'),
        jingle=Path('jingle.mp3'),
    )

    podcast.export(str(filepath).replace('.md', '.mp3'), format='mp3')
