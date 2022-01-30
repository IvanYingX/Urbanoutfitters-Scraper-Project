from setuptools import setup
from setuptools import find_packages

setup(
    name = 'h_and_m_scraper',
    version = '0.0.1',
    description = 'A scraper of the H&M website for both mens and womens clothes...',
    url = 'https://github.com/IvanYingX/Urbanoutfitters-Scraper-Project',
    author = 'James Overend, Quratulaen Ikram, Dan Bouchard',
    license = 'MIT',
    packages = find_packages(),
    install_requires = ['boto3', 'selenium', 'sklearn', 'tqdm', 'sqlalchemy', 'pandas', 'psycopg2-binary'],
)