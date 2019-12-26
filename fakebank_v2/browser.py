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

from weboob.browser import LoginBrowser, URL
from weboob.exceptions import BrowserIncorrectPassword

from .pages import LoginPage, AccountsPage, IndexPage, HistoryPage
from weboob.browser import need_login


class Fakebank_V2Browser(LoginBrowser):
    BASEURL = 'https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi'
    home = URL('/$', IndexPage)
    login = URL(r'https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi/v2/#login', LoginPage)
    accounts = URL(r'https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi/v2/accounts.json', AccountsPage)
    history = URL(r'https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi/v2/accounts/(?P<id>\d+).json',
                  HistoryPage)

    def go_home(self):
        self.home.go()
        assert self.home.is_here()

    def do_login(self):
        self.login.stay_or_go()
        self.page.login(self.username, self.password)

    @need_login
    def iter_accounts(self):
        self.accounts.stay_or_go()
        return self.page.iter_accounts()

    @need_login
    def iter_history(self, account):
        self.history.stay_or_go(id=account.id)
        return self.page.iter_history()

    # @need_login
    # def iter_history(self, account):
    #     self.history.go(id=account.id)
    #     for transaction in self.page.iter_history():
    #         yield transaction
