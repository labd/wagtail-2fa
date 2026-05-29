import re

from setuptools import find_packages, setup

install_requires = [
    "Django>=5.2",
    "Wagtail>=7.0",
    "django-otp>=1.7.0",
    "qrcode>=6.1",
]

docs_require = [
    "sphinx>=7.0",
    "sphinx_rtd_theme>=2.0",
]

tests_require = [
    "coverage>=7.0",
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "pytest-django>=4.8",
    # Linting
    "flake8>=7.0",
    "isort>=5.13",
    "flake8-blind-except>=0.2.1",
    "flake8-debugger>=4.1",
]

with open("README.rst") as fh:
    long_description = re.sub(
        "^.. start-no-pypi.*^.. end-no-pypi", "", fh.read(), flags=re.M | re.S
    )

setup(
    name="wagtail-2fa",
    version="1.8.0",
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
        "Framework :: Django :: 5.2",
        "Framework :: Django :: 6.0",
        "Framework :: Wagtail",
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
