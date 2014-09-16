pm: EXECUTABLE:= ./../bin/solve18_pm
mp: EXECUTABLE:= ./../bin/solve18_mp
mm: EXECUTABLE:= ./../bin/solve18_mm
pp: EXECUTABLE:= ./../bin/solve18_pp

pm: DERIVATIVE:= derivative_pm.f90
mp: DERIVATIVE:= derivative_mp.f90
mm: DERIVATIVE:= derivative_mm.f90
pp: DERIVATIVE:= derivative_pp.f90


FC = gfortran-4.8

BUILD_DIR := ./../build/

FCFLAGS = -Ofast -march=native -fopenmp -ffree-line-length-none

.PHONY: all clean distclean
all: $(EXECUTABLE)
pm: $(EXECUTABLE)
mp: $(EXECUTABLE)
mm: $(EXECUTABLE)
pp: $(EXECUTABLE)


$(EXECUTABLE) :
	gfortran-4.8 -Ofast -march=native -fopenmp -ffree-line-length-none zvode.f settings.f90 $(DERIVATIVE) solve18.f90 -o $(EXECUTABLE)

pm:
	gfortran-4.8 -Ofast -march=native -fopenmp -ffree-line-length-none zvode.f settings.f90 $(DERIVATIVE) solve18.f90 -o $(EXECUTABLE)

mp:
	gfortran-4.8 -Ofast -march=native -fopenmp -ffree-line-length-none zvode.f settings.f90 $(DERIVATIVE) solve18.f90 -o $(EXECUTABLE)

mm:
	gfortran-4.8 -Ofast -march=native -fopenmp -ffree-line-length-none zvode.f settings.f90 $(DERIVATIVE) solve18.f90 -o $(EXECUTABLE)

pp:
	gfortran-4.8 -Ofast -march=native -fopenmp -ffree-line-length-none zvode.f settings.f90 $(DERIVATIVE) solve18.f90 -o $(EXECUTABLE)



clean:
	@- $(RM) $(EXECUTABLE)
	@- $(RM) $(OBJS)
	rm -f *.mod
	rm -f *__genmod*
	rm -f ../bin/solve18_*


distclean: clean

