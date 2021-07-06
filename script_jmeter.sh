cp /opt/jmeter/bin/sharedfolder/Script/jmeter.properties /opt/jmeter/bin/
/opt/jmeter/bin/jmeter -Juser=${Users} -Jduration=${Duration} -n -t /opt/jmeter/bin/sharedfolder/Script/apts_demo.jmx -l /opt/jmeter/bin/sharedfolder/Report/validation.jtl -JBUILD_NUMBER=${BUILD_NUMBER}
cp /opt/jmeter/bin/sharedfolder/Report/validation.jtl /opt/jmeter/bin/Results/${PROJECT_NAME}_${BUILD_NUMBER}.jtl
