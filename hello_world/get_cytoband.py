import argparse
import sys
import re
sys.path.append('/home/yanxinyi/project/niftypub/nifty_xhmm/code')
import cytoband


def main(input_fh, band_dict):
    """
    Automatic Convert
    """
    for line in input_fh:
        record = line.strip().split("\t")
        if re.search(r'([0-9XY]+)([pq]\d+(\.\d+)?)', record[0]):
            chrom, start, end = band2coord(record[0], band_dict)
            record.extend([chrom, str(start), str(end)])
        elif re.search(r'\d+|X|Y', record[0]) and record[1].isdigit() and record[2].isdigit():
            band = cytoband.coord2band(record[0], record[1], record[2], band_dict)
            record.append(band)
        else:
            record.append('failed')
        print("\t".join(record))


if __name__ == '__main__':
    options = argparse.ArgumentParser(description='Cytobands Coordinates Converter')
    options.add_argument('-c', '--cytoband', default='/home/yanxinyi/project/niftypub/nifty_xhmm/code/cytoBand.hg19', help='cytoBand file')
    options.add_argument('-i', '--input', required=True, help='input file: bed or cytoband')

    args = options.parse_args()
    #cytobands = cytoband.read_cytoband(args.cytoband)
    cytobands = cytoband.read_cytoband('/home/yanxinyi/project/niftypub/nifty_xhmm/code/cytoBand.hg19')
    inputfh = open(args.input, 'r')

    main(inputfh, cytobands)
