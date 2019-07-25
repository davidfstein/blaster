# Install Dependencies
```
pip install -r requirements.txt
```
## Install the Blast command line tools
```
ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.18/ncbi-blast-2.2.18+.dmg
```
Follow installation instructions. 

# Running Locally
## Build a Blast Database
```
makeblastdb -in path/to/assembly/fasta -dbtype nucl -parse_seqids -title desired_db_name -out desired_db_name
```
Put the outputted files into a folder called *desired_db_name*.
Here is an example query:
```
python blaster.py -l True -p ./chrom_probes.csv -d path/desired_db_name/desired_db_name
```

# Command Line Arguments
```
python blaster.py -h
```