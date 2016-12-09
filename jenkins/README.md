Jenkins
=======

## Prepare

Get the current configuration and save it locally
curl -X GET http://user:password@hudson.server.org/job/myjobname/config.xml -o mylocalconfig.xml
 
Update the configuration via posting a local configuration file
curl -X POST http://user:password@hudson.server.org/job/myjobname/config.xml --data-binary "@mymodifiedlocalconfig.xml"
 
Creating a new job via posting a local configuration file
curl -X POST "http://user:password@hudson.server.org/createItem?name=newjobname" --data-binary "@newconfig.xml" -H "Content-Type: text/xml"

Install plugin
curl -X POST -d '<jenkins><install plugin="git@2.0" /></jenkins>' --header 'Content-Type: text/xml' http://localhost:8080/pluginManager/installNecessaryPlugins
