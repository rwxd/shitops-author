from pathlib import Path
from jinja2 import Environment, Template, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent.absolute()
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False, loader=FileSystemLoader(TEMPLATES_DIR), trim_blocks=False
)

template_prompt: Template = TEMPLATE_ENVIRONMENT.get_template("prompt.j2")
