FROM yastdevel/cpp:sle12-sp3
RUN zypper --gpg-auto-import-keys --non-interactive in --no-recommends \
  python-devel
COPY . /usr/src/app
