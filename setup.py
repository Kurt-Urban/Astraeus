from setuptools import setup, find_packages

setup(
    name="Asteroids",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "human = Asteroids.main:human",
        ],
    },
)
