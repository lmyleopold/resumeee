from setuptools import setup, find_packages
setup(
    name = 'ecloud_python_sdk',
    version = '1.1.0',
    url = "https://ecloud.10086.cn",
    packages = [
        'ecloud',
    ],
    author = 'ecloud',
    description = 'Ecloud AI SDK',
    install_requires=[
        'requests',
    ],
)