from setuptools import setup, find_packages

setup(
    name="cn-stock-holidays",
    version="1.3",
    packages=find_packages(),
    install_requires=[
        'requests',
        'click'
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
        '': ['*.txt'],
    },
    entry_points={
        'console_scripts': [
            'cn-stock-holiday-sync=cn_stock_holidays.data:sync_data',
            'cn-stock-holiday-sync-hk=cn_stock_holidays.data_hk:sync_data',
            'get-day-list=cn_stock_holidays.tools.cmd:main',
        ]
    }
)
