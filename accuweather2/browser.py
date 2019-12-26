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

from weboob.browser import PagesBrowser, URL

from .pages import SearchCitiesPage, WeatherPage


class Accuweather2Browser(PagesBrowser):
    BASEURL = 'https://www.accuweather.com/'
    # home = URL('/$', IndexPage)
    # cities = URL('/fr/fr/(?P<city_name>.*/(?P<city_id>.*)/weather-forecast/(?P<city_id>.*)', SearchCitiesPage)
    # https://www.accuweather.com/web-api/autocomplete?query=paris&language=en-us
    cities = URL('/web-api/autocomplete', SearchCitiesPage)
    weather = URL(r'fr/fr/(?P<city_name>.*)/(?P<city_id>.*)/daily-weather-forecast/(?P<city_id2>.*)', WeatherPage)

    def iter_city_search(self, pattern):
        params = {"query": pattern, "language": 'fr'}
        return self.cities.go(params=params).iter_cities()

    def iter_forecast(self, city):
        return self.weather.go(city_id=city.id, city_name=city.name, city_id2=city.id).iter_forecast()

    def get_current(self, city):
        params = {'day': 1}
        return self.weather.go(city_id=city.id, city_name=city.name, city_id2=city.id, params=params).get_current()
