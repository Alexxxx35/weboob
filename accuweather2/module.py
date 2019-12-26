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

from weboob.capabilities.base import find_object
from weboob.tools.backend import Module
from weboob.capabilities.weather import CapWeather, CityNotFound

from .browser import Accuweather2Browser

__all__ = ['Accuweather2Module']


class Accuweather2Module(Module, CapWeather):
    NAME = 'accuweather2'
    DESCRIPTION = 'accuweather2 website'
    MAINTAINER = 'BOURY'
    EMAIL = 'alexboury@hotmail.fr'
    LICENSE = 'LGPLv3+'
    VERSION = '1.6'

    BROWSER = Accuweather2Browser

    def iter_city_search(self, pattern):
        return self.browser.iter_city_search(pattern)

    def get_current(self, city_id):
        return self.browser.get_current(self.get_city(city_id))

    def iter_forecast(self, city_id):
        print(self.get_city(city_id))
        return self.browser.iter_forecast(self.get_city(city_id))

    def get_city(self, _id):
        cities = list(self.iter_city_search(_id))

        if len(cities) == 0:
            raise CityNotFound()

        try:
            return find_object(cities, id=_id, error=CityNotFound)
        except CityNotFound:
            return cities[0]
