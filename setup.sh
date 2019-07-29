#!/usr/bin/env bash

/usr/bin/python3.6 -m pip install biopython 

if [ "$3" = "true" ]; then  
    mkdir $2
    mv $1 ./$2
    cd $2
    makeblastdb -in $1 -dbtype nucl -parse_seqids -title $2 -out $2
fi