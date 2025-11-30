FROM ubuntu:25.04 AS installer

RUN apt-get update
RUN apt-get install -y python3 python3-pip curl

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable
ENV PATH="/root/.cargo/bin:${PATH}"


FROM installer as builder

RUN cargo --version
RUN pip --version

RUN apt install python3-maturin

COPY rusty_pstore/Cargo.toml Cargo.toml
# build was failing bc snapshot not found. this worked most constistently
RUN ls
COPY rusty_pstore/src/ src/

RUN maturin build --release --manylinux off
RUN ls

FROM python:3.13-slim as release
WORKDIR server/

# # Python src
COPY app/src/ app/src/
RUN ls
COPY app/requirements.txt app/requirements.txt
RUN ls
COPY --from=builder /target/wheels wheels/
RUN ls
COPY setup.sh setup.sh
RUN ./setup.sh
RUN mkdir store

COPY default_admin.py tools/default_admin.py