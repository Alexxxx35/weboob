# -*- coding: utf-8 -*-

# Copyright(C) 2019      BOURY
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

from weboob.browser.elements import method, DictElement, ItemElement, ListElement
from weboob.browser.filters.json import Dict
from weboob.browser.filters.standard import CleanText, CleanDecimal, Eval, Regexp, Format
from weboob.browser.pages import HTMLPage, JsonPage
from weboob.capabilities.weather import City, Forecast, Temperature, Current
from weboob.tools.date import date


class SearchCitiesPage(JsonPage):
    @method
    class iter_cities(DictElement):
        ignore_duplicate = True

        class item(ItemElement):
            klass = City
            obj_id = Dict('key')
            obj_name = Dict('localizedName')


class WeatherPage(HTMLPage):
    @method
    class iter_forecast(ListElement):
        item_xpath = '//div[contains(@class,"content-module ")]/a'

        class item(ItemElement):
            klass = Forecast

            obj_id = CleanText('./div[contains(@class,"date")]')

            def obj_date(self):
                actual_day_number = Eval(int,
                                         Regexp(CleanText('./div[contains(@class,"date")]'), '\w{3}\. (\d+)/(\d+)'))(
                    self)
                base_date = date.today()
                if base_date.day > actual_day_number:
                    base_date = base_date.replace(
                        month=(
                            (base_date.month % 12) + 1
                        )
                    )
                base_date = base_date.replace(day=actual_day_number)
                return base_date

            def obj_low(self):
                temp = CleanDecimal(Regexp(CleanText('./div[contains(@class,"temps")]/span[contains(@class,"low")]'),
                                           u'\/ (-*\d+)\xb0'))(self)
                unit = "C"
                return Temperature(float(temp), unit)

            def obj_high(self):
                temp = CleanDecimal(CleanText('./div[contains(@class,"temps")]/span[contains(@class,"high")]'),
                                    u'(.*)\xb0.*')(self)

                unit = "C"
                return Temperature(float(temp), unit)

            obj_text = CleanText('./span[@class="phrase"]')
            # obj_date = CleanText('./p[contains(@class,"dow")]')
            # obj_low = Temperature('./span[contains(@class,"low")]')
            # obj_high = Temperature('./span[contains(@class,"high")]')

    @method
    class get_current(ItemElement):
        klass = Current

        obj_id = date.today()
        obj_date = date.today()
        obj_text = Format('%sC° - %sC° - %s - %s',
                          CleanText('//div[@class="panel-1"]//p[@class="realFeel top"]'),
                          CleanText('//div[@class="panel-1"]//p[@class="realFeel"]'),
                          CleanText('//div[@class="panel-1"]//div[@class="phrase"]'),
                          CleanText('//div[@class="panel-1"]//div[@class="list"]'))

        def obj_temp(self):
            temp = CleanDecimal('//div[@class="panel-1"]//p[@class="value"]')(self)
            unit = CleanText('//div[@class="panel-1"]//p[@class="value"]'), (self)
            unit = "C"
            return Temperature(float(temp), unit)
