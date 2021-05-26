from setuptools import setup

setup(
    name='app',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'fastapi',
    ],
    setup_requires=[
        'pytest-runner',
        'flake8',
    ],
    tests_require=[
        'pytest',
        'pytest-mock',
        'requests',
        'validators',
        'requests_mock',
    ],
)
