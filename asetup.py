import io

from setuptools import setup, find_packages

main_ns = {}
exec(open("dash/version.py").read(), main_ns)  # pylint: disable=exec-used, consider-using-with


def read_req_file(req_type):
    with open("requires-{}.txt".format(req_type)) as fp:
        requires = (line.strip() for line in fp)
        return [req for req in requires if req and not req.startswith("#")]


setup(
    name="adash",
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
    url="https://github.com/snehilvj/dash",
)
