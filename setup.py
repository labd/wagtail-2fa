import re

from setuptools import find_packages, setup

install_requires = [
    "Django>=4.2",
    "Wagtail>=6.3",
    "django-otp>=1.6.1",
    "six>=1.17.0",
    "qrcode>=8.2",
]

docs_require = [
    "sphinx>=8.2.3",
    "sphinx_rtd_theme>=3.0.2",
]

tests_require = [
    "coverage==7.10.1",
    "pytest==8.4.1",
    "pytest-cov==6.2.1",
    "pytest-django==4.11.1",
    # Linting
    "flake8==7.3.0",
    "isort==6.0.1",
    "flake8-blind-except==0.2.1",
    "flake8-debugger==4.1.2",
    "wagtail-modeladmin==2.2.0"
]

with open("README.rst") as fh:
    long_description = re.sub(
        "^.. start-no-pypi.*^.. end-no-pypi", "", fh.read(), flags=re.M | re.S
    )

setup(
    name="wagtail-2fa",
    version="1.7.1",
    description="Two factor authentication for Wagtail",
    long_description=long_description,
    url="https://github.com/LabD/wagtail-2fa",
    author="Lab Digital",
    author_email="opensource@labdigital.nl",
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        "docs": docs_require,
        "test": tests_require,
    },
    python_requires=">=3.10",
    use_scm_version=True,
    entry_points={},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 6",
        "Framework :: Wagtail :: 7",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    zip_safe=False,
)
