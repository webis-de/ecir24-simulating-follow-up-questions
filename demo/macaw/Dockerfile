# NOTE: This does not work yet. I assume MACAW requires python3.6, which seems to be available in ubuntu:16.04; python3.7 introduces the async keyword that causes problems; some packages are not available for python3.5
FROM ubuntu:20.04

RUN apt update && apt install -y curl gpg software-properties-common
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc \
  | gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" \
  | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt install -y \
  default-jre \
  ffmpeg \
  git \
  mongodb-org \
  python3.5-dev \
  python3-pip \
  unzip \
  wget \
  zlib1g-dev

RUN python3.5 -m pip install \
  setuptools

RUN mkdir /app/

WORKDIR /app
RUN wget -O "indri-5.11.tar.gz" "https://master.dl.sourceforge.net/project/lemur/lemur/indri-5.11/indri-5.11.tar.gz?viasf=1"
RUN tar xzf indri-5.11.tar.gz
WORKDIR /app/indri-5.11
RUN ./configure CXX="g++ -D_GLIBCXX_USE_CXX11_ABI=0 -std=c++14" && make && make install
RUN pip install pyndri

# Where to install?
# WORKDIR /app
# RUN wget -O "stanford-corenlp-full-2017-06-09.zip" "http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip"
# RUN unzip "stanford-corenlp-full-2017-06-09.zip" && rm "stanford-corenlp-full-2017-06-09.zip"

WORKDIR /app
RUN git clone https://github.com/facebookresearch/DrQA.git
WORKDIR /app/DrQA
RUN python3.5 -m pip install -r requirements.txt && python3.5 setup.py develop

WORKDIR /app
RUN git clone https://github.com/microsoft/macaw.git
WORKDIR /app/macaw
RUN python3.5 -m pip install -r requirements.txt && python3.5 setup.py install

RUN mkdir -p /app/mongodb
WORKDIR /app/

COPY run.sh /app/run.sh
#ENTRYPOINT [ "./run.sh" ]

