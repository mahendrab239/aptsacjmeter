#!/bin/sh
python2 LightHouse_1_1.py -i URL.csv -b ${BUILD_NUMBER}
cat lighthouse.csv >> /opt/aptsac/jmeter/workspace/report/lighthouse.csv
echo $WORKSPACE
mv lighthouse.csv ../results/lighthouse_${BUILD_NUMBER}.csv
