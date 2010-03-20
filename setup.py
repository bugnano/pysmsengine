#!/usr/bin/env python
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

import os
from distutils.core import setup
from pySmsEngine import __version__

# TO DO -- Questo va bene sotto Linux, ma sotto altri sistemi operativi?
doc_root = os.path.join('share', 'doc', 'pySmsEngine')

_data_files = [
	(doc_root, [
		os.path.join('Doc', 'GSM0338.txt'),
		os.path.join('Doc', 'possibili_problemi.txt'),
		os.path.join('pySmsEngine', 'changelog.txt'),
		'LICENSE.txt',
	])
]

setup(name='pySmsEngine',
	version=__version__,
	author='Franco Bugnano',
	author_email='franco@bugnano.it',
	url='http://www.bugnano.it/',
	description='An open-source API package for sending and receiving SMS via a GSM device.',
	long_description='pySmsEngine is a package which can be used in order to add SMS processing capabilities in an application. pySmsEngine is written in python, and based on the Java software jSMSEngine version 1.2.7. It allows you to communicate with a compatible mobile phone or GSM Modem, and send / receive SMS messages.',
	license='GNU Library or Lesser General Public License (LGPL)',
	data_files=_data_files,
	packages=['pySmsEngine']
)

