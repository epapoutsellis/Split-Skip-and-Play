# Split-Skip-and-Play

Code to reproduce results for paper ["SPLIT, SKIP AND PLAY: VARIANCE-REDUCED PROXSKIP FOR TOMOGRAPHY
RECONSTRUCTION IS EXTREMELY FAST"](https://arxiv.org/abs/2602.09527) by Evangelos Papoutsellis, Zeljko Kereta, Kostas Papafitsoros. This is an extension of the paper ["Why do we regularise in every iteration for imaging inverse problems?"](https://arxiv.org/abs/2411.00688).

![](PnP_BM3D_1min_reconstruction.gif)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/epapoutsellis/Split-Skip-and-Play/HEAD)  

### Abstract
Many modern iterative solvers for large-scale tomographic reconstruction incur two major computational costs per iteration: expensive forward/adjoint projections to update the data fidelity term and costly proximal computations for the regulariser, often done via inner iterations. This paper studies for the first time the application of methods that couple randomised skipping of the proximal with variance-reduced subset-based optimisation of data-fit term, to simultaneously reduce both costs in challenging tomographic reconstruction tasks. We provide a series of experiments using both synthetic and real data, demonstrating striking speed-ups of the order 5x--20x compared to the non-skipped counterparts which have been so far the standard approach for efficiently solving these problems. Our work lays the groundwork for broader adoption of these methods in inverse problems.


### Installation

We use the [Core Imaging Library (CIL)](https://github.com/TomographicImaging/CIL) with some additional [new functionalities](#Appendix). Code and installation tested on macOS (Apple M2 Pro), Linux, and Windows 10.

```
conda create --name ssp -c conda-forge python=3.12 "numpy<2.0" cmake scipy six cython numba pillow jupyterlab scikit-learn dask "zarr<3" pywavelets astra-toolbox tqdm nb_conda_kernels

conda activate ssp
pip install bm3d xdesign scikit-image
pip install "setuptools<82" --upgrade

git clone https://github.com/epapoutsellis/StochasticCIL.git
cd StochasticCIL
git checkout svrg
git tag -a v1.0 -m "Version 1.0"
mkdir build
cd build
cmake ../ -DCONDA_BUILD=OFF -DCMAKE_BUILD_TYPE="Release" -DLIBRARY_LIB=$CONDA_PREFIX/lib -DLIBRARY_INC=$CONDA_PREFIX -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX
make install
```
For windows: `cmake ../ -DCONDA_BUILD=OFF`, `cmake --build . --target install`

### Citation

```
@article{2602.09527,
Author = {Evangelos Papoutsellis and Zeljko Kereta and Kostas Papafitsoros},
Title = {Split, Skip and Play: Variance-Reduced ProxSkip for Tomography Reconstruction is Extremely Fast},
Year = {2026},
Eprint = {arXiv:2602.09527},
}
```

### New CIL Functionalities

1) Splitting methods for Acquisition Data compatible with CIL and [SIRF](https://github.com/SyneRBI/SIRF).
2) Sampling methods for CIL Stochastic Functions (used also by SPDHG).
3) ApproximateGradientSumFunction (Base class for CIL Stochastic Functions)
4) SGFunction
5) SAGFunction
6) SAGAFunction
7) SVRGFunction
8) LSVRGFunction
9) PGA (Proximal Gradient Algorithm), base class for GD, ISTA, FISTA.  Designed for fixed and/or adaptive Preconditioners and step sizes.
10) Preconditioner (base class). An instance of Preconditioner can be passed to GD, ISTA, FISTA. 
11) StepSizeMethod (base class for step size search), including standard Armijo/Backtracking.
12) Callback utilities, including standard metrics (compared to a reference) and statistics of iterates. Any function (CIL), or callables from other libraries can be used.
13) PD3O (Primal Dual Three Operator Splitting Algorithm) which can be combined with a Stochastic CIL function.
14) SIRF Priors classes can be used in the CIL Optimisation Framework for free. In addition, SIRF ObjectiveFunction Classes can be used. This allows more flexibility for SIRF users to have control and monitor a CIL algorithm.

### Acknowledgements    

E. Papoutsellis acknowledges funding through the Innovate UK Analysis for Innovators (A4i) program: "Denoising of chemical imaging and tomography data" under which the experiments were initially conducted, CCPi (EPSRC grant EP/T026677/1), CCP SyneRBI (EPSRC grant EP/T026693/1).

