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

import serial
import time

# Timeout period for the phone to respond to jSMSEngine.
RECV_TIMEOUT = 30

# Delay (20ms) after each character sent. Seems that some mobile phones
# get confused if you send them the commands without any delay, even
# in slow baud rate.
DELAY_BETWEEN_CHARS = 20 / 1000.

class Error(Exception):
	pass


def _debug_print(messaggio):
	if 0:
		print messaggio
	else:
		pass


class CSerialDriver(object):
	def __init__(self, port, baud):
		self.port = port
		self.baud = baud
		self.serialPort = None


	def open(self):
		_debug_print('------------------------------------------------------------------------------')
		_debug_print('CSerialDriver.open(%s, %d)' % (str(self.port), self.baud))
		_debug_print('------------------------------------------------------------------------------')
		try:
			self.serialPort = serial.Serial(self.port, self.baud, stopbits=serial.STOPBITS_TWO, timeout=RECV_TIMEOUT)
			_debug_print('True')
			_debug_print('------------------------------------------------------------------------------')
			return True
		except serial.SerialException:
			_debug_print('False')
			_debug_print('------------------------------------------------------------------------------')
			return False


	def close(self):
		self.serialPort.close()
		self.serialPort = None


	def send(self, s):
		toSend = str(s.encode('ascii'))
		_debug_print('------------------------------------------------------------------------------')
		_debug_print('CSerialDriver.send()')
		_debug_print('------------------------------------------------------------------------------')
		_debug_print(toSend)
		_debug_print('------------------------------------------------------------------------------')
		for c in toSend:
			time.sleep(DELAY_BETWEEN_CHARS)
			try:
				self.serialPort.write(c)
			except:
				raise Error, 'Errore di scrittura su seriale'

		time.sleep(DELAY_BETWEEN_CHARS)


	def skipBytes(self, numOfBytes):
		_debug_print('------------------------------------------------------------------------------')
		_debug_print('CSerialDriver.skipBytes()')
		_debug_print('------------------------------------------------------------------------------')
		count = 0;
		while count < numOfBytes:
			try:
				c = self.serialPort.read()
			except:
				raise Error, 'Errore di lettura da seriale'

			if c != '':
				count += 1
				_debug_print(c)

		_debug_print('------------------------------------------------------------------------------')
		time.sleep(DELAY_BETWEEN_CHARS)


	def dataAvailable(self):
		if self.serialPort.inWaiting() > 0:
			return True
		else:
			return False


	def getResponse(self, timeout=RECV_TIMEOUT):
		_debug_print('------------------------------------------------------------------------------')
		_debug_print('CSerialDriver.getResponse()')
		_debug_print('------------------------------------------------------------------------------')

		buf = []
		inizio = time.time()
		while True:
			fine = time.time()
			if (fine - inizio) > timeout:
				_debug_print('serial_driver.Error: Timeout seriale scaduto')
				_debug_print('------------------------------------------------------------------------------')
				raise Error, 'Timeout seriale scaduto'

			try:
				c = self.serialPort.read()
			except:
				raise Error, 'Errore di lettura da seriale'

			buf.append(c)
			strBuf = ''.join(buf).upper()
			if	('OK\r' in strBuf) or \
				('OK\n' in strBuf) or \
				(('ERROR' in strBuf) and (strBuf.rfind('\r') > strBuf.find('ERROR'))) or \
				(('ERROR' in strBuf) and (strBuf.rfind('\n') > strBuf.find('ERROR'))) or \
				(('CPIN' in strBuf) and (strBuf.find('\r', strBuf.find('CPIN')) > -1)) or \
				(('CPIN' in strBuf) and (strBuf.find('\n', strBuf.find('CPIN')) > -1)):
				break

		response = ''.join(buf).lstrip('\r\n')
		_debug_print(response)
		_debug_print('------------------------------------------------------------------------------')

		time.sleep(DELAY_BETWEEN_CHARS)
		return response

