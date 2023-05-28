import typer
from author.templates import template_prompt
from author.logging import init_logger, logger
from author.gpt import generate_post
from author.words import get_random_words
from datetime import datetime
from datetime import UTC

app = typer.Typer()


@app.command()
def create_post(
    openai_token: str = typer.Option(..., envvar='OPENAI_TOKEN'),
    github_project: str = typer.Option('rwxd/shitops'),
    debug: bool = typer.Option(False),
    topic: str = typer.Option('', help='Use a specific topic'),
):
    if debug:
        init_logger('DEBUG')
    else:
        init_logger('WARNING')

    random_words = get_random_words()
    logger.info(f'Using {len(random_words)} random words: {random_words}')
    rendered_prompt = template_prompt.render(
        date=datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
        topic=topic,
        random_words=random_words,
    )
    post = generate_post(rendered_prompt, openai_token)
    with open(f'/home/fwrage/dev/shitops/content/posts/{post.filename}', 'w') as f:
        logger.info(f'saving post to {post.filename}')
        f.write(post.content)
