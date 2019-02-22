import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scs",
    version="0.4",
    author="Sakat",
    description="A python script for Clash of Clans",
    long_description="A python script for Clash of Clans",
    long_description_content_type="text/markdown",
    url="https://github.com/Sakatland/SCS",
    install_requires=["os", "datetime", "ast", "time", "cocapi", "requests"], 
    keywords='Clash of Clans SuperCell API COC',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ),
)
