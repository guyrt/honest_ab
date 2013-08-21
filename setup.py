try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


packages = [
    'honest_ab'
]
requires = [
    'Murmur==0.1.3',
    'Django>=1.4.0',
]
tests_require = ['mock==1.0.1']

setup(
    name='honest_ab',
    description='A/B testing framework for django',
    long_description=open('README.rst').read(),
    version='0.1',
    author=open('AUTHORS.rst').read(),
    author_email='richardtguy84@gmail.com',
    url='https://github.com/guyrt/honest_ab',
    packages=packages,
    package_data={'': ['LICENSE.rst', 'AUTHORS.rst', 'README.rst']},
    include_package_data=True,
    zip_safe=True,
    install_requires=requires,
    tests_require=tests_require,
    #test_suite='vero.tests.client_test',
    license=open('LICENSE.rst').read(),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)
