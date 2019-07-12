#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import argparse


def read_gene(bed):
    """
    :param bed: gene bed
    :return: hash
    """
    gene_hash = {}
    with open(bed) as gene_fh:
        next(gene_fh)
        for line in gene_fh:
            record = line.strip().split("\t")
            chrom = record[0].strip("chr")
            if chrom == "23":
                chrom = "X"
            if chrom == "24":
                chrom = "Y"
            start = record[1]
            end = record[2]
            gene_name = record[3]
            key = ":".join([chrom, start, end])
            gene_hash[key] = gene_name
    return gene_hash


def cnv_anno(gene_hash, cnv):
    """
    :param gene_hash:
    :param cnv:
    :return: gene
    """
    gene_list = []
    for key in gene_hash:
        record = key.strip().split(":")
        dis_chrom = record[0]
        dis_start = int(record[1])
        dis_end = int(record[2])
        cnv_parser = re.match(r'(dup|del)\((\w+):(\d+)-(\d+)\)', cnv)
        # cnv_type = cnv_parser.group(1)
        cnv_chrom = cnv_parser.group(2)
        cnv_start = int(cnv_parser.group(3))
        cnv_end = int(cnv_parser.group(4))

        if cnv_chrom == "23":
            cnv_chrom = "X"
        if cnv_chrom == "24":
            cnv_chrom = "Y"
        # https://blog.csdn.net/mrwangweijin/article/details/76302778
        if cnv_chrom == dis_chrom:
            if max(dis_start, cnv_start) < min(dis_end, cnv_end):
                overlap = min(dis_end, cnv_end) - max(dis_start, cnv_start)
            else:
                overlap = 0
        else:
            overlap = 0

        if overlap/(dis_end-dis_start) >= 0.5:
            gene_list.append(gene_hash[key])

    if gene_list:
        return ",".join(gene_list)
    else:
        return "na"


def main(disase_hash, cnv_fh):
    """
    :param disase_hash:
    :param cnv_fh:
    :return:
    """
    for record in cnv_fh:

        anno_result = []
        for cnv in record.strip().split(";"):
            cnv_parser = re.match(r'(dup|del)\((\w+):(\d+)-(\d+)\)', cnv)
            if cnv_parser:
                gene = cnv_anno(disase_hash, cnv)
                anno_result.append(gene)
            else:
                anno_result.append("NA")

        result = ";".join(anno_result)
        print(record.strip(), result, sep="\t")


if __name__ == "__main__":
    options = argparse.ArgumentParser(description='CNV gene annotation')
    options.add_argument('-d', '--gene', default='omim.dominant.gene.bed', help='default: omim.dominant.gene.bed')
    options.add_argument('-c', '--cnv', required=True, help='CNV list')
    args = options.parse_args()

    genes = read_gene(args.gene)
    cnv_list = open(args.cnv, "r")
    main(genes, cnv_list)
