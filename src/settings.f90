module settings
  implicit none
	! parameters for OBE
	double precision :: bfield = 5.d0 ! magnetic field
	double precision :: Wc1 = 2.d0 		! coupling rabi frequency
	double precision :: Wc2 = 2.d0		! coupling rabi frequency
	double precision :: Wp = 1.d0			! probe rabi frequency
	double precision :: hfs = 8.d0		! hyperfine splitting
	double precision :: G5p = 6.d0		! intermediate state lifetime
	double precision :: Gr1 = 0.05d0	! rydberg state lifetime
	double precision :: Gr2 = 0.05d0	! rydberg state lifetime
	double precision :: gp = 0.01d0		! probe laser linewidth
	double precision :: gc = 0.8d0		! coupling laser linewidth + other decoherence effects
	integer :: NProbe = 241
	integer :: NCoupling = 401
	integer :: ShiftProbe = -30
	integer :: ShiftCoupling = -50
	double precision :: StepProbe = 0.25d0
	double precision :: StepCoupling = 0.25d0
	character(len=2) :: pol

  contains
    subroutine loadSettings()
      NAMELIST/PARAMS/ bfield, Wc1, Wc2, Wp, hfs, G5p, Gr1, Gr2, gp, gc
      NAMELIST/STEPPING/ NProbe, NCoupling, ShiftProbe, ShiftCoupling, StepProbe, StepCoupling
      NAMELIST/SIM/ pol
            
      OPEN(UNIT=1, FILE='config.info')
      READ(1, NML=PARAMS)      
      READ(1, NML=STEPPING)
      READ(1, NML=SIM)
      
      CLOSE(1)

    end subroutine loadSettings
  
end module settings
