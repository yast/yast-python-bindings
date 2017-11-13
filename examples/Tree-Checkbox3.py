# encoding: utf-8

from yast import *
class TreeCheckbox3Client:
    def main(self):

      items = [
        Item(Id("a"), "a", False, []),
        Item(
          Id("x"),
          "x",
          True,
          [Item(Id("y"), "y", False, []), Item(Id("z"), "z", False, [])]
        )
      ]

      contents = HBox(
        VSpacing(20),
        VBox(
          HSpacing(70),
          VSpacing(0.2),
          #`Tree (`id(`tree), `opt(`notify, `immediate, `multiSelection),  "tree", items),
          Tree(Id("tree"), Opt("notify", "multiSelection"), "tree", items),
          #`Tree (`id(`tree), `opt(`notify),  "tree", items),
          HBox(
            #PushButton(Id("ok"), Opt("default"), Label.OKButton),
            PushButton(Id("ok"), Opt("default"), "OK"),
            #PushButton(Id("cancel"), Opt("key_F9"), Label.CancelButton)
            PushButton(Id("cancel"), Opt("key_F9"), "Cancel")
          ),
          VSpacing(0.2)
        )
      )

      UI.OpenDialog(Opt("decorated"), contents)
      UI.ChangeWidget("tree", "CurrentItem", None)
      while True:
        event = UI.WaitForEvent()
        ret = event["ID"]
        if ret == "tree":
          current2 = UI.QueryWidget(Id("tree"), "CurrentItem")
          ycpbuiltins.y2internal("current: %1", current2)

        if ret == "ok" or ret == "cancel":
          break
      current = UI.QueryWidget(Id("tree"), "CurrentItem")
      ycpbuiltins.y2internal("current before leaving: %1", current)

      UI.CloseDialog()


TreeCheckbox3Client().main()

