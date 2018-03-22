# Jlsca tutorials
Examples on how to use [Jlsca](https://github.com/Riscure/Jlsca), the side channel analysis toolkit written in Julia.

## Prerequisites

* Julia (0.6.1 is tested), https://julialang.org
* IJulia, https://github.com/JuliaLang/IJulia.jl
* Jlsca package, https://github.com/Riscure/Jlsca
* PyCall and PyPlot packages, install in julia via Pkg.add()

It all works alike on Linux, Mac, and Windows.

Here is [a docker image built on top of Orka](https://github.com/ikizhvatov/Orka/tree/master/marvelsplus) with all the prerequisites (apart from some example tracesets).  

### Starting IJulia's Jupyter with threading

Jlsca's incremental correlation benefits from more threads. By default Julia only has 1 thread, but you can configure this by setting environment variable `JULIA_NUM_THREADS`. Start the notebook like this to give Julia 2 threads:

```
JULIA_NUM_THREADS=2 julia -e "using IJulia; notebook()"
```

## Trace formats

Working with any tool starts with the data formats. Jlsca natively works with trs format, originally used by Riscure Inspector, and in addition handles other formats.

* [Daredevil (split binary) format](https://github.com/SideChannelMarvels/Daredevil). Jlsca natively supports it for both reading and writing, and includes a converter to/from trs. Whitebox example notebook below shows how to do conversion.
* [ChipWhisperer project format](https://wiki.newae.com/File_Formats). Examples of how to convert data from CWP to trs are below in RHme2 notebooks. In case you would like to export a trs into CWP, here is the noteboook: [trs2cwp.ipynb](trs2cwp.ipynb).

## DPA on SW AES implementations

These are simple examples on how to do the SCA challenges of the [RHme2 embedded CTF](https://github.com/Riscure/Rhme-2016).

* [piece of SCAke](rhme2-pieceofscake.ipynb) - correlation power analysis attack on unprotected AES-128
* [still not SCAry](rhme2-stillnotscary.ipynb) - linear regression analysis attack on AES-128 with a misalignment countermeasure
* [SCAlate](rhme2-escalate.ipynb) - correlation power analysis attack on AES-128 with a misalignment countermeasure

Tarballs with power traces available at https://drive.google.com/drive/folders/0B2slHLSL3nXaTFBWMUxHSkNmSTg, shasums included.

Here are the external writeups showing how to adapt examples above to do [RHme3 SCA qualifier challange](https://github.com/Riscure/Rhme-2017/tree/master/prequalifications/Tracing%20the%20Traces): [[1]](https://github.com/ResultsMayVary/ctf/tree/master/RHME3/tracing), [[2]](https://github.com/x8-999-github/cw-projects-experiments/blob/master/tracing_the_traces/tracing_the_traces_jlsca.ipynb), [[3]](https://gist.github.com/dqi/88c86e484fc9302694837810680d2023). Note that due to recent changes in Jlsca these writeups need minor adjustments to be runnable.

## Second-order DPA

* [Second-order DPA on the ASCAD traceset](secondorder-ascad/second-order-cpa-ascad.jl)

## DPA on whitebox implementations

* [RHme 2017 qualifier whitebox challenge](rhme2017-qual-wb.ipynb). Traces [here in the tarball](rhme2017-qual-wb-traces.tar.bz2).

## HPC (runnig on a computing cluster)

Jlsca can be run on a cluster of Linux machines.

* [HPC example](HPC.md) tested on the [Radboud University cluster](http://wiki.science.ru.nl/cncz/index.php?title=Hardware_servers&setlang=en#.5BReken-.5D.5BCompute_.5Dservers.2Fclusters) 

## DPA on HMAC-SHA

* [DPA on HMAC-SHA1](hmacsha1pinata.ipynb) running on STM32F417 with hardware SHA accelerator. This is an advanced example. Traceset [here](https://drive.google.com/open?id=0B-My9BsChztIM21sdWxWRWRrZGs).
