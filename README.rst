navmplot
======

Plotting data on Naver Maps. Here's an example

::

    from navmplot import navmplot

    # Place map
    mymap = NaverMapPlotter(36.0207091, 127.9204629, 3, 'YOUR_API_KEY')

    # Polyline
    path = [(37.75,35.42,35.57,36.30,35.80,38.70),
             (125.4,128.56,128.34,125.9,128.2,127.9)]
    path2 = [[i+.1 for i in path[0]], [i+.12 for i in path[1]]]
    mymap.plot(path[0], path[1], "plum", edge_width=10)
    mymap.plot(path2[0], path2[1], "red")

    # Scatter points
    mymap.scatter(path[0],path[1],size=40000)

    # Marker
    mymap.marker(37.75,125.5,title='mymarker')

    # Draw
    mymap.draw('mymap.html')

.. image:: https://i.imgur.com/RxuqiX4.jpg


-----

Inspired by `gmplot by Michael Woods <https://github.com/vgm64/gmplot>`_
