from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="myer-pim-sdk",
    version="1.0.0",
    author="Myer Development Team",
    author_email="dev@myer.com.au",
    description="Python SDK for Akeneo REST API integration with Myer's PIM system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/myer/myer-pim-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "redis": [
            "redis>=4.0.0",
        ],
    },
    keywords="akeneo pim myer api sdk product-information-management",
    project_urls={
        "Bug Reports": "https://github.com/myer/myer-pim-sdk/issues",
        "Source": "https://github.com/myer/myer-pim-sdk",
        "Documentation": "https://myer-pim-sdk.readthedocs.io/",
    },
)
