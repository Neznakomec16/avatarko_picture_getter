import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="avatarko_picture_getter",
    version="0.0.1",
    author="Neznakomec16",
    author_email="",
    description="Avatarko picture getter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neznakomec16/avatarko_picture_getter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'aiohttp',
        'lxml',
        'requests',
    ],
)
