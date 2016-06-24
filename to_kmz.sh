#!/bin/sh

# more for recollection than anything else --

# source shapefile is UTM zone 10m, NAD83
ogr2ogr -s_srs EPSG:26910 -t_srs EPSG:4326 -f KML -overwrite SFEI_SSFB_fo.kml SFEI_SSFB_fo.shp 
zip SFEI_SSFB_fo.kml.zip SFEI_SSFB_fo.kml
mv SFEI_SSFB_fo.kml.zip SFEI_SSFB_fo.kmz
