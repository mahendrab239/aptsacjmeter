#!/bin/sh
python2 LightHouse_1_1.py -i URL.csv -b ${BUILD_NUMBER}
cp /report/lighthouse.csv /usr/tmp/lighthouse.csv
mv /report/lighthouse.csv /usr/tmp/lighthouse_${BUILD_NUMBER}.csv
