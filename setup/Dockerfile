FROM ubuntu:18.04 as builder

LABEL MAINTAINER Mohit Sharma <mohitsharma44@gmail.com>

RUN set -ex; \
  echo "deb [trusted=yes] http://repo.iovisor.org/apt/bionic bionic-nightly main" > /etc/apt/sources.list.d/iovisor.list; \
  apt-get update -y; \
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
    auditd \
    bcc-tools \
    libelf1 \
    python3-pip \
    libbcc-examples;

COPY ./ /teleport_test_hbf/
COPY ./teleport_test_hbf/bpf_programs /usr/config/bpf_programs

RUN cd teleport_test_hbf && \
    pip3 install -r requirements_dev.txt && \
    make install

ENTRYPOINT ["teleport_test_hbf"]
