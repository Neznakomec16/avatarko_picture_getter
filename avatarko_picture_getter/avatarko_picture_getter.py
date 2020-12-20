import argparse
import asyncio
import logging
from pathlib import Path
from random import choice
from typing import List
from uuid import uuid4

import aiohttp
import requests
from lxml.html import document_fromstring, Element

from avatarko_picture_getter.settings import AvatarGeneratorError, ATTEMPTS_TO_GET_AVATAR, DESCRIPTION

logger = logging.getLogger(__name__)


class AvatarkoPictureGetter:
    _base_url = 'https://avatarko.ru'
    _image_xpath = '//div[1]/div/div[1]/div/a/img'

    @classmethod
    def _get_links(cls):
        resp = requests.get(cls._base_url + '/random')
        if resp.status_code != 200:
            raise AvatarGeneratorError(f'Response status code is not equals 200 [{resp.status_code}]')
        html = document_fromstring(resp.content)
        image_elements: List[Element] = html.xpath(cls._image_xpath)
        return [
            cls._base_url + element.attrib.get('src').replace('avatar', 'kartinka') for element in image_elements
        ]

    @classmethod
    def get_avatar(cls):
        avatar = None
        for _ in range(ATTEMPTS_TO_GET_AVATAR):
            links = cls._get_links()
            avatar_links: List[str] = list(filter(lambda elem: elem.split('.')[-1] in ['png', 'jpg'], links))
            event_loop = asyncio.get_event_loop()
            avatars = event_loop.run_until_complete(cls._get_avatars(links=avatar_links))
            avatars = list(filter(lambda elem: elem[0] == 200, avatars))
            avatar = choice(avatars) or None
            if avatar is not None:
                break
        if avatar is None:
            raise AvatarGeneratorError('Can not find any avatar')
        return avatar[1]

    @classmethod
    async def _get_avatars(cls, links: List[str]):
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(cls._fetch_content(url, session)) for url in links]
            result = await asyncio.gather(*tasks)
        return result

    @classmethod
    async def _fetch_content(cls, url: str, session: aiohttp.client.ClientSession):
        async with session.get(url) as s:
            data = s.status, await s.read()
        return data


def cli():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        '-o', "--output", default=f'{uuid4().__str__()}.png',
        help='Output file. Must ends with .jpg or .png extentions', type=str
    )
    args = parser.parse_args()
    path = Path(args.output)
    if path.is_dir():
        path = path.joinpath(f'{uuid4().__str__()}.png')
    if path.as_posix().split('.')[-1] not in ['jpg', 'png']:
        logger.warning('Output string must ends with .jpg or .png extensions')
        return
    if path.is_absolute() and not path.parent.exists():
        logger.warning(f'Creating directory with path {path.parent.as_posix()}')
        path.parent.mkdir(parents=True)
    image = AvatarkoPictureGetter.get_avatar()
    with open(args.output, 'wb') as f:
        f.write(image)
    logger.warning(f'Success. Output file is {Path(args.output).absolute().as_posix()}')


if __name__ == '__main__':
    cli()
