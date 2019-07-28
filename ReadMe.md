# Docker entry
```
docker run --env-file path/to/env_file -it -v path/to/blaster/folder:/app dstein96/blaster:0.1
```

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