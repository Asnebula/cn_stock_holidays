from setuptools import setup, find_packages

setup(
    name="cnhd",
    version="1.4.",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'click',
        'dateutil',
    ],

    # metadata for upload to PyPI
    author="Asnebula",
    author_email="Asenbula@sina.com",
    description="A List of china stock exchange holidays",
    license="MIT",
    keywords="china stock holiday exchange Shanghai, Shenzhen and HongKong",
    url="https://github.com/Asnebula/cn_stock_holidays.git",  # project home page, if any

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['files/*.txt'],
    },
    entry_points={
        'console_scripts': [
            'cnhd-sync=cnhd.data_helper:main',
            'get-day-list=cnhd.tools.cmd:main',
        ]
    }
)
