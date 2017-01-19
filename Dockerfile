FROM yastdevel/cpp
RUN zypper --gpg-auto-import-keys --non-interactive in --no-recommends \
  python-devel
COPY . /usr/src/app
