from __future__ import generators
import osgeo.ogr, osgeo.osr, osgeo, osr, ogr
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
import time, os, shutil, sys, json
from math import radians, cos, sin, asin, sqrt
from scipy.spatial import ConvexHull
import datetime
from django.contrib.gis.geos import GEOSGeometry, LineString, Point
from django.core import serializers
import psycopg2,ast
from module.GIS_API.dijkstra import dijkstra, shortest_path,shortest_path_new

'''
def home_2(lon,lat):
    d={}
    #lat = 22.716301744945156 #float(request.GET.get('lat'))
    #lon = 75.86075730621813 #float(request.GET.get('lon'))
    conn = psycopg2.connect(database="tech", user="postgres", password="dudes11081991", host="localhost", port="5432")
    print("Opened database successfully")
    cur = conn.cursor()
    cur.execute("SELECT gid, ST_X(geom),ST_Y(geom) from public.indoreroad_gis_point")
    rows = cur.fetchall()
    now = time.localtime(time.time())
    print(now[3], now[4], now[5],'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
    alpha, l = {}, []
    for row in rows:
        l.append(haversine((lon, lat), (row[1], row[2])))
        alpha[haversine((lon, lat), (row[1], row[2]))] = row[0]
    print(alpha[min(l)])
    return alpha[min(l)]

def datset_generator_new_2(c, d,nodes,points,rows):
    nodelist = []
    graph,wineshope,geraph = deadendremoval_new_2(c, d,nodes,points,rows)
    return graph,wineshope,geraph


def deadendremoval_new_2(c, d,nodes,points,rows):
    dead, legitimate = [], []
    ni = {}
    W = True
    j = 0
    graph,wineshope,geraph = circularring_new_1(c, d,nodes,points,rows)
    return graph,wineshope,geraph


def circularring_new_1(c, d,nodes,points,rows):

    poly=Point(c, d).buffer(0.0150)

    wineshope = {}
    poi = []
    now = time.localtime(time.time())
    print(now[3], now[4], now[5], 'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
    for row in rows:
        if Point(row[1],row[2]).within(poly):
            wineshope[row[0]] = [row[1],row[2]]
            print(len(wineshope))
    if input('press enter'):
        pass
    if input('press enter'):
        pass
    graph = {}
    geraph={}


    for key in points:
        if Point(key[1], key[2]).within(poly):
            li={}
            ki=[]
            for fe in nodes:
                if fe[1]==key[0]:
                    li[fe[2]]=fe[3]
                    ki.append([fe[2],fe[0]])
                if fe[2]==key[0]:
                    li[fe[1]]=fe[3]
                    ki.append([fe[1],fe[0]])
            graph[key[0]]=li
            geraph[key[0]]=ki

    print(graph)
    now = time.localtime(time.time())
    print(now[3], now[4], now[5], 'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
    if input("press enter"):
        pass

    return graph,wineshope,geraph


def haversine(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")
    lat1 = pointA[1]
    lon1 = pointA[0]
    lat2 = pointB[1]
    lon2 = pointB[0]
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r



class WineShopCoordinates(APIView):
    def get(self, request):
        coords = Result.objects.all()
        serializer = WineShopCoordinatesSerializer(coords, many=True)
        return Response(serializer.data)

    def post(self, request):
        coords = WineShopCoordinatesSerializer(data=request.data)
        print(coords.is_valid())
        if coords.is_valid():
            coords.save()
            print("##############")
            print(request.data)
            return Response(coords.data, status=status.HTTP_201_CREATED)
        return Response(coords.errors, status=status.HTTP_400_BAD_REQUEST)

def storeCoordinates(request,lat,lon):
    path=[]
    #lat = 22.716301744945156 #float(request.GET.get('lat'))
    #lon = 75.86075730621813 #float(request.GET.get('lon'))
    conn = psycopg2.connect(database="tech", user="postgres", password="dudes11081991", host="localhost", port="5432")
    print("Opened database successfully")
    cur = conn.cursor()
    cur.execute("SELECT gid, source_nod, target_nod,length_m from public.indore_road_gis_line")
    nodes = cur.fetchall()
    cur.execute("SELECT gid, ST_X(geom),ST_Y(geom) from public.indoreroad_gis_point")
    points = cur.fetchall()
    cur.execute("SELECT gid, ST_X(geom),ST_Y(geom) from public.excise_asset_shp")
    rows = cur.fetchall()
    lat = float(lat)
    lon = float(lon)
    print(lat, lon)
    startnode = home_2(lon, lat)
    now = time.localtime(time.time())
    print(now[3], now[4], now[5], "starting projectttttttttttt")
    #di,ni=datset_generator_new(75.889262000000002,22.746867000000002,75.849441999999996,22.735239000000000, path='C:/Users\shashank\Desktop/result/roadnetwork_short.shp')
    graph,wineshope,geraph = datset_generator_new_2(lon, lat,nodes,points,rows)
    for ke, value in wineshope.items():
        endnode = home_2(value[0], value[1])
        now = time.localtime(time.time())
        print(now[3], now[4], now[5], "dataset is prep")
        #dist, pred = dijkstra(graph, startnode,endnode)
        finalpath=shortest_path(graph, startnode,endnode)
        nodeset=[]
        path_id=[]
        for i in range(len(finalpath) - 1):
            nodeset.append([finalpath[i],finalpath[i+1]])           
        print(path_id,'\n')
        print(finalpath)
        print(path_id)
        if input("press enter"):
            pass
    conn.commit()
    conn.close()
'''


def home_2(lon, lat, cur):
    d = {}
    # lat = 22.716301744945156 #float(request.GET.get('lat'))
    # lon = 75.86075730621813 #float(request.GET.get('lon'))
    # conn = psycopg2.connect(database="tech", user="postgres", password="dudes11081991", host="localhost", port="5432")
    # print("Opened database successfully")
    # cur = conn.cursor()
    k=0.00001
    while True:
        cur.execute(
            '''SELECT gid, ST_X(geom),ST_Y(geom) from network_sch."NODES" WHERE ST_DWithin(geom, 'SRID=4326;POINT(%f %f).buffer(0.0050)', %f) ''' % (float(lon), float(lat),k))
        points = cur.fetchall()
        if len(points)>0:
            break
        else:
            if k>1:
                print(lon, lat,"NO NODE FOUND WITH IN 100 KILOMETER CHECK LINE 185 IN path_api_3")
            k+=(0.00001)
            print(k)
    now = time.localtime(time.time())
    #print(now[3], now[4], now[5],'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
    alpha, l = {}, []
    for row in points:
        l.append(haversine((lon, lat), (row[1], row[2])))
        alpha[haversine((lon, lat), (row[1], row[2]))] = [row[0],row[1], row[2]]
    print(alpha[min(l)],"STARTNODE/ENDNODE")
    return alpha[min(l)][0],alpha[min(l)][1],alpha[min(l)][2]



def home_2_datia(lon, lat, cur):
    d = {}
    # lat = 22.716301744945156 #float(request.GET.get('lat'))
    # lon = 75.86075730621813 #float(request.GET.get('lon'))
    # conn = psycopg2.connect(database="tech", user="postgres", password="dudes11081991", host="localhost", port="5432")
    # print("Opened database successfully")
    # cur = conn.cursor()
    k=0.00001
    while True:
        cur.execute(
            '''SELECT gid, ST_X(geom),ST_Y(geom) from network_sch.node_point WHERE ST_DWithin(geom, 'SRID=4326;POINT(%f %f).buffer(0.0050)', %f) ''' % (float(lon), float(lat),k))
        points = cur.fetchall()
        if len(points)>0:
            break
        else:
            k+=(0.00001)

    now = time.localtime(time.time())
    #print(now[3], now[4], now[5],'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
    alpha, l = {}, []
    for row in points:
        l.append(haversine((lon, lat), (row[1], row[2])))
        alpha[haversine((lon, lat), (row[1], row[2]))] = [row[0],row[1], row[2]]
    print(alpha[min(l)],"STARTNODE/ENDNODE")
    return alpha[min(l)][0],alpha[min(l)][1],alpha[min(l)][2]

def datset_generator_new_2(c, d, lon2, lat2, points,factor):
    nodelist = []
    graph = deadendremoval_new_2(c, d, lon2, lat2, points,factor)
    return graph


def deadendremoval_new_2(c, d, lon2, lat2, points,factor):
    dead, legitimate = [], []
    ni = {}
    W = True
    j = 0
    graph = circularring_new_1(c, d, lon2, lat2, points,factor)
    return graph


def circularring_new_1(c, d, lon2, lat2, cur,factor):
    distance=haversine((c, d), (lon2, lat2))/100
    print(c, d, lon2, lat2)
    #print(distance)
    #if input("press enter"):
        #pass
    now = time.localtime(time.time())
    #print(now[3], now[4], now[5],'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
    graph = {}
    cur.execute('''SELECT gid, ST_X(geom),ST_Y(geom) from network_sch."NODES" WHERE ST_Within(geom,ST_Buffer('SRID=4326;LINESTRING(%f %f,%f %f)',%f))''' % (c, d, lon2, lat2, (distance*(2.5+factor))))
    points = cur.fetchall()
    for i in points:
        cur.execute('''SELECT gid, value from network_sch.graph WHERE gid=%d'''%i[0])
        key = cur.fetchall()
        for k in key:
            graph[k[0]]=ast.literal_eval(k[1])
    return graph


def circularring_new_2(c, d, lon2, lat2, cur,factor):
    distance=haversine((c, d), (lon2, lat2))/100
    print(c, d, lon2, lat2)
    #print(distance)
    #if input("press enter"):
        #pass
    now = time.localtime(time.time())
    #print(now[3], now[4], now[5],'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
    graph = {}
    cur.execute('''SELECT node__id, ST_X(geom),ST_Y(geom) from network_sch.node_point WHERE ST_Within(geom,ST_Buffer('SRID=4326;LINESTRING(%f %f,%f %f)',%f))''' % (c, d, lon2, lat2, (distance*(2.5+factor))))
    points = cur.fetchall()
    for i in points:
        cur.execute('''SELECT gid, value from network_sch.datia_graph WHERE gid=%d'''%int(i[0]))
        key = cur.fetchall()
        for k in key:
            graph[k[0]]=ast.literal_eval(k[1])
    return graph

def circularring_new_worst(cur):
    #print(distance)
    #if input("press enter"):
        #pass
    now = time.localtime(time.time())
    #print(now[3], now[4], now[5],'ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
    graph = {}
    cur.execute('''SELECT gid, value from network_sch.datia_graph''')
    key = cur.fetchall()
    for k in key:
        graph[k[0]]=ast.literal_eval(k[1])
    return graph

def haversine(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")
    lat1 = pointA[1]
    lon1 = pointA[0]
    lat2 = pointB[1]
    lon2 = pointB[0]
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    # returns result in kilometer
    return c * r




def storeCoordinates_1(lat1, lon1, lat2, lon2):
    path = []
    # lat = 22.716301744945156 #float(request.GET.get('lat'))
    # lon = 75.86075730621813 #float(request.GET.get('lon'))
    conn = psycopg2.connect(database="tech", user="postgres", password="dudes11081991", host="localhost", port="5432")
    #print("Opened database successfully")
    cur = conn.cursor()
    # cur.execute('''SELECT gid, ST_X(geom),ST_Y(geom) from network_sch."NODES" ''')
    # points = cur.fetchall()
    cur.execute("SELECT gid, ST_X(geom),ST_Y(geom) from public.excise_asset_shp")
    rows = cur.fetchall()
    startnode = home_2(float(lon1), float(lat1), cur)
    now = time.localtime(time.time())
    #print(now[3], now[4], now[5], "starting projectttttttttttt")
    # di,ni=datset_generator_new(75.889262000000002,22.746867000000002,75.849441999999996,22.735239000000000, path='C:/Users\shashank\Desktop/result/roadnetwork_short.shp')
    graph = datset_generator_new_2(float(lon1), float(lat1), float(lon2), float(lat2), cur)
    endnode = home_2(float(lon2), float(lat2), cur)
    now = time.localtime(time.time())
    #print(now[3], now[4], now[5], "dataset is prep")
    # dist, pred = dijkstra(graph, startnode,endnode)
    finalpath = shortest_path(graph, startnode, endnode)
    print(startnode, endnode, finalpath)
    now = time.localtime(time.time())
    print(now[3], now[4], now[5], "dataset is prep")
    data = storeCoordinates_3(finalpath, cur)
    routej(data, "C:/Users\shashank\Desktop\POLY", name='FINALPATH_%f_%f_%f' % (now[3], now[4], now[5]))
    return data


def store(request):
    return 0


def creating_directoryj(name, path):
    folderName = ("%s" % name)
    folderPath = ("%s" % path)
    path = folderPath + '\\' + folderName
    if os.path.exists("%s" % path):
        shutil.rmtree("%s" % path)
    os.mkdir("%s" % path)
    return (path, folderName)


def routej(geojson, path, name):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    folderLocation, folderName = creating_directoryj(name, path)
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("resulting layer", spatialReference)
    feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
    for i in geojson:
        line = ogr.CreateGeometryFromJson(str(i))
        feature.SetGeometry(line)
        dstLayer.CreateFeature(feature)
    feature.Destroy()
    dstFile.Destroy()
from jsonmerge import merge

def storeCoordinates_3(test_list, cur,data,wkt):
    final_geom=None
    res = [[test_list[i], test_list[i + 1]]
           for i in range(len(test_list) - 1)]
    for i in res:
        cur.execute('''SELECT gid, ST_AsGeoJSON(geom),ST_AsText(geom),ST_AsEWKT(geom),geom from network_sch."ROAD" WHERE source_nod=%d AND target_nod=%d''' % (i[0], i[1]))
        nodes = cur.fetchall()
        for iut in nodes:
            if final_geom is None:
                final_geom=ogr.CreateGeometryFromJson(str(iut[1]))
            else:
                final_geom=final_geom.Union(ogr.CreateGeometryFromJson(str(iut[1])))
            print(iut[0], i[0], i[1])
            #print(iut[1])

            data.append(iut[1])
            #wkt.append(iut[2])


        cur.execute('''SELECT gid, ST_AsGeoJSON(geom),ST_AsText(geom),ST_AsEWKT(geom),geom from network_sch."ROAD" WHERE source_nod=%d AND target_nod=%d''' % (i[1], i[0]))
        nodes = cur.fetchall()
        for iut in nodes:
            if final_geom is None:
                final_geom=ogr.CreateGeometryFromJson(str(iut[1]))
            else:
                final_geom=final_geom.Union(ogr.CreateGeometryFromJson(str(iut[1])))
            final_geom = final_geom.Union(ogr.CreateGeometryFromJson(str(iut[1])))
            print(iut[0], i[0], i[1])
            #print(iut[1])
            data.append(iut[1])
            #wkt.append(iut[2])

    now = time.localtime(time.time())
    #print(now[3], now[4], now[5], "dataset is prep",'\n',final_geom.ExportToJson())
    return data,final_geom.ExportToJson()


'''
    for i,w in enumerate(finalpath):

        for iut in nodes:
            print(i,w)
            #if finalpath[i] in iut and finalpath[i + 1] in iut:
                #print(iut[0], finalpath[i], finalpath[i + 1])
                #path.append(iut[1])


    now = time.localtime(time.time())
    print(now[3], now[4], now[5], "dataset is prep")
    return path


'''

def routej_2(wkt, path, name):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    folderLocation, folderName = creating_directoryj(name, path)
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("resulting layer", spatialReference)
    feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
    line = ogr.CreateGeometryFromWkt(wkt)
    feature.SetGeometry(line)
    dstLayer.CreateFeature(feature)
    feature.Destroy()
    dstFile.Destroy()



def routej_3(snode,enode,length,geojson, path, name):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    folderLocation, folderName = creating_directoryj(name, path)
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("resulting layer", spatialReference)
    sn = ogr.FieldDefn("snode", ogr.OFTInteger64)
    dstLayer.CreateField(sn)
    en = ogr.FieldDefn("enode", ogr.OFTInteger64)
    dstLayer.CreateField(en)
    idField = ogr.FieldDefn("length", ogr.OFTReal)
    dstLayer.CreateField(idField)
    feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
    for i in geojson:
        line = ogr.CreateGeometryFromJson(str(i))
        feature.SetGeometry(line)
    feature.SetField("snode", snode)
    feature.SetField("enode", enode)
    feature.SetField("length", length)
    dstLayer.CreateFeature(feature)
    feature.Destroy()
    dstFile.Destroy()


def openfile(filepath):
    datasource=ogr.Open(filepath)
    layer=datasource.GetLayer(0)
    for feat in layer:
        geom=feat.GetGeometryRef()
        geom_poly_envelope = geom.GetEnvelope()
        #print(geom_poly_envelope[0],geom_poly_envelope[2],geom_poly_envelope[1],geom_poly_envelope[3])
        #print((geom_poly_envelope[0]+geom_poly_envelope[1])/2,(geom_poly_envelope[2]+geom_poly_envelope[3])/2)
        return (geom_poly_envelope[0]+geom_poly_envelope[1])/2,(geom_poly_envelope[2]+geom_poly_envelope[3])/2