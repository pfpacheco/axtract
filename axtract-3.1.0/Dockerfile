#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM debian:jessie

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8
# https://github.com/docker-library/python/issues/147
ENV PYTHONIOENCODING UTF-8

# extra dependencies (over what buildpack-deps already includes)
RUN apt-get update && apt-get install -y --no-install-recommends \
        apt-utils \
		tk-dev \
		net-tools \
		vim \
		xterm \
		netbase \
		apache2 \
		fuse \
		makedev \
		xterm \
		redis-server \
		python \
		python-dev \
		python-pip \
		python-setuptools \
		python-llfuse \
		python-netsnmp \
		python-support \
		python-yaml \
		python-pyparsing \
        python-libxml2 \
        python-cairocffi \
        python-rrdtool \
        python-numpy \
        python-tz \
        python-lxml \
        python-netaddr \
        python-mysqldb \
        python-gevent \
        python-soappy \
        python-pymongo \
        rsyslog \
	&& rm -rf /var/lib/apt/lists/*

ENV TERM xterm

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 20.0.2
# https://github.com/pypa/get-pip
ENV PYTHON_GET_PIP_URL https://github.com/pypa/get-pip/raw/d59197a3c169cef378a22428a3fa99d33e080a5d/get-pip.py
ENV PYTHON_GET_PIP_SHA256 421ac1d44c0cf9730a088e337867d974b91bdce4ea2636099275071878cc189e

RUN set -ex; \
	\
	wget -O get-pip.py "$PYTHON_GET_PIP_URL"; \
	echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum --check --strict -; \
	\
	python get-pip.py \
		--disable-pip-version-check \
		--no-cache-dir \
		"pip==$PYTHON_PIP_VERSION" \
	; \
	pip --version; \
	\
	find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
		\) -exec rm -rf '{}' +; \
	rm -f get-pip.py

RUN pip install --no-cache-dir virtualenv

RUN echo "/proc /opt/axtract/proc none rw,bind 0 0" >> /etc/fstab \
    && echo "/dev/pts /opt/axtract/dev/pts none rw,bind 0 0" >> /etc/fstab \
    && echo "/dev/pts /opt/axtract/dev/pts none rw,bind 0 0" >> /etc/fstab \
    && echo "/tmpfs /opt/axtract/run/shm tmpfs defaults 0 0" >> /etc/fstab

RUN echo "ntpdate 0.debian.pool.ntp.org" > /etc/cron.daily/ntpdate \
    && chmod 755 /etc/cron.daily/ntpdate

RUN mkdir -p /opt/axtract \
    && mkdir -p /opt/axtract/proc \
    && mkdir -p /opt/axtract/dev/pts \
    && mkdir -p /opt/axtract/run/shm \
    && mkdir -p /tmp/axtract

RUN mkdir -p /data \
    && mkdir -p /data/gridfs_fuse \
    && mkdir -p /data/rrddb-data \
    && mkdir -p /data/rrddb-journal

ENV DEPLOY_PATH /opt/axtract

RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    libboost-date-time1.55.0 \
    libboost-thread1.55.0 \
    libevent-2.0-5 \
    libsasl2-2 \
    libsnappy1 \
    libatomic1 \
    libyajl2 \
    libboost-filesystem1.55.0 \
    libboost-iostreams1.55.0 \
    libboost-program-options1.55.0 \
    libboost-regex1.55.0 \
    libmpfr4 \
    libmsgpack3 \
    libpython2.7 \
    libtbb2 \
    libxml2 \
    rrdtool \
    erlang-nox \
    logrotate \
    socat

COPY . /tmp/axtract

WORKDIR  /tmp/axtract

RUN dpkg -i ./all-packages/axlib*.deb \
    && dpkg -i ./all-packages/beanstalkd*.deb \
    && dpkg -i ./all-packages/librdkafka1*.deb \
    && dpkg -i ./all-packages/snzip*.deb \
    && dpkg -i ./all-packages/libbson-1.0*.deb \
    && dpkg -i ./all-packages/axtract_*.deb \
    && dpkg -i ./all-packages/axtract-northbound-lab*.deb \
    && dpkg -i ./all-packages/axtract-southbound*.deb \
    && dpkg -i ./all-packages/libapache2-mod-python_*.deb \
    && dpkg -i ./all-packages/mongodb-org* \
    && dpkg -i ./all-packages/rabbitmq-server*.deb

RUN sed -ie "s/#START=yes/START=yes/g" \
    /etc/default/beanstalkd

RUN cp /opt/axtract/contrib/mongodb/mongod \
    /etc/init.d/mongod

RUN sed -ie 's/SERVICE_ENABLED="false"/SERVICE_ENABLED="true"/g' \
    /etc/default/axtract_all_daemons

RUN rm -rf \
    /etc/default

COPY ./default /etc/default

RUN rm -rf /etc/mongod.conf

COPY ./mongo/mongod.conf /etc/

COPY ./rabbitmq/rabbitmq.config \
    /etc/rabbitmq/

COPY ./celery/etl_config.py \
    /opt/axtract/etc/

WORKDIR  /opt/axtract

RUN rm -rf custom_code/* \
    && rm -rf full_config.json

RUN mkdir -p custom_code

COPY ./custom_code /opt/axtract/custom_code

COPY ./full_config.json /opt/axtract/

RUN mknod /dev/fuse c 10 229
