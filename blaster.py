from Bio.Blast import NCBIWWW
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastnCommandline
from argparse import ArgumentParser
import csv

def has_header(csv_lines):
    if not csv_lines:
        raise Exception("The csv is empty.")
    first_line = csv_lines[0]
    return isinstance(first_line[0], str)

def read_probes(probe_csv, probe_column, off_target_column):
    with open(probe_csv) as file:
        lines = csv.reader(file)
        lines = [list(line) for line in lines]
        if has_header(lines):
            lines = lines[1:]
        lines = filter_good_probes(lines, off_target_column)
        return lines[0][0], [line[probe_column] for line in lines]

def filter_good_probes(probe_data, off_target_column):
    filtered_probe_data = [probe_d for probe_d in probe_data if probe_d[off_target_column].strip() != "None"]
    return filtered_probe_data
    
def blast_sequence(gene_of_interest, seq, database_name, program='blastn', entrez="('none')", num_results=5, word_size=7, expect=.001, url='https://blast.ncbi.nlm.nih.gov/Blast.cgi'):
    result = NCBIWWW.qblast(program, database=database_name, sequence=seq, entrez_query=entrez, alignments=num_results, hitlist_size=num_results, word_size=word_size, expect=expect, url_base=url)
    records = NCBIXML.parse(result)
    return parse_results(gene_of_interest, records)

def parse_results(gene_of_interest, records):
    blast_output = []
    for record in records:
        for i in range(0, len(record.alignments)):
            if i < len(record.alignments):
                alignment = record.alignments[i]
                if i < len(alignment.hsps):
                    hsp = alignment.hsps[i]
                    blast_output.append([gene_of_interest, hsp.query, hsp.sbjct, alignment.title, hsp.expect])
    return blast_output

def blast_local(gene_id, database_name, seqs, num_results=5, word_size=7, e_value=.001):
    blastn_cline = NcbiblastnCommandline(query=seqs, db=database_name, outfmt=5, num_alignments=num_results, word_size=word_size, evalue=e_value, out=gene_id + ".xml")
    stdout, stderr = blastn_cline()
    with open(gene_id + '.xml') as results:
        records = NCBIXML.parse(results)
        parsed = parse_results(gene_id, records)
        return parsed

def write_probe_fasta(gene_id, probes):
    with open(gene_id + '.fa', 'w+') as probe_fasta:
        for i in range(0, len(probes)):
            probe_fasta.write('>' + gene_id + str(i) + '\n')
            probe_fasta.write(probes[i].strip().strip("'").rstrip("'") + '\n')

def write_output(gene_id, output):
    with open(gene_id + '_blast.csv', 'w+') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Gene of Interest', 'Query Sequence', 'Match Sequence', 'Alignment Id', 'e Value'])
        for record in output:
            writer.writerow(record)

if __name__ == '__main__':

    userInput = ArgumentParser(description="Facilitates blasting sequences against an NCBI blast configured server.")
    requiredNamed = userInput.add_argument_group('required arguments')
    requiredNamed.add_argument('-l', '--Local', action='store', required=True,
                                help='Local or remote blast. True=local, False=remote.')
    requiredNamed.add_argument('-p', '--Path', action='store', required=True,
                                help='Path to sequence file.')
    requiredNamed.add_argument('-d', '--DatabaseName', action='store', required=True,
                                help="The database against which to blast the sequence.")
    optionalNamed = userInput.add_argument_group('optional arguments')
    optionalNamed.add_argument('-c', '--Column', action='store', required=False,
                                default=7 ,help="The column containing the sequences to be blasted.")
    optionalNamed.add_argument('--OffTargetColumn', action='store', required=False,
                                default=15, help="The column containing the off target alignment value.")
    optionalNamed.add_argument('-e', '--EntrezQuery', action='store', required=False,
                                default='(none)', help="Entrez query to be included in search.")
    optionalNamed.add_argument('-pn', '--ProgramName', action='store', required=False,
                                default='blastn', help="The blast program to use (e.g. blastn).")
    optionalNamed.add_argument('-n', '--NumResults', action='store', required=False,
                                default=5, help="Number of hits to return.")
    optionalNamed.add_argument('-w', '--WordSize', action='store', required=False,
                                default=7, help="Word size in blast search.")
    optionalNamed.add_argument('-ex', '--ExpectValue', action='store', required=False,
                                default=0.001, help="Expect value cutoff.")
    optionalNamed.add_argument('-u', '--URLBase', action='store', required=False,
                                default='https://blast.ncbi.nlm.nih.gov/Blast.cgi', help="Url of blast server to use.")
    args = userInput.parse_args()
    local = args.Local
    path = args.Path
    column = int(args.Column)
    database = args.DatabaseName
    program = args.ProgramName
    entrez_query = args.EntrezQuery
    num_results = int(args.NumResults)
    word_size = int(args.WordSize)
    e_value = float(args.ExpectValue)
    off_target_column = int(args.OffTargetColumn)
    url = args.URLBase

    gene_id, probes = read_probes(path, column, off_target_column)
    gene_id = gene_id.strip("'").rstrip("'")

    if local.lower() == 'false':
        for probe in probes:
            output = blast_sequence(gene_id, probe, database, program, entrez_query, num_results, word_size, e_value, url)
            write_output(gene_id, output)
    else:
        write_probe_fasta(gene_id, probes)
        output = blast_local(gene_id, database, gene_id + '.fa', num_results, word_size, e_value)
        write_output(gene_id, output)
    
