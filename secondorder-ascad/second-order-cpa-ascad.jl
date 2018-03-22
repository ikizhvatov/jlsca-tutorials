# Script version of the second order attack example using the ASCAD traceset

addprocs(2) # add 2 workers (good for 2 CPU cores)

@everywhere begin
    using Jlsca.Trs
    using Jlsca.Sca
end

# configure attack parameters
nrTraces = 1000 
fname = "ASCAD.trs"
keyByteNum = 3   # key byte to attack; ASCAD examples and truncated traceset are for the 3rd key byte
condavg = false  # use conditional leakage averaging

# set up the attack
attack = AesSboxAttack()
attack.xor = false
if condavg
    anal = CPA()
else
    anal = IncrementalCPA()
end
anal.leakages = [HW()]
params = DpaAttack(attack,anal)
maxCols = 150000 # number of columns that go in one tile in correlation computation; can be larger for large RAM sizes
params.maxCols = maxCols
params.maxColsPost = maxCols
params.targetOffsets = [keyByteNum]

# open the traceset
@everywhere trs = InspectorTrace($fname)

# add the second-order combining pass over traces
@everywhere addSamplePass(trs, SecondOrderPass(AbsDiff()))

if condavg
    # use conditional leakge averaging
    @everywhere setPostProcessor(trs, CondAvg(SplitByTracesBlock()))
else
    # use incremental correlation computation (like in Daredevil or Inspector)
    @everywhere setPostProcessor(trs, IncrementalCorrelation(SplitByTracesBlock()))
end

# run the attack
sca(DistributedTrace(), params, 1, nrTraces)

# graceful completion
@everywhere popSamplePass(trs)
@everywhere popSamplePass(trs)
@everywhere close(trs)
