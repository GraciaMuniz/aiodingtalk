from setuptools import setup, find_packages


setup(
    name='aiodingtalk',
    version='0.2',
    description='Asyncio-based client for Alibaba Dingtalk IM',
    author='Rocky Feng',
    author_email='folowing@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
