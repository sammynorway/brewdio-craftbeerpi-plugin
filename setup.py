from pathlib import Path

from setuptools import setup


ROOT = Path(__file__).parent


setup(
    name="cbpi4-brewdio",
    version="0.2.1",
    description="Synchronize Brewdio recipes into CraftBeerPi 4",
    long_description=(ROOT / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/sammynorway/brewdio-craftbeerpi-plugin",
    project_urls={
        "Repository": "https://github.com/sammynorway/brewdio-craftbeerpi-plugin.git",
        "Issues": "https://github.com/sammynorway/brewdio-craftbeerpi-plugin/issues",
    },
    author="Anders H. Samuelsen",
    maintainer="Anders H. Samuelsen",
    license="GPL-3.0-or-later",
    python_requires=">=3.10",
    packages=["cbpi4_brewdio"],
    package_data={"cbpi4_brewdio": ["config.yaml"]},
    include_package_data=True,
    install_requires=[
        "aiohttp>=3.8",
        "PyYAML>=6.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
