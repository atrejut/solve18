

include 'obessmm.f90'


subroutine solve(fsup, gp, gc, hfR, muBB, Wp, Wc, dwp, dwc, f5p, Delta, nv, vs, output)
	implicit none
	integer, parameter :: neq=324 !Number of equations
	double complex, dimension(neq, neq) :: matrix
	double complex, intent(in) :: fsup
	double precision, intent(in) :: gp, gc, hfR, muBB, Wp, Wc, dwp, dwc, f5p
	double complex, dimension(nv), intent(out) :: output
	double complex :: y0(neq)
	integer :: info, nv, n
	integer, dimension(neq) :: ipiv
	double precision :: v, deltap, deltac, Delta
	double precision, dimension(nv) :: vs
	double precision :: vmax = 15.d0

	double precision, parameter :: root2 = dsqrt(2.d0)
	double precision, parameter :: root3 = dsqrt(3.d0)

	integer :: stateSelector(4)

!	stateSelector = (/7, 26, 45, 64/) ! for pp and pm polarisation
	stateSelector = (/24, 43, 62, 81/) ! for mp and mm polarisation
!	stateSelector = (/109, 128, 147, 166/) ! for transposed matrix, row/column ordering ?

!$OMP PARALLEL DO DEFAULT(FIRSTPRIVATE) SHARED(output)
	do n = 1, nv
		v = vs(n)
		deltap = v/780.e-3
		deltac = Delta-v/486.e-3

		y0 = (0.0d0, 0.0d0)
		y0(1) = fsup
		y0(20)= fsup
		y0(39)= fsup
		y0(58)= fsup
		y0(77)= fsup


		call make_matrix(fsup, gp, gc, deltap, deltac, hfR, muBB, Wp, Wc, dwp, dwc, f5p, matrix)
		call ZGETRF(neq, neq, matrix, neq, ipiv, info)
		call ZGETRS('N', neq, 1, matrix, neq, ipiv, y0, neq, info)

		output(n) = 2.d0/root2*(y0(stateSelector(2)) + y0(stateSelector(3))) + 2.d0/root3*(y0(stateSelector(1)) + y0(stateSelector(4))) ! why factor 2 ?! (needed for agreement with mathematica)
	end do
!$OMP END PARALLEL DO

end subroutine