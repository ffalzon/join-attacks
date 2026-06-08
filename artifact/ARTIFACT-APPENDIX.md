# Artifact Appendix

Paper title: Beyond the Output: Inference Attacks on Private Set Union and
Multi-Key Private Matching

Requested Badge(s):
  - [x] **Available**
  - [x] **Functional**
  - [x] **Reproduced**

Authors can provide this content _either_ as a separate file in their artifact
_or_ as part of their existing documentation (e.g., `README.md`). In the latter
case, you should have the same section titles as in this template.

This template includes several placeholders. When filling in this template for
their artifact, the authors should:

1. Remove this note.
2. Delete the sections that are _not_ required for the badge(s) they are
   applying for.
3. Omit suffixes of the form "(required/encouraged for badge ...)" from the
   section titles.
4. Authors should not leave the placeholder descriptions initially provided with
   this file into the submitted version with their artifact.

While this template is provided for artifact review, you should write your
instructions for someone trying to reuse your artifact in the future (i.e., not
an artifact reviewer).

## Description

This repository contains the artifacts accompanying the paper "Beyond the Output: Inference Attacks on Private Set Union and Multi-Key Private Matching" by Andrea Raguso, Francesca Falzon, Tianxin Tang, and Kenneth Paterson, published at PETs 2026.
In the paper, we present several inference attacks, which allows an adversary that is allowed to interact with an ideal functionality to gain information about the non-adversarial inputs. We present attacks against the following functionalities: PSU, PSU-CA, the ideal functionality of Meta's multi-key PrivateID protocol (MK-PrivateID) $\mathcal{F}_{\textsf{MKPM}}$, and the extended functionality of MK-PrivateID that includes additional protocol leakage $\mathcal{F}_{\textsf{L-MKPM}}$.

This artifact repository contains implementations of said attacks and the corresponding functionalities, as well as a measurement infrastructure to evaluate the efficiency of our attacks. We measure both the attack runtimes, as well as the number of queries (ideal functionality evaluations) performed by the attack.

The artifact broadly has three stages: Data generation for the attacks against MK-PrivateID, performing measurements, and formatting data.
The final output of this artifact is a set of CSV files which contain the measurements which we plot in our paper.

### Security/Privacy Issues and Ethical Concerns
Our artifact consists of simple measurements run locally on a single core (per experiment). Our attacks are run on synthetically generated data.
No security features are disabled and no sensitive data is being used.

## Basic Requirements

### Hardware Requirements
While our experiments could in principle be carried out on a laptop,
the time to perform all measurements would exceed any practical time frame.
We therefore ran our experiments on a server with the following specifications:
- 64 Core AMD EPYC 7742 2.25GHz Processor
- 512GB DDR4 3200MHz ECC Server Memory

Our test suite requires 61 cores and used roughly 10GB of memory.
The AMD EPYC 7742 processor has 64 physical and 128 logical cores, 
where the logical cores $i$ and $(i+64)$ are mapped to the same physical core.
We use this when assigning experiments to physical cores. 
Concretely, our measurement scripts bind different experiments to the (logical) cores $i$ and $i+64$ for $0\leq i\leq 60$ using `taskset`.

### Software Requirements (Required for Functional and Reproduced badges)
1. **OS**: Our server has Ubuntu 24.04.4 LTS installed, although our experiment suite should run on other Linux installations as well.
The docker file we provide is based on Debian 13.5 "Trixie". 
2. **OS Packages**: We use `taskset` and `tmux` to assign the experiments to cores and keep sessions alive.
3. **Packaging**: We provide a Docker file with the necessary OS and Python packages installed. We use docker version 29.5.2.
4. **Programming language**: Our experiments are implemented in Python. We use Python 3.12.3.
5. **Packages**: We require the `Faker` package for generating synthetic data
6. **ML Models**: Our artifact requires no machine learning models.
7. **Data Sets**: Our data sets are generated synthetically and the script for doing so is contained in this artifact. However, since the generation takes some time, we include the data sets we used for our measurements in the artifact as well. They are located under `experiment_data/paper`.

### Estimated Time and Storage Consumption 
The artifact should consume no more than 1GB of disk space.
Assuming Docker is installed, the environment can be set up and verified in under 30 minutes.

Running the full measurement suite with the same number of iterations as we did in our paper takes 30 human-minutes and roughly 250 compute-hours.

## Environment

### Accessibility

This artifact is accessible from the public Github repository 
[https://github.com/deRaguso/mkpid-attacks-artifact](
https://github.com/deRaguso/mkpid-attacks-artifact/tree/main).

### Set up the environment

Start by cloning the repository and changing your current working directory to the repository.

```bash
git clone git@github.com:deRaguso/mkpid-attacks-artifact.git
cd mkpid-attacks-artifact
```

We provide a docker file with the necessary software dependencies, which should be built first. Please make sure that Docker is installed on your system.

```bash
docker build -t artifact_image .
```

### Testing the Environment

The environment can be tested by running the experiment suite on very small test data sets. To this end, launch the Docker container, attach the current working directory as a volume, set the context to be
that volume, and provide an interactive bash terminal:

```bash
docker run --rm -it -v $.:/workspaces/artifact \
    -w /workspaces/artifact \
    --entrypoint bash artifact_image
```

Then within the Docker container, run:

```bash
./test.sh
```
The test script will first check that the logical CPUs 0-60 and 64-124 are available and that processes can be bound to them.
Next, it checks that tmux is functional by starting a dummy tmux session.
It then generates a range of small data sets, which are stored under `experiment_data/small`. Finally, our measurement suite is run on said data sets. 
The experiments are run sequentially, but each experiment is bound to the same processor as it's real (large) counterpart.
To ensure that any Python exceptions are clearly visible, we run the experiments without any informational console outputs apart from showing, which cores are being tested. 
This should only take a few minutes, and you should see no error messages or exceptions.

The measurements are stored under `measurements/small`. There should be six files, corresponding to the six attacks shown in the evaluation section of the paper, see the outline below.
Finally, format the data with:

```bash
python3 format_measurements.py measurements/small
```
This should result in the file tree shown below. The directory `measureements/small` should contain 100 CSV files. If all files are present, the test was successful.

```
measurements/small
├── Baseline.csv
├── MKPSI.csv
├── PSU.csv
├── PSUCA.csv
├── RecordEnumeration.csv
├── Snake.csv
└── formatted
    └── MKPSI_queries_over_mr
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── MKPSI_queries_over_n
        ├── V100MR0.0.csv
        ├── V100MR0.1.csv
            ...
        └── V100MR1.0.csv
    └── MKPSI_recovery_over_QB
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── MKPSI_time_over_MR
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── MKPSI_time_over_n
        ├── V100MR0.0.csv
        ├── V100MR0.1.csv
            ...
        └── V100MR1.0.csv
    └── PSUCA_queries_over_mr
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── PSUCA_queries_over_n
        ├── V100MR0.0.csv
        ├── V100MR0.1.csv
            ...
        └── V100MR1.0.csv
    └── PSUCA_recovery_over_QB
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── PSUCA_time_over_MR
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── PSUCA_time_over_n
        ├── V100MR0.0.csv
        ├── V100MR0.1.csv
            ...
        └── V100MR1.0.csv
    └── PSU_time_over_mr
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── PSU_time_over_n
        ├── V100MR0.0.csv
        ├── V100MR0.1.csv
            ...
        └── V100MR1.0.csv
    └── recon_time_over_MR
        ├── V100T50.csv
        ├── V100T60.csv
            ...
        └── V100T150.csv
    └── recon_time_over_n
        ├── V100MR0.0.csv
        ├── V100MR0.1.csv
            ...
        └── V100MR1.0.csv
```

## Artifact Evaluation 

Our artifact should confirm the time and query measurements presented in Section 8 ("Experimental Evaluation") and Appendix H ("Additional Evaluation Results") in our paper. 
Since all experiments are executed simultaneously, we present this as one claim and describe our measurement suite as one large experiment.

### Main Results and Claims

#### Main Result: Attack Efficiency

The main result we show with this artifact is that our attacks can be carried out efficiently, i.e., with only a small overhead on top of the normal protocol executions. For all attacks, we measure the runtime.
For the attacks which perform an adaptive number of queries, 
we additionally measure the number of queries (ideal functionality evaluations) performed by the attack, as well as the performance of the attack under limited query budgets.

In our work, we show the following plots, which we group by attack for this document. 

1. **PSU-Diff**: Runtimes largely follow from Python's implementation of set operations.
   1. Runtime over intersection ratio $\rho = |T\cap Y| / |T|$ (Figure 9a)
   2. Runtime over target set size $|T|$ (Figure 9b). 
2. **PSU-CA-SearchTree**
   1. Number of queries over target set size $|T|$ (Figure 10a). Grows linearly.
   2. Runtime over intersection ratio $\rho$ (Figure 11a). Symmetric w.r.t. values of $\rho$: values of $\rho$ close to $0$ or $1$ yield smaller runtime measurements, values close to $0.5$ yield the highest measurements.
   3. Runtime over target set size $|T|$ (Figure 11c). Grows linearly.
   4. Number of queries over intersection ratio $\rho$ (Figure 18a). Same behavior as in point 2.2.
   5. Recovered fraction of the intersection and set difference, and total inferred membership information over allocated query budget (Figure 19) 
3. **MKPM-SearchTree**
   1. Number of queries over target set size $|T|$ (Figure 10b). Grows linearly. 
   2. Runtime over match rate $\eta$ (Figure 11b). See PSU-CA-SearchTree, point 2.2.
   3. Runtime over target set size $|T|$ (Figure 11d). Grows linearly.
   4. Number of queries over match rate $\eta$ (Figure 18b). Same behavior as in points 2.2, 2.4, and 3.2.
4. **$T$-Reconstruction attacks** (Baseline, EnumAttack, SnakeAttack)
   1. Runtime over match rate $\eta$ (Figure 10a). Runtimes remain roughly constant and are thus largely independent of $\eta$.
   2. Runtime over target set size $|T|$ (Figure 10b). Grows linearly.

#### Experiment: Run Measurement Suite
- Time: 20 human-minutes + 250 compute-hours

The experiment runs our measurement suite as described above on data described in the paper.
For our attacks against the PSU and PSU-CA functionalities, the experiment data consists of a recovery set $Y$ of a fixed size and
a target set $T$ whose size we vary from $50\%$ to $150\%$ of $|Y|$. Both sets contain randomly sampled integers.
Furthermore, we vary the intersection ratio $\rho := |T \cap Y|/|T|$ from $0\%$ to $100\%$. For the attack against PSU-CA, we further vary the allocated query budget from $10\%$ to $100\%$ of the theoretical upper bound of queries. This is not necessary for the attack against PSU, since it always performs two queries.
We set $|Y|=10^6$ for the attack against PSU and $|Y|=10^4$ for the attack against PSU-CA.

The data for the attacks against $\mathcal{F}_{\textsf{L-MKPM}}$ is generated very similarly, with the exception that instead of simple sets, we now consider the sets of records located under `experiment_data/paper`. 
Correspondingly, we vary the slightly more complicated match rate $\eta$ instead of the intersection ratio $\rho$, see Section 8 of the paper.
We set $|Y| = 10^4$.

To start the experiments, run:
```bash
./run_experiments.sh
```

The measurement scripts repeat each experiment $50$ times. The raw measurements are stored in `measurements/large`.
This will take a long time. Once the command `tmux ls` shows no sessions of the form `mpmc-chunk<i>` or `PSU<i>`, all individual experiments are completed. 
You can then format the measured data.

```bash
python3 format_measurements.py measurements/large
```

The result is a similar file tree as shown in [Testing the Environment](#testing-the-environment).
The measurement data reported within those (formatted) files (in `measurements/large/formatted`) can be directly compared to the measurement data we use for the plots in our paper, which we provide in `measurements/paper`. 
Since each experiment is repeated $50$ times and we report the average, we do not expect any large deviations from the provided results.
However, we did not run our experiments within a docker container, which may cause some differences in time measurements. 


## Limitations
For the measurements reported in the paper, we did not run our experiments in a docker container, but on the server's OS (Ubuntu 24.04.4 LTS) directly. While we do not expect it, this may result in differences in the runtime measurements. These are hard to estimate without re-running the experiments.

## Notes on Reusability

Our measurement infrastructure is flexible with respect to the considered input sizes. Running the attacks against MK-PrivateID with larger inputs can be done by generating larger data sets using `gen_MKPID_data.py`. The input sizes for the attacks against PSU and PSU-CA can be changed by modifying the parameters for `measure_PSU.py` in `run_experiments.sh`.
Our infrastructure includes code to measure the runtime and required number of queries for any attack, as well as re-usable implementations of the relevant ideal functionalities we consider in the paper. New attacks can therefore be added by placing their implementation in the `attacks` folder and extending the measurement scripts accordingly. 