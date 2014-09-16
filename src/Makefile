pm: EXECUTABLE:=../bin/solve18_pm
mp: EXECUTABLE:=../bin/solve18_mp
mm: EXECUTABLE:=../bin/solve18_mm
pp: EXECUTABLE:=../bin/solve18_pp

pm: DERIVATIVE:=derivative_pm.f90
mp: DERIVATIVE:=derivative_mp.f90
mm: DERIVATIVE:=derivative_mm.f90
pp: DERIVATIVE:=derivative_pp.f90

FC = gfortran-4.8

BUILD_DIR := ./../build/

FCFLAGS = -Ofast -march=native -fopenmp -ffree-line-length-none -flto
EXTRAFLAGS = -fmodulo-sched -fmodulo-sched-allow-regmoves -funsafe-loop-optimizations
LOOPFLAGS = -funroll-loops -floop-block
# profiling can give a small speed gain
# first compile with -fprofile-generate, run once (possibly single-threaded)
# then compile with flags below
# PROFILEFLAGS -fprofile-use -fprofile-correction

.PHONY: all clean distclean

all: pm mp mm pp 
pm: compile
mp: compile
mm: compile
pp: compile


compile : solve18.f90 zvode.f settings.f90 $(DERIVATIVE) $(EXECUTABLE)
	gfortran-4.8 $(FCFLAGS) $(EXTRAFLAGS) $(LOOPFLAGS) zvode.f settings.f90 $(DERIVATIVE) solve18.f90 -o $(EXECUTABLE)

clean:
	@- $(RM) $(EXECUTABLE)
	@- $(RM) $(OBJS)
	rm -f *.mod
	rm -f *__genmod*
	rm -f ../bin/solve18_*


distclean: clean

