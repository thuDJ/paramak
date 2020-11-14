# build with the following command
# sudo docker build -t paramak .

# Run with the follwoing command
# sudo docker run -it paramak

# test with the folowing command
# sudo docker run --rm paramak pytest /tests

FROM continuumio/miniconda3

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# RUN useradd -ms /bin/bash cq

# WORKDIR /home/cq/

# USER root

RUN apt-get install -y libgl1-mesa-glx

RUN conda install -c cadquery -c conda-forge cadquery=2

# USER cq

# Copy over the source code
COPY paramak paramak/
COPY setup.py setup.py
COPY README.md README.md

RUN pip install .
# additional neutronics features avaialbe with pip install .[neutronics]

# Copy over the test folder
COPY tests tests/

WORKDIR paramak/examples

CMD ["/bin/bash"]
