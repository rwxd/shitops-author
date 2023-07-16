import requests
import base64
import json

from author.logging import logger


def upload_blog_post_to_github(token: str, path: str, content: str):
    url = f'https://api.github.com/repos/rwxd/shitops/contents/content/posts/{path}'

    author = {'name': 'Professional Blogger', 'email': 'musk@shitops.de'}
    data = {
        'message': f'fix: new blog post {path}',
        # Encode the content into bytes, then base64 encode these bytes for the GitHub API.
        # Finally, decode the result back into a UTF-8 string for JSON compatibility.
        'content': base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        'commiter': author,
        'author': author,
    }

    headers = {'Authorization': f'token {token}', 'Content-Type': 'application/json'}
    logger.info(f'Uploading post to github')

    response = requests.put(url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        logger.info(f'File uploaded to github')
    elif response.status_code == 200:
        logger.info(f'File updated in github')
    else:
        logger.error(f'Error: {response.status_code}, {response.text}')
