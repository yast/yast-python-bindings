FROM yastdevel/cpp
RUN zypper --gpg-auto-import-keys --non-interactive in --no-recommends \
  python-devel swig autoconf-archive
COPY . /usr/src/app
