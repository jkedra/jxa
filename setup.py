import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jxa",
    version="0.0.2",
    author="Jurek Kedra",
    author_email="jurek.kedra@gmail.com",
    description="Generic Libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jkedra/jxa",
    packages=['jxa'],
    python_requires='>=3.3, <4',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
)
