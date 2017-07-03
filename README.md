# Jlsca tutorials
Examples on how to use Jlsca, the side channel analysis toolkit written in Julia.

## Prerequisites

* Julia (0.6.0 is tested), https://julialang.org
* IJulia, https://github.com/JuliaLang/IJulia.jl
* Jlsca package, https://github.com/Riscure/Jlsca
* Pycall and PyPlot packages, install in julia via Pkg.add()

It all works alike on Linux, Mac, and Windows.

## Examples RHme2

These are examples on how to do the SCA challenges of the [RHme2 embedded CTF](https://github.com/Riscure/Rhme-2016).

* [piece of SCAke](rhme2-pieceofscake.ipynb) - correlation power analysis attack on unprotected AES-128
* [still not SCAry](rhme2-stillnotscary.ipynb) - linear regression analysis attack on AES-128 with a misalignment countermeasure
* [eSCAlate](rhme2-escalate.ipynb) - correlation power analysis attack on on AES-128 with a misalignment countermeasure

Tarballs with power traces available at https://drive.google.com/drive/folders/0B2slHLSL3nXaTFBWMUxHSkNmSTg

### Starting IJulia's Jupyter with threading

Jlsca's incremental correlation benefits from more threads. By default Julia only has 1 thread, but you can configure this by setting environment variable 'JULIA_NUM_THREADS'. Start the notebook like this to give Julia 2 threads:

```
JULIA_NUM_THREADS=2 julia -e "using IJulia; notebook()"
```

## Example HPC (runnig on a computing cluster)

Jlsca can be run on a cluster of Linux machines.

* [HPC example](HPC.md) tested on the [Radboud University cluster](http://wiki.science.ru.nl/cncz/index.php?title=Hardware_servers&setlang=en#.5BReken-.5D.5BCompute_.5Dservers.2Fclusters) 
