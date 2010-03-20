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

AT_OK = 'OK\r'
AT_AT = 'AT\r'

AT_ECHO_OFF = 'ATE0\r'

AT_CMD_MODE = '+++'

AT_DISABLE_INDICATIONS = 'AT+CNMI=0,0,0,0\r'

AT_SIEMENS_SMS_STORAGE = 'AT+CPMS=MT\r'

AT_ERICSSON_SMS_STORAGE = 'AT+CPMS="ME","SM"\r'
AT_ERICSSON_T630_DISABLE_INDICATIONS = 'AT+CNMI=2,0,0,0\r'
AT_ERICSSON_DISABLE_INDICATIONS = 'AT+CNMI=3,0,0,0\r'

AT_MANUFACTURER = 'AT+CGMI\r'
AT_MODEL = 'AT+CGMM\r'
AT_SERIALNO = 'AT+CGSN\r'
AT_IMSI = 'AT+CIMI\r'
AT_BATTERY = 'AT+CBC\r'
AT_SIGNAL = 'AT+CSQ\r'
AT_SOFTWARE = 'AT+CGMR\r'

AT_LIST = 'AT+CMGL=%s\r'
#AT_LIST = 'AT+CMGL="%s"\r'

AT_SEND_MESSAGE = 'AT+CMGS=%s\r'
#AT_SEND_MESSAGE = 'AT+CMGS="%s"\r'
AT_KEEP_LINK_OPEN = 'AT+CMMS=1\r'

AT_DELETE_MESSAGE = 'AT+CMGD=%s\r'

AT_ASCII_MODE = 'AT+CMGF=1\r'
AT_PDU_MODE = 'AT+CMGF=0\r'
AT_SET_CHARSET = 'AT+CSCS=%s\r'

AT_CHECK_LOGIN = 'AT+CPIN?\r'
AT_LOGIN = 'AT+CPIN="%s"\r'
AT_READY = 'READY\r'

