from setuptools import setup, find_packages

version = "0.2"

setup(
    name='django-demail',
    version=version,
    packages=find_packages(exclude=['test_app']),
    author='Gary Reynolds',
    author_email='gary@touch.asn.au',
    description='Delegating email backend.',
    url='https://github.com/goodtune/django-demail',
    install_requires=[
        'Django',
    ],
    test_suite='test_app.runtests.runtests',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
    ],
)
