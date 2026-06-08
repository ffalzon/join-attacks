# Artifact Appendix

Paper title: Beyond the Output: Inference Attacks on Private Set Union and
Multi-Key Private Matching

Requested Badge(s):
  - [x] **Available**
  - [ ] **Functional**
  - [ ] **Reproduced**

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

This artifact repository contains implementations of said attacks and the corresponding functionalities, as well as a measurement infrastructure to evaluate the efficiency of our attacks. 

The artifact broadly has three stages: Data generation for the attacks against MK-PrivateID, performing measurements, and formatting data.
The final output of this artifact is a set of CSV files which contain the measurements which we plot in our paper.

### Security/Privacy Issues and Ethical Concerns
Our artifact consists of simple measurements run locally on a single core (per experiment).
No security features are disabled and no sensitive data is used.

## Basic Requirements (Required for Functional and Reproduced badges)

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
3. TODO
4. **Programming language**: Our experiments are implemented in Python. We use Python 3.12.3.
5. **Packages**: We require the `Faker` package for generating synthetic data
6. **ML Models**: Our artifact requires no machine learning models.
7. **Data Sets**: Our data sets are generated synthetically and the script for doing so is contained in this artifact. However, since the generation takes some time, we include the data sets we used for our measurements in the artifact as well. They are located under `experiment_data/paper`.





Replace this with the software required to run your artifact and its versions,
as follows.

1. List the OS you used to run your artifact, along with its version (e.g.,
   Ubuntu 22.04). If your artifact can only run on a specific OS or a specific
   OS version, list it and explain why here. In general, your artifact reviewers
   will probably have access to a machine with a different OS or different OS
   version than yours; they should still be able to run appropriately packaged
   artifacts.
2. List the OS packages that your artifact requires, along with their versions.
3. Artifact packaging: If you use a container runtime (e.g., Docker) to run the
   artifact, list the container runtime and its version (e.g., Docker 23.0.3).
   If you use VMs, list the hypervisor (e.g., VirtualBox) to run the artifact.
4. List the programming language compiler or interpreter you used to run your
   artifact (e.g., Python 3.13.7). Your Docker image or VM image should have
   this version of the programming languages installed already. Your Dockerfile
   should start from a base image with this programming language version.
5. List packages that your artifact depends on, along with their versions. For
   example, Python-based privacy-preserving machine learning artifacts typically
   require `numpy`, `scipy`, etc. You may point to a file in your artifact with
   this list, such as a `requirements.txt` file. If you rely on proprietary
   software (e.g. Matlab R2025a), list this here and consider providing access
   to reviewers through HotCRP.
6. List any Machine Learning Models required to run your artifact, along with
   their versions. If your model is hosted on a different repository, such as on
   Zenodo, then your artifact should download it automatically (same for
   datasets). If a required ML model is _not_ in your artifact, provide a dummy
   model to demonstrate the functionality of the rest of your artifact.
7. List any datasets required to run your artifact. If any required dataset is
   not in your artifact, you should provide a synthetic dataset that showcases
   the expected data format.

### Estimated Time and Storage Consumption (Required for Functional and Reproduced badges)

The artifact should consume no more than 1GB of disk space.
Once access to adequate hardware is secured, the environment can be set up and verified in roughly 30 minutes.

Running the full measurement suite with the same number of iterations as we did in our paper takes toughly 250 compute-hours.
Formatting the measured data to obtain the desired CSV files can also be done with a single command and is very fast.

## Environment (Required for all badges)

In the following, describe how to access your artifact and all related and
necessary data and software components. Afterward, describe how to set up
everything and how to verify that everything is set up correctly.

### Accessibility (Required for all badges)

Replace the following by a description of how to access your artifact via
persistent sources. Valid hosting options are institutional and third-party
digital repositories (e.g., GitHub, Gitlab, BitBucket, Zenodo, Figshare, etc.).
Please do not use personal web pages or cloud storage services like Google
Drive, Dropbox, etc.

Note that once your artifact evaluation is finalized and a badge decision has
been made, artifact chairs will collect a stable and persistent reference to
your artifact to list on the website. For version-controlled repositories (e.g.,
Git repositories), this will be a specific commit-id or tag.

You _should not_ link to a specific commit here at submission time, as changes
will likely happen during the evaluation process to address the reviewers'
feedback, resulting in the link being out-of-date. Instead, you may link to the
latest commit in your branch (e.g. main) as follows:
https://github.com/PoPETS-AEC/example-docker-python-pip/tree/main

### Set up the environment (Required for Functional and Reproduced badges)

Replace the following by a description of how one should set up the environment
for your artifact, including downloading and installing dependencies and the
installation of the artifact itself (i.e., from the very first download or clone
command one should perform). Be as specific as possible here. If possible, use
code segments to simplify the workflow, e.g.,

```bash
git clone git@github.com:PoPETS-AEC/example-docker-python-pip.git
docker build -t example-docker-python-pip:main .
```
This artifact is obtainable from the following public github repository: TBD.
Please change your working directory into the artifact repository.
We provide a docker file with the necessary software dependencies, which should be built first.

```bash
git clone git@github.com:PoPETS-AEC/example-docker-python-pip.git
cd <FOLDER NAME>
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
It then generates a range of small data sets, which are stored under `experiment_data/small`. Finally, our measurement suite in run on said data sets. This should take a few minutes at most.
If the command `tmux ls` (within the docker container) shows no sessions of the format `mpmc-chunk<i>` or `PSU<i>`, all experiments have been carried out.

The measurements are stored under `measurements/small`. There should be six files, corresponding to the six attacks shown in the evaluation section of the paper, see the outline below.


Next format the data with:

```bash
python3 format_measurements.py measurements/small
```
This should result in the following file tree:
TODO

## Artifact Evaluation (Required for Functional and Reproduced badges)

Our artifact should confirm the time and query measurements presented in Section 8 ("Experimental Evaluation") in our paper. 
Since all experiments are executed simultaneously, we present this as one claim and describe our measurement suite as one large experiment.

### Main Results and Claims

#### Main Result: Attack Efficiency


Describe the results in 1 to 3 sentences. Mention what the independent and
dependent variables are; independent variables are the ones on the x-axes of
your figures, whereas the dependent ones are on the y-axes. By varying the
independent variable (e.g., file size) in a given manner (e.g., linearly), we
expect to see trends in the dependent variable (e.g., runtime, communication
overhead) vary in another manner (e.g., exponentially). Refer to the related
sections, figures, and/or tables in your paper and reference the experiments
that support this result/claim. See example below.

#### Experiment: Run Measurement Suite
- Time: 20 human-minutes + 250 compute-hours

The experiment runs our measurement suite as described above on data described in the paper.
For our attacks against the PSU and PSU-CA functionalities, the experiment data consists of a victim set $Y$ of a fixed size and
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

#### Experiment 2: Example Name

- Time: 10 human-minutes + 3 compute-hours
- Storage: 20GB

This example experiment reproduces
[Main Result 2: Example Name](#main-result-2-example-name), the following script
will run the simulation automatically with the different parameters specified in
the paper. (You may run the following command from the example Docker image.)

```bash
python3 main.py
```

Results from this example experiment will be aggregated over several iterations
by the script and output directly in raw format along with variances and
standard deviations in the `output-folder/` directory. You will also find there
the plots for "Figure 1a" in `.pdf` format and the table for "Table 3" in `.tex`
format. These can be directly compared to the results reported in the paper, and
should not quantitatively vary by more than 5% from expected results.


## Limitations
For measurements reported in the paper, we did not run our experiments in a docker container, but on the server's OS (Ubuntu 24.04.4 LTS) directly. While we do not expect it, this may result in differences in the runtime measurements, which is hard estimate without re-running the experiments.

## Notes on Reusability (Encouraged for all badges)

First, this section might not apply to your artifacts. Describe how your
artifact can be used beyond your research paper, e.g., as a general framework.
The overall goal of artifact evaluation is not only to reproduce and verify your
research but also to help other researchers to re-use and extend your artifacts.
Discuss how your artifacts can be adapted to other settings, e.g., more input
dimensions, other datasets, and other behavior, through replacing individual
modules and functionality or running more iterations of a specific module.