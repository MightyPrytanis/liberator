"""
Setup script for Liberator.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text() if readme_file.exists() else ''

setup(
    name='liberator',
    version='1.0.0',
    description='Liberate apps from proprietary platforms (Base44, Replit, etc.)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Liberator Project',
    author_email='',
    url='https://github.com/yourusername/liberator',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        # No external dependencies - pure Python standard library
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'liberator=liberator.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving',
    ],
    keywords='extract export portability open-source base44 replit',
)
