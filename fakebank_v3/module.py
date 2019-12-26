# -*- coding: utf-8 -*-

# Copyright(C) 2019      alex
#
# This file is part of a weboob module.
#
# This weboob module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This weboob module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this weboob module. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from .browser import FakebankBrowser
from weboob.tools.backend import Module, BackendConfig
from weboob.capabilities.bank import CapBank, AccountNotFound
from weboob.tools.value import Value, ValueBool, ValueInt, ValueBackendPassword
# from .browser import Fakebank_V2Browser

__all__ = ['Fakebank_V3Module']


class Fakebank_V3Module(Module, CapBank):
    NAME = 'fakebank'
    DESCRIPTION = 'fakebank website'
    MAINTAINER = 'alex'
    EMAIL = 'alexboury@ħotmail.fr'
    LICENSE = 'LGPLv3+'
    VERSION = '1.5'

    BROWSER = FakebankBrowser

    CONFIG = BackendConfig(Value('username', label='Username', regexp='.+'),
                           ValueBackendPassword('password', label='Password'))

    def create_default_browser(self):
        return self.create_browser(
            self.config['login'].get(), self.config['password'].get())

    def iter_accounts(self):
        for account in self.browser.iter_accounts():
            yield account

    def iter_history(self, account):
        return self.browser.iter_history(account)
