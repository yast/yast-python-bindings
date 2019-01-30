FROM yastdevel/cpp
RUN zypper --gpg-auto-import-keys --non-interactive in --no-recommends \
  python-devel python3-devel swig autoconf-archive python-six python3-six
COPY . /usr/src/app
