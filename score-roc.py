import sys

with open(sys.argv[1]) as f:
	lines = f.readlines()
lines = [l.strip() for l in lines]
clusters = {}

allind = []
for l in lines:
	k = l.split()[1]
	ind = l.split()[0]
	allind.append(l.split()[0])
	if not ind in clusters.keys():
		clusters[ind] = k
	else:
		clusters[ind].append(k)

with open(sys.argv[2]) as f:
	lines = f.readlines()
lines = [l.strip() for l in lines]
trueclusters = {}


for l in lines:
	k = l.split()[1]
	ind = l.split()[0]
	if not ind in trueclusters.keys():
		trueclusters[ind] = k
	else:
		trueclusters[ind].append(k)

tp, tn,fp,fn = 0,0,0,0
for aa in allind:
	for bb in allind:
		if aa!= bb:
			if clusters[aa] == clusters[bb]:
				if trueclusters[aa] == trueclusters[bb]:
					tp += 1
				else:
					fp += 1
			elif clusters[aa] != clusters[bb]:
				if trueclusters[aa] != trueclusters[bb] :
					tn += 1
				else:
					fn += 1

n = len(allind)*(len(allind)-1)

print("{:.5f} {:.5f} {:.5f} {:.5f}".format(tp/n,tn/n,fn/n,fp/n))
# print("TP: ", tp/n)
# print("TN: ", tn/n)
# print("FN: ", fn/n)
# print("FP: ", fp/n)

