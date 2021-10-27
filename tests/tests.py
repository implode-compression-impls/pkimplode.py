#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path
import mmap
from secrets import token_bytes

from fileTestSuite.unittest import FTSTestClass, GeneratedTestProgram

thisDir = Path(__file__).resolve().absolute().parent
repoRootDir = thisDir.parent

sys.path.insert(0, str(repoRootDir))

from collections import OrderedDict
dict = OrderedDict

from pkimplode import compress, compressBytesChunkedToBytes, compressStreamToBytes
from pklib_base import decodeHeader
import pkblast


class PkImplodeTestClass(FTSTestClass):
	@classmethod
	def getFileTestSuiteDir(cls) -> Path:
		return thisDir / "testDataset"

	def _testPack(self, chall: bytes, resp: bytes):
		tpName = chall.__class__.__name__
		#with self.subTest("compress " + tpName):
		#	self.assertEqual(resp, compress(chall))
		with self.subTest("compressBytesChunkedToBytes " + tpName):
			compressionType, dictionarySize = decodeHeader(resp)
			compressed = compressBytesChunkedToBytes(chall, compressionType=compressionType, dictionarySize=dictionarySize)
			self.assertEqual(resp, compressed)
		#with self.subTest("compressBytesChunkedToBytes " + tpName):
		#	self.assertEqual(resp, compressBytesChunkedToBytes(chall))
		#with self.subTest("compressBytesWholeToBytes " + tpName):
		#	self.assertEqual(resp, compressBytesWholeToBytes(chall))

	def _testCompressionCorrectness(self, decomp: bytes):
		comp = compressBytesChunkedToBytes(decomp)
		decomp1 = pkblast.decompressBytesWholeToBytes(comp)
		self.assertEqual(decomp, decomp1)

	def _testProcessorImpl(self, challFile: Path, respFile: Path, paramsDict=None) -> None:
		self._testChallengeResponsePair(challFile.read_bytes(), respFile.read_bytes())
		#pass

	def _testChallengeResponsePair(self, chall, resp):
		self._testPack(chall, resp)

		#with mmap.mmap(-1, len(chall), access=mmap.ACCESS_READ|mmap.ACCESS_WRITE) as mm:
		#	mm.write(chall)
		#	mm.seek(0)
		#	self._testPack(mm, resp)

	def testImplodeDecoder(self):
		for i in range(1024):
			with self.subTest(additionalSize = i):
				decomp = token_bytes(10000 + i)
				comp = self._testCompressionCorrectness(decomp)

		self._testChallenge(decomp, comp)


if __name__ == "__main__":
	GeneratedTestProgram(PkImplodeTestClass)
