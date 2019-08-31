# gender-detection-elastic-search-kibana-genderize
Gender study of DBLP authors by means of elasticsearch and kibana and genderize.io API for python. Dataset link: https://dblp.uni-trier.de/xml/

Start Elasticsearch:

~/Programas/elasticsearch-6.6.1/bin$ ./elasticsearch

Create index named practice:

curl -XPUT -k localhost:9200/practice

View created index:

curl -k localhost:9200/_cat/indices

Create a mapping based on mappingPRactice.json file:

elasticdump --input=mappingPractice.json --output=http://localhost:9200 --type=mapping --output-index=practice --headers='{"Content-Type": "application/json"}'

View the created mapping:

curl -k localhost:9200/practice/_mapping/

Load the data:

elasticdump --datos_formato_elastic.json --output=http://localhost:9200 --type=data --output-index=practice --headers='{"Content-Type": "application/json"}'

Start Kibana:

~/Programas/kibana-6.6.1-linux-x86_64/bin$ ./kibana

Open a browser and load localhost:5601. Create a new index pattern assotiated to our index practice and from now on we have the available attributes to start gender analysis.
