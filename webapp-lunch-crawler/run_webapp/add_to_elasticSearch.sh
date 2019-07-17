#!/bin/bash
curl -XPUT http://localhost:9200/restaurants
for filename in data_for_elasticsearch/out/*.json; do
	curl -H 'Content-Type: application/json' -XPOST 'localhost:9200/restaurants/_doc' --data-binary @$filename
done
