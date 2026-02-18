#!/bin/bash
set -euxo pipefail

python -m ipykernel install --user --name ssp --display-name "Python (ssp)"

if [ ! -d "StochasticCIL" ]; then
  git clone https://github.com/epapoutsellis/StochasticCIL.git
fi

cd StochasticCIL
git fetch --all --tags
git checkout svrg

# no idea why
git config user.email "binder@local"
git config user.name "Binder Build"

if git rev-parse -q --verify refs/tags/v1.0 >/dev/null; then
  if [ "$(git cat-file -t v1.0)" != "tag" ]; then
    git tag -d v1.0
    git tag -a v1.0 -m "Version 1.0"
  fi
else
  git tag -a v1.0 -m "Version 1.0"
fi

mkdir -p build
cd build

cmake ../ -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DCONDA_BUILD=OFF \
  -DCMAKE_BUILD_TYPE=Release \
  -DLIBRARY_LIB="${CONDA_PREFIX}/lib" \
  -DLIBRARY_INC="${CONDA_PREFIX}" \
  -DCMAKE_INSTALL_PREFIX="${CONDA_PREFIX}" \
  -DPython_EXECUTABLE="${CONDA_PREFIX}/bin/python"

make -j"$(nproc)"
make install
