#!usr/bin/python

import pdb
import file_operations as fo

FNAME = '3rdFireTestSet.hdf5'


def main():
    data = fo.Data()
    fo.readFile(FNAME, data)
    #print (data._sample_rate)
    print("HELLO!")
    #data.release()

# pdb.set_trace()
# pass
if __name__ == "__main__":
    main()

    # print (sample_rate[()])