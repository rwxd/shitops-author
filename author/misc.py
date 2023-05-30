from datetime import datetime
from datetime import UTC
from author.logging import logger


def get_filename_of_post(content: str, suffix: str = '.md') -> str:
    title = datetime.now(UTC).strftime('%Y-%m-%d-%H-%M-%S')
    for line in content.split('\n'):
        if line.lower().startswith('title'):
            title = line.split(':')[1].strip().replace(' ', '-').lower()
            title = ''.join(e for e in title if e.isalnum() or e == '-')
            break
    title = title + suffix
    logger.info(f'title created "{title}"')
    return title


def remove_mermaid_diagrams_from_text(content: str) -> str:
    start = '{{ <mermaid> }}'
    end = '{{ </mermaid> }}'
    while start in content:
        start_index = content.find(start)
        end_index = content.find(end)
        content = content[:start_index] + content[end_index + len(end) :]
    return content
