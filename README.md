# gender-detection-elastic-search-kibana-genderize
Gender study of DBLP authors by means of elasticsearch and kibana and genderize.io API for python. Dataset link: https://dblp.uni-trier.de/xml/
Readme: Elasticsearch

Una vez tenemos listos los ficheros: 
    • datos_formato_elastic.json
    • mappingPractice.json

Ejecutamos el siguiente proceso para la carga de datos a elasticsearch y kibana:

    1. Desde la Terminal levantamos elasticsearch:
~/Programas/elasticsearch-6.6.1/bin$ ./elasticsearch

    2. En una terminal nueva, creamos un índice llamado practice:
curl -XPUT -k localhost:9200/practice

    3. Consultamos el índice creado:
curl -k localhost:9200/_cat/indices

    4. Creamos el mapping a partir del fichero mappingPractice.json:

elasticdump --input=mappingPractice.json --output=http://localhost:9200 --type=mapping --output-index=practice --headers='{"Content-Type": "application/json"}'

    5. Consultamos la creación del mapping:
curl -k localhost:9200/practice/_mapping/

    6. Cargamos nuestros datos en el índice creado:
elasticdump --datos_formato_elastic.json --output=http://localhost:9200 --type=data --output-index=practice --headers='{"Content-Type": "application/json"}'

    7. Una vez recibimos la confirmación de carga completa de nuestros datos, en una terminal nueva lanzamos Kibana: 
~/Programas/kibana-6.6.1-linux-x86_64/bin$ ./kibana

    8. Abrimos el navegador y vamos a localhost:5601 y en la interfaz de Kibana creamos un nuevo Index pattern asociado a nuestro índice ‘practice’. a partir de este momento ya tenemos disponibles todos los atributos para realizar el análisis objetivo de esta práctica.
