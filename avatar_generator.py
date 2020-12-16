import asyncio
from random import choice
from typing import List

import aiohttp
import requests
from lxml.html import document_fromstring, Element

from settings import AvatarGeneratorError, ATTEMPTS_TO_GET_AVATAR


class AvatarGenerator:
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
            cls._base_url + element.attrib.get('src').replace('avatar', 'kartinka') for element in  image_elements
        ]

    @classmethod
    def get_avatar(cls):
        avatar = None
        for _ in range(ATTEMPTS_TO_GET_AVATAR):
            links = cls._get_links()
            avatar_links: List[str] = list(filter(lambda elem: elem.split('.')[-1] in ['png', 'jpg'], links))
            avatars = asyncio.run(cls._get_avatars(links=avatar_links))
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


if __name__ == '__main__':
    with open('test.png', 'wb') as f:
        f.write(AvatarGenerator.get_avatar())