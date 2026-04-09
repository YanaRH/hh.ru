from setuptools import setup, find_packages

setup(
    name="hh-parser",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "psycopg2-binary",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "hh-parser=hh_parser.main:main",
        ],
    },
    author="Your Name",
    description="HH.ru вакансии парсер",
)