from datetime import datetime
from datetime import UTC
from author.logging import logger


def get_filename_of_post(content: str) -> str:
    suffix = '.md'
    title = datetime.now(UTC).strftime('%Y-%m-%d-%H-%M-%S')
    for line in content.split('\n'):
        if line.lower().startswith('title'):
            title = line.split(':')[1].strip().replace(' ', '-').lower()
            title = ''.join(e for e in title if e.isalnum() or e == '-')
            break
    title = title + suffix
    logger.info(f'title created "{title}"')
    return title
