#!/bin/bash
set -e -x

PROJECT=llb3d
PYBINS="/opt/python/cp36-cp36m/bin /opt/python/cp37-cp37m/bin"

# Compile wheels
for PYBIN in $PYBINS; do
    cd /io
    "${PYBIN}/pip" install -e ".[dev]" &&
    "${PYBIN}/python" setup.py sdist bdist_egg bdist_wheel || exit 1
done

mkdir /dist
mv /io/dist/*.whl /dist

# Bundle external shared libraries into the wheels
for whl in /dist/*.whl; do
    auditwheel repair "$whl" -w /io/dist/ || exit 1
done

# Install packages and test
for PYBIN in $PYBINS; do
    "${PYBIN}/pip" install $PROJECT --no-index -f /io/dist || exit 1
    cd "$HOME"
    "${PYBIN}/pytest" --pyargs $PROJECT && "${PYBIN}/pylint" $PROJECT || exit 1
done
