# Jlsca and High-Performance Computing

Jlsca can be run on a cluster of Linux machines. Here is an example tested on the [Radboud University cluster](http://wiki.science.ru.nl/cncz/index.php?title=Hardware_servers&setlang=en#.5BReken-.5D.5BCompute_.5Dservers.2Fclusters).

The example is run from the login node on several machines in the cluster. The login node and the machines on the cluster share the same user home folder (mounted over NFS) where Julia is installed and the traceset is located.

This example uses the traceset from testcase01 of https://github.com/ikizhvatov/dpa-tools-benchmarking.

### 1. Environment setup

To run Julia on the cluster, some general preparation is necessary.

1. Setup passwordless SSH login from the login node to the used cluster nodes. Passwordless means:

    * Setup the login with SSH key using `ssh-copy-id` (and generating the SSH key pair if not yet exists). This is done from the login node once per node where the workers will be deployed.
    * If needed, cache the SSH private key password with `ssh-agent` and `ssh-add`. This is done once every login to the login node (and can be put in one of the login scripts of course).

2. Install Julia by uncompressing a generic Linux tarball from https://julialang.org/downloads/ in the home directory. 

3. Setup the environment, such that every node knows where Julia is and with how many threads to run it. I added the folowing to the `.profile`:

```bash
export PATH=/home/ilyak/julia-903644385b/bin:$PATH
NCORES=`grep "^cpu cores" /proc/cpuinfo | sort -u | awk '{print $4}'`
export JULIA_NUM_THREADS=${NCORES}
```

### 2. Example preparation for the multi-node setting

The exisiting code needs a simple modification to be run on the cluster.

1. Clone the https://github.com/ikizhvatov/dpa-tools-benchmarking repo into the home folder on the cluster to get the traceset and the attack code that is used as the base.

2. in the `tescase01`, add a line to the top of (a copy of) `main-inccpa.jl` with the specification of the nodes where workers will be deployed. In my case four nodes:

```julia
addprocs([("cn89.science.ru.nl", 4), ("cn88.science.ru.nl", 2), ("cn13.science.ru.nl", 2), ("cn99.science.ru.nl", 2)]; tunnel=true, exeflags="--depwarn=no")
```

Each node spec (optionally) includes the number of workers on each node. Normally, the number of workers is equal to the number of physical CPUs on the node.

On some clusters, even no modifications to the code woudl be necessary, but a `--machinefile` option passing julia a list of nodes from a file. In my case, the `tunnel` option appeared to be necessary for the processes to communicate between the nodes, so I used the `addprocs` way.

The `--depwarns=no` was added to avoid warnings from Julia version 0.6.0, it may not be necessary here and below any more as the Jlsca code has been adapted.

### 3. Execution

Execute the code normally from the login node:

```bash
ilyak@lilo5:~/dpa-tools-benchmarking/testcase01$ julia --depwarn=no main-inccpa-multinode.jl aes128_sb_ciph_deadbeefcafebabe1122334455667788.trs
```

It will take some time to start up, and then you can observe the script printing out a large number of workers. On the worker nodes, you can observe several julia processes spawned and the load going up.

The execution of this example in my case took 100 seconds.

### 4. Future work

* Profile the code in the multi-node setting, identify bottlenecks and improve
* Make it possible to use a machine with a diffent Julia environment to launch the code. See the following question: https://discourse.julialang.org/t/using-remote-workers-on-linux-from-mac-os-master/4395
* Utilise [ClusterManagers](https://github.com/JuliaParallel/ClusterManagers.jl)
