from setuptools import setup

setup(
    name="sudoqgen",
    version="0.0.1",
    description="A Sudoku image generator",
    url="yetoarrive",
    author="yetoarrive",
    license="MIT",
    packages=["sudoqgen"],
    install_requires=[
        "opencv-python",
        "numpy",
        "glob2",
        "tqdm",
    ],
    extra_require={
        "dev": ["flake8", "black", "pre-commit"]
    },
)