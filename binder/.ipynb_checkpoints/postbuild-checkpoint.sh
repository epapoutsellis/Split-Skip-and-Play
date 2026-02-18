#!/bin/bash
set -euxo pipefail

# Optional: nice kernel name in Jupyter
python -m ipykernel install --user --name ssp --display-name "Python (ssp)"

# Clone + build StochasticCIL (svrg branch)
if [ ! -d "StochasticCIL" ]; then
  git clone https://github.com/epapoutsellis/StochasticCIL.git
fi

cd StochasticCIL
git fetch --all --tags
git checkout svrg

# Create tag only if missing (idempotent)
if ! git tag -l | grep -qx "v1.0"; then
  git tag -a v1.0 -m "Version 1.0"
fi

mkdir -p build
cd build

cmake ../ \
  -DCONDA_BUILD=OFF \
  -DCMAKE_BUILD_TYPE=Release \
  -DLIBRARY_LIB="${CONDA_PREFIX}/lib" \
  -DLIBRARY_INC="${CONDA_PREFIX}" \
  -DCMAKE_INSTALL_PREFIX="${CONDA_PREFIX}"

make -j"$(nproc)"
make install
