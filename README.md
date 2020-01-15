# SODA (Species bOundry Delimitation using Astral)

SODA is a tool for species delimitation using only gene tree topologies. It's a fast way of doing species delimitation and mostly finding population boundaries within individuals. It uses the polytomy test developed by [Sayyari et. al ](https://www.mdpi.com/2073-4425/9/3/132/htm) implemented inside ASTRAL package.

- You can find the details of the algorithm and benchmarks in the following paper:

	* Rabiee, Maryam, and Siavash Mirarab. “SODA: Multi-Locus Species Delimitation Using Quartet Frequencies.” BioRxiv, 2019, 869396. doi:10.1101/869396.

# INSTALLATION:

For running ASTRAL you only need to have Java installed, however, SODA is written in Python and it uses Dendropy package which is easy to install with ***pip***. You can find installation instructions [here](https://dendropy.org).

# EXECUTION:
For running soda you need your gene trees in newick format in one file and your guide tree in another file. If you haven't obtained the guide tree, you can easily run ASTRAL and estimate the species tree.

```
java -jar __ASTRAL_jarfile__  -i <genetrees.tre> -o <output.tree>
```


If you know the correct rooting of the species tree, use that to reroot the species tree. Then you can easily run SODA:

```
python3 species_delimitation.py <guidetree.tree> <output.cl> [cut-off]
```
The cut off value is optional, by default it has been set to 0.05. It can be changed and it will affect the number of species. Check out the experiments in the [paper](https://www.biorxiv.org/content/10.1101/869396v1.abstract) 

If you don't, SODA can take care of it. You can use the *delimit-gts.sh* script.

```
./delimit-gts.sh [Gene Tree File] [Guide Tree File] [Output Name] [Out directory] [ASTRAL jar file]
```

## Interpreting the output

The output of SODA is name of the individuals and a corresponding number. Individuals that have the same number assigned are in the same group and comprise a distinct species than individuals with other numbers.
Sample output is:

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
So here four different goup has been identified within these individuals.


