
filename = '3rdFireTestSet.hdf5'

import h5py

f = h5py.File(filename,'r')

time_data = f['/dru/capture/data']
labels = f['/dru/capture/labels']
sample_rate = f['/dru/capture/rdt/sample_rate']
pga_gain_code = f['/dru/capture/rdt/pga_gain_code']

print ("%s\t" % ("time_data"))

print (pga_gain_code[()])
#for i in range (len(time_data)):
#	print(time_data[i])
f.close()

#import pdb
#pdb.set_trace()
#pass