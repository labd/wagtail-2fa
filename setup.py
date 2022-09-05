import re

from setuptools import find_packages, setup

install_requires = [
    "Django>=3.2",
    "Wagtail>=2.15",
    "django-otp>=0.8.1",
    "six>=1.14.0",
    "qrcode>=6.1",
]

docs_require = [
    "sphinx>=1.4.1",
    "sphinx_rtd_theme>=0.4.3",
]

tests_require = [
    "coverage==5.5",
    "pytest==7.1.3",
    "pytest-cov==2.12.1",
    "pytest-django==4.4.0",
    # Linting
    "flake8==3.9.2",  # 3.7.9
    "isort==5.9.3",
    "flake8-blind-except==0.2.0",
    "flake8-debugger==4.0.0",
]

with open("README.rst") as fh:
    long_description = re.sub(
        "^.. start-no-pypi.*^.. end-no-pypi", "", fh.read(), flags=re.M | re.S
    )

setup(
    name="wagtail-2fa",
    version="1.6.0",
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
    python_requires=">=3.7",
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
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=False,
)
