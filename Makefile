#-----------------------------------------------------------------------
#     This Makefile just prints a list of supported environments
#-----------------------------------------------------------------------
#+ This file is part of the aepy package.
#+
#+ Copyright (C) 2012-2018 Berk Onat
#+
#+ This Package and Source Code are LICENCED to be used only with 
#+ explicit permision from the auther above and proof of acknowledgement 
#+ from the auther. In any other case of distribution, mofification, 
#+ usage, code addition, merge, pull, recoding are subject to 
#+ LICENSE aquire. Please contact with author to buy a LICENSE ti use 
#+ the package.
#+
#+ This program is distributed in the hope that it will be useful, but
#+ WITHOUT ANY WARRANTY; without even the implied warranty of
#+ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

.PHONY: all

all:
	if [ ! -d "aenet" ]; then git clone https://github.com/berkonat/aenet.git; fi; \
	cd aenet/src && \
	patch < ../../sfsetup.patch && \
	patch < ../../generate.patch && \
	rm -rf f90wrap_*.f90 && \
	f90wrap -m aepy aeio.f90 aenet.f90 constants.f90 geometry.f90 input.f90 optimize.f90 potential.f90 random.f90 sfsetup.f90 trainset.f90 ext/chebyshev.f90 ext/feedforward.f90 ext/io.f90 ext/lclist.f90 ext/sfbasis.f90 ext/sortlib.f90 ext/symmfunc.f90 ext/timing.f90 ext/xsflib.f90 && \
	make clean && \
	cd ../lib && make && cd ../src && \
	make -f ../../Makefile.gfortran_serial && \
	patch < ../../f90wrap_lclist.patch && \
	patch < ../../f90wrap_aenet.patch && \
	patch < ../../f90wrap_potential.patch && \
	patch < ../../f90wrap_sfsetup.patch && \
	f2py-f90wrap --fcompiler=gfortran -I. -c -m _aepy -L../lib/ -llbfgsb -llapack -lblas f90wrap_*.f90 *.o

clean :
	rm -f *.o
	for f in *.mod; do rm -f $$f; done
	for f in *~; do rm -f $$f; done
