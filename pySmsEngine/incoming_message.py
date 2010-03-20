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

_CARATTERI_HEX = '0123456789ABCDEFabcdef'

class CIncomingMessage(object):
	def __init__(self, pdu, memIndex):
		self.memIndex = memIndex

		i = int(pdu[0:2], 16)
		index = (i + 1) * 2
		index += 2

		i = int(pdu[index:index+2], 16)
		j = index + 4
		originator = []
		for k in range(0, i, 2):
			originator.append(pdu[j+k+1])
			originator.append(pdu[j+k])
		originator = "+" + "".join(originator)
		if originator[-1] == 'F':
			originator = originator[:-1]

		# Type of Address
		addr = int(pdu[j-2:j], 16)
		if (addr & 0x70) == 0x50:
			#Alphanumeric, (coded according to GSM TS 03.38 7-bit default alphabet)
			originator = textFromPduHex(pdu[j:j+i])[:i]

		index = j + k + 2;
		protocol = int(pdu[index] + pdu[index+1], 16) & 0x0C
		index += 2
		# TO DO -- Per ora non mi interessa -- year
		index += 2
		# TO DO -- Per ora non mi interessa -- month
		index += 2
		# TO DO -- Per ora non mi interessa -- day
		index += 2
		# TO DO -- Per ora non mi interessa -- hour
		index += 2
		# TO DO -- Per ora non mi interessa -- min
		index += 2
		# TO DO -- Per ora non mi interessa -- sec
#		index += 4
		index += 6
		# TO DO -- Posso fare finta che il protocollo sia sempre PDU
		if protocol == 4:
			index += 2
			str1 = []
			while (index + 2) <= len(pdu):
				i = int(pdu[index] + pdu[index+1], 16)
				str1.append(unichr(i))
				index += 2;
			str1 = u''.join(str1)
		elif protocol == 8:
			index += 2;
			str1 = []
			while (index + 4) <= len(pdu):
				i = int(pdu[index] + pdu[index+1], 16)
				j = int(pdu[index+2] + pdu[index+3], 16)
				str1.append(unichr((i*256) + j))
				index += 4;
			str1 = u''.join(str1)
		else:
			textLength = int(pdu[index] + pdu[index+1], 16)
			str1 = textFromPduHex(pdu[index+2:])[:textLength]

		self.originator = originator
		# TO DO -- Per ora non mi interessa -- date
		self.text = str1


class CIncomingMessageAscii(object):
	def __init__(self, memIndex, originator, text):
		self.memIndex = memIndex
		self.originator = originator

		# Il testo in modalita' ASCII e' composto da sole cifre esadecimali, e deve essere
		# di lunghezza multipla di 4
		testo_hex = filter(lambda x: x in _CARATTERI_HEX, text)
		di_troppo = len(testo_hex) % 4
		if di_troppo:
			testo_hex = testo_hex[:-di_troppo]

		buf = []
		i = 0
		while i < len(testo_hex):
			buf.append(unichr(int(testo_hex[i:i+4], 16)))
			i += 4

		self.text = u''.join(buf)

