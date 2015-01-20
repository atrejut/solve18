#!/bin/sh

outfile=${1%.*}.py

sed 's/$/],/' $1 > $outfile
sed -i 's/^/[/' $outfile
sed -i 's/Sqrt\[ *\([0-9][0-9]*\/*[0-9]*\)\]/root\1/g' $outfile
sed -i 's/I/1j/g' $outfile
sed -i '1i def make_matrix(fsup, gp, gc, dp, dc, hfR, muBB, Wp, Wc, dwp, dwc, f5p):\n\treturn np.array([' $outfile
sed -i -e "\$a])" $outfile