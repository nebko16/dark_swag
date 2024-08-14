from setuptools import setup, find_packages

setup(
    name='dark_swag',
    version='1.0.4',
    author='nebko16',
    author_email='nebko16@gmail.com',
    description='Dark mode Swagger for your FastAPI apps',
    license='GPL-3.0',
    keywords='fastapi openapi swagger dark night darkmode dark-mode theme docs documentation',
    packages=find_packages(where='src'),
    install_requires=[
        'fastapi',
        'jinja2',
        'python-multipart'
    ],
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.6',
    long_description='This module enables Swagger OpenAPI docs that default to dark mode but can be toggled on or off, specifically for FastAPI. Requires virtually zero work to implement. DarkSwag has an optional argument for adding your project or company logo. Implementation is cake, depending on how you implement it. The easiest implementation method involves importing the FastAPI class override, and that\'s it.  See the `Github` [README](https://github.com/nebko16/dark_swag/blob/main/README.md) for more info.',
    long_description_content_type='text/markdown',
    url='https://github.com/nebko16/dark_swag',
)
