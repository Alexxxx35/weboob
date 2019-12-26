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

from weboob.browser.pages import LoggedPage, HTMLPage, pagination
from weboob.browser.filters.html import Attr, AbsoluteLink
from weboob.browser.filters.standard import CleanDecimal, CleanText, Regexp, Date
from weboob.capabilities import NotAvailable
from weboob.capabilities.bank import Account, Transaction
from weboob.browser.elements import method, ItemElement, TableElement


class IndexPage(HTMLPage):
    pass


class LoginPage(HTMLPage):
    def login(self, username, password):
        form = self.get_form(xpath='/html/body/fieldset/form')
        form['login'] = username
        form['password'] = password
        self.browser.location('https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi/v1/login',
                              method='POST')
        form.submit()


class AccountsPage(LoggedPage, HTMLPage):
    @method
    class iter_accounts(TableElement):
        head_xpath = '/html/body/table/thead'
        item_xpath = '/html/body/table/tbody/tr'

        class item(ItemElement):
            klass = Account
            obj_id = Regexp(Attr('.//a', 'href'), r'(\d+)')  # type of object=int
            obj_label = CleanText('./td[1]')  # account name
            obj_balance = CleanDecimal('./td[2]', replace_dots=True)  # value in euro


class HistoryPage(LoggedPage, HTMLPage):
    @pagination
    @method
    class iter_history(TableElement):
        head_xpath = '//table/thead'
        item_xpath = '//table/tbody/tr'

        def next_page(self):
            AbsoluteLink('//a[text()="▶"]', default=None)(self)

        class item(ItemElement):
            klass = Transaction
            obj_date = Date(CleanText('./td[1]'), dayfirst=True)
            obj_label = CleanText('./td[2]')

            def obj_amount(self):
                return CleanDecimal('./td[4]', replace_dots=True, default=NotAvailable)(self) \
                       or CleanDecimal('./td[3]', replace_dots=True)(self)
