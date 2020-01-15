gt=$1
sp=$2
out=$3
outdir=$4
jarfile=$5

test $# -ne "5" && echo "Usage: $0 [Gene Tree File] [Species Tree File] [Output Name] [Out directory] [ASTRAL jar file]" && exit 1

java -jar $jarfile  -i $gt -o $outdir/$out.tre -q $sp -p0 -t10 2> $outdir/$out.err 
echo "First polytomy test is done."
nw_reroot $outdir/$out.tre $(nw_labels -L $outdir/$out.tre | sort -n | head -1) | nw_topology - > $outdir/$out.tre.rt
echo "Guide tree is rerooted on the branch with minimum p-value and saved to $outdir/$out.tre.rt"
java -jar $jarfile  -i $gt -o $outdir/${out}2.tre -q $outdir/$out.tre.rt -p0 -t10 2> $outdir/${out}2.err
echo "Second polytomy test is done."
python3 ./species_delimitation.py $outdir/${out}2.tre $outdir/$out.cl 0.05 > /dev/null
