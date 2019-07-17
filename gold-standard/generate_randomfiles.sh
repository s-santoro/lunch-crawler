#!/bin/bash
ls Output/ | sort -R | head -$1 | while read file; do
	cp Output/$file files
done
