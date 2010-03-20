#! /usr/bin/env python
# -*- coding: ascii -*-

#	pySmsEngine API.
#	An open-source API package for sending and receiving SMS via a GSM device.
#	jSMSEngine  Copyright (C) 2002-2005, Thanasis Delenikas, Athens/GREECE
#	pySmsEngine Copyright (C) 2005-2007, Franco Bugnano
#
#	pySmsEngine is a package which can be used in order to add SMS processing
#		capabilities in an application.
#		pySmsEngine is written in python, and based on the Java software
#		jSMSEngine version 1.2.7.
#		It allows you to communicate with a compatible mobile phone or GSM
#		Modem, and send / receive SMS messages.
#
#	pySmsEngine is distributed under the LGPL license.
#
#	This library is free software; you can redistribute it and/or
#		modify it under the terms of the GNU Lesser General Public
#		License as published by the Free Software Foundation; either
#		version 2.1 of the License, or (at your option) any later version.
#	This library is distributed in the hope that it will be useful,
#		but WITHOUT ANY WARRANTY; without even the implied warranty of
#		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#		Lesser General Public License for more details.
#	You should have received a copy of the GNU Lesser General Public
#		License along with this library; if not, write to the Free Software
#		Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from gsm_alphabet import *

class CStatusReportMessage(object):
	def __init__(self, pdu, memIndex):
		self.memIndex = memIndex

		i = int(pdu[0:2], 16)
		index = (i+1) * 2
		index += 4

		i = int(pdu[index:index+2], 16)
		j = index + 4
		recipient = []
		for k in range(0, i, 2):
			recipient.append(pdu[j+k+1])
			recipient.append(pdu[j+k])
		if recipient[-1] == 'F':
			del recipient[-1]

		index = j + i
		index += 14
		index += 14
		i = int(pdu[index:index+1], 16)
		if (i & 0x60) == 0:
			self.text = "00 - Succesful Delivery."
		if (i & 0x20) == 0x20:
			self.text = "01 - Errors, will retry dispatch."
		if (i & 0x40) == 0x40:
			self.text = "02 - Errors, stopped retrying dispatch."
		if (i & 0x60) == 0x60:
			self.text = "03 - Errors, stopped retrying dispatch."

		self.originator = "TO:" + ''.join(recipient)

