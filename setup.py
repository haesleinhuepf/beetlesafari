import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="beetlesafari",
    version="0.1.0",
    author="haesleinhuepf",
    author_email="robert.haase@tu-dresden.de",
    description="A library for working with light sheet imaging data of developing embryos, e.g. _Tribolium castaneum_.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haesleinhuepf/beetlesafari",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["numpy", "pyopencl", "toolz", "scikit-image", "requests", "pyclesperanto-prototype==0.7.0", "napari==0.4.5", "magicgui==0.2.6", "dask", "cachetools", "napari_pyclesperanto_assistant==0.7.2"],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
