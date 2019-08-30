#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile, tools, CMake
import os

class ClapackConan(ConanFile):

    name = "clapack"
    version = "3.2.1"
    url = "http://github.com/fbergmann/conan-clapack"
    homepage = "https://github.com/copasi/copasi-dependencies/tree/master/src/clapack"
    author = "Frank Bergmann"
    license = "MIT"

    description = (" F2C translation of LAPACK 3.2.1"
" To get revisions info about LAPACK 3.2.1, please see http://www.netlib.org/lapack/lapack-3.2.1.html ")

    settings = "os", "arch", "compiler", "build_type"

    options = {
        "fPIC": [True, False]
    }

    default_options = (
        "fPIC=True"
    )

    generators = "cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

        if self.settings.os == "Linux":
            del self.options.fPIC


    def source(self):
        tools.get('https://github.com/copasi/copasi-dependencies/releases/download/v4.26.213/CLAPACK-3.2.1-Source.zip')
        os.rename("CLAPACK-3.2.1-Source", "src") 
        tools.replace_in_file('src/CMakeLists.txt', "include(GNUInstallDirs)", '''include(GNUInstallDirs)

include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()''')

    def _configure(self, cmake):
        args = ["-DBUILD_TESTING=OFF"]
        if self.settings.compiler == 'Visual Studio' and 'MT' in self.settings.compiler.runtime:
            args.append('-DWITH_STATIC_RUNTIME=ON')

        cmake.configure(build_folder="build", args=args, source_folder="src")

    def build(self):
        cmake = CMake(self)
        self._configure(cmake)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        self._configure(cmake)
        cmake.install()
        cmake.patch_config_paths()
        self.copy("*.lib", dst="lib", keep_path=False)
        if self.settings.os == "Windows":
            self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):

        libfile1 = "lapack"
        libfile2 = "blas"
        libfile3 = "f2c"

        if not self.settings.os == "Windows":
            libfile1 = "lib" + libfile1 + ".a"
            libfile2 = "lib" + libfile2 + ".a"
            libfile3 = "lib" + libfile3 + ".a"
        else:
            libfile1 += ".lib"
            libfile2 += ".lib"
            libfile3 = "lib" + libfile3 + ".lib"

        self.cpp_info.libs = [libfile1, libfile2, libfile3]

        self.cpp_info.defines = ['HAVE_BLASWRAP_H', 'HAVE_F2C_H', 'HAVE_CLAPACK_H', 'NO_BLAS_WRAP']
