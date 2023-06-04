#!/usr/bin/env python
#
# This module is part of the rtmpSnoop project
#  https://github.com/andreafabrizi/rtmpSnoop
#
# Copyright (C) 2013 Andrea Fabrizi <andrea.fabrizi@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA
#
from scapy.all import hexdump

class Stream():
    
    def __init__(self, stream = b""):
        self.stream = stream
        self.offset = 0
        self.size = len(stream)
        self.dontScanAgain = False
        self.unmergedData = []

    #Appends new data to the buffer
    def appendData(self, data):
        self.unmergedData.append(data)
        self.size +=len(data)
    
    #Merges the buffered data into the stream
    def _mergeData(self):
        if self.unmergedData:
            self.stream += b"".join(self.unmergedData);
            self.unmergedData = []
    
    #Prints the stream 
    def dump(self):
        self._mergeData()
        hexdump(self.stream[self.offset:])

    #Gets n bytes from the stream and increments the offset
    def getBytes(self, n):
        if self.offset + n> self.size:
            raise StreamNoMoreBytes

        self._mergeData()
        bytes = self.stream[self.offset:self.offset+n]
        self.offset = self.offset + n
        return bytes

    #Get a single byte from the stream
    def getByte(self):
        return ord(self.getBytes(1))

    #Reads n bytes from the stream without incrementing the offset
    def readBytes(self, n):
        if self.offset >= self.size:
            return None

        self._mergeData()
        bytes = self.stream[self.offset:self.offset+n]
        return bytes

    #Returns True if there are bytes to be read, False otherwise
    def haveBytes(self):
        if self.offset >= self.size:
            return False
        else:
            return True

class StreamNoMoreBytes(Exception):
    pass

