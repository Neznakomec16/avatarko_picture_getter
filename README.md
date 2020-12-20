## Avatarko picture getter

Tool to get random avatar from https://avatarko.ru

### Instalation

```
pip install avatarko_picture_getter
```

### Usage

For use as command line interface(cli)
```
python -m avatarko_picture_getter [-o filepath]
```
or
```
from avatarko_picture_getter import AvatarkoPictureGetter

with open('some_picture.png', 'wb') as f:
    f.write(AvatarkoPictureGetter.get_avatar())
```
