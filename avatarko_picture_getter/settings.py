import os


class AvatarGeneratorError(Exception):
    pass


ATTEMPTS_TO_GET_AVATAR = int(os.environ.get('ATTEMPTS_TO_GET_AVATAR', '3'))
DESCRIPTION = 'Tool to get random avatar from https://avatarko.ru'

