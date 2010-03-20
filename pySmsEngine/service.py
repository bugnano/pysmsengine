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

import time
import re
import serial_driver
from StringIO import StringIO
from at_commands import *
from incoming_message import CIncomingMessage, CIncomingMessageAscii
from status_report_message import CStatusReportMessage

# This error value is returned when the operation was succesfull.
ERR_OK = 'ERR_OK'

# This error value is returned when the GSM device asks for a PIN number,
# however the PIN given is invalid. Please check your PIN.
ERR_SIM_PIN_ERROR = 'ERR_SIM_PIN_ERROR'

# This error value is returned when the GSM device does not support ASCII or
# PDU mode. This is a fatal error, in the sense that jSMSEngine can work only
# with GSM devices supporting ASCII or PDU Mode.
ERR_COMM_NOT_SUPPORTED = 'ERR_COMM_NOT_SUPPORTED'

# This error value is returned when the GSM device does not support the 
# AT+CNMI command for disabling indications to TE.
ERR_CANNOT_DISABLE_INDICATIONS = 'ERR_CANNOT_DISABLE_INDICATIONS'

# This error value is returned when the service is not connected to the GSM device.
# You should call method connect().
ERR_NOT_CONNECTED = 'ERR_NOT_CONNECTED'

# Default value for information that is not reported by the GSM device. 
DEFAULT_VALUE_NOT_REPORTED = '* N/A *'

# This error value is returned when a send-message operation failed.
# This could be attributed to a number of reasons: Coverage problems,
# invalid recipient phone number, GSM device malfunction.
ERR_SEND_FAILED = 'ERR_SEND_FAILED'

# This error value is returned when the specific message was not found.
# Double-check your message and/or memory index used.
ERR_MESSAGE_NOT_FOUND = 'ERR_MESSAGE_NOT_FOUND'

# This is a generic error, which is not classified yet. More error classifications may
# be introduced at a later stage.
ERR_GENERIC_ERROR = 'ERR_GENERIC_ERROR'

ERR_CHARSET_NOT_SUPPORTED = 'ERR_CHARSET_NOT_SUPPORTED'

# Classi in modalita' ASCII
CLASS_ALL_ASCII = 'ALL'
CHARSET_UCS2 = 'UCS2'

# Classi in modalita' PDU
CLASS_ALL = '4'
CLASS_REC_UNREAD = '0'
CLASS_REC_READ = '1'
CLASS_STO_UNSENT = '2'
CLASS_STO_SENT = '3'

# Timeout di lettura e di invio SMS, piu' lunghi di quelli normali perche' trattano piu' dati
TMEOUT_READ_MSG = 60
TMEOUT_SEND_MSG = 60

_ReMessaggioAscii = re.compile(r'''
	^														# Inizio stringa
	\+														# Carattere +
''' + AT_LIST[AT_LIST.find('+')+1:AT_LIST.find('=')] + '''	# Comando AT_LIST tra '+' e '='
	:\s*													# : ed eventualmente qualche spazio
	([0-9]+)												# Un numero che indica memIndex
	,\s*													# , ed eventualmente qualche spazio
	"[^"]*"													# Qualcosa tra " che indica la classe
	,\s*													# , ed eventualmente qualche spazio
	"([^"]*)"												# Qualcosa tra " che indica il mittente
	.*														# Eventuali altri caratteri
	$														# Fine stringa
''', re.VERBOSE | re.IGNORECASE | re.DOTALL)

class CDeviceInfo(object):
	def __init__(self):
		self.manufacturer = ''
		self.model = ''


class CService(object):
	def __init__(self, port, baud=9600):
		self.connected = False
		self.simPin = u''
		self.serialDriver = serial_driver.CSerialDriver(port, baud)
		self.deviceInfo = CDeviceInfo()


	def getManufacturer(self):
		whatToDiscard = '+' + AT_MANUFACTURER.replace('AT+', '').replace('\r', '') + ': '
		self.serialDriver.send(AT_MANUFACTURER)
		response = self.serialDriver.getResponse()
		if AT_OK in response:
			response = response.replace(AT_OK, '')
			response = response.replace('\r', '')
			response = response.replace('\n', '')
			response = response.replace(whatToDiscard, '')
			response = response.replace('"', '')
		else:
			response = DEFAULT_VALUE_NOT_REPORTED
		return response


	def getModel(self):
		whatToDiscard = '+' + AT_MODEL.replace('AT+', '').replace('\r', '') + ': '
		self.serialDriver.send(AT_MODEL)
		response = self.serialDriver.getResponse()
		if AT_OK in response:
			response = response.replace(AT_OK, '')
			response = response.replace('\r', '')
			response = response.replace('\n', '')
			response = response.replace(whatToDiscard, '')
			response = response.replace('"', '')
		else:
			response = DEFAULT_VALUE_NOT_REPORTED
		return response


	def refreshDeviceInfo(self):
		if self.connected:
			self.deviceInfo.manufacturer = self.getManufacturer()
			self.deviceInfo.model = self.getModel()
			return ERR_OK
		else:
			return ERR_NOT_CONNECTED + '(1)'


	def connect(self, simPin):
		if self.serialDriver.open():
			self.simPin = simPin
			time.sleep(2)
			self.serialDriver.send(AT_ECHO_OFF);
			self.serialDriver.getResponse();
			self.serialDriver.send(AT_AT);
			if self.serialDriver.getResponse().upper() == AT_OK:
				if self.simPin:
					self.serialDriver.send(AT_CHECK_LOGIN);
					if AT_READY not in self.serialDriver.getResponse().upper():
							self.serialDriver.send(AT_LOGIN % self.simPin)
							if AT_OK not in self.serialDriver.getResponse().upper():
								self.serialDriver.close()
								self.connected = False
								return ERR_SIM_PIN_ERROR
							else:
								# Pin OK - wait 20 seconds for the GSM device to boot up...
								time.sleep(10)
								self.serialDriver.send(AT_AT)
								self.serialDriver.getResponse()
								time.sleep(10)
								self.serialDriver.send(AT_AT)
								self.serialDriver.getResponse()

				self.serialDriver.send(AT_PDU_MODE)
				response1 = self.serialDriver.getResponse().upper()
				response2 = AT_OK
				try:
					# Il Motorola L2 sembra dare un doppio OK qui, per tenere la compatibilita'
					# tengo il doppio OK facoltativo
					response2 = self.serialDriver.getResponse().upper()	
				except serial_driver.Error:
					pass

				# In ogni caso deve essere OK per entrambi
				if (response1, response2) != (AT_OK, AT_OK):
					self.serialDriver.close()
					self.connected = False
					return ERR_COMM_NOT_SUPPORTED
				else:
					self.connected = True
					self.refreshDeviceInfo()
					if 'ERICSSON' in self.deviceInfo.manufacturer.upper():
						if '630' in self.deviceInfo.model:
							self.serialDriver.send(AT_ERICSSON_T630_DISABLE_INDICATIONS)
						else:
							self.serialDriver.send(AT_ERICSSON_DISABLE_INDICATIONS)
					else:
						self.serialDriver.send(AT_DISABLE_INDICATIONS)

					if self.serialDriver.getResponse().upper() == AT_OK:
						if 'SIEMENS' in self.deviceInfo.manufacturer.upper():
							self.serialDriver.send(AT_SIEMENS_SMS_STORAGE)
							self.serialDriver.getResponse()
						elif 'ERICSSON' in self.deviceInfo.manufacturer.upper():
							self.serialDriver.send(AT_ERICSSON_SMS_STORAGE)
							self.serialDriver.getResponse()
					else:
						self.serialDriver.close()
						self.connected = False
						return ERR_CANNOT_DISABLE_INDICATIONS
			else:
				self.serialDriver.close()
				self.connected = False
		else:
			self.connected = False

		if self.connected:
			return ERR_OK
		else:
			return ERR_NOT_CONNECTED + '(2)'


	def sendMessageList(self, messageList):
		if self.connected:
			outList = messageList
			self.serialDriver.send(AT_PDU_MODE)
			response = self.serialDriver.getResponse()
			self.serialDriver.send(AT_KEEP_LINK_OPEN)
			response = self.serialDriver.getResponse()
			error = ERR_OK
			for message in outList:
				pdu = message.getPDU()
				j = len (pdu)
				j /= 2
				# TO DO -- Bisogna vedere se decrementare j o no
				j -= 1
				self.serialDriver.send(AT_SEND_MESSAGE % str (j))
				time.sleep(300 / 1000.)
				while not self.serialDriver.dataAvailable():
					time.sleep(10 / 1000.)
				while self.serialDriver.dataAvailable():
					self.serialDriver.skipBytes(1)
				self.serialDriver.send(pdu)
				self.serialDriver.send(chr(26))
				response = self.serialDriver.getResponse(TMEOUT_SEND_MSG)
				if AT_OK not in response.upper():
					error = ERR_SEND_FAILED
			return error
		else:
			return ERR_NOT_CONNECTED + '(3)'


	def sendMessage(self, message):
		messageList = [message]
		return self.sendMessageList(messageList)


	def isIncomingMessage(self, pdu):
		if pdu == '':
			return False

		i = int(pdu[0:2], 16)
		index = (i + 1) * 2

		i = int(pdu[index:index+2], 16)
		if (i & 0x03) == 0:
			return True
		else:
			return False


	def isStatusReportMessage(self, pdu):
		if pdu == '':
			return False

		i = int(pdu[0:2], 16)
		index = (i + 1) * 2

		i = int(pdu[index:index+2], 16);
		if (i & 0x02) == 2:
			return True
		else:
			return False


	def readMessagesAscii(self, messageList):
		if not self.connected:
			return ERR_NOT_CONNECTED + '(4)'

		self.serialDriver.send(AT_CMD_MODE)
		del messageList[0:]
		self.serialDriver.send(AT_ASCII_MODE)
		response = self.serialDriver.getResponse()

		# Imposto il character set UCS2 fisso, con Motorola L2 funge...
		self.serialDriver.send(AT_SET_CHARSET % CHARSET_UCS2)
		response = self.serialDriver.getResponse().upper()
		if AT_OK not in response.upper():
			return ERR_CHARSET_NOT_SUPPORTED + '(1)'

		self.serialDriver.send(AT_LIST % CLASS_ALL_ASCII)
		response = self.serialDriver.getResponse(TMEOUT_READ_MSG)
		reader = StringIO(response.replace('\r\n', '\n').replace('\r', '\n'))
		first_message = True
		memIndex = None
		originator = None
		text = ''
		line = reader.readline().strip()
		while (line != '') and (line.upper() != 'OK'):
			m = _ReMessaggioAscii.match(line)
			if m is None:
				# Non e' un comando, quindi e' il testo del messaggio
				text = text + line
			else:
				# E' un comando, se non e' il primo messaggio, memorizzo quello precedente
				if first_message:
					first_message = False
				else:
					messageList.append(CIncomingMessageAscii(memIndex, originator, text.strip()))

				# Ricavo i dati di questo messaggio
				memIndex = m.group(1)
				originator = m.group(2)
				text = ''

			# Leggo la linea successiva
			line = reader.readline().strip()

		# Memorizzo l'ultimo messaggio
		if memIndex is not None:
			messageList.append(CIncomingMessageAscii(memIndex, originator, text.strip()))

		return ERR_OK


	def readMessages(self, messageList, messageClass=CLASS_ALL):
		if self.connected:
			self.serialDriver.send(AT_CMD_MODE)
			del messageList[0:]
			self.serialDriver.send(AT_PDU_MODE)
			response = self.serialDriver.getResponse()
			self.serialDriver.send(AT_LIST % messageClass)
			response = self.serialDriver.getResponse(TMEOUT_READ_MSG)
			reader = StringIO(response.replace('\r\n', '\n').replace('\r', '\n'))
			line = reader.readline().strip()
			while (line != '') and (line.upper() != 'OK'):
				i = line.find(':')
				j = line.find(',')
				# TO DO -- BUG: i e j possono valere -1
				memIndex = line[i+1:j].strip()
				pdu = reader.readline().strip()
				if self.isIncomingMessage(pdu):
					messageList.append(CIncomingMessage(pdu, memIndex))
				elif self.isStatusReportMessage(pdu):
					messageList.append(CStatusReportMessage(pdu, memIndex))
				line = reader.readline().strip()
			return ERR_OK
		else:
			return ERR_NOT_CONNECTED + '(5)'


	def deleteMessage(self, memIndex):
		if self.connected:
			if int(memIndex) > 0:
				self.serialDriver.send(AT_DELETE_MESSAGE % memIndex)
				response = self.serialDriver.getResponse()
				if AT_OK in response.upper():
					return ERR_OK
				else:
					return ERR_MESSAGE_NOT_FOUND + '(1)'
			else:
				return ERR_GENERIC_ERROR + '(1)'
		else:
			return ERR_NOT_CONNECTED + '(6)'

