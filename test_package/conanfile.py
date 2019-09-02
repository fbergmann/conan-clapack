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
        if self.settings.arch =="x86" and self.settings.compiler == "gcc":
            # i see strange hangs on linux 32 bit & gcc so skipping those for now
            return
        with tools.chdir('bin'):
            self.run('test_lapack.exe' if self.settings.os == 'Windows' else './test_lapack', run_environment=True)