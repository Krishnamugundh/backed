import setuptools

setuptools.setup(
    name='audio_detections',
    version='0.0.2',
    description='Audio description for voice classification',
    author='mugu',
    author_email='forbusinesssuseonly1986@gmail.com',
    py_modules=['pywin32_postinstall'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
    
