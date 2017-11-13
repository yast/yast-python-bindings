# encoding: utf-8

# WaitForEvent.ycp
#
# Example for common usage of UI::WaitForEvent()
from yast import *
class WaitForEventClient:
    def main(self):
      # Build dialog with a selection box and some buttons.
      #
      # Output goes to the log file: ~/.y2log for normal users
      # or /var/log/YaST2/y2log for root.

      timeout_millisec = 20 * 1000

      UI.OpenDialog(
        VBox(
          SelectionBox(
            Id("pizza"),
            Opt("notify", "immediate"),
            "Select your Pi&zza:",
            [
              Item(Id("napoli"), "Napoli"),
              Item(Id("funghi"), "Funghi"),
              Item(Id("salami"), "Salami"),
              Item(Id("prociutto"), "Prosciutto"),
              Item(Id("stagioni"), "Quattro Stagioni"),
              Item(Id("chef"), "A la Chef", True)
            ]
          ),
          HBox(
            PushButton(Id("ok"), "&OK"),
            PushButton(Id("cancel"), "&Cancel"),
            HSpacing(),
            PushButton(Id("details"), "&Details...")
          )
        )
      )

      event = {}
      id = None
      while True:
        event = UI.WaitForEvent(timeout_millisec)
        id = event["ID"] # We'll need this often - cache it

        if id == "pizza":
          if event["EventReason"] == "Activated":
            # Handle pizza "activate" (double click or space pressed)

            ycpbuiltins.y2milestone("Pizza activated")
            id = "details" # Handle as if "Details" button were clicked
          elif event["EventReason"] == "SelectionChanged":
            # Handle pizza selection change

            ycpbuiltins.y2milestone("Pizza selected")

        if id == "details":
          ycpbuiltins.y2milestone("Show details")

        if id == "timeout":
          # Handle timeout

          ycpbuiltins.y2milestone("Timeout detected by ID")

        if event["EventType"] == "TimeoutEvent": # Equivalent
          # Handle timeout

          ycpbuiltins.y2milestone("Timeout detected by event type")

          # Open a popup dialog

          UI.OpenDialog(
            VBox(Label("Not hungry?"), PushButton(Opt("default"), "&OK"))
          )
          UI.TimeoutUserInput(10 * 1000) # Automatically close after 10 seconds
          UI.CloseDialog()
        if id == "ok" or id == "cancel":
          break


      UI.CloseDialog()


WaitForEventClient().main()

