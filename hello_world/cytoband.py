#!/usr/bin/env python
# -*- coding:utf-8 -*-

###############################################################################
# Name: Cytobands Coordinates Converter                                       #
#       Format conversion between cytogenetic bands and genomic coordinates   #
# Author: Jiguang Peng                                                        #
# Email: pengjiguang@genomics.cn                                              #
# Version 1.0 - 17/07/2019                                                    #
###############################################################################

import re
import argparse
from collections import namedtuple


CYTOBAND = namedtuple('CYTOBAND', ('chrom', 'start', 'end', 'name', 'giestain', 'length'))


def read_cytoband(band_file):
    """
    Read
    """
    if isinstance(band_file, str):
        band_file = open(band_file, 'r')
    band_dict = dict()
    for line in band_file:
        chrom, start, end, name, giestain = line.strip().split("\t")
        chrom, start, end = coord_unify(chrom, start, end)
        length = end - start
        band = CYTOBAND(chrom, start, end, name, giestain, length)
        create_two_dim_dict(band_dict, chrom, name, band)
    return band_dict


def coord2band(chrom, start, end, band_dict, threshold=0):
    """
    Convert Genomics Coordinates to Cytobands
    """
    chrom, start, end = coord_unify(chrom, start, end)
    start_band = end_band = ''
    for band in band_dict[chrom].values():
        if band.start <= start <= band.end and float(band.end - start) / band.length > threshold:
            start_band = band.name
        if band.start < end <= band.end and float(end - band.start) / band.length > threshold:
            end_band = band.name
    if not start_band and not end_band:
        return chrom + 'toosmall'
    elif start_band == end_band:
        return chrom + start_band
    elif 'p' in start_band and 'p' in end_band:
        return chrom + end_band + start_band
    else:
        return chrom + start_band + end_band


def band2coord(band, band_dict):
    """
    Convert Cytobands to Coordinates
    """
    pattern1 = re.compile(r'([0-9XY]+)([pq]\d+(\.\d+)?)([pq]\d+(\.\d+)?)')
    pattern2 = re.compile(r'([0-9XY]+)([pq]\d+(\.\d+)?)')
    match1 = pattern1.match(band)
    match2 = pattern2.match(band)
    if match1:
        chrom, band1, band2 = match1.group(1, 2, 4)
        if 'p' in band1 and 'p' in band2:
            start = band_dict[chrom][band2].start
            end = band_dict[chrom][band1].end
        else:
            start = band_dict[chrom][band1].start
            end = band_dict[chrom][band2].end
    elif match2:
        chrom, band = match2.group(1, 2)
        start = band_dict[chrom][band].start
        end = band_dict[chrom][band].end
    else:
        chrom, start, end = 'na', 'na', 'na'
    return chrom, start, end


def overlap(start1, end1, start2, end2):
    if max(start1, start2) < min(end1, end2):
        return min(end1, end2) - max(start1, start2)
    else:
        return 0


def coord_unify(chrom, start, end):
    """
    Genomic Coordinates Unify Tool
    """
    chrom = chrom.replace('chr', '')
    chrom = chrom.replace('23', 'X')
    chrom = chrom.replace('24', 'Y')
    chrom = chrom.replace('25', 'MT')
    if not isinstance(start, int):
        start = int(start.replace(',', ''))
    if not isinstance(end, int):
        end = int(end.replace(',', ''))
    return chrom, start, end


def create_two_dim_dict(thedict, key1, key2, value):
    """
    add two dimension dict
    """
    if key1 in thedict:
        thedict[key1].update({key2: value})
    else:
        thedict.update({key1: {key2: value}})


def main(input_fh, band_dict):
    """
    Automatic Convert
    """
    for line in input_fh:
        record = line.strip().split("\t")
        if re.search(r'([0-9XY]+)([pq]\d+(\.\d+)?)', record[-1]):
            chrom, start, end = band2coord(record[-1], band_dict)
            record.extend([chrom, str(start), str(end)])
        elif re.search(r'\d+|X|Y', record[0]) and record[1].isdigit() and record[2].isdigit():
            band = coord2band(record[0], record[1], record[2], band_dict)
            record.append(band)
        else:
            record.append('failed')
        print("\t".join(record))


# cytobands = read_cytoband('cytoBand.hg19')


if __name__ == '__main__':
    options = argparse.ArgumentParser(description='Cytobands Coordinates Converter')
    options.add_argument('-c', '--cytoband', default='cytoBand.hg19', help='cytoBand file')
    options.add_argument('-i', '--input', required=True, help='input file: bed or cytoband')

    args = options.parse_args()
    cytobands = read_cytoband(args.cytoband)
    inputfh = open(args.input, 'r')

    main(inputfh, cytobands)
