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

import re
from io import BytesIO

import requests
from weboob.browser.elements import ItemElement, method, ListElement, DictElement
from weboob.browser.filters.html import Attr, Link
from weboob.browser.filters.json import Dict
from weboob.browser.filters.standard import Regexp, CleanText, CleanDecimal, Date
from weboob.browser.pages import HTMLPage, LoggedPage, pagination
from weboob.capabilities.bank import Account, Transaction
from weboob.tools.captcha.virtkeyboard import SimpleVirtualKeyboard


class FakeBankVirtKeyboard(SimpleVirtualKeyboard):
    codesep = ','
    symbols = {'0': ('186885cbec914f8adff8f82df395a6b5'),
               '1': ('26e418932c82fd00c8e66e6ffe60a947'),
               '2': ('dccd9b32fdc6af43afcf16a0f167af4d'),
               '3': ('454cc3883295ca0ecfa90a1f4a12d59a'),
               '4': ('e74acff187773d953e6fb12b5785bb96'),
               '5': ('8cab72d408a7a837ae074306900f285f'),
               '6': ('95589d5257cec27b27023e53af85e794'),
               '7': ('fcfd1b0b42e47fe5c0763018b19afe7f'),
               '8': ('1b84b7459f0af7b034b3e4d32129e4bf'),
               '9': ('14e6f2437057d625f82b0526c8accdf1'),
               }


class LoginPage(HTMLPage):
    def login(self, username, password):
        img_src = CleanText('/html/body/fieldset/form/img/@src')(self.doc)
        f = BytesIO(self.browser.open(img_src).content)
        vk = FakeBankVirtKeyboard(file=f, cols=4, rows=4)
        code = vk.get_string_code(password)

        form = self.get_form(xpath='/html/body/fieldset/form')
        form['login'] = username
        form['code'] = code
        form.submit()


class ListPage(LoggedPage, HTMLPage):
    @method
    class get_accounts(ListElement):
        item_xpath = '/html/body/div/div'

        class item(ItemElement):
            klass = Account

            obj_id = Regexp(Attr('./a', 'onclick'), r'(\d+)')
            obj_label = CleanText('./a/text()')
            obj_balance = CleanDecimal('./text()')

    @pagination
    @method
    class iter_history(DictElement):
        def find_elements(self):

            item_xpath = '/html/body/script[3]'
            for el in self.el.xpath(item_xpath):

                transactions = el.text_content()
                transactions = transactions.split(';')

                for line in transactions:
                    line_cont = {}
                    line = line.split(',')
                    if len(line) != 1:
                        line_cont['label'] = line[0].strip('\nadd_transaction("')
                        line_cont['date'] = re.sub(r'"', '', line[1])
                        line_cont['amount'] = line[2].strip('")')

                        yield line_cont

        class item(ItemElement):
            klass = Transaction

            obj_amount = CleanDecimal(CleanText(Dict('amount')))
            obj_label = CleanText(Dict('label'))
            obj_date = Date(CleanText(Dict('date')))

        def next_page(self):
            if Link(u'//a[text()="▶"]')(self) is not None:
                self.page.browser.history_form['page'] = CleanDecimal(Link(u'//a[text()="▶"]'))(self)
                return requests.Request("POST", self.page.url, data=self.page.browser.history_form)
