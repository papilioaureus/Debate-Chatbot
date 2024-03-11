from setuptools import setup, find_packages
from pathlib import Path

# version
here = Path(__file__).absolute().parent
version_data = {}
with open(here.joinpath("debchatlib", "__init__.py"), "r") as f:
    exec(f.read(), version_data)
version = version_data.get("__version__", "0.0")

install_requires = [
    "python-dotenv>=1.0.0"
    , "huggingface-hub>=0.20.2"
    , "langchain>=0.1.0"
    , "langchain-community>=0.0.12"
    , "langchain-openai>=0.0.3"
    , "openai>=1.7.2"
    , "transformers>=4.35.0"
    , "torch>=2.2.0"
    , "torchaudio>=2.2.0"
    , "torchvision>=0.17.0"
    , "accelerate>=0.21.0"
    , "ipywidgets>=8.1.2"
]

setup(
    name="debchatlib",
    version=version,
    install_requires=install_requires,
    package_dir={"debchatlib": "debchatlib"},
    python_requires=">=3.6, <3.10",
    packages=find_packages(where=".", exclude=["docs", "examples", "tests"]),
)
