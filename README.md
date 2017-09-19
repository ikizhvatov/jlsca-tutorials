# Jlsca tutorials
Examples on how to use Jlsca, the side channel analysis toolkit written in Julia.

## Prerequisites

* Julia (0.6.0 is tested), https://julialang.org
* IJulia, https://github.com/JuliaLang/IJulia.jl
* Jlsca package, https://github.com/Riscure/Jlsca
* PyCall and PyPlot packages, install in julia via Pkg.add()

It all works alike on Linux, Mac, and Windows.

### Starting IJulia's Jupyter with threading

Jlsca's incremental correlation benefits from more threads. By default Julia only has 1 thread, but you can configure this by setting environment variable 'JULIA_NUM_THREADS'. Start the notebook like this to give Julia 2 threads:

```
JULIA_NUM_THREADS=2 julia -e "using IJulia; notebook()"
```

## Examples RHme2

These are simple examples on how to do the SCA challenges of the [RHme2 embedded CTF](https://github.com/Riscure/Rhme-2016).

* [piece of SCAke](rhme2-pieceofscake.ipynb) - correlation power analysis attack on unprotected AES-128
* [still not SCAry](rhme2-stillnotscary.ipynb) - linear regression analysis attack on AES-128 with a misalignment countermeasure
* [SCAlate](rhme2-escalate.ipynb) - correlation power analysis attack on AES-128 with a misalignment countermeasure
    * A writeup showing how to adapt this example example to do [RHme3 SCA qualifier challange](https://github.com/Riscure/Rhme-2017/tree/master/prequalifications/Tracing%20the%20Traces): https://github.com/ResultsMayVary/ctf/tree/master/RHME3/tracing
    * Another one: https://github.com/x8-999-github/cw-projects-experiments/blob/master/tracing_the_traces/tracing_the_traces_jlsca.ipynb
    * Yet another one (with a rather weird key verification): https://gist.github.com/dqi/88c86e484fc9302694837810680d2023

Tarballs with power traces available at https://drive.google.com/drive/folders/0B2slHLSL3nXaTFBWMUxHSkNmSTg, shasums included.

## Examples whitebox

* [RHme 2017 qualifier whitebox challenge](rhme2017-qual-wb.ipynb). Traces [here in the tarball](rhme2017-qual-wb-traces.tar.bz2).

## Example HPC (runnig on a computing cluster)

Jlsca can be run on a cluster of Linux machines.

* [HPC example](HPC.md) tested on the [Radboud University cluster](http://wiki.science.ru.nl/cncz/index.php?title=Hardware_servers&setlang=en#.5BReken-.5D.5BCompute_.5Dservers.2Fclusters) 

## Examples SHA (HMAC)

* [DPA on HMAC-SHA1 running on STM32F417 with hardware SHA accelerator](hmacsha1pinata.ipynb). This is an advanced example.
