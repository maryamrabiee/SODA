import dendropy
import collections
import sys




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

			if children[1].state == 'P' and children[0].state == 'N':

				add_clade(clades, children[0])
				for nd in children[0].postorder_iter():
					nd.state = 'P'
				
				c1.state = 'P'				

			if children[0].state == 'P' and children[1].state == 'P':
				node.state = 'P'

		if node.state != 'P' and node.parent_node and node.label:
				
				if node.label != 'NA' and float(node.label) < cutoff :
					add_clade(clades, node)
					for nd in node.postorder_iter():
						nd.state= 'P'
					node.state = 'P'
		# print_node(node)
					
	return clades


def find_root(rt_node, cutoff):
	for node in rt_node.postorder_node_iter():	
		if  node.parent_node and node.label and node.label != 'NA':
			
				if float(node.label) < cutoff :
					return node.edge

if "__main__" == __name__:
	
	fname = sys.argv[1]
	out = sys.argv[2]
	mle = dendropy.Tree.get(
	    file=open(fname, "r"),
	    schema='newick',
	    rooting='force-rooted')

	if len(sys.argv)==3:
		cutoff = float(sys.argv[3])

	else:
		cutoff = 0.05


	
#	if root != "unrooted":
#		e = find_root(mle,cutoff)
#		new_root = mle.reroot_at_edge(e)
#	elif root != "rooted"
#		print("The guide must be either rooted or unrooted")
#		exit()
		
	print(mle.as_string(schema="newick"))
	for i in mle.postorder_node_iter():
		i.state = 'N'


	clades = find_clades(mle, cutoff)
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

	# print(len(clades))
	mle.prune_leaves_without_taxa()
	#print(mle.as_string(schema="newick"))

