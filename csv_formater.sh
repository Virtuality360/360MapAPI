#!/bin/bash

# Create spinner
spin() {
    spinner="/|\\-/|\\-"
    while :
    do
        for i in `seq 0 7`
        do
            echo -n "${spinner:$i:1}"
            echo -en "\010"
            sleep 0.5
        done
    done
}

# Enable spinner
spin & SPIN_PID=$!
trap "kill -9 $SPIN_PID" `seq 0 15`

clear

# postgres --> csv

echo "Reprojecting the data ... can take a few minutes"
time ogr2ogr -f CSV -lco GEOMETRY=AS_XY -select longitude,latitude,mcc,mnc,lac,cid -s_srs EPSG:4269 -t_srs EPSG:3857 -oo X_POSSIBLE_NAMES=longitude -oo Y_POSSIBLE_NAMES=latitude data/gsm_qp_web_mercator.csv data/gsm_qp_raw.csv


cat data/gsm_qp_web_mercator.csv |  sed 's/"//g' > data/gsm_qp_web_mercator_int.csv
#echo "Cleaning up"
#rm data/gsm_qp_raw.csv 2>/dev/null

# Kill the spinner
kill -9 $SPIN_PID

echo "Done"