from setuptools import setup, find_packages

setup(
    name='NetVis',
    version='0.1.0',
    author='Arturas Razinkovas-Baziukas',
    author_email='arturas.razinkovas-baziukas@ku.lt',
    description='A library that combines NetworkX analytic methods and PyVis visualization.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/NetVis',
    packages=find_packages(),
    install_requires=[
        'networkx',
        'pyvis',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)