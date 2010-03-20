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

from service import *
from outgoing_message import COutgoingMessage

#PORT = u'/dev/ttyACM0'
PORT = ur'\\.\COM6'
BAUD = 115200
SIM_PIN = u'1234'

MSG_TEXT = u'Prova invio SMS da PC di Franco'
MSG_UNMBER = u'+393331122345'

MEM_INDEX = u'313'

Srv = None

def testConnect():
	global Srv

	Srv = CService(PORT, BAUD)
	esito = Srv.connect(SIM_PIN)
	print "------------------------------------------------------------------------------"
	print "connect()"
	print "------------------------------------------------------------------------------"
	print esito
	print "------------------------------------------------------------------------------"
	return esito


def testSend():
	global Srv

#	esito = testConnect()
#	if esito != ERR_OK:
#		return

	msg = COutgoingMessage(MSG_UNMBER, MSG_TEXT)
	esito = Srv.sendMessage(msg)
	print "------------------------------------------------------------------------------"
	print "sendMessage()"
	print "------------------------------------------------------------------------------"
	print esito
	print "------------------------------------------------------------------------------"


def testRead():
	global Srv

#	esito = testConnect()
#	if esito != ERR_OK:
#		return

	msgList = []
	esito = Srv.readMessages(msgList, CLASS_ALL)
	print "------------------------------------------------------------------------------"
	print "readMessages()"
	print "------------------------------------------------------------------------------"
	print esito
	print "------------------------------------------------------------------------------"
	for msg in msgList:
		print "memIndex: " + msg.memIndex
		print "originator: " + msg.originator.encode('latin_1')
		print "text:"
		print msg.text.encode('latin_1')
		print "------------------------------------------------------------------------------"


def testReadAscii():
	global Srv

#	esito = testConnect()
#	if esito != ERR_OK:
#		return

	msgList = []
	esito = Srv.readMessagesAscii(msgList)
	print "------------------------------------------------------------------------------"
	print "readMessagesAscii()"
	print "------------------------------------------------------------------------------"
	print esito
	print "------------------------------------------------------------------------------"
	for msg in msgList:
		print "memIndex: " + msg.memIndex
		print "originator: " + msg.originator.encode('latin_1')
		print "text:"
		print msg.text.encode('latin_1')
		print "------------------------------------------------------------------------------"


def testDelete():
	global Srv

#	esito = testConnect()
#	if esito != ERR_OK:
#		return

	esito = Srv.deleteMessage(MEM_INDEX)
	print "------------------------------------------------------------------------------"
	print "deleteMessage()"
	print "------------------------------------------------------------------------------"
	print esito
	print "------------------------------------------------------------------------------"

if __name__ == '__main__':
	testConnect()
#	testRead()
	testReadAscii()
#	testDelete()
#	testRead()
#	testSend()
#	testRead()

