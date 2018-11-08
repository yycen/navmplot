from __future__ import absolute_import

import json
import math
import os
import requests
import warnings

from collections import namedtuple

from navmplot.color_dicts import mpl_color_map, html_color_codes
from navmplot.naver_maps_templates import SYMBOLS, CIRCLE, TEXT, MAP, POLYLINE, COORD, MARKER

Symbol = namedtuple('Symbol', ['symbol', 'lat', 'long', 'size'])

class InvalidSymbolError(Exception):
    pass

class NaverMapPlotter(object):

    def __init__(self, center_lat, center_lng, zoom, apikey):
        self.center = (float(center_lat), float(center_lng))
        self.zoom = int(zoom)
        self.apikey = str(apikey)
        self.paths = []
        self.points = []
        self.symbols = []
        self.coloricon = os.path.join(os.path.dirname(__file__), 'markers/{}.png')
        self.color_dict = mpl_color_map
        self.html_color_codes = html_color_codes

    @classmethod
    def from_geocode(cls, location_string, zoom=13):
        pass

    def marker(self, lat, lng, color='#FF0000', c=None, title="no implementation"):
        if c:
            color = c
        if len(color)>0 and color[0] != '#':
            color = self.color_dict.get(color, color)
            color = self.html_color_codes.get(color, '#FFA500')
        self.points.append((lat, lng, color[1:], title))

    def scatter(self, lats, lngs, color=None, size=None, marker=False, c=None, s=None, symbol='o', **kwargs):
        color = color or c
        size = size or s or 40
        kwargs["color"] = color
        kwargs["size"] = size
        settings = self._process_kwargs(kwargs)
        for lat, lng in zip(lats, lngs):
            if marker:
                self.marker(lat, lng, settings['color'])
            else:
                self._add_symbol(Symbol(symbol, lat, lng, size), **settings)

    def _add_symbol(self, symbol, color=None, c=None, **kwargs):
        color = color or c
        kwargs.setdefault('face_alpha', 0.5)
        kwargs.setdefault('face_color', "#000000")
        kwargs.setdefault("color", color)
        settings = self._process_kwargs(kwargs)
        self.symbols.append((symbol, settings))

    def _process_kwargs(self, kwargs):
        settings = dict()
        settings["edge_color"] = kwargs.get("color", None) or \
                                 kwargs.get("edge_color", None) or \
                                 kwargs.get("ec", None) or \
                                 "#000000"

        settings["edge_alpha"] = kwargs.get("alpha", None) or \
                                 kwargs.get("edge_alpha", None) or \
                                 kwargs.get("ea", None) or \
                                 1.0
        settings["edge_width"] = kwargs.get("edge_width", None) or \
                                 kwargs.get("ew", None) or \
                                 1.0
        settings["face_alpha"] = kwargs.get("alpha", None) or \
                                 kwargs.get("face_alpha", None) or \
                                 kwargs.get("fa", None) or \
                                 0.3
        settings["face_color"] = kwargs.get("color", None) or \
                                 kwargs.get("face_color", None) or \
                                 kwargs.get("fc", None) or \
                                 "#000000"

        settings["color"] = kwargs.get("color", None) or \
                            kwargs.get("c", None) or \
                            settings["edge_color"] or \
                            settings["face_color"]

        # Need to replace "plum" with "#DDA0DD" and "c" with "#00FFFF" (cyan).
        for key, color in settings.items():
            if 'color' in key:
                if len(color)>0 and color[0] != '#':
                    color = self.color_dict.get(color, color)
                    color = self.html_color_codes.get(color, '#FFA500')
                    settings[key] = color

        return settings

    def plot(self, lats, lngs, color=None, c=None, **kwargs):
        color = color or c
        kwargs.setdefault("color", color)
        settings = self._process_kwargs(kwargs)
        path = zip(lats, lngs)
        self.paths.append((path, settings))

    def draw(self, htmlfile):
        with open(htmlfile, 'w') as f:
            map_text = self.write_map_text()
            polylines_text = self.write_paths_text()
            points_text = self.write_points_text()
            symbols_text = self.write_symbols_text()
            all_text = TEXT.format(apikey=self.apikey, MAP=map_text, POLYLINES=polylines_text,
                                    MARKERS=points_text, SYMBOLS=symbols_text)
            print(all_text)
            f.write(all_text)

    def write_map_text(self):
        ret = MAP.format(zoom=self.zoom, lat=self.center[0], lng=self.center[1])
        return ret
    
    def write_paths_text(self):
        ret = str()
        for path, settings in self.paths:
            ret += self.write_polyline_text(path, settings)
        return ret
    
    def write_polyline_text(self, path, settings):
        COORDS = self.write_path_coords_text(path, settings)

        strokeColor = settings.get('color') or settings.get('edge_color')
        strokeOpacity = settings.get('edge_alpha')
        strokeWeight = settings.get('edge_width')
        ret = POLYLINE.format(COORDS=COORDS, strokeColor=strokeColor, 
                            strokeOpacity=strokeOpacity, strokeWeight=strokeWeight)
        return ret
    
    def write_path_coords_text(self, path, settings):
        ret = str()
        for coordinate in path:
            ret += COORD.format(lat=coordinate[0], lng=coordinate[1])
        return ret

    def write_points_text(self):
        ret = str()
        for point in self.points:
            ret += self.write_point_text(point[0], point[1], point[2], point[3])
        return ret

    def write_point_text(self, lat, lng, color, title):
        icon = self.coloricon.format(color)
        ret = MARKER.format(lat=lat, lng=lng, icon=icon, title=title)
        return ret

    def write_symbols_text(self):
        ret = str()
        for symbol, settings in self.symbols:
            ret += self.write_symbol_text(symbol, settings)
        return ret

    def write_symbol_text(self, symbol, settings):
        strokeColor = settings.get('color') or settings.get('edge_color')
        strokeOpacity = settings.get('edge_alpha')
        strokeWeight = settings.get('edge_width')
        fillColor = settings.get('face_color')
        fillOpacity = settings.get('face_alpha')
        try:
            template = SYMBOLS[symbol.symbol]
        except KeyError:
            raise InvalidSymbolError('Symbol {} is not implemented'.format(symbol.symbol))

        ret = template.format(lat=symbol.lat, lng=symbol.long, size=symbol.size, strokeColor=strokeColor,
                                strokeOpacity=strokeOpacity, strokeWeight=strokeWeight,
                                fillColor=fillColor, fillOpacity=fillOpacity)
        return ret

if __name__ == "__main__":

    mymap = NaverMapPlotter(36.0207091, 127.9204629, 3, 'your_api_key')

    path = [(37.75,35.42,35.57,36.30,35.80,38.70),
             (125.4,128.56,128.34,125.9,128.2,127.9)]
    path2 = [[i+.1 for i in path[0]], [i+.12 for i in path[1]]]
    mymap.plot(path[0], path[1], "plum", edge_width=10)
    mymap.plot(path2[0], path2[1], "red")
    mymap.marker(37.75,125.5,title='mymarker')
    mymap.scatter(path[0],path[1],size=40000)

    mymap.draw('mymap.html')
