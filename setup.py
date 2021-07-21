import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="rangers-tools",
    version="0.1",
    author="Denis Ballakh",
    description="Space Rangers HD game file format tools",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/denballakh/rangers-tools",
    packages=setuptools.find_packages(),
    python_requires='>=3.9',
)
