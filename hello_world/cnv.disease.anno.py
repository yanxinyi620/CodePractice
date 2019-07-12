#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import argparse


def read_disease(bed):
    """
    :param bed: disease bed
    :return: hash
    """
    disease_hash = {}
    with open(bed) as disease_fh:
        next(disease_fh)
        for line in disease_fh:
            record = line.strip().split("\t")
            chrom = record[0]
            if chrom == "23":
                chrom = "X"
            if chrom == "24":
                chrom = "Y"
            start = record[1]
            end = record[2]
            cnvtype = record[3]
            # length = record[4]
            disease_name = record[5]
            key = ":".join([chrom, start, end, cnvtype])
            disease_hash[key] = disease_name
    return disease_hash


def cnv_anno(disease_hash, cnv):
    """
    :param disease_hash:
    :param cnv:
    :return: disease
    """
    disease_list = []
    overlap_list = []
    for key in disease_hash:
        record = key.strip().split(":")
        dis_chrom = record[0]
        dis_start = int(record[1])
        dis_end = int(record[2])
        dis_type = record[3]
        cnv_parser = re.match(r'(dup|del)\((\w+):(\d+)-(\d+)\)', cnv)
        cnv_type = cnv_parser.group(1)
        cnv_chrom = cnv_parser.group(2)
        cnv_start = int(cnv_parser.group(3))
        cnv_end = int(cnv_parser.group(4))

        if cnv_chrom == "23":
            cnv_chrom = "X"
        if cnv_chrom == "24":
            cnv_chrom = "Y"
        # https://blog.csdn.net/mrwangweijin/article/details/76302778
        if cnv_chrom == dis_chrom and cnv_type == dis_type:
            if max(dis_start, cnv_start) < min(dis_end, cnv_end):
                overlap = min(dis_end, cnv_end) - max(dis_start, cnv_start)
            else:
                overlap = 0
        else:
            overlap = 0

        if overlap >= 100000 or overlap/(dis_end-dis_start) >= 0.5:
            disease_list.append(disease_hash[key])
            if overlap < 1000000:
                overlap_list.append(str(int(overlap / 1000)) + "Kb")
            else:
                overlap_list.append(str("%.2f" % (overlap / 1000000)) + "Mb")

    if disease_list:
        return "+".join(disease_list), "+".join(overlap_list)
    else:
        return "na", "na"


def main(disase_hash, cnv_fh):
    """
    :param disase_hash:
    :param cnv_fh:
    :return:
    """
    for record in cnv_fh:

        anno_result = []
        anno_overlap = []
        for cnv in record.strip().split(";"):
            cnv_parser = re.match(r'(dup|del)\((\w+):(\d+)-(\d+)\)', cnv)
            if cnv_parser:
                disease, overlap = cnv_anno(disase_hash, cnv)
                anno_result.append(disease)
                anno_overlap.append(overlap)
            else:
                anno_result.append("NA")
                anno_overlap.append("NA")

        result = ";".join(anno_result)
        overlap = ";".join(anno_overlap)
        print(record.strip(), result, overlap, sep="\t")


if __name__ == "__main__":
    options = argparse.ArgumentParser(description='CNV disease annotation')
    options.add_argument('-d', '--disease', default='disease.bed', help='default: disease.bed')
    options.add_argument('-c', '--cnv', required=True, help='CNV list')
    args = options.parse_args()

    diseases = read_disease(args.disease)
    cnv_list = open(args.cnv, "r")
    main(diseases, cnv_list)