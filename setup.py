import setuptools
#read the content from Readme.md file and give the description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

#versision is specified
__version__ = "0.0.0"

REPO_NAME = "AI-Solution"
AUTHOR_USER_NAME = "k17hawk"
SRC_REPO = "AI_solution"
AUTHOR_EMAIL = "kumardahal536@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)