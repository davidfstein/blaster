# Docker entry
```
docker run --env-file path/to/env_file -it -v path/to/blaster/folder:/app dstein96/blaster:0.1
```

# Env File Arguments
1. build_db:
..options: true or false
..whether or not to build a blast db. If you have a prebuilt db, set to false
2. reference_fasta:
..path to the fasta file containing the reference assembly
..can leave blank if not building a db
3. blast_db_name:
..the name of the blast database against which to search 
..can leave blank if not building a db

# Perform a local blast search
```
1. alias python=/usr/bin/python3.6
2. python blaster.py -l True -p ./chrom_probes.csv -d path/to/desired_db_name/desired_db_name
3. exit (to exit the docker container)
```

# Command Line Arguments
```
python blaster.py -h
```