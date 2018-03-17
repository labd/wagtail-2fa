from setuptools import find_packages, setup

docs_require = [
    'sphinx>=1.4.0',
]

tests_require = [
    'coverage==.4.2',
    'pytest==3.0.5',
    'pytest-django==3.1.2',

    # Linting
    'isort==4.2.5',
    'flake8==3.0.3',
    'flake8-blind-except==0.1.1',
    'flake8-debugger==1.4.0',
]

setup(
    name='wagtail-2fa',
    version='0.0.2',
    description="Something I made",
    long_description=open('README.rst', 'r').read(),
    url='https://github.com/LabD/wagtail-2fa',
    author="Michael van Tellingen, Mike Dingjan",
    author_email="opensource@labdigital.nl",
    install_requires=[
        'Django>=1.11',
        'django-otp>=0.4.3',
        'six>=1.1',
        'qrcode>=5.3',
    ],
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
