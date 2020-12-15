pkimplode.py
============
~~[wheel (GitLab)](https://gitlab.com/KOLANICH/pkimplode.py/-/jobs/artifacts/master/raw/dist/pkimplode-0.CI-py3-none-any.whl?job=build)~~
[wheel (GHA via `nightly.link`)](https://nightly.link/implode-compression-impls/pkimplode.py/workflows/CI/master/pkimplode-0.CI-py3-none-any.whl)
~~![GitLab Build Status](https://gitlab.com/KOLANICH/pkimplode.py/badges/master/pipeline.svg)~~
~~![GitLab Coverage](https://gitlab.com/KOLANICH/pkimplode.py/badges/master/coverage.svg)~~
[![Coveralls Coverage](https://img.shields.io/coveralls/implode-compression-impls/pkimplode.py.svg)](https://coveralls.io/r/implode-compression-impls/pkimplode.py)
[![GitHub Actions](https://github.com/implode-compression-impls/pkimplode.py/workflows/CI/badge.svg)](https://github.com/implode-compression-impls/pkimplode.py/actions/)
[![Libraries.io Status](https://img.shields.io/librariesio/github/implode-compression-impls/pkimplode.py.svg)](https://libraries.io/github/implode-compression-impls/pkimplode.py)
[![License](https://img.shields.io/github/license/implode-compression-impls/pkimplode.py.svg)](./License.md)

This are free and Open-Source ctypes-based bindings to [`libimplode`](https://github.com/implode-compression-impls/libimplode) which is [a ripped out part](https://github.com/ladislav-zezula/StormLib/blob/master/src/pklib/implode.c) of [`pkglib`](https://github.com/ladislav-zezula/StormLib/tree/master/src/pklib) which is a Free Open-Source implementation of PKWare Data Compression Library (DCL) compression format, which itself was ripped out of [`StormLib`](https://github.com/ladislav-zezula/StormLib), all of which are by [Ladislav Zezula](https://github.com/ladislav-zezula).

For decompression you need [`pkblast.py`](https://github.com/implode-compression-impls/pkblast.py) a separate wrapper to a [separate library](https://github.com/madler/zlib/tree/master/contrib/blast) by [Mark @madler Adler](https://github.com/madler).

Benefits of CTypes-based impl:

* Supports python versions other than CPython
* No need to recompile python module after python version upgrade

Drawbacks:
* performance and overhead may be worse, than in the case of a cext.

Installation
------------

In order to make it work you need a package with `liblast` itself installed into your system using your distro package manager. If your distro doesn't provide one, you can build it yourself using CMake CPack from the sources [by the link](https://github.com/implode-compression-impls/libimplode). You will get 2 packages, one with the headers and another one with the shared library. Only the one with the lib is mandatory.

Usage
-----

The package contains multiple functions. They have names matching the regular expression `^decompress(Stream|Bytes(Whole|Chunked))To(Stream|Bytes)$`.

The first subgroup describes the type of input argument, the second subgroup describes the type of output.
* If input is `Bytes`, then you need
    * `Whole`, which means that the lib gots a pointer to whole array with compressed data. This is considered to be **the optimal input format**.
    * `Chunked` (which means the data are processed in reality by `decompressStreamTo$3`) was created mainly for convenience of testing.
* Otherwise it is an object acting like a stream. In this case you can also provide `chunkSize`, because streams are processed in chunks. Larger the chunk - less the count of chunks in the stream, so less overhead on calls of callbacks, but more memory is needed to store the chunk.

The second subgroup describes the type of the result.
* The internal type of the result is always a `Stream`. This is considered to be **the optimal output format**. It is because we don't know the size of output ahead of time, so have to use streams.
* `Bytes` are only for your convenience and just wrap the `decompress$1ToStream` with a context with `BytesIO`.
