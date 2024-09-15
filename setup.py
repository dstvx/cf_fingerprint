from setuptools import setup, find_packages
from pathlib import Path

# Get the directory where setup.py is located
base_dir = Path(__file__).parent.resolve()

# Read the contents of README.md
long_description = (base_dir / 'README.md').read_text(encoding='utf-8')

setup(
    name='cf_fingerprint',
    version='1.0.0',
    description='A Python implementation for generating a 32-bit fingerprint of files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='dstvx',
    author_email='thomas.brionesm@gmail.com',
    url='https://github.com/dstvx/cf_fingerprint',
    license='MIT',
    packages=find_packages(),  # Automatically find and include the cf_fingerprint package
    install_requires=['numpy'],  # Dependencies
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',  # Minimum Python version requirement
)