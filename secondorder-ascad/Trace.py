'''
This file is part of pysca toolbox, license is GPLv3, see https://www.gnu.org/licenses/gpl-3.0.en.html
Authors: Erik van den Brink, Ilya Kizhvatov, Pol van Aubel
Version: 1.0, 2017-05-14

Open an INS TraceSet

Versions of this file:

v0.6 28-05-2017 (Pol)
    * performance greatly improved by using np.fromfile

v0.55 05-12-2014 (yet unidentified author at Riscure)
    * Added writing trace fileSize

v0.5 12-11-2013 (Ilya)
    * Fixed the format typo; a bit of cleanup

v0.4 12-11-2013 (Ilya)
    * Fixed the sample reading bug in general

v0.3 11-09-2013 (Erik)
    * Fixed sample reading bug in getTrace() as pointed out by Ilya

v0.2 5-3-2013 (Erik)
    * Fixed __iter__ method and removed the no longer necesarry getTraces() method
    * Moved header constants inside TraceSet class
    * Removed debug code
'''

from __future__     import print_function

import sys
import struct
import numpy as np

class Trace():
    def __init__(self, title, data, samples):
        self._title = title
        self._data = data
        self._samples = samples

class TraceSet():
    #header definitions
    NumberOfTraces          = 0x41
    NumberOfSamplesPerTrace = 0x42
    SampleCoding            = 0x43
    DataSpace               = 0x44
    TitleSpace              = 0x45
    GlobalTitle             = 0x46
    Description             = 0x47
    XLabel                  = 0x49
    YLabel                  = 0x4a
    XScale                  = 0x4b
    YScale                  = 0x4c
    ScopeRange              = 0x55
    ChannelCoupling         = 0x56
    Offset                  = 0x57
    ScopeID                 = 0x59
    TraceBlock              = 0x5F #Trace block, a flat memory space

    # enum for sampe coding
    CodingByte  = 0x01
    CodingShort = 0x02
    CodingInt   = 0x04
    CodingFloat = 0x14

    def __init__(self):
        self._handle = None
        self._traceBlockOffset = None
        self._numberOfTraces = None
        self._numberOfSamplesPerTrace = None
        self._sampleCoding = None
        self._npSampleCoding = None
        self._sampleCodingByteSize = None
        self._titleSpace = 0
        self._dataSpace = 0
        self._yscale = 1
        self._fileName = None

        #properties
        self._sampleSpace = None
        self._traceSpace = None
        self._traceBlockSpace = 0

        self._iterIndex = 0

    def __iter__(self):
        for i in range(self._numberOfTraces):
            yield self.getTrace(i)

    def _readUINT8(self):
        return struct.unpack("B",self._handle.read(1))[0];

    def _readUINT16(self):
        return struct.unpack("H",self._handle.read(2))[0];

    def _readUINT32(self):
        return struct.unpack("I",self._handle.read(4))[0];

    def _readFloat32(self):
        return struct.unpack("f",self._handle.read(4))[0];

    def _writeUINT8(self, val):
        #print "UINT8: %02x"%(val&0xFF)
        return self._handle.write(struct.pack("B",(val&0xFF)));

    def _writeUINT16(self, val):
        #print "UINT16: %04x"%(val&0xFFFF)
        return self._handle.write(struct.pack("H",(val&0xFFFF)));

    def _writeUINT32(self, val):
        #print "UINT32: %08x"%(val&0xFFFFFFFF)
        return self._handle.write(struct.pack("I",(val&0xFFFFFFFF)));

    def _writeTitleSpace(self, val):
        self._writeUINT8(self.TitleSpace)
        self._writeUINT8(1)
        self._writeUINT8(val)
        self._titleSpace = val

    def _writeNumberOfTraces(self, val):
        self._writeUINT8(self.NumberOfTraces)
        self._writeUINT8(4)
        self._writeUINT32(val)
        self._numberOfTraces = val

    def _updateNumberOfTraces(self, val):
        self.findTag(self.NumberOfTraces)
        self._writeUINT8(self.NumberOfTraces)
        self._writeUINT8(4)
        self._writeUINT32(val)
        self._numberOfTraces = val

    def _writeDataSpace(self, val):
        self._writeUINT8(self.DataSpace)
        self._writeUINT8(2)
        self._writeUINT16(val)
        self._dataSpace = val

    def _writeNumberOfSamplesPerTrace(self, val):
        self._writeUINT8(self.NumberOfSamplesPerTrace)
        self._writeUINT8(4)
        self._writeUINT32(val)
        self._numberOfSamplesPerTrace = val

    def _writeSampleCoding(self, val):
        self._writeUINT8(self.SampleCoding)
        self._writeUINT8(1)
        self._writeUINT8(val)
        self._sampleCoding = val

    def _writeTraceBlock(self):
        self._writeUINT8(self.TraceBlock)
        self._writeUINT8(0)

    def open(self, fileName):
        self._handle = open(fileName,'rb')
        f = self._handle
        f.seek(0,2)

        fileSize = f.tell()
        f.seek(0)
        offset = 0

        while (offset < fileSize - self._traceBlockSpace):
            tag = ord(f.read(1))
            length = ord(f.read(1))
            addLen = 0

            if ((length & 0x80) != 0): #length is encoded in more then 1 byte
                addLen = length & 0x7F #how many byte the length is actually encoded in.
                length = 0
                for i in range(addLen):
                    length = length + (ord(f.read(1)) << (i * 8))

            if tag == self.TraceBlock:
                self._sampleSpace = self._numberOfSamplesPerTrace * self._sampleCodingByteSize
                self._traceSpace = self._sampleSpace + self._dataSpace + self._titleSpace
                self._traceBlockSpace = self._numberOfTraces * self._traceSpace

                self._traceBlockOffset = f.tell() #get current pos
                f.seek(self._traceBlockOffset + self._traceBlockSpace) # XXX: why this?
            elif tag == self.TitleSpace:
                if length != 1:
                    raise ValueError("Incorrect length for TitleSpace header field")
                self._titleSpace = self._readUINT8()
            elif tag == self.NumberOfTraces:
                if length != 4:
                    raise ValueError("Incorrect length for NumberOfTraces header field")
                self._numberOfTraces = self._readUINT32()
            elif tag == self.DataSpace:
                if length != 2:
                    raise ValueError("Incorrect length for DataSpace header field")
                self._dataSpace = self._readUINT16()
            elif tag == self.NumberOfSamplesPerTrace:
                if length != 4:
                    raise ValueError("Incorrect length for NumberOfSamplesPerTrace header field")
                self._numberOfSamplesPerTrace = self._readUINT32()
            elif tag == self.YScale:
                if length != 4:
                    raise ValueError("Incorrect length for YScale header field")
                self._yscale = self._readFloat32()
            elif tag == self.SampleCoding:
                if length != 1:
                    raise ValueError("Incorrect length for SampleCoding header field")
                self._sampleCoding = self._readUINT8()
                #compensate for float sample coding tag
                if self._sampleCoding == self.CodingFloat: #float
                    self._sampleCodingByteSize = 4
                    self._npSampleCoding = "float32"
                else:
                    self._npSampleCoding = "int" + str(self._sampleCoding * 8)
                    self._sampleCodingByteSize = self._sampleCoding
            else:
                print("Unhandled tag: %x len: %d" % (tag, length), file=sys.stderr) # TODO: support other optional tags
                f.read(length)

            offset = offset + 2 + addLen + length

    def findTag(self,searchTag):
        if (self._handle == None):
            return 0
        f = self._handle
        f.seek(0,2)
        fileSize = f.tell()
        f.seek(0)
        offset = 0

        while (offset < fileSize - self._traceBlockSpace):
            tag = ord(f.read(1))
            length = ord(f.read(1))
            addLen = 0

            if ((length & 0x80) != 0): #length is encoded in more then 1 byte
                addLen = length & 0x7F #how many byte the length is actually encoded in.
                length = 0
                for i in range(addLen):
                    length = length + (ord(f.read(1)) << (i * 8))
            if (tag == searchTag):
                f.seek(offset)
                return 1
            f.read(length)
            offset = offset + 2 + addLen + length
        return 0

    def new(self, fileName, titleSpace, sampleCoding, dataSpace, numberOfSamples):
        self._fileName = fileName
        self._handle = open(fileName,'wb')
        self._handle.close()
        self._handle = open(fileName,'r+b')

        self._writeTitleSpace(titleSpace)
        self._writeSampleCoding(sampleCoding)
        if self._sampleCoding == self.CodingFloat: #float
            self._sampleCodingByteSize = 4
            self._npSampleCoding = "float32"
        else:
            self._npSampleCoding = "int" + str(self._sampleCoding * 8)
            self._sampleCodingByteSize = self._sampleCoding
        self._writeDataSpace(dataSpace)
        self._writeNumberOfSamplesPerTrace(numberOfSamples)
        self._writeNumberOfTraces(0)
        self._sampleSpace = self._numberOfSamplesPerTrace * self._sampleCodingByteSize
        self._traceSpace = self._sampleSpace + self._dataSpace + self._titleSpace
        self._traceBlockSpace = self._numberOfTraces * self._traceSpace
        self._writeTraceBlock()
        self._traceBlockOffset = self._handle.tell() #get current pos

    def getTrace(self, traceIndex):
        if (self._handle == None):
            return None
        f = self._handle
        f.seek(self._traceBlockOffset + traceIndex * self._traceSpace)
        
        title = f.read(self._titleSpace)
        data = np.fromfile(f, dtype='uint8', count=self._dataSpace)
        samples = np.fromfile(f, dtype=self._npSampleCoding, count=self._numberOfSamplesPerTrace)

        return Trace(title, data, samples)

    def addTrace(self, trace):
        if (self._handle == None):
            return
        f = self._handle
        f.seek(0,2)

        # we only accept exact same size inputs
        if (len(trace._title) != self._titleSpace):
            raise ValueError("Wrong title size! %08x/%08x"%(len(trace._title),self._titleSpace))
        f.write(trace._title)
        if (len(trace._data) != self._dataSpace):
            raise ValueError("Wrong data size!")
        trace._data.tofile(f)
        trace._samples.tofile(f)
        self._numberOfTraces+=1
        # update the trace count
        self._updateNumberOfTraces(self._numberOfTraces)
        # go to the end again
        f.seek(0,2)

    def close(self):
        self._handle.close()
