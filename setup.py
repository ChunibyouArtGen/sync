from setuptools import find_packages, setup

setupdict = {
    "name": "sync",
    "version": "0.0.1",
    "packages": find_packages(),
    "include_package_data": True,
    "install_requires": ["websockets", "bson"],
}
if __name__ == "__main__":
    setup(**setupdict)
