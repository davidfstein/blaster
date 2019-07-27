#!/usr/bin/env bash

mkdir $2
mv $1 ./$2
cd $2
makeblastdb -in $1 -dbtype nucl -parse_seqids -title $2 -out $2

