#!/bin/sh

# IMPORTANT: THIS FILE PRODUCES SOME BUGS, MOST OF WHICH YOUR FORTRAN COMPILER
# WILL REMIND YOU OF, AND THEY ARE TRIVIAL TO FIX
# THE IMPORTANT THING TO REMEMBER IS TO CHANGE Gp TO G5p, AS FORTRAN 
# DOES NOT DISTINGUISH CAPITALISATION AND OTHERWISE SILENTLY CONFUSES IT WITH
# gp

echo "REMEMBER G5p !! (READ COMMENT IN THIS FILE)"

tr '\n,' ' \n' < $1 > /tmp/test.tmp
tr '{}' '  ' < /tmp/test.tmp > /tmp/test2.tmp
tr -s ' ' ' ' </tmp/test2.tmp > $2
sed -i 's/y\([0-9][0-9]*\)/y(\1)/g' $2
sed -i 's/Sqrt\[ *\([0-9][0-9]*\/*[0-9]*\)\]/root\1/g' $2
sed -i 's/ y(\([0-9][0-9]*\)) ==/dydt(\1) =/' $2
sed -i 's/I /j*/g' $2
sed -i 's/\([a-zA-Z0-9()]\) \([a-zA-Z0-9()]\)/\1*\2/g' $2
sed -i 's/\/ /\//g' $2
sed -i 's/[ \/(][0-9][0-9]*/&.d0/g' $2
sed -i 's/y(\([0-9]*\).d0)/y(\1)/g' $2
sed -i 's/dydt(\([0-9]*\).d0)/dydt(\1)/g' $2
