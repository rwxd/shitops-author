from datetime import datetime
from datetime import UTC
from author.logging import logger
from pathlib import Path
import boto3
import botocore.client
from author.logging import logger


def get_filename_of_post(content: str, suffix: str = ".md") -> str:
    title = datetime.now(UTC).strftime("%Y-%m-%d-%H-%M-%S")
    for line in content.split("\n"):
        if line.lower().startswith("title"):
            title = line.split(":")[1].strip().replace(" ", "-").lower()
            title = "".join(e for e in title if e.isalnum() or e == "-")
            break
    title = title + suffix
    logger.info(f'title created "{title}"')
    return title


def remove_mermaid_diagrams_from_text(content: str) -> str:
    start = "{{ <mermaid> }}"
    end = "{{ </mermaid> }}"
    while start in content:
        start_index = content.find(start)
        end_index = content.find(end)
        content = content[:start_index] + content[end_index + len(end) :]
    return content


def get_podcast_link(filename: str) -> str:
    return f"https://s3.chaops.de/shitops/podcasts/{filename}"


def insert_podcast_link_into_blog_post(blog_post: str, filename: str) -> str:
    podcast_link = get_podcast_link(filename)
    podcast_html = (
        'Listen to the interview with our engineer: {{<audio src="'
        + podcast_link
        + '" class="audio">}}'
    )
    return blog_post.replace("PODCAST_PLACEHOLDER", podcast_html)


def upload_podcast_to_s3(podcast: Path, s3_access_key: str, s3_secret_key: str):
    bucket = "shitops"
    s3_endpoint_url = "https://s3.chaops.de"
    s3 = boto3.resource(
        "s3",
        endpoint_url=s3_endpoint_url,
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key,
        config=botocore.client.Config(signature_version="s3v4"),
        region_name="us-east-1",
    )
    logger.info(f"Uploading {podcast} to s3")
    s3.Bucket(bucket).upload_file(Filename=str(podcast), Key=f"podcasts/{podcast.name}")
    logger.info(f"Finished uploading to s3")
