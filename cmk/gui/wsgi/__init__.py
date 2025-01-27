#!/usr/bin/env python
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2019             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

import functools
import wsgiref.util

from cmk.gui.wsgi.applications import CheckmkApp


def apache_env(func):
    @functools.wraps(func)
    def _add_apache_env(environ, start_response):
        if not environ.get('REQUEST_URI'):
            environ['REQUEST_URI'] = wsgiref.util.request_uri(environ)

        if not environ.get('SCRIPT_NAME'):
            environ['SCRIPT_NAME'] = environ.get('PATH_INFO', '/')
            environ['PATH_INFO'] = '/'

        return func(environ, start_response)

    return _add_apache_env


def make_app():
    return apache_env(CheckmkApp)


__all__ = ['make_app']
