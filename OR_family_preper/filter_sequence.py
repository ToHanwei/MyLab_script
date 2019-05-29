# coding: utf-8

import pandas as pd
from sys import argv
import argparse


__auther__ = "Wei"
__date__ = "2019-05-06"
__email__ = "hanwei@shanghaitech.edu.cn"


def Command_line():
	"""Parse command line."""
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", help="input filename, sequences file")
	parser.add_argument("-e", "--excel", help="input filename, excel file")
	parser.add_argument("-o", "--output", help="output filename")
	args = parser.parse_args()
	return args


def Information(excel):
	"""Analyse information of excel file"""
	fil = []
	namelist = ["Uncharacterized", "Putative", "Ubiquilin-like"]
	namelist = [element.upper() for element in namelist]
	info = pd.read_excel(excel, index_col=0)
	seqtype = info['Protein name'].apply(lambda x: str(x).split()[0])
	for line in seqtype.values:
		if line.upper() in namelist:
			fil.append(False)
		else:
			fil.append(True)
	info = info[fil]
	return info["Accession"].values


def Filter_seq(seqfile, outfile, acces):
	"""Filter sequences depandend on accesion"""
	out = open(outfile, "w")
	with open(seqfile, 'r') as seqopen:
		seqreads = seqopen.read()[1:].split("\n>")
	for seq in seqreads:
		if seq.split("\n")[0] in acces:
			out.write(">"+seq+"\n")
	out.close()


def main():
	args = Command_line()
	excel = args.excel
	seqfile = args.input
	outfile = args.output
	acces = Information(excel)
	Filter_seq(seqfile, outfile, acces)
	


if __name__ == "__main__":
	main()
