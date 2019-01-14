ARG DOCKER_IMAGE
FROM $DOCKER_IMAGE
RUN cd /tmp && \
    curl -L https://github.com/Kitware/CMake/releases/download/v3.13.2/cmake-3.13.2.tar.gz -o cmake-3.13.2.tar.gz && \
    tar xf cmake-3.13.2.tar.gz && \
    cd /tmp/cmake-3.13.2 && \
    ./bootstrap && \
    make && \
    make install && \
    cd /tmp && \
    curl -L http://download.icu-project.org/files/icu4c/63.1/icu4c-63_1-src.tgz -o icu4c-63_1-src.tgz && \
    tar xf icu4c-63_1-src.tgz && \
    cd /tmp/icu/source && \
    CPPFLAGS="-DU_STATIC_IMPLEMENTATION -DUCONFIG_ONLY_COLLATION=1 -DUCONFIG_NO_LEGACY_CONVERSION=1 -DUCONFIG_NO_COLLATION=1" ./runConfigureICU Linux --enable-static --disable-shared --disable-tests --disable-samples --prefix=/opt/icu && \
    make && \
    make install && \
    rm -rf /tmp/*
