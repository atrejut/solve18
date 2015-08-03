

include 'obesspp.f90'


subroutine solve(fsup, gp, gc, hfR, muBB, Wp, Wc, dwp, dwc, f5p, ndc, dcs, ndp, dps, output)
	implicit none
	integer, parameter :: neq=324 !Number of equations
	double complex, dimension(neq, neq) :: matrix
	double complex, intent(in) :: fsup
	double precision, intent(in) :: gp, gc, hfR, muBB, Wp, Wc, dwp, dwc, f5p
	double complex, dimension(ndp, ndc), intent(out) :: output
	double complex :: y0(neq)
	integer :: info, ndp, ndc, i, j
	integer, dimension(neq) :: ipiv
	double precision :: deltap, deltac, Delta
	double precision, dimension(ndc) :: dcs
	double precision, dimension(ndp) :: dps
	double precision :: vmax = 15.d0

	double precision, parameter :: root2 = dsqrt(2.d0)
	double precision, parameter :: root3 = dsqrt(3.d0)

	integer :: stateSelector(4)

	stateSelector = (/7, 26, 45, 64/) ! for pp and pm polarisation
!	stateSelector = (/24, 43, 62, 81/) ! for mp and mm polarisation
!	stateSelector = (/109, 128, 147, 166/) ! for transposed matrix, row/column ordering ?

!$OMP PARALLEL DO DEFAULT(FIRSTPRIVATE) SHARED(output)
	do i = 1, ndp
		do j = 1, ndc
			deltap = dps(i)
			deltac = dcs(j)

			y0 = (0.0d0, 0.0d0)
			y0(1) = fsup
			y0(20)= fsup
			y0(39)= fsup
			y0(58)= fsup
			y0(77)= fsup


			call make_matrix(fsup, gp, gc, deltap, deltac, hfR, muBB, Wp, Wc, dwp, dwc, f5p, matrix)
			call ZGETRF(neq, neq, matrix, neq, ipiv, info)
			call ZGETRS('N', neq, 1, matrix, neq, ipiv, y0, neq, info)

			output(i, j) = 2.d0/root2*(y0(stateSelector(2)) + y0(stateSelector(3))) + 2.d0/root3*(y0(stateSelector(1)) + y0(stateSelector(4))) ! why factor 2 ?! (needed for agreement with mathematica)
		end do
	end do
!$OMP END PARALLEL DO

end subroutine
