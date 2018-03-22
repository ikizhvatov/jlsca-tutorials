#!/usr/bin/env python

# Convert the raw ASCAD traceset from from https://github.com/ANSSI-FR/ASCAD into trs format.
# Loosely based on ASCAD_generate.py
# Requries Trace.py with write support

import h5py
import numpy as np
import Trace as trs # python interface to trs format

ascad = h5py.File("ASCAD_data/ASCAD_databases/ATMega8515_raw_traces.h5", "r") # change this to your location of the ASCAD database
traces = ascad['traces']
plaintexts = ascad['metadata']['plaintext']
ciphertexts = ascad['metadata']['ciphertext']

# default sample range used in ASCAD and in Benjamin Timon's paper for key byte 3 recovery
min_range = 45400
max_range = 46100

newTs = trs.TraceSet()
newTs.new("ASCAD.trs", 0, trs.TraceSet.CodingByte, len(np.hstack((plaintexts[0], ciphertexts[0]))), max_range - min_range)

for i in range(len(traces)):
    newTs.addTrace(trs.Trace(b'', np.hstack((plaintexts[i], ciphertexts[i])), traces[i,min_range:max_range]))
newTs.close()

exit()

# The ASCAD traceset corect key, for reference
# key = [77, 251, 224, 242, 114, 33, 254, 16, 167, 141, 74, 220, 142, 73, 4, 105]
