from setuptools import setup, find_packages


def get_description():
    with open("README.rst") as f:
        return f.read()


setup(
    # Package meta-data
    name="django-rest-email-auth",
    version="3.0.3",
    description="Django app for email based authentication and registration.",
    long_description=get_description(),
    author="Chathan Driehuys",
    author_email="chathan@driehuys.com",
    url="https://github.com/cdriehuys/django-rest-email-auth",
    license="MIT",
    # Additional classifiers for PyPI
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        # Supported versions of Django
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        # Supported versions of Python
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    # Include the actual source code
    include_package_data=True,
    packages=find_packages(),
    # Dependencies
    install_requires=[
        "Django >= 2.2, < 3.2",
        "django-email-utils >= 1.0, < 2.0",
        # DRF 3.10 is the first to support our minimum Django version of 2.2.
        "djangorestframework >= 3.10",
    ],
)
