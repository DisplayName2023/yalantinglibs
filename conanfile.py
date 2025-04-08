from os.path import join
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, collect_libs
from pathlib import Path

class YalantinglibsConan(ConanFile):
    name = "yalantinglibs"
    license = "MIT"
    author = "Yalantinglibs"
    url = "yalantinglibs"
    version = "0.3.9-1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"
    exports_sources = "CMakeLists.txt", "include/*", "cmake/*" # "src/*", 

    build_policy = "missing"
    short_paths = True

    requires = "magic_enum/0.9.6"

    def requirements(self):
        self.requires("asio/1.28.0")
        
    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_TESTING"] = False
        tc.generate()
        
        deps = CMakeDeps(self)
        deps.generate()



    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        copy(self, "*.h", self.build_folder, join(self.package_folder, "include"), keep_path=True)
        copy(self, "*.lib", self.build_folder, join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.dll", self.build_folder, join(self.package_folder, "bin"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
        self.output.info("package_info() " + ' '.join(self.cpp_info.libs))
        self.cpp_info.names["cmake_find_package"] = "yalantinglibs"
        self.cpp_info.names["cmake_find_package_multi"] = "yalantinglibs"