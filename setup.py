from setuptools import setup, find_packages

setup(
    name="invert-pdf-colors",
    version="0.1.0",
    description="Tools to invert PDF colors by converting to images, inverting, and recombining",
    author="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "Pillow>=10.0.0",
        "PyPDF4>=1.27.0",
        "PyPDF2>=3.0.0",
        "wand>=0.6.10",
        "tqdm>=4.66.0",
        "natsort>=8.4.0",
    ],
    python_requires=">=3.8",
)
