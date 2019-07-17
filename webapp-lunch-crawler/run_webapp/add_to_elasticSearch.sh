#!/bin/bash
for filename in menu/*.json; do
	curl -H 'Content-Type: application/json' -XPOST 'localhost:9200/restaurants/_doc' --data-binary @$filename
done
