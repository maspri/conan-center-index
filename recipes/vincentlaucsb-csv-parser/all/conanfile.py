from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os

required_conan_version = ">=1.33.0"


class VincentlaucsbCsvParserConan(ConanFile):
    name = "vincentlaucsb-csv-parser"
    description = "Vince's CSV Parser with simple and intuitive syntax"
    topics = ("conan", "csv-parser", "csv", "rfc 4180", "parser", "generator")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/vincentlaucsb/csv-parser"
    license = "MIT"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"

    exports_sources = "CMakeLists.txt"

    options = {"header_only": [True, False]}

    default_options = {"header_only": False}

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def validate(self):
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, 11)

        compiler = self.settings.compiler
        compiler_version = tools.Version(self.settings.compiler.version)
        if compiler == "gcc" and compiler_version < "7":
            raise ConanInvalidConfiguration("gcc version < 7 not supported")

    def package_id(self):
        if self.options.header_only:
            self.info.header_only()

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def build(self):
        if not self.options.header_only:
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        if self.options.header_only:
            self.copy(pattern="*", dst="include", src=os.path.join(self._source_subfolder, "single_include"))
        else:
            self.copy(pattern="*.h", dst="include", src=os.path.join(self._source_subfolder, "include"))
            self.copy(pattern="*.hpp", dst="include", src=os.path.join(self._source_subfolder, "include"))

            self.copy(pattern="*.a", dst="lib", src="lib")
            self.copy(pattern="*.lib", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["csv"]

        if self.settings.os in ("Linux", "FreeBSD"):
            self.cpp_info.system_libs.append("pthread")
