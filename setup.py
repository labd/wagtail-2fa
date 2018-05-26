import re

from setuptools import find_packages, setup

install_requires = [
    'Django>=1.11',
    'Wagtail>=2.1',
    'django-otp>=0.4.3',
    'six>=1.1',
    'qrcode>=5.3',
]

docs_require = [
    'sphinx>=1.4.0',
]

tests_require = [
    'coverage==.4.2',
    'pytest==3.6.0',
    'pytest-cov==2.5.1',
    'pytest-django==3.1.2',

    # Linting
    'isort==4.2.5',
    'flake8==3.0.3',
    'flake8-blind-except==0.1.1',
    'flake8-debugger==1.4.0',
]

with open('README.rst') as fh:
    long_description = re.sub(
        '^.. start-no-pypi.*^.. end-no-pypi', '', fh.read(), flags=re.M | re.S)

setup(
    name='wagtail-2fa',
    version='1.0.0',
    description="Two factor authentication for Wagtail",
    long_description=long_description,
    url='https://github.com/LabD/wagtail-2fa',
    author="Lab Digital",
    author_email="opensource@labdigital.nl",
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'docs': docs_require,
        'test': tests_require,
    },
    use_scm_version=True,
    entry_points={},
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=False,
)
