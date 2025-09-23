# Import Libraries
import geopandas as gpd
import shapely
from shapely.geometry import Polygon, LineString, Point

# Load Chile OSM
gdf = gpd.read_file("chile-latest.osm.pbf",
                    layer="lines",
                    engine="pyogrio",
                    use_arrow=True)

# Define resolution for map chunks
d_lat = 0.006386316
d_lon = 0.012574627

# Define bounding box for whole map
lon_min = -70.659651347
lon_max = -70.559012583
lat_min = -33.469000293
lat_max = -33.404207483
box = Polygon([(lon_max,
                lat_max),
               (lon_max,
                lat_min),
               (lon_min,
                lat_min),
               (lon_min,
                lat_max),
               (lon_max,
                lat_max)])

# Get bounded region from maps
santiago = gdf.copy()
santiago.geometry = gdf.intersection(box)
santiago = santiago[~santiago.geometry.is_empty]

# Test and show zone
m = santiago[(~santiago.highway.isna()) &
             (santiago.highway != 'footway')].explore()
m.save("box.html")

# Divide zone into chunks 
N_lon = int((lon_max-lon_min)/d_lon)
N_lat = int((lat_max-lat_min)/d_lat)

def fix_len(l):
    if len(l) > 7:
        return l[0:7]
    elif len(l) == 7:
        return l
    else:
        return fix_len(l+"0")

# i=5
# j=3
# divide
for i in range(N_lon):
    for j in range(N_lat):
        lon_min_d = lon_min + i*d_lon
        lon_max_d = lon_min + (i+1)*d_lon
        lat_min_d = lat_min + j*d_lat
        lat_max_d = lat_min + (j+1)*d_lat
        b = Polygon([(lon_max_d, lat_max_d),
                     (lon_max_d, lat_min_d),
                     (lon_min_d, lat_min_d),
                     (lon_min_d, lat_max_d),
                     (lon_max_d, lat_max_d)])
        chunk = santiago.copy()
        chunk.geometry = chunk.intersection(b)
        chunk = chunk[~chunk.geometry.is_empty]
        chunk = chunk[(~chunk.highway.isna()) & (chunk.highway != 'footway') & (chunk.geometry.type == 'LineString')]
        Z_lon = chunk.geometry.map(lambda x: x.xy[0])
        Z_lat = chunk.geometry.map(lambda x: x.xy[1])

        Z_lon = Z_lon.map(lambda x: list(map(lambda y: str(y).replace("-","").replace(".", ""),x)))
        Z_lat = Z_lat.map(lambda x: list(map(lambda y: str(y).replace("-","").replace(".", ""),x)))

        Z_lon= Z_lon.map(lambda x: list(map(fix_len, x)))
        Z_lat= Z_lat.map(lambda x: list(map(fix_len, x)))
        
        # write MAPS
        # with open('map_test/maps2.h', 'a') as f:
        #     for k in range(len(Z_lon)):
        #         f.write(f"long lat_{i}_{j}_{k}[{len(Z_lon.iloc[k])}] = "+"{"+str(Z_lat.iloc[k]).replace("[","").replace("]","").replace("'","")+"};\n")
        #         f.write(f"long lon_{i}_{j}_{k}[{len(Z_lon.iloc[k])}] = "+"{"+str(Z_lon.iloc[k]).replace("[","").replace("]","").replace("'","")+"};\n")
        #     f.write("\n")
        #     f.write(f"COORDS map_lon_{i}_{j}[] ="+"{\n")
        #     for k in range(len(Z_lon)):
        #         f.write("{"+f"lon_{i}_{j}_{k},"+str(len(Z_lat.iloc[k]))+"},"+"\n")
        #     f.write("};\n")
        #     f.write(f"COORDS map_lat_{i}_{j}[] ="+"{\n")
        #     for k in range(len(Z_lon)):
        #         f.write("{"+f"lat_{i}_{j}_{k},"+str(len(Z_lon.iloc[k]))+"},"+"\n")
        #     f.write("};\n")
        
        # write CHUNKS
        with open("map_test\chunks.h",'a') as f:
            f.write( "{"+
                    f"map_lon_{i}_{j}, map_lat_{i}_{j}, {len(Z_lon)}, "+
                    fix_len(str(lon_min_d).replace("-","").replace(".",""))+", "+
                    fix_len(str(lon_max_d).replace("-","").replace(".",""))+", "+
                    fix_len(str(lat_min_d).replace("-","").replace(".",""))+", "+
                    fix_len(str(lat_max_d).replace("-","").replace(".",""))+
                    "},\n")
        # print(len(chunk), f"_{i}_{j}")
        
        # m = .explore()
        # m.save(f"chunks/box_{i}_{j}.html")
        
def map_a(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  
def which_chunk(lat, lon):
    a = map_a(lon,lon_min,lon_max,0,N_lon-1)
    b = map_a(lat,lat_min,lat_max,0,N_lat-1)
    return (int(a),int(b))

which_chunk(-33.4317298,-70.6114102)
which_chunk(-33.4255137,-70.6329901)
which_chunk(lat_min,lon_min)

for i in range(N_lon):
    for j in range(N_lat):
        lon_min_d = lon_min + i*d_lon
        lon_max_d = lon_min + (i+1)*d_lon
        lat_min_d = lat_min + j*d_lat
        lat_max_d = lat_min + (j+1)*d_lat
        
        print(fix_len(str(lat_min).replace("-","").replace(".","")))
        print(fix_len(str(lat_max).replace("-","").replace(".","")))
        print(fix_len(str(lon_min).replace("-","").replace(".","")))
        print(fix_len(str(lon_max).replace("-","").replace(".","")))
        
for i in range(N_lon):
    for j in range(N_lat):
        print( f"else if (i == {i} and j == {j})"+"{")
        print(f"m = map_lon_{i}_{j};")
        print("}")

print("CHUNK maps[] = {")
for i in range(N_lon):
    for j in range(N_lat):
        print( "{"+f"map_lon_{i}_{j}, map_lat_{i}_{j}, 128" +"},")
        
# {map_lon_0_0, map_lat_0_0, 128}

box_lon_min = -70.62192;
box_lon_max = -70.57162;
box_lat_min = -33.44345;
box_lat_max = -33.40513;

(-70.5790919 - box_lon_min) * (3 - 0) / (box_lon_max - box_lon_min) + 0

(-70.611153 - box_lon_min) * (4 - 0) / (box_lon_max - box_lon_min) + 0
(-33.431480 - box_lat_min) * (6 - 0) / (box_lat_max - box_lat_min) + 0