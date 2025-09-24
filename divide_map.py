# Import Libraries
import geopandas as gpd
from shapely.geometry import Polygon, LineString, Point
import os.path

# Load Chile OSM
gdf = gpd.read_file("chile-latest.osm.pbf",
                    layer="lines",
                    engine="pyogrio",
                    use_arrow=True)

# Define resolution for map chunks
d_lat = 0.006386316
d_lon = 0.012574627
# Define how many chunks per direction
n_lat = 7
n_lon = 6

# Define bounding box for whole map

# Eliodoro Yañez
# lon_min = -70.659651347
# lat_min = -33.469000293

# Paranal
lon_min = -70.459651347
lat_min = -24.669000293

lon_max = lon_min+d_lon*n_lon
lat_max = lat_min+d_lat*n_lat

box = Polygon( [(lon_max, lat_max),
                (lon_max, lat_min),
                (lon_min, lat_min),
                (lon_min,lat_max),
                (lon_max,lat_max)])

# Get bounded region from map
santiago = gdf.copy()
santiago.geometry = gdf.intersection(box)
santiago = santiago[~santiago.geometry.is_empty]

# Test and show zone
m = santiago[(~santiago.highway.isna()) & (santiago.highway != 'footway')].explore()
m.save("box.html")

# fix length of long integers
def fix_len(l):
    if len(l) > 7:
        return l[0:7]
    elif len(l) == 7:
        return l
    else:
        return fix_len(l+"0")
    
# prepare file
with open('map_test/chunks.h', 'a') as f:
    f.write(f'int n_lat = {n_lat};\n')
    f.write(f'int n_lon = {n_lon};\n')
    f.write(f'double d_lat = {d_lat};\n')
    f.write(f'double d_lon = {d_lon};\n')
    f.write(f'double box_lon_min = {lon_min};\n')
    f.write(f'double box_lon_max = {lon_max};\n')
    f.write(f'double box_lat_min = {lat_min};\n')
    f.write(f'double box_lat_max = {lat_max};\n')
    f.write('CHUNK maps[] = {\n')

# divide
for i in range(n_lon):
    for j in range(n_lat):
        # getting coordinates for the chunk
        lon_min_d = lon_min + i*d_lon
        lon_max_d = lon_min + (i+1)*d_lon
        lat_min_d = lat_min + j*d_lat
        lat_max_d = lat_min + (j+1)*d_lat
        # defining poligon for the chunk
        b = Polygon([(lon_max_d, lat_max_d),
                     (lon_max_d, lat_min_d),
                     (lon_min_d, lat_min_d),
                     (lon_min_d, lat_max_d),
                     (lon_max_d, lat_max_d)])
        
        # chunking the chunk
        chunk = santiago.copy()
        chunk.geometry = chunk.intersection(b)
        
        # filtering the chunk
        chunk = chunk[~chunk.geometry.is_empty]
        chunk = chunk[(~chunk.highway.isna()) & (chunk.highway != 'footway') & (chunk.geometry.type == 'LineString')]
        
        # formatting coordinates to save in file
        Z_lon = chunk.geometry.map(lambda x: x.xy[0])
        Z_lat = chunk.geometry.map(lambda x: x.xy[1])

        Z_lon = Z_lon.map(lambda x: list(map(lambda y: str(y).replace("-","").replace(".", ""),x)))
        Z_lat = Z_lat.map(lambda x: list(map(lambda y: str(y).replace("-","").replace(".", ""),x)))

        Z_lon= Z_lon.map(lambda x: list(map(fix_len, x)))
        Z_lat= Z_lat.map(lambda x: list(map(fix_len, x)))
        
        # write MAPS
        with open('map_test/maps.h', 'a') as f:
            for k in range(len(Z_lon)):
                f.write(f"long lat_{i}_{j}_{k}[{len(Z_lon.iloc[k])}] = "+"{"+str(Z_lat.iloc[k]).replace("[","").replace("]","").replace("'","")+"};\n")
                f.write(f"long lon_{i}_{j}_{k}[{len(Z_lon.iloc[k])}] = "+"{"+str(Z_lon.iloc[k]).replace("[","").replace("]","").replace("'","")+"};\n")
            f.write("\n")
            f.write(f"COORDS map_lon_{i}_{j}[] ="+"{\n")
            for k in range(len(Z_lon)):
                f.write("{"+f"lon_{i}_{j}_{k},"+str(len(Z_lat.iloc[k]))+"},"+"\n")
            f.write("};\n")
            f.write(f"COORDS map_lat_{i}_{j}[] ="+"{\n")
            for k in range(len(Z_lon)):
                f.write("{"+f"lat_{i}_{j}_{k},"+str(len(Z_lon.iloc[k]))+"},"+"\n")
            f.write("};\n\n")
        
        # write CHUNKS
        with open("map_test/chunks.h",'a') as f:
            f.write( "{"+
                    f"map_lon_{i}_{j}, map_lat_{i}_{j}, {len(Z_lon)}, "+
                    fix_len(str(lon_min_d).replace("-","").replace(".",""))+", "+
                    fix_len(str(lon_max_d).replace("-","").replace(".",""))+", "+
                    fix_len(str(lat_min_d).replace("-","").replace(".",""))+", "+
                    fix_len(str(lat_max_d).replace("-","").replace(".",""))+
                    "},\n")
        # print(len(chunk), f"_{i}_{j}")
        
        # m = chunk.explore()
        # m.save(f"chunks/box_{i}_{j}.html")

# end chunk file
with open('map_test/chunks.h', 'a') as f:
    f.write('};\n')
    
## TESTING ##        

def map_a(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  
def which_chunk(lat, lon):
    a = map_a(lon,lon_min,lon_max,0,n_lon)
    b = map_a(lat,lat_min,lat_max,0,n_lat)
    return (a,b,a*n_lon+b)

which_chunk(-33.4317298,-70.6114102)
which_chunk(-33.4255137,-70.6329901)
which_chunk(-24.640463, -70.388875)
which_chunk(-24.6407791,-70.38854)
which_chunk(lat_min,lon_min)

for i in range(n_lon):
    for j in range(n_lat):
        lon_min_d = lon_min + i*d_lon
        lon_max_d = lon_min + (i+1)*d_lon
        lat_min_d = lat_min + j*d_lat
        lat_max_d = lat_min + (j+1)*d_lat
        
        print(fix_len(str(lat_min).replace("-","").replace(".","")))
        print(fix_len(str(lat_max).replace("-","").replace(".","")))
        print(fix_len(str(lon_min).replace("-","").replace(".","")))
        print(fix_len(str(lon_max).replace("-","").replace(".","")))
        
for i in range(n_lon):
    for j in range(n_lat):
        print( f"else if (i == {i} and j == {j})"+"{")
        print(f"m = map_lon_{i}_{j};")
        print("}")

print("CHUNK maps[] = {")
for i in range(n_lon):
    for j in range(n_lat):
        print( "{"+f"map_lon_{i}_{j}, map_lat_{i}_{j}, 128" +"},")
        
# {map_lon_0_0, map_lat_0_0, 128}

box_lon_min = -70.62192;
box_lon_max = -70.57162;
box_lat_min = -33.44345;
box_lat_max = -33.40513;

(-70.5790919 - box_lon_min) * (3 - 0) / (box_lon_max - box_lon_min) + 0
(-70.611153 - box_lon_min) * (4 - 0) / (box_lon_max - box_lon_min) + 0
(-33.431480 - box_lat_min) * (6 - 0) / (box_lat_max - box_lat_min) + 0

# lon_min_d = lon_min + 3*d_lon
# lon_max_d = lon_min + (3+1)*d_lon
# lat_min_d = lat_min + 4*d_lat
# lat_max_d = lat_min + (4+1)*d_lat
# b = Polygon([(lon_max_d, lat_max_d),
#                 (lon_max_d, lat_min_d),
#                 (lon_min_d, lat_min_d),
#                 (lon_min_d, lat_max_d),
#                 (lon_max_d, lat_max_d)])
# chunk = santiago.copy()
# chunk.geometry = chunk.intersection(b)
# chunk = chunk[~chunk.geometry.is_empty]
# chunk = chunk[(~chunk.highway.isna()) & (chunk.highway != 'footway') & (chunk.geometry.type == 'LineString')]
# chunk.explore().save("chunk.html")