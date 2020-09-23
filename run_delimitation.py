from sys import argv
from math import log,ceil
import argparse
import subprocess
from species_delimitation import run_delimitation
import dendropy
import collections
import re

#__len__()
def run_astral(gene_trees, n, g, out, mapping, guide_tree):

	bashCommand = "java -Xmx"+ str(100 * ceil(log(n * g, 10)* log(n, 10)))+"m -jar ./Astral/astral.5.7.3.jar -i "+gene_trees+" -o "+ out + " -t 10"

	if mapping:
		bashCommand += " -a "+ mapping

	if guide_tree:
		bashCommand += " -q "+ guide_tree

	print("==========================Running " + bashCommand+"=========================")

	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = process.communicate()

	print("==========================ASTRAL run finished=======================")

	if mapping:
		#lines = error.split()
		r1 = re.findall(r"\n\(\S*;\n",error.decode('utf-8'))
		print(r1)
		print("***return",r1[-1].strip())
		return dendropy.Tree.get(data=r1[-1].strip(),schema='newick')


	return dendropy.Tree.get(
	    			file=open(out, "r"),
	     		schema='newick')

def root_guide_tree(gene_trees, n, g, out, mapping,tree):
	p_vals = [(float(l.label),l) for l in tree.postorder_internal_node_iter() if l.label and l.label != "NA"]
	min_p = min(p_vals, key = lambda x: x[0])
	print("Minimum p-value in the tree is " + str(min_p[0]))
	#node = tree.find_node_with_label(min_p)

	tree.reroot_at_edge(min_p[1].edge)
	path = out+".rt"
	tree.write(path=path,schema='newick')
	print("The guide tree is successfully rerooted and written into "+ path)
	gt = run_astral(gene_trees, n, g, out+"2", mapping, path)
	return gt


if "__main__" == __name__:

	cutoff = 0.05
	parser = argparse.ArgumentParser()
	parser.add_argument("-i","--input gene trees",required=True,help="A newick file containing all the gene trees")
	parser.add_argument("-o","--output file",required=True,help="Output file for the delimitation")
	parser.add_argument("-d","--output directory",required=True,help="Output directory for the tree files")
	parser.add_argument("-t","--guide tree",required=False,help="The guide tree to do delimitation on, if available")
	parser.add_argument("-a","--mapping",required=False,help="The mapping file of individuals to species; each line has two columns, first is individual label and second is the population it belongs to")
	parser.add_argument("-r","--rooted",required=False,action='store_true',help="Whether the guide tree is rooted or needs rerooting")
	parser.add_argument("-c","--cutoff",required=False,default = cutoff, help="The mapping file of individuals to species; each line has two columns, first is individual label and second is the population it belongs to")
	
	if len(argv) == 1:
		parser.print_help()
		exit(0)

	args = vars(parser.parse_args())

	gene_trees_path =  args["input gene trees"]
	out_dir = args["output directory"]
	mapping = args["mapping"]
	guide_tree = args["guide tree"]

	with open(gene_trees_path) as f:
		lines = f.readlines()
	lines = [l.strip() for l in lines]

	taxa = dendropy.TaxonNamespace()
	trees = dendropy.TreeList(taxon_namespace=taxa)
	trees.read(path=gene_trees_path, schema='newick')
	n = taxa.__len__()
	print(n)
	tree = run_astral(gene_trees_path, n, len(lines), out_dir+"astral.out", mapping ,guide_tree)

	print(tree.as_string(schema="newick"))
	if not args["rooted"] or not args["guide tree"]:
		tree = root_guide_tree(gene_trees_path, n, len(lines), out_dir+"astral.out", None , tree)
	
	run_delimitation(tree, args["output file"], float(args["cutoff"]))

