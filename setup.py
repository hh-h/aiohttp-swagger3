from aiohttp_swagger3 import __version__
from pathlib import Path, PurePath
from setuptools import setup

readme = Path(__file__).with_name("README.rst")

with open(PurePath(__file__).parent / "requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="aiohttp-swagger3",
    version=__version__,
    packages=["aiohttp_swagger3"],
    package_data={
        "aiohttp_swagger3": [
            "schema/schema.json",
            "swagger_ui/*",
            "redoc_ui/*",
            "redoc_ui/fonts/montserrat/*",
            "redoc_ui/fonts/roboto/*",
            "rapidoc_ui/*",
        ],
    },
    url="https://github.com/hh-h/aiohttp-swagger3",
    license="Apache 2",
    author="Valetov Konstantin",
    author_email="forjob@thetrue.name",
    description="validation for aiohttp swagger openAPI 3",
    long_description=readme.read_text("utf-8"),
    long_description_content_type="text/x-rst",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 4 - Beta",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Framework :: AsyncIO",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.6",
    install_requires=install_requires,
)
