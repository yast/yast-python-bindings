# encoding: utf-8

from yast import *
class InternalErrorClient:
    def main(self):
      # This will cause an internal error since UI::UserInput() is called without
      # any dialog being opened.

      while True:
        ret = UI.UserInput()
        ycpbuiltins.y2milestone("UI::UserInput() returned %1", ret)


InternalErrorClient().main()

