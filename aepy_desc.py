import aepy.aepy_fbind as aepy
import numpy as np
from ase import Atoms
from ase.io import read

PI = aepy.constants.pi

types = ['Ti', 'O']

#files = [
#    "../../../../aenet-example-02-TiO2-Chebyshev/01-generate/Ti.fingerprint.stp",
#    "../../../../aenet-example-02-TiO2-Chebyshev/01-generate/O.fingerprint.stp"
#    ]

files = [
    "tests/Ti.fingerprint.stp",
    "tests/O.fingerprint.stp"
    ]

ntypes = len(types)
tdict = {}
for ti, tv in enumerate(types):
    tdict[tv] = ti + 1

stp_list = aepy.sfsetup.Setup_Xntypes_Array(ntypes)
stp_list.init_array_items()

for fi, fv in enumerate(files):
    stp_list.items[fi] = aepy.sfsetup.read_setup_parameters(fv, np.array(types[fi], dtype='S2', order='F'))
    aepy.sfsetup.stp_print_info(stp_list.items[fi])

rmin, rmax = aepy.sfsetup.stp_get_range(ntypes, stp_list)

sfb = []
for si, stp in enumerate(stp_list.items):
    if 'chebyshev' in stp.sftype.strip().lower():
        sfb.append(aepy.sfsetup.setup_basis_chebyshev(stp))
    #elif 'behler2011' in stp.sftype.strip().lower():
    #    sfb.append(aepy.sfsetup.setup_symmfunc_behler2011(si+1, stp))

nsf_max = 0
rcmin = rmin
rcmax = rmax
for sf in stp_list.items:
    if sf.rc_min < rcmin: rcmin = sf.rc_min
    if sf.rc_max > rcmax: rcmax = sf.rc_max
    if sf.nsf > nsf_max: nsf_max = sf.nsf

print('Global Rc_min : ' + str(rcmin))
print('Global Rc_max : ' + str(rcmax))
print('Global N_sf_max : ' + str(nsf_max))

nnb_max = 0
nnb_max = aepy.lclist.lcl_nmax_nbdist(rcmin, rcmax)
print('Max # of Neighbors : ' + str(nnb_max))

aepy.sfsetup.stp_init(ntypes, stp_list, nnb_max)

nbcoo = np.zeros((3,nnb_max), dtype=np.float, order='F')
nbdist = np.zeros(nnb_max, dtype=np.float, order='F')
nbtype = np.zeros(nnb_max, dtype=np.int32, order='F')
#sfderiv_i = np.asfortranarray(np.zeros((3,nsf_max), dtype=np.float32))
#sfderiv_j = np.asfortranarray(np.zeros((3,nsf_max,nnb_max), dtype=np.float32))

db = read('tests/structure0001.xsf')
if isinstance(db, Atoms):
    pbc = True if np.any(db.pbc) else False
    atomType = np.array([tdict[i] for i in db.get_chemical_symbols()], dtype=np.int32)
    latVec = np.asfortranarray(db.cell.T)
    recLattVec = aepy.geometry.geo_recip_lattice(latVec)
    cooLat = np.matmul(np.array(recLattVec, order='F'), np.asfortranarray(db.positions.T))/(2.*PI)
    aepy.lclist.lcl_init(rcmin, rcmax, 
		    latVec, len(db.numbers), 
		    atomType, cooLat, pbc)
    #aepy.lclist.lcl_print_info()
    desc = []
    for ai, atom in enumerate(db):
	nnb = nnb_max
	itype1 = atomType[ai]
	iatom = ai + 1
        #print(ai,itype1)
	nnb, stat = aepy.lclist.lcl_nbdist_cart(iatom, nnb, nbcoo, nbdist, r_cut=rcmax, nbtype=nbtype)
	#aepy.sfsetup.stp_eval(itype1, db.positions[ai], nnb, nbcoo, nbtype, stp_list.items[itype1-1], sfval)
	nsf = stp_list.items[itype1-1].nsf
        sfval = np.zeros(nsf_max, dtype=np.float, order='F')
	if 'chebyshev' in stp_list.items[itype1-1].sftype.strip().lower():
	    aepy.sfbasis.sfb_eval(sfb[itype1-1], itype1, db.positions[ai], nnb, nbtype, nbcoo, nsf, sfval)
        elif 'behler2011' in stp_list.items[itype1-1].sftype.strip().lower():
	    #aepy.sfsetup.stp_eval(itype1, db.positions[ai], nnb, nbcoo, nbtype, stp_list.items[itype1-1], sfval)
	    aepy.symmfunc.sf_fingerprint(itype1, db.positions[ai], nnb, nbcoo, nbtype, nsf, sfval)
	desc.append(sfval)
    aepy.lclist.lcl_final()

print(desc)

