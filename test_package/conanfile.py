from conans import ConanFile, CMake, tools
import os
import shutil

class RaptorTestConan(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        mat_path = os.path.join(self.source_folder, "matrix.txt")
        shutil.copy(mat_path, 'bin')
        with tools.chdir('bin'):
            self.run('test_lapack.exe' if self.settings.os == 'Windows' else './test_lapack', run_environment=True)