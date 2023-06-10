from setuptools import find_packages, setup


setup(
    name='textos',
    packages=find_packages(include=['textos']),
    version='0.1.0',
    description='My first Python library',
    author='Me',
    license='MIT',
    install_requires=['stanza','numpy','pandas','nltk','langdetect','flair','scikit-learn','num2words','requests','joblib', 'newspaper3k'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)