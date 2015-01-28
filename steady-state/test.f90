

include 'matrix.f90'


subroutine solve(fsup, gp, gc, hfR, muBB, Wp, Wc, dwp, dwc, f5p, output)
	implicit none
	integer, parameter :: neq=324 !Number of equations
	double complex, dimension(neq, neq) :: matrix
	double complex, intent(in) :: fsup
	double precision, intent(in) :: gp, gc, hfR, muBB, Wp, Wc, dwp, dwc, f5p
	double complex, dimension(81, 201), intent(out) :: output
	double complex :: y0(neq)
	integer :: info, dp, dc
	integer, dimension(neq) :: ipiv
	double precision :: deltap, deltac
	double precision :: vmax = 15.d0
	double precision :: delta_min = -22
	double precision :: delta_max = 22

	double precision, parameter :: root2 = dsqrt(2.d0)
	double precision, parameter :: root3 = dsqrt(3.d0)

	integer :: stateSelector(4)

	stateSelector = (/7, 26, 45, 64/)
!	stateSelector = (/109, 128, 147, 166/) ! for transposed matrix, row/column ordering ?

!$OMP PARALLEL DO DEFAULT(FIRSTPRIVATE) SHARED(output)
	do dp = 1, 81
		deltap = -20 + 0.5*(dp-1)

		do dc = 1, 201
			deltac = -50 + 0.5*(dc-1)

			if (deltac < delta_min-deltap*780.d0/480.d0) then
				cycle
			end if
			if (deltac > delta_max-deltap*780.d0/480.d0) then
				cycle
			end if

			y0 = (0.0d0, 0.0d0)
			y0(1) = fsup
			y0(20)= fsup
			y0(39)= fsup
			y0(58)= fsup
			y0(77)= fsup


			call make_matrix(fsup, gp, gc, deltap, deltac, hfR, muBB, Wp, Wc, dwp, dwc, f5p, matrix)
			call ZGETRF(neq, neq, matrix, neq, ipiv, info)
			call ZGETRS('N', neq, 1, matrix, neq, ipiv, y0, neq, info)

			output(dp, dc) = 2.d0/root2*(y0(stateSelector(2)) + y0(stateSelector(3))) + 2.d0/root3*(y0(stateSelector(1)) + y0(stateSelector(4))) ! why factor 2 ?! (needed for agreement with mathematica)
		end do
	end do
!$OMP END PARALLEL DO

end subroutine