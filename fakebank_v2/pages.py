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

from weboob.tools.json import json
from weboob.browser.filters.json import Dict

from weboob.browser.pages import LoggedPage, HTMLPage, JsonPage, pagination
from weboob.browser.filters.html import Attr
from weboob.browser.filters.standard import CleanDecimal, CleanText, Regexp, Date
from weboob.capabilities.bank import Account, Transaction
from weboob.browser.elements import method, TableElement, ItemElement, DictElement
from weboob.browser.filters.html import Link, TableCell
from weboob.browser.filters.html import CSS


class IndexPage(HTMLPage):
    pass


class LoginPage(HTMLPage):

    def login(self, username, password):
        json_data = {
            'login': username,
            'password': password
        }
        self.browser.location('https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi/v2/login.json',
                              data=json_data, method='POST')


class AccountsPage(JsonPage):
    @method
    class iter_accounts(DictElement):
        item_xpath = 'accounts'

        class item(ItemElement):
            klass = Account
            obj_id = CleanText(Dict('id'))
            obj_label = CleanText(Dict('label'))
            obj_balance = CleanText(Dict('balance'))


class HistoryPage(LoggedPage, JsonPage):
    @pagination
    @method
    class iter_history(DictElement):
        item_xpath = 'transactions'

        class item(ItemElement):
            klass = Transaction
            obj_amount = CleanText(Dict('amount'))
            obj_label = CleanText(Dict('label'))
            def obj_date(self):
                obj_date = Date(CleanText(Dict('date')))(self)
                print(obj_date)

