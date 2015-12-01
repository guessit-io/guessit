FROM ubuntu

MAINTAINER Rémi Alvergnat <toilal.dev@gmail.com>

ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

WORKDIR /root

COPY docker/base_dependencies.txt /root/base_dependencies.txt
RUN apt-get update && \
    apt-get install -y $(cat /root/base_dependencies.txt) && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/base_dependencies.txt /etc/dpkg/dpkg.cfg.d/02apt-speedup

ENV PYTHONDONTWRITEBYTECODE true
RUN git clone https://github.com/yyuu/pyenv.git /root/.pyenv
RUN pyenv install 3.4.3 && pyenv global 3.4.3

COPY / /root/guessit/

WORKDIR /root/guessit/

RUN pip install -e .

ENTRYPOINT ["guessit"]

