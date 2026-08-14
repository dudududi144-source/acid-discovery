"""
ACID - Autonomous Computational Intelligence Discovery
"""
from setuptools import setup, find_packages

setup(
    name="acid-discovery",
    version="9.0.0",
    description="Autonomous Computational Intelligence Discovery",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ACID Team",
    url="https://github.com/dudududi144-source/acid-discovery",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "httpx>=0.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "acid=acid_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="ai discovery evolution substrate verification transfer",
)
