from conans import ConanFile, CMake
import os

class RaptorTestConan(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        self.run(os.path.join("bin", "test_lapack" + " ../../matrix.txt"), run_environment=True)
