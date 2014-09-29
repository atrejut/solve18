EXECUTABLE:=../bin/solve18_$(MAKECMDGOALS)
DERIVATIVE:=derivative_$(MAKECMDGOALS).f90

FC = gfortran

BUILD_DIR := ./../build/

FCFLAGS = -Ofast -march=native -fopenmp -ffree-line-length-none -flto
EXTRAFLAGS = -fmodulo-sched -fmodulo-sched-allow-regmoves -funsafe-loop-optimizations
LOOPFLAGS = -funroll-loops
# profiling can give a small speed gain
# first compile with -fprofile-generate, run once (possibly single-threaded)
# then compile with flags below
# PROFILEFLAGS -fprofile-use -fprofile-correction

.PHONY: all clean distclean pm mp mm pp

all:
	$(MAKE) mp
	$(MAKE) pm
	$(MAKE) mm
	$(MAKE) pp

pm: $(EXECUTABLE)
mp: $(EXECUTABLE)
mm: $(EXECUTABLE)
pp: $(EXECUTABLE)


$(EXECUTABLE) : solve18.f90 zvode.f settings.f90 $(DERIVATIVE)
#	$(FC) $(FCFLAGS) $(EXTRAFLAGS) $(LOOPFLAGS) zvode.f settings.f90 $(DERIVATIVE) solve18.f90 -o $(EXECUTABLE)
	ifort -fast -i8 -openmp zvode.f settings.f90 $(DERIVATIVE) solve18.f90 -o $(EXECUTABLE)

clean:
	@- $(RM) $(EXECUTABLE)
	@- $(RM) $(OBJS)
	rm -f *.mod
	rm -f *__genmod*
	rm -f ../bin/solve18_*


distclean: clean

