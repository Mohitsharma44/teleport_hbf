FROM ubuntu:22.04 as builder

LABEL MAINTAINER Mohit Sharma <mohitsharma44@gmail.com>

RUN apt-get update && \
    apt-get install -y kmod python3-pip bpfcc-tools

COPY ./ /teleport_test_hbf/
COPY ./teleport_test_hbf/bpf_programs /usr/config/bpf_programs

RUN cd teleport_test_hbf && \
    pip3 install -r requirements_dev.txt && \
    make install

ENTRYPOINT ["teleport_test_hbf"]
