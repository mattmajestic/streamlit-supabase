from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="streamlit_supabase",
    version="0.5",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Matt Majestic",
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    project_urls={
        "GitHub Repository": "https://github.com/mattmajestic/streamlit-supabase",
    },
)
