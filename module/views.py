import psycopg2
from module.GIS_API.PATH_API_3 import *
import time, os, shutil, osgeo.ogr, osgeo.osr, ogr, sys, osr, json,ast,json
from math import radians, cos, sin, asin, sqrt
from module.GIS_API.dijkstra import shortest_path_new



def storeCoordinates_6(startnodeX, startnodeY, endnodeX, endnodeY,cur,data,wkt,conn,startnode,endnode):
    X = True
    factor = 0
    json1,distace_route=None,0
    while X:
        graph=circularring_new_1(float(startnodeX),float(startnodeY),float(endnodeX),float(endnodeY),cur,factor)
        #print(graph)
        finalpath, dist, pred = shortest_path_new(graph, int(startnode), int(endnode))
        # dist, pred = dijkstra(graph, int(star[0]), int(end[0]))
        if dist == 'no' and pred == 'no':
            factor += 0.5
            #print(factor)
            distance = haversine((float(startnodeX),float(startnodeY)),
                                 (float(endnodeX),float(endnodeY))) / 100
            print(distance * (2.5 + factor))
            if (distance * (2.5 + factor)) > 1:
                print("CHECK DATASET", int(startnode), int(endnode),"###################################################################")
                X = False

        else:
            data,json1= storeCoordinates_3(finalpath, cur,data,wkt)
            now = time.localtime(time.time())
            #print(now[3], now[4], now[5],dist[endnode],dist[startnode],'\n',wkt)
            distace_route=float(dist[endnode])
            #routej([json1], "C:/Users\shashank\Desktop\POLY", name='FINALPATH_%f_%f_%f' % (now[3], now[4], now[5]))
            X = False
    return data,json1,distace_route



def dataset_mp_api(request,lon1,lat1,lon2,lat2):
    #lon1 = 78.5195
    #lat1 = 23.0718
    #lon2 = 78.7437
    #lat2 = 23.0060
    #lat1,lon1,lat2,lon2,data,wkt=None,None,[],[],[],[]
    data, wkt=[],[]
    conn = psycopg2.connect(database="tech", user="postgres", password="dudes11081991", host="localhost", port="5432")
    print("Opened database successfully")
    cur = conn.cursor()
    startnode, startnodeX, startnodeY = home_2(lon1, lat1, cur)
    endnode, endnodeX, endnodeY = home_2(lon2, lat2, cur)
    di=0
    coord1,coord2,coord3,coord_all=[],[],[],[]
    #print(i[6], "################", lat1, lon1, float(j[4]), float(j[3]), "#################", j[2])
    if int(startnode) != int(endnode):
        data, pat, dis = storeCoordinates_6(startnodeX, startnodeY, endnodeX, endnodeY, cur, data, wkt, conn, startnode, endnode)
        #print(pat,'\n',dis,'\n',data)
        coord = [k for k in ast.literal_eval(pat)['coordinates']]
        for i in coord:
            for j in i:
                coord_all.append(j)
        print(coord_all)




        '''
        coord=[k for k in ast.literal_eval(pat)['coordinates']]
        for i in coord:
            print(i)
            print(i)
            if input("press enter"):
                pass
            if di<dis/3:
                print("i am in")
                di=di+haversine(tuple(i[0]),tuple(i[1]))
                coord1.append(i)
            print(coord1)
            if input("press enter"):
                pass
            elif (dis/3)<=di<(2*dis/3):
                di = di + haversine(tuple(i[0]), tuple(i[1]))
                coord2.append(i)
            print(coord2)
            if input("press enter"):
                pass
            elif di<=(2*dis/3):
                di = di + haversine(tuple(i[0]), tuple(i[1]))
                coord2.append(i)
            print(coord3)
            if input("press enter"):
                pass
        #assert di==dis
        print(di,dis)
        print(coord1,'\n',coord2,'\n',coord3)'''
        return HttpResponse(pat, content_type='application/json')
    else:
        dista = haversine((startnodeX, startnodeY), (lon2, lat2))
        line = ogr.Geometry(ogr.wkbLineString)
        line.AddPoint(startnodeX, startnodeY)
        line.AddPoint(lon2, lat2)
        line.ExportToJson()
        print(line)
        return HttpResponse(line, content_type='application/json')

def dataset_route(request):
    shortlist = []
    conn = psycopg2.connect(database="tech", user="postgres", password="dudes11081991", host="localhost", port="5432")
    print("Opened database successfully")
    cur = conn.cursor()
    wine_coords = []
    data, wkt = [], []
    cur.execute(
        '''SELECT gid, sid, assetguid, shop, division, district, circle, shop_name, license_ty, license_nu, licensee_n, dept_code, mappingsta, asset_code, 
        ST_X(geom),ST_Y(geom),geom FROM network_sch.wineshop''')

    wine_data = cur.fetchall()
    for i in wine_data:
        lon1, lat1=i[14],i[15]
        for j in wine_data:
            lon2, lat2=j[14],j[15]
            startnode, startnodeX, startnodeY = home_2(lon1, lat1, cur)
            endnode, endnodeX, endnodeY = home_2(lon2, lat2, cur)
            di = 0
            coord1, coord2, coord3 = [], [], []
            #print(i[6], "################", lat1, lon1, float(j[4]), float(j[3]), "#################", j[2])
            if int(startnode) != int(endnode):
                data, pat, dis = storeCoordinates_6(startnodeX, startnodeY, endnodeX, endnodeY, cur, data, wkt, conn, startnode, endnode)
                cur.execute(
                    "INSERT INTO network_sch.wineshop_route (sid_start, assetguid_start, shop_start, division_start, district_start, circle_start, shop_name_start, license_ty_start, "
                    "license_nu_start, licensee_n_start, dept_code_start, asset_loc_start, "
                    "asset_lo_1_start, mappingsta_start, asset_code_start, sid_end, "
                    "assetguid_end, shop_end, division_end, district_end, circle_end, "
                    "shop_name_end, license_ty_end, license_nu_end, licensee_n_end, "
                    "dept_code_end, asset_loc_end, asset_lo_1_end, mappingsta_end, "
                    "asset_code_end, route) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(
                        str(i[1]) , "'" + str(i[2]) + "'", "'" + str(i[3]) + "'",
                        "'" + str(i[4]) + "'", "'" + str(i[5]) + "'", "'" + str(i[6]) + "'", "'" + str(i[7]) + "'",
                        "'" + str(i[8]) + "'", "'" + str(i[9]) + "'", "'" + str(i[10]) + "'", "'" + str(i[11]) + "'",
                        lon1,lat1, "'" + str(i[12]) + "'", "'" + str(i[13]) + "'",

                       str(j[1]) , "'" + str(j[2]) + "'", "'" + str(j[3]) + "'",
                        "'" + str(j[4]) + "'", "'" + str(j[5]) + "'", "'" + str(j[6]) + "'", "'" + str(j[7]) + "'",
                        "'" + str(j[8]) + "'", "'" + str(j[9]) + "'", "'" + str(j[10]) + "'", "'" + str(j[11]) + "'",
                        lon2, lat2, "'" + str(j[12]) + "'", "'" + str(j[13]) + "'",

                         "'" + str(pat) + "'"))
                conn.commit()

            else:
                dista = haversine((startnodeX, startnodeY), (lon2, lat2))
                line = ogr.Geometry(ogr.wkbLineString)
                line.AddPoint(startnodeX, startnodeY)
                line.AddPoint(lon2, lat2)
                line.ExportToJson()
                print(line.ExportToJson())

                cur.execute(
                    "INSERT INTO network_sch.wineshop_route (sid_start, assetguid_start, shop_start, division_start, "
                    "district_start, circle_start, shop_name_start, license_ty_start, license_nu_start, "
                    "licensee_n_start, dept_code_start, asset_loc_start, asset_lo_1_start, mappingsta_start, "
                    "asset_code_start, sid_end, assetguid_end, shop_end, division_end, district_end, circle_end, s"
                    "hop_name_end, license_ty_end, license_nu_end, licensee_n_end, dept_code_end, asset_loc_end, asset_lo_1_end, mappingsta_end, asset_code_end, route) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(
                         str(i[1]) , "'" + str(i[2]) + "'", "'" + str(i[3]) + "'",
                        "'" + str(i[4]) + "'", "'" + str(i[5]) + "'", "'" + str(i[6]) + "'", "'" + str(i[7]) + "'",
                        "'" + str(i[8]) + "'", "'" + str(i[9]) + "'", "'" + str(i[10]) + "'", "'" + str(i[11]) + "'",
                        lon1, lat1, "'" + str(i[16]) + "'", "'" + str(i[17]) + "'",

                        str(j[1]) , "'" + str(j[2]) + "'", "'" + str(j[3]) + "'",
                        "'" + str(j[4]) + "'", "'" + str(j[5]) + "'", "'" + str(j[6]) + "'", "'" + str(j[7]) + "'",
                        "'" + str(j[8]) + "'", "'" + str(j[9]) + "'", "'" + str(j[10]) + "'", "'" + str(j[11]) + "'",
                        lon2, lat2, "'" + str(j[12]) + "'", "'" + str(j[13]) + "'",

                        "'"+str(line.ExportToJson())+"'"))
                conn.commit()
                #return HttpResponse(line, content_type='application/json')
                if input("press enter"):
                    pass



def school_id(cur):
    sch_gid=[]
    cur.execute('''SELECT a.gid as wine_gid, a.geom FROM network_sch.wineshop a''')
    rows = cur.fetchall()
    for i in rows:
        sch_gid.append(i[0])
    return sch_gid


def dataset_set_mp_new(request):
    now = time.localtime(time.time())
    print(now)
    lat1,lon1,lat2,lon2,data,wkt=None,None,[],[],[],[]
    conn = psycopg2.connect(database="tech", user="postgres", password="dudes11081991", host="localhost", port="5432")
    print("Opened database successfully")
    cur = conn.cursor()
    id_list=school_id(cur)
    print(id_list,len(id_list))
    for pid in id_list:
        cur.execute('''SELECT gid, sid, assetguid, shop, division, district, circle, shop_name, license_ty, license_nu, licensee_n, dept_code, mappingsta, asset_code, 
        ST_X(geom),ST_Y(geom),geom FROM network_sch.wineshop where gid=%d'''%pid)
        rows = cur.fetchall()
        #print(rows)
        for i in rows:
            lon1,lat1=float(i[14]),float(i[15])
            #print(float(i[7]),float(i[8]),"###############################################")
            cur.execute('''SELECT gid, sid, assetguid, shop, division, district, circle, shop_name, license_ty, license_nu, licensee_n, dept_code, mappingsta, asset_code, 
        ST_X(geom),ST_Y(geom),geom FROM network_sch.wineshop WHERE ST_Within(geom,ST_Buffer('SRID=4326;POINT(%f %f)',%f))'''%(lon1,lat1,0.100))
            #cur.execute('''select hab_id,ST_X(geom),ST_Y(geom)  from network_sch.ms_datia WHERE ST_Within(geom,ST_Buffer('SRID=4326;POINT(%f %f)',%f))''' % (lon1, lat1, 0.050))
            #SELECT avg(ST_X(ST_Centroid(a.geom))) as X,avg(ST_Y(ST_Centroid(a.geom))) as Y FROM network_sch.hab_mp a, network_sch.village  b  WHERE ST_Intersects(a.geom,b.geom)
            cols = cur.fetchall()
            print(cols)
            for j in cols:
                startnode, startnodeX, startnodeY = home_2(float(lon1), float(lat1), cur)
                endnode, endnodeX, endnodeY = home_2(float(j[14]),float(j[15]), cur)
                #print(i[6],"################",lat1, lon1, float(j[4]), float(j[3]),"#################",j[2])
                if int(startnode)!=int(endnode):
                    data,pat,dis=storeCoordinates_6(startnodeX, startnodeY, endnodeX, endnodeY, cur,data,wkt,conn,startnode,endnode)
                    cur.execute(
                        "INSERT INTO network_sch.wineshop_route (sid_start, assetguid_start, shop_start, division_start, district_start, circle_start, shop_name_start, license_ty_start, "
                        "license_nu_start, licensee_n_start, dept_code_start, asset_loc_start, "
                        "asset_lo_1_start, mappingsta_start, asset_code_start, sid_end, "
                        "assetguid_end, shop_end, division_end, district_end, circle_end, "
                        "shop_name_end, license_ty_end, license_nu_end, licensee_n_end, "
                        "dept_code_end, asset_loc_end, asset_lo_1_end, mappingsta_end, "
                        "asset_code_end, route) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(
                            str(i[1]), "'" + str(i[2]) + "'", "'" + str(i[3]) + "'",
                                       "'" + str(i[4]) + "'", "'" + str(i[5]) + "'", "'" + str(i[6]) + "'",
                                       "'" + str(i[7]) + "'",
                                       "'" + str(i[8]) + "'", "'" + str(i[9]) + "'", "'" + str(i[10]) + "'",
                                       "'" + str(i[11]) + "'",
                            lon1, lat1, "'" + str(i[12]) + "'", "'" + str(i[13]) + "'",

                            str(j[1]), "'" + str(j[2]) + "'", "'" + str(j[3]) + "'",
                                       "'" + str(j[4]) + "'", "'" + str(j[5]) + "'", "'" + str(j[6]) + "'",
                                       "'" + str(j[7]) + "'",
                                       "'" + str(j[8]) + "'", "'" + str(j[9]) + "'", "'" + str(j[10]) + "'",
                                       "'" + str(j[11]) + "'",
                            j[14], j[15], "'" + str(j[12]) + "'", "'" + str(j[13]) + "'",

                                       "'" + str(pat) + "'"))
                    conn.commit()
                    print(dis)
                else:
                    dista=haversine((startnodeX, startnodeY),(float(j[14]),float(j[15])))
                    line = ogr.Geometry(ogr.wkbLineString)
                    line.AddPoint(startnodeX, startnodeY)
                    line.AddPoint(float(j[14]),float(j[15]))
                    cur.execute(
                        "INSERT INTO network_sch.wineshop_route (sid_start, assetguid_start, shop_start, division_start, "
                        "district_start, circle_start, shop_name_start, license_ty_start, license_nu_start, "
                        "licensee_n_start, dept_code_start, asset_loc_start, asset_lo_1_start, mappingsta_start, "
                        "asset_code_start, sid_end, assetguid_end, shop_end, division_end, district_end, circle_end, s"
                        "hop_name_end, license_ty_end, license_nu_end, licensee_n_end, dept_code_end, asset_loc_end, asset_lo_1_end, mappingsta_end, asset_code_end, route) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(
                            str(i[1]), "'" + str(i[2]) + "'", "'" + str(i[3]) + "'",
                                       "'" + str(i[4]) + "'", "'" + str(i[5]) + "'", "'" + str(i[6]) + "'",
                                       "'" + str(i[7]) + "'",
                                       "'" + str(i[8]) + "'", "'" + str(i[9]) + "'", "'" + str(i[10]) + "'",
                                       "'" + str(i[11]) + "'",
                            lon1, lat1, "'" + str(i[12]) + "'", "'" + str(i[13]) + "'",

                            str(j[1]), "'" + str(j[2]) + "'", "'" + str(j[3]) + "'",
                                       "'" + str(j[4]) + "'", "'" + str(j[5]) + "'", "'" + str(j[6]) + "'",
                                       "'" + str(j[7]) + "'",
                                       "'" + str(j[8]) + "'", "'" + str(j[9]) + "'", "'" + str(j[10]) + "'",
                                       "'" + str(j[11]) + "'",
                            j[14],j[15], "'" + str(j[12]) + "'", "'" + str(j[13]) + "'",

                                       "'" + str(line.ExportToJson()) + "'"))
                    conn.commit()
                    print(line)

            now = time.localtime(time.time())
            print(now)
            if input("press enter"):
                pass
            #routej(data, "C:/Users\shashank\Desktop\POLY", name='FINALPATH_%f_%f_%f' % (now[3], now[4], now[5]))
            #return render(request, 'wkt_data_loader.html', {'list': wkt,'point':[lon1,lat1]})


def dataset_set_mp_new_bifurcated(request):

    now = time.localtime(time.time())

    print(now)
    lat1,lon1,lat2,lon2,data,wkt=None,None,[],[],[],[]
    conn = psycopg2.connect(database="tech", user="postgres", password="dudes11081991", host="localhost", port="5432")
    print("Opened database successfully")
    cur = conn.cursor()
    id_list=school_id(cur)
    print(id_list,len(id_list))
    for pid in id_list:
        cur.execute('''SELECT gid, sid, assetguid, shop, division, district, circle, shop_name, license_ty, license_nu, licensee_n, dept_code, mappingsta, asset_code, 
        ST_X(geom),ST_Y(geom),geom FROM network_sch.wineshop where gid=%d'''%pid)
        rows = cur.fetchall()
        #print(rows)
        for i in rows:
            lon1,lat1=float(i[14]),float(i[15])
            #print(float(i[7]),float(i[8]),"###############################################")
            cur.execute('''SELECT gid, sid, assetguid, shop, division, district, circle, shop_name, license_ty, license_nu, licensee_n, dept_code, mappingsta, asset_code, 
        ST_X(geom),ST_Y(geom),geom FROM network_sch.wineshop WHERE ST_Within(geom,ST_Buffer('SRID=4326;POINT(%f %f)',%f))'''%(lon1,lat1,0.100))
            #cur.execute('''select hab_id,ST_X(geom),ST_Y(geom)  from network_sch.ms_datia WHERE ST_Within(geom,ST_Buffer('SRID=4326;POINT(%f %f)',%f))''' % (lon1, lat1, 0.050))
            #SELECT avg(ST_X(ST_Centroid(a.geom))) as X,avg(ST_Y(ST_Centroid(a.geom))) as Y FROM network_sch.hab_mp a, network_sch.village  b  WHERE ST_Intersects(a.geom,b.geom)
            cols = cur.fetchall()
            print(cols)
            for j in cols:
                startnode, startnodeX, startnodeY = home_2(float(lon1), float(lat1), cur)
                endnode, endnodeX, endnodeY = home_2(float(j[14]),float(j[15]), cur)
                #print(i[6],"################",lat1, lon1, float(j[4]), float(j[3]),"#################",j[2])
                if int(startnode)!=int(endnode):
                    coord_1_d, coord_2_d, coord_3_d = {"type": "MultiLineString", "coordinates": []}, {
                        "type": "MultiLineString",
                        "coordinates": []}, {
                                                          "type": "MultiLineString", "coordinates": []}
                    coord_all = []
                    data,pat,dis=storeCoordinates_6(startnodeX, startnodeY, endnodeX, endnodeY, cur,data,wkt,conn,startnode,endnode)
                    di=0
                    coord = ast.literal_eval(pat)
                    for iota in coord["coordinates"]:
                        for jota in iota:
                            coord_all.append(tuple(jota))
                    for io in range(len(coord_all) - 1):
                        if di < (dis / 3):
                            coord_1_d["coordinates"].append([list(coord_all[io]), list(coord_all[io + 1])])
                            di = di + haversine(coord_all[io], coord_all[io + 1])
                        elif (dis / 3) <= di < (2 * dis / 3):
                            coord_2_d["coordinates"].append([list(coord_all[io]), list(coord_all[io + 1])])
                            di = di + haversine(coord_all[io], coord_all[io + 1])

                        elif di >= (2 * dis / 3):
                            coord_3_d["coordinates"].append([list(coord_all[io]), list(coord_all[io + 1])])
                            di = di + haversine(coord_all[io], coord_all[io + 1])

                    cur.execute(
                        "INSERT INTO network_sch.wineshop_route_bi (sid_start, assetguid_start, shop_start, division_start, district_start, circle_start, shop_name_start, license_ty_start, "
                        "license_nu_start, licensee_n_start, dept_code_start, asset_loc_start, "
                        "asset_lo_1_start, mappingsta_start, asset_code_start, sid_end, "
                        "assetguid_end, shop_end, division_end, district_end, circle_end, "
                        "shop_name_end, license_ty_end, license_nu_end, licensee_n_end, "
                        "dept_code_end, asset_loc_end, asset_lo_1_end, mappingsta_end, "
                        "asset_code_end, route_1,route_2,route_3) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(
                            str(i[1]), "'" + str(i[2]) + "'", "'" + str(i[3]) + "'",
                                       "'" + str(i[4]) + "'", "'" + str(i[5]) + "'", "'" + str(i[6]) + "'",
                                       "'" + str(i[7]) + "'",
                                       "'" + str(i[8]) + "'", "'" + str(i[9]) + "'", "'" + str(i[10]) + "'",
                                       "'" + str(i[11]) + "'",
                            lon1, lat1, "'" + str(i[12]) + "'", "'" + str(i[13]) + "'",

                            str(j[1]), "'" + str(j[2]) + "'", "'" + str(j[3]) + "'",
                                       "'" + str(j[4]) + "'", "'" + str(j[5]) + "'", "'" + str(j[6]) + "'",
                                       "'" + str(j[7]) + "'",
                                       "'" + str(j[8]) + "'", "'" + str(j[9]) + "'", "'" + str(j[10]) + "'",
                                       "'" + str(j[11]) + "'",
                            j[14], j[15], "'" + str(j[12]) + "'", "'" + str(j[13]) + "'",

                                       "'" + str(json.dumps(coord_1_d)) + "'","'" + str(json.dumps(coord_2_d)) + "'","'" + str(json.dumps(coord_3_d)) + "'"))
                    conn.commit()
                    print(dis)
                else:
                    dista=haversine((startnodeX, startnodeY),(float(j[14]),float(j[15])))
                    line = ogr.Geometry(ogr.wkbLineString)
                    line.AddPoint(startnodeX, startnodeY)
                    line.AddPoint(float(j[14]),float(j[15]))
                    cur.execute(
                        "INSERT INTO network_sch.wineshop_route_bi (sid_start, assetguid_start, shop_start, division_start, "
                        "district_start, circle_start, shop_name_start, license_ty_start, license_nu_start, "
                        "licensee_n_start, dept_code_start, asset_loc_start, asset_lo_1_start, mappingsta_start, "
                        "asset_code_start, sid_end, assetguid_end, shop_end, division_end, district_end, circle_end, s"
                        "hop_name_end, license_ty_end, license_nu_end, licensee_n_end, dept_code_end, asset_loc_end, asset_lo_1_end, mappingsta_end, asset_code_end, route_1) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(
                            str(i[1]), "'" + str(i[2]) + "'", "'" + str(i[3]) + "'",
                                       "'" + str(i[4]) + "'", "'" + str(i[5]) + "'", "'" + str(i[6]) + "'",
                                       "'" + str(i[7]) + "'",
                                       "'" + str(i[8]) + "'", "'" + str(i[9]) + "'", "'" + str(i[10]) + "'",
                                       "'" + str(i[11]) + "'",
                            lon1, lat1, "'" + str(i[12]) + "'", "'" + str(i[13]) + "'",

                            str(j[1]), "'" + str(j[2]) + "'", "'" + str(j[3]) + "'",
                                       "'" + str(j[4]) + "'", "'" + str(j[5]) + "'", "'" + str(j[6]) + "'",
                                       "'" + str(j[7]) + "'",
                                       "'" + str(j[8]) + "'", "'" + str(j[9]) + "'", "'" + str(j[10]) + "'",
                                       "'" + str(j[11]) + "'",
                            j[14],j[15], "'" + str(j[12]) + "'", "'" + str(j[13]) + "'",

                                       "'" + str(line.ExportToJson()) + "'"))
                    conn.commit()
                    print(line)

            now = time.localtime(time.time())
            print(now)
            if input("press enter"):
                pass
            #routej(data, "C:/Users\shashank\Desktop\POLY", name='FINALPATH_%f_%f_%f' % (now[3], now[4], now[5]))
            #return render(request, 'wkt_data_loader.html', {'list': wkt,'point':[lon1,lat1]})