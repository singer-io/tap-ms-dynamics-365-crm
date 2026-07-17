

from setuptools import setup, find_packages


setup(name="tap-ms-dynamics-365-crm",
      version="0.0.2",
      description="Singer.io tap for extracting data from ms-dynamics-365-crm API",
      author="Stitch",
      url="http://singer.io",
      classifiers=["Programming Language :: Python :: 3 :: Only"],
      py_modules=["tap_ms_dynamics_365_crm"],
      install_requires=[
        "singer-python==6.8.0",
        "requests==2.34.2",
        "backoff==2.2.1",
        "msal==1.34.0"
      ],
      entry_points="""
          [console_scripts]
          tap-ms-dynamics-365-crm=tap_ms_dynamics_365_crm:main
      """,
      packages=find_packages(),
      package_data = {
          "tap_ms_dynamics_365_crm": ["schemas/*.json"],
      },
      include_package_data=True,
)
