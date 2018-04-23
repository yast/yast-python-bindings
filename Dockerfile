FROM yastdevel/cpp:sle15
RUN zypper --gpg-auto-import-keys --non-interactive in --no-recommends \
  python-devel python3-devel swig autoconf-archive
COPY . /usr/src/app
