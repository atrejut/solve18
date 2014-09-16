EXECUTABLE:= ./../bin/solve18

FC = gfortran-4.8

BUILD_DIR := ./../build/
F_OBJS = zvode.o
F90_OBJS = solver18.o
OBJS := $(addprefix $(BUILD_DIR), $(F_OBJS))
OBJS90 := $(addprefix $(BUILD_DIR), $(F90_OBJS))

FCFLAGS = -Ofast -march=native -fopenmp -ffree-line-length-none

.PHONY: all clean distclean
all: $(EXECUTABLE)

$(EXECUTABLE) :
	gfortran-4.8 -Ofast -march=native -fopenmp -ffree-line-length-none zvode.f settings.f90 solve18.f90 -o $(EXECUTABLE)

clean:
	@- $(RM) $(EXECUTABLE)
	@- $(RM) $(OBJS)
	rm -f *.mod
	rm -f *__genmod*


distclean: clean

