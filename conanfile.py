import os

from conans import ConanFile
from conans.model import Generator
from conans.paths import get_conan_user_home


class Bazel(Generator):
    def __init__(self, conanfile):
        super().__init__(conanfile)
        self.cache_root = os.path.join(get_conan_user_home(), ".conan", "data")

    @property
    def filename(self):
        pass

    @property
    def content(self):
        sections = []
        for dep_name, dep_cpp_info in self.deps_build_info.dependencies:
            dep_source = self.create_bazel_lib(dep_cpp_info)
            if dep_source:
                sections.append(dep_source)
        build_file = "\n".join(sections)

        source = """def add_conan_repository():
    native.new_local_repository(
        name = "external",
        path = "{0}",
        build_file_content = \"\"\"{1}\"\"\"
    )
""".format(self.cache_root, build_file)
        return {"BUILD.bazel": "", "conan.bzl": source}

    def create_bazel_lib(self, cpp_info):
        if not cpp_info.include_paths and not cpp_info.libs:
            return None

        result = ""
        if cpp_info.libs:
            result += "cc_import(\n"
            result += "    name = \"{0}_precompiled\",\n".format(cpp_info.name)
            result += "    static_library = \"{0}/lib{1}.a\"\n".format(
                self.cache_relpath(cpp_info.lib_paths[0]), cpp_info.libs[0])
            result += ")\n\n"

        result += "cc_library(\n"
        result += "    name = \"{0}\",\n".format(cpp_info.name)
        if cpp_info.include_paths:
            result += "    hdrs = glob([{0}]),\n".format(
                ", ".join("\"{0}/**\"".format(self.cache_relpath(path)) for path in cpp_info.include_paths))
            result += "    includes = [{0}],\n".format(
                ", ".join("\"{0}\"".format(self.cache_relpath(path)) for path in cpp_info.include_paths))
        if cpp_info.libs:
            result += "    deps = [\":%s_precompiled\"],\n" % cpp_info.name
        result += "    visibility = [\"//visibility:public\"]\n"
        result += ")\n"
        return result

    def cache_relpath(self, path):
        return os.path.relpath(path, self.cache_root)


class BazelGeneratorPackage(ConanFile):
    name = "conan-bazel"
    version = "0.1"
    license = "MIT"
    author = "Sergey Chelombitko"
    url = "https://github.com/technoir42/conan-bazel"
    description = "Bazel generator for Conan"
