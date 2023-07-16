import openai
import os
from dataclasses import dataclass
from author.misc import get_filename_of_post
from author.logging import logger
from author.templates import template_podcast_from_blog_post

ENGINE = 'gpt-3.5-turbo'


@dataclass
class Post:
    content: str
    filename: str


def generate_post(prompt: str) -> Post:
    logger.info(f'prompting openai')
    client = openai.ChatCompletion.create(
        model=ENGINE,
        messages=[
            {'role': 'user', 'content': prompt},
        ],
        # What sampling temperature to use, between 0 and 2.
        # Higher values like 0.8 will make the output more random,
        # while lower values like 0.2 will make it more focused and deterministic.
        temperature=1.0,
        # Number between -2.0 and 2.0.
        # Positive values penalize new tokens based on their existing frequency in the text so far,
        # decreasing the model's likelihood to repeat the same line verbatim.
        frequency_penalty=0.0,
        # Number between -2.0 and 2.0. Positive values penalize new tokens based on
        # whether they appear in the text so far, increasing the model's
        # likelihood to talk about new topics.
        presence_penalty=1.0,
    )
    content = client.choices[0].message.content
    filename = get_filename_of_post(content)
    logger.debug(client.usage)
    return Post(content, filename)


def prompt_openai(prompt: str) -> str:
    client = openai.ChatCompletion.create(
        model=ENGINE,
        messages=[
            {'role': 'user', 'content': prompt},
        ],
        # What sampling temperature to use, between 0 and 2.
        # Higher values like 0.8 will make the output more random,
        # while lower values like 0.2 will make it more focused and deterministic.
        temperature=1.0,
        # Number between -2.0 and 2.0.
        # Positive values penalize new tokens based on their existing frequency in the text so far,
        # decreasing the model's likelihood to repeat the same line verbatim.
        frequency_penalty=0.0,
        # Number between -2.0 and 2.0. Positive values penalize new tokens based on
        # whether they appear in the text so far, increasing the model's
        # likelihood to talk about new topics.
        presence_penalty=1.0,
    )
    content = client.choices[0].message.content
    logger.info(f'Text generated with {len(content.split(" "))} words')
    logger.debug(client.usage)
    return content
