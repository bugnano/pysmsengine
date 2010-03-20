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

GSM_ALPHABET = u'@\xa3$\xa5\xe8\xe9\xf9\xec\xf2\xc7\n\xd8\xf8\r\xc5\xe5\u0394_\u03a6\u0393\u039b\u03a9\u03a0\u03c8\u03a3\u03b8\u039e \xc6\xe6\xdf\xc9 !"#\xa4%&\'()*+,-./0123456789:;<=>?\xa1ABCDEFGHIJKLMNOPQRSTUVWXYZ\xc4\xd6\xd1\xdc\xa7\xbfabcdefghijklmnopqrstuvwxyz\xe4\xf6\xf1\xfc\xe0'

def _subNegative(n):
	if n == -1:
		return GSM_ALPHABET.rfind('?')
	else:
		return n

def pduHexFromText(text):
	oldBytes = map(GSM_ALPHABET.rfind, text)
	oldBytes = map(_subNegative, oldBytes)

	bitSet = []
	for num in oldBytes:
		for i in range(7):
			if num & (1 << i):
				bitSet.append(1)
			else:
				bitSet.append(0)

	newBytes = []
	while True:
		n = 0
		for i in range(8):
			if len(bitSet) == 0:
				break
			if bitSet[0] == 1:
				n |= 1 << i
			del bitSet[0]
		newBytes.append("%0.2x" % n)
		if len(bitSet) == 0:
			break
	return ''.join(newBytes)


def textFromPduHex(pdu):
	oldBytes = []
	for i in range(0, len(pdu), 2):
		oldBytes.append(int(pdu[i] + pdu[i+1], 16))

	bitSet = []
	for num in oldBytes:
		for i in range(8):
			if num & (1 << i):
				bitSet.append(1)
			else:
				bitSet.append(0)

	newBytes = []
	while True:
		n = 0
		if len(bitSet) >= 7:
			for i in range(7):
				if bitSet[0] == 1:
					n |= 1 << i
				del bitSet[0]
			newBytes.append(GSM_ALPHABET[n])
		else:
			break
	return u''.join(newBytes)


if __name__ == '__main__':
	print pduHexFromText(u'hellohello')
	print textFromPduHex('E8329BFD4697D9EC37')
	print pduHexFromText('1234567')
	print pduHexFromText('1234567@')
	print textFromPduHex(pduHexFromText('1'))
	print textFromPduHex(pduHexFromText('12'))
	print textFromPduHex(pduHexFromText('123'))
	print textFromPduHex(pduHexFromText('1234'))
	print textFromPduHex(pduHexFromText('12345'))
	print textFromPduHex(pduHexFromText('123456'))
	print textFromPduHex(pduHexFromText('1234567'))
	print textFromPduHex(pduHexFromText('12345678'))
	print textFromPduHex(pduHexFromText('123456789'))
	print textFromPduHex(pduHexFromText('1234567890'))
	print textFromPduHex(pduHexFromText('12345678901'))
	print textFromPduHex(pduHexFromText('123456789012'))
	print textFromPduHex(pduHexFromText('1234567890123'))
	print textFromPduHex(pduHexFromText('12345678901234'))
	print textFromPduHex(pduHexFromText('123456789012345'))
	print textFromPduHex(pduHexFromText('1234567890123456'))
	print textFromPduHex(pduHexFromText('12345678901234567'))
