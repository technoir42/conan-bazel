# conan-bazel

Bazel Generator for Conan.

## Usage
Add remote repository with the package:

```
conan remote add sch https://api.bintray.com/conan/sch/conan
```

Add package and enable the generator in `conanfile.txt`:

```
[requires]
conan-bazel/0.1

[generators]
Bazel
```

Install the package, telling Conan to build it from source:

```
conan install --build conan-bazel/* ..
```

Add the generated repository to Bazel:

```
load("//repo-dir:conan.bzl", "add_conan_repository")
add_conan_repository()
```
