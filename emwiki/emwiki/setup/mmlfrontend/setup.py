from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "mmlfrontend",
    version = "1.0.0",
    author = "Kazuhisa Nakasho",
    author_email = "kazuhisa.nakasho@gmail.com",
    description = "MML-Frontend",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mimosa-project/mmlfrontend",
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Development Status :: 5 - Production/Stable",
    ],
    python_requires='>=3',
    setup_requires = ['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'dev': [
            'pytest>=4',
            'wheel',
        ],
    },
    zip_safe=False,
)
