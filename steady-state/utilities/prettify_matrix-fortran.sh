#!/bin/sh

outfile=${1%.*}.f90
sed 's/$/,\&/' $1 > $outfile


sed -i 's/^/\t\&/' $outfile
sed -i 's/Sqrt\[ *\([0-9][0-9]*\/*[0-9]*\)\]/root\1/g' $outfile
sed -i 's/I/j/g' $outfile
sed -i 's/0/z/g' $outfile
sed -i 's_\([ \/(]\)\([1-9][0-9]*\)_\1(\2.d0, 0.d0)_g' $outfile

sed -i '1i subroutine make_matrix(fsup, gp, gc, dp, dc, hfR, muBB, Wp, Wc, dwp, dwc, f5p, output)\n\tdouble complex, intent(in) :: fsup\n\tdouble precision, intent(in) :: gp, gc, dp, dc, hfR, muBB, Wp, Wc, dwp, dwc, f5p\n\tdouble complex, dimension(324*324), intent(out) :: output\n\tcomplex, parameter :: j = cmplx(0, 1)\n\tdouble precision, parameter :: root2 = dsqrt(2.d0)\n\tdouble precision, parameter :: root3 = dsqrt(3.d0)\n\tdouble precision, parameter :: root6 = dsqrt(6.d0)\n\tdouble complex, parameter :: z = (0.d0, 0.d0)\n\toutput=(/&' $outfile
sed -i -e "\$a\&/)\nend subroutine" $outfile