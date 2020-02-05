import sys
import argparse
from pyfaidx import Fasta
from collections import namedtuple

VCFRecord = namedtuple('VCFRecord', ("chrom", "pos", 'ref', 'alt'))


# test
'''
genome = Fasta('/data/hg19/hg19.fa')
genome.keys()
genome['chr13'][20763209-1:20763209].seq
genome['chr13'][20763209-1:20763209].name
'''


def bed2vcf(chrom, start, ref, alt):
    """
    transform bed to vcf, and complement the missing "." in ref and alt
    :param chrom:
    :param start:
    :param ref:
    :param alt:
    :return: VCFRecord
    """
    start = int(start)
    chrom = chrom.replace('chr', '')
    if ref in ['','.','-'] or alt in ['','.','-']:
        pos = start
        chrom_num = 'chr' + str(chrom)
        complement = genome[chrom_num][start-1:start].seq
        ref = (complement + ref).replace('.', '').replace('-', '')
        alt = (complement + alt).replace('.', '').replace('-', '')
    else:
        pos = start + 1
    
    return VCFRecord(chrom, pos, ref, alt)


def main():
    for line in bed_fh:
        if line.strip().startswith("##"):
            continue
        elif line.strip().startswith("#"):
            header = line.strip().split("\t")
            print("\t".join(["#CHROM", "POS", "rsID"] + header[3:]))
            header[0] = header[0].replace("#", "")
            continue
        records = line.strip('\n').split("\t")

        chrom = records[0]
        start = int(records[1])
        ref = records[3]
        alt = records[4]

        vcfrecord = bed2vcf(chrom, start, ref, alt)
        result = [vcfrecord.chrom, str(vcfrecord.pos), '-', vcfrecord.ref, vcfrecord.alt]
        result = result + records[5:]
        print("\t".join(result))


if __name__ == '__main__':
    options = argparse.ArgumentParser(description='Hearing Loss ACMG Interpretation 2018')
    options.add_argument('-b', '--bed', required=True, help='bed file chr-start-end format')

    args = options.parse_args()
    bed_fh = open(args.bed)

    genome = Fasta('/data/hg19/hg19.fa')

    main()
