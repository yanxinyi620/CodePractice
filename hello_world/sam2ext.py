import sys
import re
input=sys.argv[1]
out=sys.argv[2]

a = list(map(str, range(1,23)))
chrlen = ['chr'+i for i in a]+['chrX','xhrY','chrM']

f1 = open(out,'w')
for i in open(input):
	a = i.strip().split('\t')
	
	if len(bin(int(a[1],10))[2:])>=5 and bin(int(a[1],10))[-5]=='1' and (a[2] in chrlen):
		b = 'R'
		c = a[9]
		d = '35'
		e = trans35(a[6])
		
		if a[1]=='chrY' or abs(int(readlen))<chrlen[a[1]]:
			f1.write('\t'.join(a[1:7])+'\t'+readlen+'\tS\n')
		else:
			f1.write('\t'.join(a[1:7])+'\t'+readlen+'\tL\n')
	elif len(bin(int(a[3],10))[2:])>=6 and bin(int(a[3],10))[-6]=='1' and bin(int(a[3],10))[-5]=='0' and (a[1] in chrlen):
		a[3] = 'F'
		a[4] = a[4][0:35]
		a[5] = '35'
		a[6] = trans35(a[6])
		
		if a[1]=='chrY' or abs(int(readlen))<chrlen[a[1]]:
			f1.write('\t'.join(a[1:7])+'\t'+readlen+'\tS\n')
		else:
			f1.write('\t'.join(a[1:7])+'\t'+readlen+'\tL\n')
f1.close()
