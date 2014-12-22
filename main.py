
import pdb
import file_operations as fo

FNAME = '3rdFireTestSet.hdf5'

def main():
    fo.readFile(FNAME)
    data = fo.Data(time_data,labels,sample_rate, pga_gain_code)
    print (data._sample_rate)

pdb.set_trace()
#pass
if __name__ == "__main__":
    main()

#print (sample_rate[()])