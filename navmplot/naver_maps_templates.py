CIRCLE = """
var center = new naver.maps.LatLng({lat}, {lng});
var radius = {size};
var circle = new naver.maps.Circle({{
        strokeColor: '{strokeColor}',
        strokeOpacity: {strokeOpacity},
        strokeWeight: {strokeWeight},
        fillColor: '{fillColor}',
        fillOpacity: {fillOpacity},
        center: center,
        radius: radius,
        clickable: true,
        map: map
    }});
"""

TEXT = """      
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no">
    <title>Naver Map TEST</title>
    <script type="text/javascript" src="https://openapi.map.naver.com/openapi/v3/maps.js?clientId={apikey}&submodules=visualization,drawing"></script>
</head>
<body style="margin:0px; padding:0px;">
<div id="map" style="width:100%;height:800px;"></div>
<script>
{MAP}
{POLYLINES}
{MARKERS}
{SYMBOLS}
</script>
</body>
</html>
"""

MAP="""
var map = new naver.maps.Map('map', {{
    zoomControl: true,
    zoomControlOptions: {{
        style: naver.maps.ZoomControlStyle.LARGE,
        position: naver.maps.Position.TOP_RIGHT
    }},
    mapTypeControl: true,
    zoom: {zoom},
    center: new naver.maps.LatLng({lat}, {lng})
}});
"""

POLYLINE="""
var data = [
{COORDS}
];
var polyline = new naver.maps.Polyline({{
        path: data,
        strokeColor: '{strokeColor}',
        strokeOpacity: {strokeOpacity},
        strokeWeight: {strokeWeight},
        clickable: true,
        map: map
    }});
"""

COORD="""new naver.maps.LatLng({lat},{lng}),
"""

MARKER="""
var position = new naver.maps.LatLng({lat}, {lng});
var markerOptions = {{
    position: position,
    map: map,
    title: '{title}',
    icon: '{icon}'
}};
var marker = new naver.maps.Marker(markerOptions);
"""

SYMBOLS = {'o': CIRCLE,
}
