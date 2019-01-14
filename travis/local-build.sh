# 64-bit
DOCKER_IMAGE=quay.io/pypa/manylinux1_x86_64 \
docker build -t manylinux-llb3d --build-arg DOCKER_IMAGE travis/docker
docker run --rm -v `pwd`:/io manylinux-llb3d /io/travis/build-wheels.sh || exit 1

# 32-bit
DOCKER_IMAGE=quay.io/pypa/manylinux1_i686 \
docker build -t manylinux-llb3d-32 --build-arg DOCKER_IMAGE travis/docker
PRE_CMD=linux32 \
docker run --rm -v `pwd`:/io manylinux-llb3d-32 $PRE_CMD /io/travis/build-wheels.sh || exit 1
