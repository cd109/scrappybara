import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrappybara",
    version="1.0.1",
    author="Eric Perriard",
    author_email="contact@scrappybara.com",
    description="Natural Language Processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ericperriard.github.io/scrappybara",
    packages=[
        "scrappybara",
        "scrappybara.data",
        "scrappybara.langmodel",
        "scrappybara.normalization",
        "scrappybara.pipeline",
        "scrappybara.preprocessing",
        "scrappybara.semantics",
        "scrappybara.syntax",
        "scrappybara.utils",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.5',
)
