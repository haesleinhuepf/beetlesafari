import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="beetlesafari",
    version="0.3.1",
    author="Robert Haase",
    author_email="robert.haase@tu-dresden.de",
    description="A napari plugin for loading and working with light sheet imaging data of developing embryos acquired using ClearControl, e.g. _Tribolium castaneum_.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haesleinhuepf/beetlesafari",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["numpy", "pyopencl", "toolz", "scikit-image", "requests", "pyclesperanto-prototype", "napari", "magicgui", "dask", "cachetools", "napari-tools-menu"],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: napari",
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
    ],
    entry_points={
        "napari.plugin": [
            "beetlesafari = beetlesafari",
        ],
    },
)

