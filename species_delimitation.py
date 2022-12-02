import dendropy
import collections
import sys
import argparse



def reroot(mle,root):
	oldroot = mle.seed_node
	newlen = root.edge.length/2 if root.edge.length else None
	mle.reroot_at_edge(root.edge,length1=newlen,length2=newlen,suppress_unifurcations=False)
    #'''This is to fix internal node labels when treated as support values'''
	while oldroot.parent_node != mle.seed_node and oldroot.parent_node != None:
		oldroot.label = oldroot.parent_node.label
		oldroot = oldroot.parent_node
		if len(oldroot.sister_nodes()) > 0:
			oldroot.label = oldroot.sister_nodes()[0].label
	mle.suppress_unifurcations()
	return root



def print_node(n):
	if n.is_leaf():
		print(n.taxon.label.replace(" ", "_"), n.state)
	else:
		print(n.label, n.state)


def add_clade(clades, node):
	clade = [i for i in node.leaf_iter() if i.state != 'P']
	if clade:
		clades.append(clade)
	return

def find_clades(rt_node,cutoff):
	clades = []
	for node in rt_node.postorder_node_iter():	
		# print_node(node)

		if not node.is_leaf():
			children = [child for child in node.child_node_iter()]
			c1 = children[0]
			c2 = children[1]

			if children[0].state == 'P' and children[1].state == 'N':

				add_clade(clades, children[1])
				for nd in children[1].postorder_iter():
					nd.state = 'P'
				c2.state = 'P'
				c2.mark = 'T'				

			if children[1].state == 'P' and children[0].state == 'N':

				add_clade(clades, children[0])
				for nd in children[0].postorder_iter():
					nd.state = 'P'
				
				c1.state = 'P'	
				c1.mark = 'T'			

			if children[0].state == 'P' and children[1].state == 'P':
				node.state = 'P'
				node.mark = 'T'

		if node.state != 'P' and node.parent_node and node.label:
				
				if node.label != 'NA' and float(node.label) < cutoff :
					add_clade(clades, node)
					for nd in node.postorder_iter():
						nd.state= 'P'
					node.state = 'P'
					node.mark = 'T'

		# print_node(node)
	if not clades:
		add_clade(clades, rt_node)	
	return clades


def print_extended_sp(tree, output_extended, out_dir):
	tre = tree.clone()
	for node in tre.postorder_node_iter():
		if node.mark != 'T' and node.edge.is_internal():
			node.edge.collapse()
		#	print("collapse")
	print("Extenxed species tree: \n" + tre.as_string(schema="newick"))
	if output_extended:
		f = open(out_dir+"/astral.ext.tre", "w")
		f.write(tre.as_string(schema="newick"))
		f.close()


def find_root(rt_node, cutoff):
	for node in rt_node.postorder_node_iter():	
		if  node.parent_node and node.label and node.label != 'NA':
			
				if float(node.label) < cutoff :
					return node.edge

def run_delimitation(tree, out, cutoff, output_extended, out_dir):

	for i in tree.postorder_node_iter():
		i.state = 'N'
		i.mark = 'F'

	clades = find_clades(tree, cutoff)
	#print("Clades:\n"+"\n  ".join(clades))
	print_extended_sp(tree, output_extended, out_dir)

	f = open(out, "w")	
	for i,l in enumerate(clades):
		a = [node.taxon.label for node in l]
		counter = collections.Counter(a)
		# cluster = counter.most_common(1)[0][0]+"_"+str(i)
		cluster = counter.most_common(1)[0][0]
		for node in l:
			print(node.taxon.label.replace(" ", "_")+"\t" + cluster)
			f.write(node.taxon.label.replace(" ", "_")+"\t" + str(i) + "\n")
		print()
	f.close()
	tree.prune_leaves_without_taxa()
