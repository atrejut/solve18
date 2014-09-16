
program test_18level
	use settings
	implicit none
	integer,parameter :: neq=324 !Number of equations
	double precision :: x0, xend, tic,toc, rwork(20+neq), delta(2), dummy1(50), dummy3
	double complex :: y0(neq), zwork(15*neq)
	integer :: istate, iwork(30), n, m, dummy2(33), dummy4(8), ticr, tocr, clockrate
	integer :: percentDone = 0
	integer :: stateSelector(4)
	double complex, dimension(:, :), allocatable :: results
	common /ZVOD01/ dummy1, dummy2
	common /ZVOD02/ dummy3, dummy4
	external :: obedot
	Character(len=6) :: filedescriptor
!$OMP THREADPRIVATE(/ZVOD01/, /ZVOD02/)
	
	call loadSettings()
	
	if (pol .eq. 'pp' .or. pol .eq. 'pm') then
		stateSelector = (/7, 26, 45, 64/)
	else if (pol .eq. 'mm' .or. pol .eq. 'mp') then
		stateSelector = (/24, 43, 62, 81/)
	else
		write(*, *) 'INVALID STATE', pol
	endif
	
	write (*, *) 'running with B=', bfield
	write (*, *) 'running for polarisation ', pol
	
	allocate(results(NCoupling, NProbe))
	
	call system_clock(ticr)
	call CPU_TIME(tic)
!$OMP PARALLEL DO DEFAULT(PRIVATE) SHARED(results, Nprobe, Ncoupling, ShiftProbe, ShiftCoupling, StepProbe, StepCoupling, percentDone, stateSelector)
	do n = 1, NProbe
	delta(1) = ShiftProbe + StepProbe*(n - 1)
	!write (*, *) 'running calcualation for dp = ', delta(1)
	do m=1, NCoupling
		delta(2) = ShiftCoupling + StepCoupling*(m - 1)
		! initialise work arrays
		rwork = 0.0d0
		iwork = 0
		iwork(6) = 5000 ! increase maximum number of steps allowed
		
		! initial conditions for OBE
		y0 = cmplx(0.0d0, 0.0d0)
		y0(1) = cmplx(0.2d0, 0.0d0)
		y0(20)= cmplx(0.2d0, 0.0d0)
		y0(39)= cmplx(0.2d0, 0.0d0)
		y0(58)= cmplx(0.2d0, 0.0d0)
		y0(77)= cmplx(0.2d0, 0.0d0)
		x0 = 0.0d0
		xend = 3.5d0
		istate = 1
		call zvode(obedot, neq, y0, x0, xend, 1, 1.d-8, 1.d-8, 1, istate, 1, zwork, 15*neq, rwork, 20+neq, iwork, 30, obedot, 10, delta, 0)
		results(m, n) = 1.d0/dsqrt(2.d0)*(y0(stateSelector(2)) + y0(stateSelector(3))) + 1.d0/dsqrt(3.d0)*(y0(stateSelector(1)) + y0(stateSelector(4)))
		! with coefficients 1/root3, 1/root2, 1/root2, 1/root3
	end do
!$OMP ATOMIC
	percentDone = percentDone + 1
	WRITE(*, '(f5.1 a)') REAL(percentDone)/REAL(NProbe)*100, '% done'
	end do
!$OMP END PARALLEL DO
	call CPU_TIME(toc)
	call system_clock(tocr, clockrate)
	!Solver Statistics
	write(*, *) 'execution took ', INT((toc-tic)/60), 'minutes of CPU time'
	write(*, *) 'execution took ', (tocr-ticr)/clockrate/60, 'real-time minutes'
	
	write(filedescriptor, "(F6.2)") bfield
	open(15, file='../results/'//pol//'/B'//filedescriptor//'.txt')
	do n = 1, NCoupling
		write(15, *) AIMAG(results(n, :))
	end do
	close(15)
	
	deallocate(results)
	
end program

