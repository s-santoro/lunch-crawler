#!/bin/bash
ls Testdata_raw/Official_Testdata/Output/ | sort -R | head -500 | while read file; do
	cp Testdata_raw/Official_Testdata/Output/$file files
done



#for (( i=1; i<=500; ++i))
#do
#	echo $i
#done
