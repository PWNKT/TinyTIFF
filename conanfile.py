from conan import ConanFile
from conan.tools.files import copy
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps


class TinyTiffRecipe(ConanFile):
    name = "tinytiff"
    version = "1.0"

    license = "GNU Lesser General Public License 3.0 (LGPL 3.0)"
    author = "Jan W. Krieger jan@jkrieger.de"
    url = "https://github.com/jkriege2/TinyTIFF"
    description = "This is a lightweight C/C++ library, which is able to read and write basic TIFF files. \
        It is significantly faster than libTIFF, especially in writing large multi-frame TIFFs."
    topics = (
        "lib",
        "file-format",
        "tiff-files",
        "tiff-encoder",
        "tiff-ios",
        "Resources",
    )

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "TinyTIFF_BUILD_SHARED_LIBS": [True, False],
        "TinyTIFF_BUILD_STATIC_LIBS": [True, False],
        "TinyTIFF_USE_WINAPI_FOR_FILEIO": [True, False],
        "TinyTIFF_BUILD_WITH_ADDITIONAL_DEBUG_OUTPUT": [True, False],
        "TinyTIFF_BUILD_DECORATE_LIBNAMES_WITH_BUILDTYPE": [True, False],
        "TinyTIFF_BUILD_TESTS": [True, False],
        # "CMAKE_INSTALL_PREFIX": "ANY",
    }
    default_options = {
        "TinyTIFF_BUILD_SHARED_LIBS": False,
        "TinyTIFF_BUILD_STATIC_LIBS": True,
        "TinyTIFF_USE_WINAPI_FOR_FILEIO": False,
        "TinyTIFF_BUILD_WITH_ADDITIONAL_DEBUG_OUTPUT": False,
        "TinyTIFF_BUILD_DECORATE_LIBNAMES_WITH_BUILDTYPE": False,
        "TinyTIFF_BUILD_TESTS": False,
    }

    exports_sources = (
        "CMakeLists.txt",
        "src/*",
        "cmake/*",
        "tests/*",
        "readme.txt.in",
        "README.md",
    )

    def config_options(self):
        if self.settings.os == "Windows":
            self.settings.compiler = "Visual Studio"

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.variables.update(self._generate_cmake_variables())
        tc.generate()

    def configure(self):
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def build_requirements(self):
        self.tool_requires("cmake/3.22.6")

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = []

        if self.options.TinyTIFF_BUILD_STATIC_LIBS:
            self.cpp_info.components["static"].libs = ["TinyTIFF"]
        if self.options.TinyTIFF_BUILD_SHARED_LIBS:
            self.cpp_info.components["shared"].libs = ["TinyTIFFShared"]

    def _generate_cmake_variables(self):
        options = {}
        if self.options.TinyTIFF_BUILD_SHARED_LIBS:
            options["TinyTIFF_BUILD_SHARED_LIBS"] = "ON"
        else:
            options["TinyTIFF_BUILD_SHARED_LIBS"] = "OFF"

        if self.options.TinyTIFF_BUILD_STATIC_LIBS:
            options["TinyTIFF_BUILD_STATIC_LIBS"] = "ON"
        else:
            options["TinyTIFF_BUILD_STATIC_LIBS"] = "OFF"

        if self.options.TinyTIFF_USE_WINAPI_FOR_FILEIO:
            options["TinyTIFF_USE_WINAPI_FOR_FILEIO"] = "ON"
        else:
            options["TinyTIFF_USE_WINAPI_FOR_FILEIO"] = "OFF"

        if self.options.TinyTIFF_BUILD_WITH_ADDITIONAL_DEBUG_OUTPUT:
            options["TinyTIFF_BUILD_WITH_ADDITIONAL_DEBUG_OUTPUT"] = "ON"
        else:
            options["TinyTIFF_BUILD_WITH_ADDITIONAL_DEBUG_OUTPUT"] = "OFF"

        if self.options.TinyTIFF_BUILD_DECORATE_LIBNAMES_WITH_BUILDTYPE:
            options["TinyTIFF_BUILD_DECORATE_LIBNAMES_WITH_BUILDTYPE"] = "ON"
        else:
            options["TinyTIFF_BUILD_DECORATE_LIBNAMES_WITH_BUILDTYPE"] = "OFF"

        if self.options.TinyTIFF_BUILD_TESTS:
            options["TinyTIFF_BUILD_TESTS"] = "ON"
        else:
            options["TinyTIFF_BUILD_TESTS"] = "OFF"

        return options
