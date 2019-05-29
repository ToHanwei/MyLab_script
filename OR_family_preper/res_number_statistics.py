# coding:utf-8

from sys import argv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

__auther__ = "Wei"
__date__ = "2019-05-07"
__email__ = "hanwei@shanghaitech.edu.cn"


def statistic(filename, isfilter=False):
	"""Statistic the number of OR sequence leng"""
	seq_dict = defaultdict(int)
	seqout = open("proteins-matched-confirm-lengfilter.txt", 'w')
	with open(filename, 'r') as resread:
		seqs = resread.read()[1:].split("\n>")
	total, reslist = 0, []
	for seq in seqs:
		lines = seq.split("\n")
		value = ""
		for line in lines[1:]:
			value += line
		seq_dict[len(value)] += 1
		total += 1
		reslist.append(len(value))
		if isfilter and isfilter[0]<=len(value)<=isfilter[1]:
			seqout.write(">"+seq+"\n")
	return seq_dict, total, reslist

def section(Dict, u, total):
	"""Number section statisitic"""
	out = open("Section_statistic.txt", 'w')
	keys = sorted(Dict.keys())
	center = keys.index(u)
	i, SUM = 0, Dict[u]
	out.write("[%d %d]\t%d\t%.3f\n" % (u, u, SUM,  SUM/total))
	while True:
		i += 1
		try:
			p = keys[center - i]
			l = keys[center + i]
			if center-i <= 0: break
		except IndexError as e:
			break
		SUM += Dict[p]
		SUM += Dict[l]
		out.write("[%d %d]\t%d\t%.3f\n" % (p, l, SUM, SUM/total))
		if SUM/total >= 0.8: break
	out.close()
	

def PlotFig(List, Type="show"):
	"""Plot Figure"""
	#y = np.arange(0, 0.052, 0.001)
	#x1 = [260] * 52
	#x2 = [360] * 52
	#plt.plot(x1, y, c='r')
	#plt.plot(x2, y, c='r')
	plt.hist(List, 500, density=True)
	plt.xlabel("Leng of sequence")
	plt.ylabel("Probability")
	plt.title("Numer of OR sequences")
	#plt.grid(True)
	#plt.text(100, 0.051, 260)
	#plt.text(350, 0.051, 360)
	if Type == "show":
		plt.show()
	elif Type == "save":
		fig = plt.gcf()
		fig.savefig("./Number of OR.png", dpi=200)
	else:
		print("No show, No save")


def main():
	"""Main function, Run the script"""
	filename = argv[1]
	seq_dict, total, reslist = statistic(filename, (290, 330))
	section(seq_dict, 310, total)
	PlotFig(reslist, 'save')


if __name__ == "__main__":
	main()	


