#!/bin/sh
python2 LightHouse_1_1.py -i URL.csv -b ${BUILD_NUMBER}
docker cp /report/lighthouse.csv /opt/aptsac/jmeter/workspace/report
