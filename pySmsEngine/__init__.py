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

'''
# Per utilizzare pySmsEngine:
import pySmsEngine

# Per prima cosa bisonga connettersi con la porta seriale
porta_seriale = 0	# La numerazione della porta seriale parte SEMPRE da 0
sim_pin = '1234'	# Il codice PIN della SIM
srv = pySmsEngine.CService(porta_seriale)
if srv.connect(sim_pin) != pySmsEngine.ERR_OK:
	pass			# Errore di connessione con la porta seriale

# Per inviare un messaggio:
msg_number = u'+393331122333'
msg_text = u'Ciao'	# Il messaggio DEVE essere una stringa UNICODE
if filter(lambda x: x not in pySmsEngine.GSM_ALPHABET, msg_text):
	pass			# Il messaggio contiene caratteri non validi

msg = pySmsEngine.COutgoingMessage(msg_number, msg_text)
if srv.sendMessage(msg) != pySmsEngine.ERR_OK:
	pass			# Errore di trasmissione del messaggio

# Per inviare piu' messaggi:
msg_list = [msg, msg, msg]
if srv.sendMessageList(msg_list) != pySmsEngine.ERR_OK:
	pass			# Errore di trasmissione dei messaggi

# Per leggere tutti i messaggi:
msg_list = []
if srv.readMessages(msg_list) != pySmsEngine.ERR_OK:
	pass			# Errore di ricezione dei messaggi

for msg in msg_list:
	# msg.memIndex   --> e' una stringa che contiene l'indice in memoria del messaggio
	# msg.originator --> e' una stringa UNICODE che contiene il mittente (numero o nome)
	# msg.text       --> e' una stringa UNICODE che contiene il testo del messaggio
	pass

# Per cancellare i messaggi uno alla volta
for msg in msg_list:
	if srv.deleteMessage(msg.memIndex) != pySmsEngine.ERR_OK:
		pass		# Errore di cancellazione del messaggio

# ATTENZIONE: TUTTE le funzioni qui indicate potrebbero generare un'eccezione di tipo
# pySmsEngine.Error, quindi e' meglio fare tutto in un blocco try.
'''

__version__ = '1.0.0'
__date__ = '2007-01-24'
__copyright__ = 'Copyright (C) 2005-2007, Franco Bugnano'

from service import *
from outgoing_message import COutgoingMessage
from gsm_alphabet import GSM_ALPHABET
from serial_driver import Error

