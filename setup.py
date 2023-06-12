from setuptools import find_packages, setup
from setuptools.command.install import install


setup(
    name='CodeFest_Ad_Astra',
    packages=find_packages(include=['SapaceInvaders']),
    version='0.1.0',
    description='My first Python library',
    author='Me',
    license='MIT',
    install_requires=['botocore==1.29.151','urllib3==1.26.16','stanza==1.5.0','pandas==2.0.2','nltk==3.8.1','flair==0.12.2','scikit-learn==1.2.1','num2words==0.5.12','requests==2.31.0','joblib', 'newspaper3k==0.2.8', 'PyPDF2==3.0.1', 'python-docx==0.8.11', 'ultralytics', 'easyocr'],
    include_package_data=True,
)