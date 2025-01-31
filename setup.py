from setuptools import find_packages, setup

setupdict = {
    "name":
    "sync",
    "version":
    "0.1.0",
    "packages":
    find_packages(),
    "include_package_data":
    True,
    "install_requires":
    ["websockets", "bson", 'colorlog', 'numpy', 'pandas', 'numpy'],
}
if __name__ == "__main__":
    setup(**setupdict)
