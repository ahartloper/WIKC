C     A Hartloper, 17-04-2020
      SUBROUTINE MPC(UE,A,JDOF,MDOF,N,JTYPE,X,U,UINIT,MAXDOF,
     * LMPC,KSTEP,KINC,TIME,NT,NF,TEMP,FIELD,LTRAN,TRAN)
C
      INCLUDE 'ABA_PARAM.INC'
C
      DIMENSION UE(MDOF),A(MDOF,MDOF,N),JDOF(MDOF,N),X(6,N),
     * U(MAXDOF,N),UINIT(MAXDOF,N),TIME(2),TEMP(NT,N),
     * FIELD(NF,NT,N),LTRAN(N),TRAN(3,3,N)
C     Internal variables
      real(8) :: disp_beam(3), rot_beam(3), w_beam, warp_fun,
     *      I33(3, 3)
      real(8) :: rmat(3, 3), rmat3(3), link(3)
      integer :: i
C     Definition start
      disp_beam = U(1:3, 2)
      rot_beam = U(4:6, 2)
      w_beam = U(7, 2)
      warp_fun = 1.d0
      I33 = 0.d0
      do i = 1, 3
            I33(i, i) = 1.d0
      end do
      rmat = rvec2rmat(rot_beam)
      rmat3 = rmat(1:3, 3)
C     Constraint equations
      link = X(1:3, 1) - X(1:3, 2)
      UE(1:3) = matmul(rmat, link) + disp_beam + warp_fun*w_beam*rmat3
      do i = 1, 3
            JDOF(i, 1) = i
      end do
C     Constraint linearization
      A(1:3, 1:3, 1) = I33
      A(1:3, 1:3, 2) = -I33
      A(1:3, 4:6, 2) = skew(link + warp_fun * w_beam * rmat3)
      A(1:3,   7, 2) = -warp_fun * rmat3
      do i = 1, 7
            JDOF(i, 2) = i
      end do
      RETURN

      INCLUDE

C     Rotation vector to rotation matrix using Rodriguez forumla
      PURE FUNCTION RVEC2RMAT(rvec) RESULT(rrr)
      real(8), intent(in) :: rvec(3)
      real(8), intent(out) :: rrr(3, 3)
      real(8) :: r, rr(3), r_out_r(3, 3), small_tol
      parameter(small_tol=1.e-14)
      r = norm2(rvec)
      if (r < small_tol) then
            rrr = I33
      else
            rr = rvec / r
            forall (i = 1:3)
                  forall(j = 1:3) r_out_r(i, j) = rr(i) * rr(j)
            end forall
            rrr = cos(r)*I33 + (1.d0-cos(r))*r_out_r + sin(r)*skew(rr)
      end if
      END FUNCTION

C     Vector to skew-symmetric matrix
      PURE FUNCTION SKEW(v) RESULT(m)
      real(8), intent(in) :: v(3)
      real(8), intent(out) :: m(3, 3)
      m(1:3, 1) = [0.d0, -v(3), v(2)]
      m(1:3, 2) = [v(3), 0.d0, -v(1)]
      m(1:3, 3) = [-v(2), v(1), 0.d0]
      END FUNCTION

      END SUBROUTINE
