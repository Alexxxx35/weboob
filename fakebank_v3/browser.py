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

__all__ = ['Fakebank_V3Browser']

from weboob.browser import LoginBrowser, URL
from weboob.exceptions import BrowserIncorrectPassword
from weboob.browser import need_login
from .pages import IndexPage, AccountsPage, LoginPage, HistoryPage

class Fakebank_V3Browser(LoginBrowser, PagesBrowser):
    BASEURL = 'https://people.lan.budget-insight.com/'

    login = URL('/~ntome/fake_bank.wsgi/v3/login', LoginPage)
    accounts = URL(r'https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi/v3/app', ListPage)
    account_url = URL(r'https://people.lan.budget-insight.com/~ntome/fake_bank.wsgi/v3/app', HistoryPage)

    def go_home(self):
        self.home.go()
        assert self.home.is_here()

    def do_login(self):
        self.login.stay_or_go()
        self.page.login(self.username, self.password)

    @need_login
    def iter_accounts(self):
        self.accounts.go(data={'action': 'accounts'})
        return self.page.iter_accounts()

    @need_login
    def get_history(self, account):
        self.history_form = {}
        self.history_form['action'] = 'history'
        self.history_form['account_id'] = account.id
        self.history_form['page'] = '1'
        self.history_page.go(data=self.history_form)
        # for transaction in self.page.iter_history():
        #     yield transaction
        return self.page.iter_history()


