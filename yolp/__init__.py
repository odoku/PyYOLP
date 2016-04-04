# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import requests
import xmltodict


API_URLS = {
    'geocoder':          'http://geo.search.olp.yahooapis.jp/OpenLocalPlatform/V1/geoCoder',
    'reverse_geocoder':  'http://reverse.search.olp.yahooapis.jp/OpenLocalPlatform/V1/reverseGeoCoder',
    'distance':          'http://distance.search.olp.yahooapis.jp/OpenLocalPlatform/V1/distance',
    'zipcode':           'http://search.olp.yahooapis.jp/OpenLocalPlatform/V1/zipCodeSearch',
    'place_info':        'http://placeinfo.olp.yahooapis.jp/V1/get',
    'contents_geocoder': 'http://contents.search.olp.yahooapis.jp/OpenLocalPlatform/V1/contentsGeoCoder',
    'datum_convert':     'http://datum.search.olp.yahooapis.jp/OpenLocalPlatform/V1/datumConvert',
    'altitude':          'http://alt.search.olp.yahooapis.jp/OpenLocalPlatform/V1/getAltitude',
}


class YOLPError(Exception):
    def __init__(self, response, message, code, detail):
        super(YOLPError, self).__init__(message)
        self.response = response
        self.code = code
        self.message = message
        self.detail = detail


class YOLP(object):
    def __init__(self, appid):
        self.appid = appid
        self._response = None
        self._result = None

    def request(self, url, params=None):
        params = params if params is not None else {}
        params.update({
            'appid':  self.appid,
            'output': 'json',
        })
        params = {k: v for k, v in params.items() if v is not None}
        self._response = requests.get(url, params=params)

        try:
            data = self._response.json()
        except ValueError:
            data = xmltodict.parse(self._response.text)

        if 'Error' in data:
            raise YOLPError(
                self._response,
                data['Error']['Message'],
                int(data['Error']['Code']) if 'Code' in data['Error'] else None,
                data['Error']['Detail'] if 'Detail' in data['Error'] else '',
            )

        return data

    @property
    def response(self):
        '''
        直前にリクエストしたAPIのレスポンスを返します。
        '''
        return self._response

    @property
    def result(self):
        '''
        直前にリクエストしたAPIの ResultInfo を返します。
        '''
        return self._result

    def geocode(
        self, query=None, ei=None, lat=None, lon=None, bbox=None,
        datum=None, wgs=None, tky=None, ac=None, al=None, ar=None,
        recursive=None, sort=None, exclude_prefecture=None, exclude_seireishi=None,
        start=None, page=None, results=None, detail=None,
    ):
        '''
        住所をキーワードとして検索し、その位置情報を提供します。
        http://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/geocoder.html

        yolp = YOLP('YOUR_APP_ID')
        yolp.geocode('東京都千代田区丸の内一丁目')
        '''
        data = self.request(API_URLS['geocoder'], {
            'query': query,
            'ei': ei,
            'lat': lat,
            'lon': lon,
            'bbox': bbox,
            'datum': datum,
            'wgs': wgs,
            'tky': tky,
            'ac': ac,
            'al': al,
            'ar': ar,
            'recursive': recursive,
            'sort': sort,
            'exclude_prefecture': exclude_prefecture,
            'exclude_seireishi': exclude_seireishi,
            'start': start,
            'page': page,
            'results': results,
            'detail': detail,
        })
        self._result = data['ResultInfo']
        return data['Feature'] if 'Feature' in data else []

    def reverse_geocode(self, lat, lon, datum=None):
        '''
        指定の地点の住所情報を取得する機能を提供します。
        http://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/reversegeocoder.html

        yolp = YOLP('YOUR_APP_ID')
        yolp.reverse_geocode(35.674891, 139.763153)
        '''
        data = self.request(API_URLS['reverse_geocoder'], {
            'lat': lat,
            'lon': lon,
            'datum': datum,
        })
        self._result = data['ResultInfo']
        return data['Feature'] if 'Feature' in data else []

    def distance(self, start, end):
        '''
        2点間の緯度経度を指定して地球の楕円体に合わせた正確な距離を計算した結果を提供します。
        http://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/distance.html

        yolp = YOLP('YOUR_APP_ID')
        yolp.distance((35.680243, 139.767448), (35.674891, 139.763153))
        '''
        data = self.request(API_URLS['distance'], {
            'coordinates': '{},{} {},{}'.format(start[1], start[0], end[1], end[0]),
        })
        self._result = data['ResultInfo']
        return data['Feature'] if 'Feature' in data else []

    def zipcode(
        self, query=None, ac=None, sort=None, zkind=None,
        results=None, start=None, detail=None,

    ):
        '''
        郵便番号を指定して、位置情報や郵便番号名称が取得できます。
        http://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/zipcodesearch.html

        yolp = YOLP('YOUR_APP_ID')
        yolp.zipcode('100-0005')
        '''
        data = self.request(API_URLS['zipcode'], {
            'query': query,
            'ac': ac,
            'sort': sort,
            'zkind': zkind,
            'results': results,
            'start': start,
            'detail': detail,
        })
        self._result = data['ResultInfo']
        return data['Feature'] if 'Feature' in data else []

    def place(self, lat, lon):
        '''
        指定された緯度経度付近の主要ランドマーク名やエリア名などを返します。
        http://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/placeinfo.html

        yolp = YOLP('YOUR_APP_ID')
        yolp.place(35.674891, 139.763153)
        '''
        data = self.request(API_URLS['place_info'], {
            'lat': lat,
            'lon': lon,
        })
        self._result = None
        return data['ResultSet']

    def contents(self, query, ei=None, category=None, results=None):
        '''
        コンテンツジオコーダAPIは、場所を表すキーワードを検出し、その位置情報（緯度、経度など）を出力します。
        http://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/contentsgeocoder.html

        yolp = YOLP('YOUR_APP_ID')
        yolp.contents('東京都千代田区丸の内一丁目')
        '''
        data = self.request(API_URLS['contents_geocoder'], {
            'query': query,
            'ei': ei,
            'category': category,
            'results': results,
        })
        self._result = data['ResultInfo']
        return data['Feature'] if 'Feature' in data else []

    def datum(self, *coordinates, **options):
        '''
        緯度経度を日本測地系と世界測地系で相互変換します。
        http://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/datum.html

        yolp = YOLP('YOUR_APP_ID')
        yolp.datum((35.680243, 139.767448))
        yolp.datum((35.680243, 139.767448), (35.674891, 139.763153))
        '''
        data = self.request(API_URLS['datum_convert'], {
            'coordinates': ','.join(['{},{}'.format(c[1], c[0]) for c in coordinates]),
            'datum': options.get('datum'),
        })
        self._result = data['ResultInfo']
        return data['Feature'] if 'Feature' in data else []

    def altitude(self, *coordinates):
        '''
        指定の地点の標高データを取得する機能を提供します。
        http://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/altitude.html

        yolp = YOLP('YOUR_APP_ID')
        yolp.altitude((35.680243, 139.767448))
        '''
        data = self.request(API_URLS['altitude'], {
            'coordinates': ','.join(['{},{}'.format(c[1], c[0]) for c in coordinates]),
        })
        self._result = data['ResultInfo']
        return data['Feature'] if 'Feature' in data else []
