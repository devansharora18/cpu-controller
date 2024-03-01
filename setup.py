from setuptools import setup, find_packages

VERSION = '0.0.9'
DESCRIPTION = 'Turn on/off CPU cores in Linux'
LONG_DESCRIPTION = 'A package that allows you to turn on/off CPU cores in Linux to increase battery life'

# Setting up
setup(
    name="cpu_controller_linux",
    version=VERSION,
    author="Devansh Arora",
    author_email="hsnaved.reverse@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
	include_package_data=True,
    install_requires=['PyQt6'],
    keywords=['python', 'linux', 'cpu', 'battery life', 'cpu cores',],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
    entry_points={
        'console_scripts': [
            'cpu-controller = cpu_controller_linux.main:main',
        ],
    },
	package_data={'cpu_controller_linux': ['cpu.png']},
)
