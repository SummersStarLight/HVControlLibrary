#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2013  <ast1@linuxAnKa>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

# Echo client program
import socket

HOST = ''    				 # The remote host
PIC_PORT = 3737              # The same port as used by the server
TRC_PORT = 2828

class PBBHAL:
        def __init__(self):
                self.PICsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.PICsock.connect((HOST, PIC_PORT))
                
				self.TRCsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.TRCsock.connect((HOST, TRC_PORT))

        def setCLVoltage(self,input):
                strData = "setCLMidVoltage " + str(input)
                self.PICsock.sendall(strData)
                data = self.PICsock.recv(1024)
                #print 'Received', repr(data)

        def getCLMidVoltage(self):
                self.TRCsock.sendall('getCLMidVoltage')
                data = self.TRCsock.recv(1024)
                return float(data)
                

        def getCLMidCurrent(self):
                self.TRCsock.sendall('getCLMidCurrent')
                data = self.TRCsock.recv(1024)
                return float(data)
                
        def __del__(self):
                self.PICsock.close()
                self.TRCsock.close()

if (__name__ == "__main__"):
        x = PBBHAL()
        x.setCLVoltage(1000)
        print "CL mid voltage readback:%f" %(x.getCLMidVoltage())
        print "CL mid current readback:%f" %(x.getCLMidCurrent())

