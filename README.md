## Avatarko picture getter

Tool to get random avatar from https://avatarko.ru

### Instalation

```
pip install avatar_generator
```

### Usage

For use as command line interface(cli)
```
python avatarko_picture_getter.py [-o filepath]
```
or
```
from avatarko_picture_getter import AvatarkoPictureGetter

with open('some_picture.png', 'wb') as f:
    f.write(AvatarkoPictureGetter.get_avatar())
```
