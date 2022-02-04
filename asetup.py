import io

from setuptools import setup, find_packages

main_ns = {}
exec(open("dash/version.py").read(), main_ns)  # pylint: disable=exec-used, consider-using-with


def read_req_file(req_type):
    with open("requires-{}.txt".format(req_type)) as fp:
        requires = (line.strip() for line in fp)
        return [req for req in requires if req and not req.startswith("#")]


setup(
    name="async-dash",
    version=main_ns["__version__"],
    author="Snehil Vijay",
    author_email="snehilvj@outlook.com",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    license="MIT",
    description="Async port of the official Plotly Dash library",
    long_description=io.open("README.md", encoding="utf-8").read(),  # pylint: disable=consider-using-with
    long_description_content_type="text/markdown",
    install_requires=read_req_file("install"),
    python_requires=">=3.7",
    url="https://github.com/snehilvj/async-dash",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Dash",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Database :: Front-Ends",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Widget Sets",
    ],
)
