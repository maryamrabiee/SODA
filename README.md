# SODA (Species bOundry Delimitation using Astral)

SODA is a tool for species delimitation using only gene tree topologies. It's a fast way of doing species delimitation and relies on a polytomy test developed by [Sayyari et. al ](https://www.mdpi.com/2073-4425/9/3/132/htm) implemented inside ASTRAL package. SODA has been in our tests slightly less accurate than BPP but it is far faster.  

- You can find the details of the algorithm and benchmarks in the following paper:

	* Rabiee, Maryam, and Siavash Mirarab. “SODA: Multi-Locus Species Delimitation Using Quartet Frequencies.” BioRxiv, 2019, 869396. doi:10.1101/869396.

# INSTALLATION:

## Prerequisites

* Java, version 1.6 or later 
* Dendropy, version > 4.0.0; Dendropy package which is easy to install with ***pip***. You can find installation instructions [here](https://dendropy.org).

## Steps:

1. Clone the code from this github page or download [the zip file](https://github.com/maryamrabiee/SODA/archive/master.zip). 
2. Unzip the package if you downloaded the zip file.
3. `cd` into the directory where SODA code is placed. 

There is installation is required for the current version of SODA. 

# EXECUTION:
For running soda you need your gene trees in newick format in one file and your guide tree in another file. The guide tree is option. If you haven't obtained the guide tree, SODA uses ASTRAL to compute one.



For running SODA, given only input gene trees, you should run following command:

```
python3 run_delimitation.py -i [Gene Tree File] -d [Out directory] -o [Output Name]  
```

You can see the list of options by running:

```
python3 run_delimitation.py 
```


* If you know the correct rooting of the species tree, use the `-r` option ("rooted") so that SODA avoids  rerooting the tree.
* The p-value cutoff value is optional (by default it has been set to 0.05) but can be changed and it will affect the number of species. Check out the experiments in the [paper](https://www.biorxiv.org/content/10.1101/869396v1.abstract).
* Use `-a` option to tell SODA about the population groupings known *a priori*. SODA will not break these populations. 

## Examples
With the data given in the `samle_data` directory you can test SODA on your machine with following commands. To run SODA just with gene trees and a mapping of individuals to populations, you should set options as:

```
python3 run_delimitation.py  -i sample_data/all-gene-trees.tre.pruned -d output/ -o delim.cl  -a sample_data/mapping.txt   
```
The delimitation of the population can be found in the `delim.cl` file.
To run SODA with a rooted guide tree and a specific cut off value you can run this command:

```
python3 run_delimitation.py -i sample_data/all-gene-trees.tre.pruned -d output/ -o delim.cl  -t sample_data/astral.out.rt -r
```

## Interpreting the output

The output of SODA is the names of individuals and a corresponding number per each individual. Individuals that have the same number assigned to them are in the same group and comprise a distinct species.

A Sample output would look like:

```
P_min12908      0
P_min39119      0
P_min13868      0
P_min18421      0
P_min13898      0
P_min5292       0
P_v_meri16      1
P_v_cos199      1
P_v_vers_1      2
P_v_vir379      3
P_x_xant_1      3
...
```
Here, four different species have been identified.

In addition to the output file, inside the directory given using `-d`, SODA saves several files. These include the guide tree, before rooting, after rooting, and after annotation with p-values per each branch. 


