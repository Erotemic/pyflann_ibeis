#!/usr/bin/env python
r"""
Build Wheels:
    pip install cibuildwheel

    CIBW_BUILD_VERBOSITY=1 \
    CIBW_TEST_REQUIRES="-r requirements/tests.txt" \
    CIBW_TEST_COMMAND='python {project}/run_tests.py' \
    CIBW_SKIP='pp*' \
        cibuildwheel --config-file pyproject.toml --platform linux --arch x86_64
"""
import sys
from collections import OrderedDict
import re
from os.path import exists, dirname, join


def parse_version(fpath):
    """
    Statically parse the version number from a python file
    """
    value = static_parse("__version__", fpath)
    return value


def static_parse(varname, fpath):
    """
    Statically parse the a constant variable from a python file
    """
    import ast

    if not exists(fpath):
        raise ValueError("fpath={!r} does not exist".format(fpath))
    with open(fpath, "r") as file_:
        sourcecode = file_.read()
    pt = ast.parse(sourcecode)

    class StaticVisitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            for target in node.targets:
                if getattr(target, "id", None) == varname:
                    try:
                        self.static_value = node.value.value
                    except AttributeError:
                        self.static_value = node.value.s

    visitor = StaticVisitor()
    visitor.visit(pt)
    try:
        value = visitor.static_value
    except AttributeError:
        import warnings

        value = "Unknown {}".format(varname)
        warnings.warn(value)
    return value


def parse_description():
    """
    Parse the description in the README file

    CommandLine:
        pandoc --from=markdown --to=rst --output=README.rst README.md
        python -c "import setup; print(setup.parse_description())"
    """
    readme_fpath = join(dirname(__file__), "README.rst")
    # This breaks on pip install, so check that it exists.
    if exists(readme_fpath):
        with open(readme_fpath, "r") as f:
            text = f.read()
        return text
    return ""


def parse_requirements(fname="requirements.txt", versions=False):
    """
    Parse the package dependencies listed in a requirements file but strips
    specific versioning information.

    Args:
        fname (str): path to requirements file
        versions (bool | str, default=False):
            If true include version specs.
            If strict, then pin to the minimum version.

    Returns:
        List[str]: list of requirements items

    CommandLine:
        python -c "import setup, ubelt; print(ubelt.urepr(setup.parse_requirements()))"
    """
    require_fpath = fname

    def parse_line(line, dpath=""):
        """
        Parse information from a line in a requirements text file

        line = 'git+https://a.com/somedep@sometag#egg=SomeDep'
        line = '-e git+https://a.com/somedep@sometag#egg=SomeDep'
        """
        # Remove inline comments
        comment_pos = line.find(" #")
        if comment_pos > -1:
            line = line[:comment_pos]

        if line.startswith("-r "):
            # Allow specifying requirements in other files
            target = join(dpath, line.split(" ")[1])
            for info in parse_require_file(target):
                yield info
        else:
            # See: https://www.python.org/dev/peps/pep-0508/
            info = {"line": line}
            if line.startswith("-e "):
                info["package"] = line.split("#egg=")[1]
            else:
                if "--find-links" in line:
                    # setuptools doesnt seem to handle find links
                    line = line.split("--find-links")[0]
                if ";" in line:
                    pkgpart, platpart = line.split(";")
                    # Handle platform specific dependencies
                    # setuptools.readthedocs.io/en/latest/setuptools.html
                    # #declaring-platform-specific-dependencies
                    plat_deps = platpart.strip()
                    info["platform_deps"] = plat_deps
                else:
                    pkgpart = line
                    platpart = None

                # Remove versioning from the package
                pat = "(" + "|".join([">=", "==", ">"]) + ")"
                parts = re.split(pat, pkgpart, maxsplit=1)
                parts = [p.strip() for p in parts]

                info["package"] = parts[0]
                if len(parts) > 1:
                    op, rest = parts[1:]
                    version = rest  # NOQA
                    info["version"] = (op, version)
            yield info

    def parse_require_file(fpath):
        dpath = dirname(fpath)
        with open(fpath, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    for info in parse_line(line, dpath=dpath):
                        yield info

    def gen_packages_items():
        if exists(require_fpath):
            for info in parse_require_file(require_fpath):
                parts = [info["package"]]
                if versions and "version" in info:
                    if versions == "strict":
                        # In strict mode, we pin to the minimum version
                        if info["version"]:
                            # Only replace the first >= instance
                            verstr = "".join(info["version"]).replace(">=", "==", 1)
                            parts.append(verstr)
                    else:
                        parts.extend(info["version"])
                if not sys.version.startswith("3.4"):
                    # apparently package_deps are broken in 3.4
                    plat_deps = info.get("platform_deps")
                    if plat_deps is not None:
                        parts.append(";" + plat_deps)
                item = "".join(parts)
                yield item

    packages = list(gen_packages_items())
    return packages


try:
    class EmptyListWithLength(list):
        def __len__(self):
            return 1

        def __repr__(self):
            return 'EmptyListWithLength()'

        def __str__(self):
            return 'EmptyListWithLength()'
except Exception:
    raise RuntimeError('FAILED TO ADD BUILD CONSTRUCTS')


NAME = 'pyflann_ibeis'


VERSION = version = parse_version('pyflann_ibeis/__init__.py')  # must be global for git tags

AUTHORS = ['Jon Crall', 'Marius Muja']
AUTHOR_EMAIL = 'erotemic@gmail.com'
URL = 'https://github.com/Erotemic/pyflann_ibeis'
LICENSE = 'BSD'
DESCRIPTION = 'FLANN (for IBEIS) - Fast Library for Approximate Nearest Neighbors'


setupkw = {}
setupkw["install_requires"] = parse_requirements(
    "requirements/runtime.txt", versions="loose"
)
setupkw["extras_require"] = {
    "all": parse_requirements("requirements.txt", versions="loose"),
    "runtime": parse_requirements("requirements/runtime.txt", versions="loose"),
    "tests": parse_requirements("requirements/tests.txt", versions="loose"),
    "optional": parse_requirements("requirements/optional.txt", versions="loose"),
    "build": parse_requirements("requirements/build.txt", versions="loose"),
    "docs": parse_requirements("requirements/docs.txt", versions="loose"),
    "all-strict": parse_requirements("requirements.txt", versions="strict"),
    "runtime-strict": parse_requirements(
        "requirements/runtime.txt", versions="strict"
    ),
    "tests-strict": parse_requirements("requirements/tests.txt", versions="strict"),
    "optional-strict": parse_requirements(
        "requirements/optional.txt", versions="strict"
    ),
    "build-strict": parse_requirements("requirements/build.txt", versions="strict"),
    "docs-strict": parse_requirements("requirements/docs.txt", versions="strict"),
}


KWARGS = OrderedDict(
    name=NAME,
    version=VERSION,
    author=', '.join(AUTHORS),
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=parse_description(),
    long_description_content_type='text/x-rst',
    url=URL,
    license=LICENSE,
    **setupkw,

    # --- PACKAGES ---
    # The combination of packages and package_dir is how scikit-build will
    # know that the cmake installed files belong in the pyflann module and
    # not the data directory.

    packages=[
        'pyflann_ibeis',
        # These are generated modules that will be created via build
        'pyflann_ibeis.lib',
    ],
    package_dir={
        'pyflann_ibeis': 'pyflann_ibeis',
        # Note: this requires that FLANN_LIB_INSTALL_DIR is set to pyflann/lib
        # in the src/cpp/CMakeLists.txt
        'pyflann_ibeis.lib': 'pyflann_ibeis/lib',
    },
    package_data={
        'pyflann_ibeis': ['py.typed', '*.pyi'],
    },

    include_package_data=False,
    # List of classifiers available at:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 6 - Mature',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        # 'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition'
    ],
    cmake_args=[
        '-DBUILD_C_BINDINGS=ON',
        '-DBUILD_MATLAB_BINDINGS=OFF',
        '-DBUILD_EXAMPLES=OFF',
        '-DBUILD_TESTS=OFF',
        '-DBUILD_DOC=OFF',
    ],
    ext_modules=EmptyListWithLength(),  # hack for including ctypes bins
)

if __name__ == '__main__':
    """
    python -c "import pyflann_ibeis; print(pyflann_ibeis.__file__)"
    """
    import skbuild
    skbuild.setup(**KWARGS)
