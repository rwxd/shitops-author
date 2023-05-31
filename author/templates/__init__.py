from pathlib import Path
from jinja2 import Environment, Template, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent.absolute()
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False, loader=FileSystemLoader(TEMPLATES_DIR), trim_blocks=False
)

template_blog_post: Template = TEMPLATE_ENVIRONMENT.get_template("blog_post.j2")
template_podcast_from_blog_post: Template = TEMPLATE_ENVIRONMENT.get_template(
    "podcast_from_blog_post.j2"
)
template_podcast_intro: Template = TEMPLATE_ENVIRONMENT.get_template('podcast_intro.j2')
template_az_speech_ssml: Template = TEMPLATE_ENVIRONMENT.get_template(
    'az_speech_ssml.j2'
)
