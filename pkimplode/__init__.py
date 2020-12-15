import typing
from collections.abc import ByteString
from io import BytesIO, IOBase
from mmap import mmap
from warnings import warn
from zlib import crc32 as crc32_zlib

from pklib_base import PklibError
from pklib_base.enums import CompressionType

from .ctypes import _compressStream


__all__ = ("compressStreamToStream", "compressStreamToBytes", "compressBytesChunkedToStream", "compressBytesChunkedToBytes", "compress")

allowed_dict_sizes = frozenset((1024, 2048, 4096))

DEFAULT_DICTIONARY_SIZE = 4096


def compressStreamToStream(inputStream: IOBase, outputStream: IOBase, compressionType: CompressionType = CompressionType.binary, dictionarySize: int = DEFAULT_DICTIONARY_SIZE) -> None:
	"""Used to do streaming compression. The first arg is the stream to read from, the second ard is the stream to write to.
	May be a memory map. `chunkSize` is the hint"""

	assert dictionarySize in allowed_dict_sizes, "Unallowed dict size, must be from " + repr(allowed_dict_sizes)

	errorCode = _compressStream(inputStream, outputStream, compressionType=int(compressionType), dictionarySize=dictionarySize)

	if errorCode:
		raise Exception(PklibError(errorCode))


def compressBytesChunkedToStream(rawData: ByteString, outputStream: IOBase, compressionType: CompressionType = CompressionType.binary, dictionarySize: int = DEFAULT_DICTIONARY_SIZE) -> int:
	"""Compresses `rawData` into `outputStream`."""
	with BytesIO(rawData) as inputStream:
		return compressStreamToStream(inputStream, outputStream, compressionType, dictionarySize)


def compressBytesChunkedToBytes(rawData: ByteString, compressionType: CompressionType = CompressionType.binary, dictionarySize: int = DEFAULT_DICTIONARY_SIZE) -> int:
	"""Compresses `rawData` into `bytes`."""
	with BytesIO() as outputStream:
		compressBytesChunkedToStream(rawData, outputStream, compressionType, dictionarySize)
		return outputStream.getvalue()


def compressStreamToBytes(inputStream: IOBase, compressionType: CompressionType = CompressionType.binary, dictionarySize: int = DEFAULT_DICTIONARY_SIZE) -> int:
	"""Compresses `inputStream` into `outputStream`. Processes the whole data."""
	with BytesIO() as outputStream:
		compressStreamToStream(inputStream, outputStream, compressionType, dictionarySize)
		return outputStream.getvalue()


_functionsUseCaseMapping = (
	compressStreamToStream,
	compressBytesChunkedToStream,
	compressStreamToBytes,
	compressBytesChunkedToBytes,
)


def compress(rawData: typing.Union[ByteString, IOBase], outputStream: typing.Optional[IOBase] = None) -> int:
	"""A convenience function. It is better to use the more specialized ones since they have less overhead. It compresses `rawData` into `outputStream` and returns a tuple `(left, output)`.
	`rawData` can be either a stream, or `bytes`-like stuff.
	If `outputStream` is None, then it returns `bytes`. If `outputStream` is a stream, it writes into it.
	`left` returned is the count of bytes in the array/stream that weren't processed."""

	isOutputBytes = outputStream is None
	isInputBytes = isinstance(rawData, (ByteString, mmap))
	selector = isOutputBytes << 1 | int(isInputBytes)
	func = _functionsUseCaseMapping[selector]
	argz = [rawData]
	if not isOutputBytes:
		argz.append(outputStream)
	warn("Use " + func.__name__ + " instead.")
	return func(*argz)
