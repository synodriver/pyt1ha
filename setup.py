# -*- coding: utf-8 -*-
import glob
import os
import re
import sys
import sysconfig
from collections import defaultdict

try:
    from Cython.Build import cythonize
    from Cython.Compiler.Version import version as cython_version
    from packaging.version import Version
except ImportError:
    Cython = None
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext

BUILD_ARGS = defaultdict(lambda: ["-O3", "-g0"])

for compiler, args in [
    ("msvc", ["/EHsc", "/DHUNSPELL_STATIC", "/Oi", "/O2", "/Ot"]),
    ("gcc", ["-O3", "-g0"]),
]:
    BUILD_ARGS[compiler] = args

os.environ["CFLAGS"] = "-save-temps -mno-avx2 -mno-avx -maes" # "-msse4.1 -mfma -mavx -march=native"

def has_option(name: str) -> bool:
    if name in sys.argv[1:]:
        sys.argv.remove(name)
        return True
    name = name.strip("-").upper()
    if os.environ.get(name, None) is not None:
        return True
    return False

class build_ext_compiler_check(build_ext):
    def build_extensions(self):
        compiler = self.compiler.compiler_type
        args = BUILD_ARGS[compiler]
        for ext in self.extensions:
            ext.extra_compile_args.extend(args)
            if self.compiler.compiler_type == "msvc":
                ext.define_macros.extend([("restrict", "__restrict")])
            else:
                pass
                # ext.extra_compile_args.extend(["-msse4.1", "-mfma", "-mavx"])
        super().build_extensions()


c_sources = ["t1ha/backends/cython/_t1ha.pyx"] + glob.glob("./dep/src/*.c")
# c_sources = list(filter(lambda x: "main" not in x, c_sources))
extensions = [
    Extension(
        "t1ha.backends.cython._t1ha",
        c_sources,
        include_dirs=["./dep"],
    ),
]
cffi_modules = ["t1ha/backends/cffi/build.py:ffibuilder"]


def get_dis():
    with open("README.markdown", "r", encoding="utf-8") as f:
        return f.read()


def get_version() -> str:
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "t1ha", "__init__.py"
    )
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    result = re.findall(r"(?<=__version__ = \")\S+(?=\")", data)
    return result[0]


packages = find_packages(exclude=("test", "tests.*", "test*"))


def has_option(name: str) -> bool:
    if name in sys.argv[1:]:
        sys.argv.remove(name)
        return True
    return False

if sysconfig.get_config_var("Py_GIL_DISABLED"):
    print("build nogil")
    define_macros = (
        ("Py_GIL_DISABLED", "1"),
    )  # ("CYTHON_METH_FASTCALL", "1"), ("CYTHON_VECTORCALL",  1)]

compiler_directives = {
    "cdivision": True,
    "embedsignature": True,
    "boundscheck": False,
    "wraparound": False,
}
if Version(cython_version) >= Version("3.1.0a0"):
    compiler_directives["freethreading_compatible"] = True
setup_requires = []
install_requires = []
setup_kw = {}
if has_option("--use-cython"):
    print("building cython")
    setup_requires.append("cython>=3.0.10")
    setup_kw["ext_modules"] = cythonize(
        extensions,
        compiler_directives=compiler_directives,
    )
if has_option("--use-cffi"):
    print("building cffi")
    setup_requires.append("cffi>=1.0.0")
    install_requires.append("cffi>=1.0.0")
    setup_kw["cffi_modules"] = cffi_modules


def main():
    version: str = get_version()

    dis = get_dis()
    setup(
        name="t1ha",
        version=version,
        url="https://github.com/synodriver/pyt1ha",
        packages=packages,
        keywords=["hash"],
        description="t1ha hash",
        long_description_content_type="text/markdown",
        long_description=dis,
        author="synodriver",
        author_email="diguohuangjiajinweijun@gmail.com",
        python_requires=">=3.9",
        setup_requires=setup_requires,
        install_requires=install_requires,
        license="BSD",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            "Programming Language :: C",
            "Programming Language :: Cython",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
        ],
        include_package_data=True,
        zip_safe=False,
        cmdclass={"build_ext": build_ext_compiler_check},
        **setup_kw
    )


if __name__ == "__main__":
    main()
