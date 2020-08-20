from setuptools import setup, find_packages


setup(
    name='aiodingtalk',
    version='0.5',
    description='Asyncio-based client for Alibaba Dingtalk IM',
    author='Rocky Feng',
    author_email='folowing@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['aiohttp>=3.6.2'],
    zip_safe=False,
)
