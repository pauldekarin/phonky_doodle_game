from setuptools import setup, find_packages

setup(
    name='phonky_doodle',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pgzero',
    ],
    entry_points={
        'console_scripts': [
            'play=phonky_doodle.run_game:main',  # Указываем путь к функции main в run_game.py
        ],
    },
)