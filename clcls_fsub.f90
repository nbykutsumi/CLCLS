module clcls_fsub
!-------------------------------
CONTAINS
!-------------------------------
SUBROUTINE ret_pyyx_mergir(a1latBnd,a1lonBnd,a1latDat,a1lonDat, ny, nx, nl, a1y, a1x)
implicit none

integer         ny, nx, nl
!--- input -----
double precision,dimension(nx)  :: a1lonBnd ! Boundary
!f2py intent(in)                   a1lonBnd

double precision,dimension(ny)  :: a1latBnd ! Boundary
!f2py intent(in)                   a1latBnd

double precision,dimension(nl)  :: a1latDat, a1lonDat
!f2py intent(in)                   a1latDat, a1lonDat
!--- out  ------
integer,dimension(nl)           :: a1y, a1x
!f2py intent(out)                  a1y, a1x

!--- internal --
double precision                   lat0, lon0
double precision                   lat, lon
integer                            il
integer                            y, x, ytmp, xtmp
!--- para ------
double precision,parameter      :: dlat = 0.036385689d0
double precision,parameter      :: dlon = 0.036378335d0

!---------------
lat0 = a1latBnd(1)
lon0 = a1lonBnd(1)
!---------------
a1y = -9999
a1x = -9999
do il = 1,nl
    lon = a1lonDat(il)
    lat = a1latDat(il)
    xtmp = floor((lon-lon0)/dlon) + 1
    ytmp = floor((lat-lat0)/dlat) + 1

    ! check if x < nx
    if (xtmp.ge.nx)then
        xtmp = nx -1
    end if
    ! check if y < yx
    if (ytmp.ge.ny)then
        ytmp = ny -1
    end if

    ! check x
    if (lon.ge.a1lonBnd(xtmp))then
        if (lon.lt.a1lonBnd(xtmp+1))then
            x = xtmp
        else if (lon.lt.a1lonBnd(xtmp+2))then
            x = xtmp+1
        else
            print *,"check x",x,"lon=",lon
            print *,"lon0=",lon0,"dlon=",dlon
        end if
    else
        if (lon.ge.a1lonBnd(xtmp-1))then
            x = xtmp-1
        else
            print *,"check x",x,"lon=",lon
        end if
    end if

    ! check y
    if (lat.ge.a1latBnd(ytmp))then
        if (lat.lt.a1latBnd(ytmp+1))then
            y = ytmp
        else if (lat.lt.a1latBnd(ytmp+2))then
            y = ytmp+1
        else
            print *,"check y",y,"lat=",lat
        end if
    else
        if (lat.ge.a1latBnd(ytmp-1))then
            y = ytmp-1
        else
            print *,"check y",y,"lat=",lat
        end if
    end if

    ! set y and x
    a1y(il) = y-1
    a1x(il) = x-1

end do
return 
END SUBROUTINE
!-------------------------------
end module clcls_fsub
