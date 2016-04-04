# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import pytest

from yolp import YOLP, YOLPError


class TestGeocode(object):
    def test_unauthorized(self):
        yolp = YOLP('INVALID_APP_ID')
        with pytest.raises(YOLPError):
            yolp.geocode('東京都千代田区丸の内一丁目')

    @pytest.mark.parametrize('address', [
        '名古屋県愛知市なごや1-1-2',
        '渋谷県東京区西3-19-2',
        'ほげたろう',
    ])
    def test_invalid_address(self, yolp, address):
        data = yolp.geocode(address)
        assert isinstance(data, list)
        assert len(data) == 0

    # @pytest.mark.parametrize('params', [
    #     {'query': '東京都千代田区丸の内一丁目', 'lat': -100.0, 'lon': -203.0},
    # ])
    # def test_invalid_params(self, yolp, params):
    #     with pytest.raises(YOLPError) as errinfo:
    #         yolp.geocode(**params)
    #     assert errinfo.value.code == 204

    @pytest.mark.parametrize('address', ['東京都千代田区丸の内一丁目'])
    def test_valid_address(self, yolp, address):
        data = yolp.geocode(address)
        assert isinstance(data, list)
        assert len(data) >= 1


class TestReverseGeocode(object):
    def test_unauthorized(self):
        yolp = YOLP('INVALID_APP_ID')
        with pytest.raises(YOLPError):
            yolp.reverse_geocode(35.674891, 139.763153)

    @pytest.mark.parametrize('lat, lon', [
        (0.0, 0.0),
        (25.0, 120.0),
    ])
    def test_unknown_point(self, yolp, lat, lon):
        data = yolp.reverse_geocode(lat, lon)
        assert isinstance(data, list)
        assert len(data) == 0

    @pytest.mark.parametrize('params', [
        {'lat': -100.0, 'lon': -203.0},
    ])
    def test_invalid_params(self, yolp, params):
        with pytest.raises(YOLPError) as errinfo:
            yolp.reverse_geocode(**params)
        assert errinfo.value.code == 1004

    @pytest.mark.parametrize('lat, lon', [(35.674891, 139.763153)])
    def test_valid_point(self, yolp, lat, lon):
        data = yolp.reverse_geocode(lat, lon)
        assert isinstance(data, list)
        assert len(data) >= 1


class TestDistance(object):
    def test_unauthorized(self):
        yolp = YOLP('INVALID_APP_ID')
        with pytest.raises(YOLPError):
            yolp.distance((35.680243, 139.767448), (35.674891, 139.763153))

    @pytest.mark.parametrize('start, end', [
        ((-100.0, -203.0), (-100.0, -204.0),),
    ])
    def test_invalid_points(self, yolp, start, end):
        with pytest.raises(YOLPError) as errinfo:
            yolp.distance(start, end)
        assert errinfo.value.code == 400

    @pytest.mark.parametrize('start, end', [
        ((35.680243, 139.767448), (35.674891, 139.763153),),
    ])
    def test_valid_points(self, yolp, start, end):
        data = yolp.distance(start, end)
        assert isinstance(data, list)
        assert len(data) >= 1


class TestZipCode(object):
    def test_unauthorized(self):
        yolp = YOLP('INVALID_APP_ID')
        with pytest.raises(YOLPError):
            yolp.zipcode('100-0005')

    @pytest.mark.parametrize('zipcode', [
        '000-0000',
        '999-9999',
    ])
    def test_invalid_zipcode(self, yolp, zipcode):
        data = yolp.zipcode(zipcode)
        assert isinstance(data, list)
        assert len(data) == 0

    @pytest.mark.parametrize('zipcode', ['100-0005'])
    def test_valid_zipcode(self, yolp, zipcode):
        data = yolp.zipcode(zipcode)
        assert isinstance(data, list)
        assert len(data) >= 1


class TestPlace(object):
    def test_unauthorized(self):
        yolp = YOLP('INVALID_APP_ID')
        with pytest.raises(YOLPError):
            yolp.place(35.674891, 139.763153)

    @pytest.mark.parametrize('lat, lon', [
        ('a', 'b'),
        (0.0, 0.0),
        (25.0, 120.0),
        (-100.0, -203.0),
    ])
    def test_unknown_point(self, yolp, lat, lon):
        data = yolp.place(lat, lon)
        assert isinstance(data, dict)
        assert len(data['Area']) == 0

    @pytest.mark.parametrize('lat, lon', [(35.674891, 139.763153)])
    def test_valid_point(self, yolp, lat, lon):
        data = yolp.place(lat, lon)
        assert isinstance(data, dict)
        assert len(data['Area']) >= 1


class TestContents(object):
    def test_unauthorized(self):
        yolp = YOLP('INVALID_APP_ID')
        with pytest.raises(YOLPError):
            yolp.contents('東京都千代田区丸の内一丁目')

    @pytest.mark.parametrize('address', ['あsだjlks'])
    def test_invalid_address(self, yolp, address):
        data = yolp.contents(address)
        assert isinstance(data, list)
        assert len(data) == 0

    @pytest.mark.parametrize('address', ['東京都千代田区丸の内一丁目'])
    def test_contents(self, yolp, address):
        data = yolp.contents(address)
        assert isinstance(data, list)
        assert len(data) >= 1


class TestDatum(object):
    def test_unauthorized(self):
        yolp = YOLP('INVALID_APP_ID')
        with pytest.raises(YOLPError):
            yolp.datum((35.680243, 139.767448))

    @pytest.mark.parametrize('points', [
        (('a', 'b'),),
    ])
    def test_invalid_points(self, yolp, points):
        with pytest.raises(YOLPError):
            yolp.datum(*points, datum='tky')

    @pytest.mark.parametrize('points', [
        ((35.680243, 139.767448),),
        ((35.680243, 139.767448), (35.674891, 139.763153)),
    ])
    def test_valid_points(self, yolp, points):
        data = yolp.datum(*points, datum='tky')
        assert isinstance(data, list)
        assert len(data) == len(points)


class TestAltitude(object):
    def test_unauthorized(self):
        yolp = YOLP('INVALID_APP_ID')
        with pytest.raises(YOLPError):
            yolp.altitude((35.680243, 139.767448))

    @pytest.mark.parametrize('points', [
        (('a', 'b'),),
    ])
    def test_invalid_points(self, yolp, points):
        with pytest.raises(YOLPError):
            yolp.altitude(*points)

    @pytest.mark.parametrize('points', [
        ((35.680243, 139.767448),),
        ((35.680243, 139.767448), (35.674891, 139.763153)),
    ])
    def test_altitude(self, yolp, points):
        data = yolp.altitude(*points)
        assert isinstance(data, list)
        assert len(data) == len(points)
