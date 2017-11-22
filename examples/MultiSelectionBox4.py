# encoding: utf-8

from yast import *
class MultiSelectionBox4Client:
    def main(self):

      items = [
        Item(Id("a"), "a"),
        Item(Id("x"), "x"),
        Item(Id("y"), "y"),
        Item(Id("z"), "z")
      ]

      contents = HBox(
        VSpacing(20),
        VBox(
          HSpacing(70),
          VSpacing(0.2),
          MultiSelectionBox(
            Id("multisel"),
            Opt("notify"),
            "Multiselection",
            items
          ),
          HBox(
            #PushButton(Id("ok"), Opt("default"), Label.OKButton),
            #PushButton(Id("cancel"), Opt("key_F9"), Label.CancelButton)
            PushButton(Id("ok"), Opt("default"), "OK"),
            PushButton(Id("cancel"), Opt("key_F9"), "Cancel")
          ),
          VSpacing(0.2)
        )
      )

      UI.OpenDialog(Opt("decorated"), contents)
      UI.ChangeWidget("multisel", "CurrentItem", None)

      UI.ChangeWidget("multisel", "SelectedItems", [Id("a"), Id("x")])
      UI.ChangeWidget("multisel", "SelectedItems", [Id("y"), Id("z")])

      selected_items = UI.QueryWidget(Id("multisel"), "SelectedItems")

      ycpbuiltins.y2milestone("Selected items: %1", selected_items)
      ycpbuiltins.y2milestone(
        "Current item: %1",
        UI.QueryWidget(Id("multisel"), "CurrentItem")
      )
      while True:
        event = UI.WaitForEvent()
        ret = event["ID"]
        if ret == "multisel":
          current2 = UI.QueryWidget(Id("multisel"), "CurrentItem")
          ycpbuiltins.y2internal("current: %1", current2)

        if ret == "ok" or ret == "cancel":
          break
      current = UI.QueryWidget(Id("multisel"), "CurrentItem")
      ycpbuiltins.y2internal("current before leaving: %1", current)
      UI.CloseDialog()


MultiSelectionBox4Client().main()

