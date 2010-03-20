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

class COutgoingMessage(object):
	def __init__(self, recipient, text):
		self.recipient = recipient
		self.text = text

	def toBCDFormat(self, s):
		if (len(s) % 2) != 0:
			s = s + "F"
		bcd = []
		for i in range(0, len(s), 2):
			bcd.append(s[i+1])
			bcd.append(s[i])
		return "".join(bcd)

	def getPDU(self):
		# TO DO -- Bisogna vedere se far valere pdu "" oppure "00"
#		pdu = ""
		pdu = "00"
		pdu = pdu + "11"
		pdu = pdu + "00"
		str1 = self.recipient
		if str1[0] == '+':
			str1 = self.toBCDFormat(str1[1:])
			str2 = "%0.2x" % (len(self.recipient) - 1)
			str1 = "91" + str1
		else:
			str1 = self.toBCDFormat(str1)
			str2 = "%0.2x" % len(self.recipient)
			str1 = "81" + str1

		pdu = pdu + str2 + str1
		pdu = pdu + "00"
		pdu = pdu + "00"
		pdu = pdu + "FF"
		str1 = "%0.2x" % len(self.text)
		str2 = pduHexFromText(self.text)
		pdu = pdu + str1 + str2;
		return pdu.upper()

