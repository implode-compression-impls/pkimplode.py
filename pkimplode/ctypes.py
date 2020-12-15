import ctypes

from pklib_base import ReadFunT, WriteFunT, _initLibrary, getStreamCallbacks

__all__ = ("TCmpStruct", "sizeConstants", "_compressStream")


specializedSizeConstantsFields = (
	("internalStructSize", None),
	("OFFSS_SIZE2", 516),
	("LITERALS_COUNT", 774),
	("HASHTABLE_SIZE", 2304),
	("BUFF_SIZE", 8708)
)


def _getFieldsForInternalStateStructure(sizeConstants):  # pylint:disable=redefined-outer-name
	return [
		("distance", ctypes.c_uint),
		("out_bytes", ctypes.c_uint),
		("out_bits", ctypes.c_uint),
		("dsize_bits", ctypes.c_uint),
		("dsize_mask", ctypes.c_uint),
		("ctype", ctypes.c_uint),
		("dsize_bytes", ctypes.c_uint),
		("dist_bits", ctypes.c_ubyte * sizeConstants.common.DIST_SIZES),
		("dist_codes", ctypes.c_ubyte * sizeConstants.common.DIST_SIZES),
		("nChBits", ctypes.c_ubyte * sizeConstants.LITERALS_COUNT),
		("nChCodes", ctypes.c_ushort * sizeConstants.LITERALS_COUNT),
		("offs09AE", ctypes.c_ushort),
		("param", ctypes.POINTER(None)),
		("read_buf", ReadFunT),
		("write_buf", WriteFunT),
		("offs09BC", ctypes.c_ushort * sizeConstants.OFFSS_SIZE2),
		("offs0DC4", ctypes.c_ulong),
		("phash_to_index", ctypes.c_ushort * sizeConstants.HASHTABLE_SIZE),
		("phash_to_index_end", ctypes.c_ushort),
		("out_buff", ctypes.c_char * sizeConstants.common.OUT_BUFF_SIZE),
		("work_buff", ctypes.c_ubyte * sizeConstants.BUFF_SIZE),
		("phash_offs", ctypes.c_ushort * sizeConstants.BUFF_SIZE),
	]


TCmpStruct = None


def implode(read_buf: ReadFunT, write_buf: WriteFunT, work_buf: ctypes.POINTER(TCmpStruct), arbitraryData: ctypes.POINTER(None), compressionType: ctypes.POINTER(ctypes.c_uint), dictionarySize: ctypes.POINTER(ctypes.c_uint)) -> ctypes.c_uint:  # pylint:disable=too-many-arguments
	return lib.implode(read_buf, write_buf, work_buf, arbitraryData, compressionType, dictionarySize)


lib, TCmpStruct, sizeConstants = _initLibrary(implode, "TCmpStruct", specializedSizeConstantsFields, _getFieldsForInternalStateStructure)

def _compressStream(inputStream, outputStream, compressionType, dictionarySize) -> int:
	s = TCmpStruct()

	comprTypeInt = ctypes.c_uint(compressionType)
	dictionarySizeInt = ctypes.c_uint(dictionarySize)

	return implode(
		*getStreamCallbacks(inputStream, outputStream),
		work_buf=ctypes.byref(s),
		arbitraryData=None,
		compressionType=ctypes.byref(comprTypeInt),
		dictionarySize=ctypes.byref(dictionarySizeInt)
	)
