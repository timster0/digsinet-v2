# DigSiNet v2

This project is an enhancement of the original DigSiNet PoC specified in a paper by [Rieger et al.: DigSiNet](https://doi.org/10.1109/NOMS59830.2024.10575632) and the corresponding [GitHub Repository](https://github.com/srieger1/digsinet/). An excerpt of the original repo is here:

> This project implements a proof-of-concept environment to run Network Digital Twins (NDT). It primarily uses [containerlab](https://containerlab.dev/), but can also use other platforms to build, manage and monitor the twins. The concept uses multiple twins that can leverage different platforms, topologies and tools to specifically simulate and emulate only parts of the functionality of the real network. As they only partially share characteristics with the real network and multiple ones can be used an combined with each sibling using a different platform being well-suited for its purpose, they are called siblings instead of twins. See [this paper]

# Motivation for v2

The original PoC had several flaws, primarily because of the multithread, especially the GIL, behaviour of python. While trying to implement NATS as a message broker, several design flaws were encountered that made further development more challenging. This repo attempts to overcome these challenges by changing the implementation design:

- the Realnet controller is outsourced into its own subprocess
- subprocesses run in an async runtime by default to enable concurrency

# Requirements

- Python >=3.12
- [uv](https://github.com/astral-sh/uv)
- [containerlab](https://containerlab.dev/)