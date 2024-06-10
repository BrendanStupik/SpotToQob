from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='SpotToQob',
    version='1.0.2',
    author='Brendan Stupik',
    author_email='spottoqob@brendanstupik.anonaddy.com',
    description='Backup a CSV or Spotify playlist URL using Qobuz-dl',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/BrendanStupik/SpotToQob',
    packages=find_packages(),
    install_requires=[
        'spotipy>=2.0.0',
        'pandas>=1.0.0',
        'configparser>=5.0.0',
        'qobuz-dl>=0.9.9.10'
    ],
    entry_points={
        'console_scripts': [
            'SpotToQob = SpotToQob.SpotToQob:main'
        ]
    }
)
