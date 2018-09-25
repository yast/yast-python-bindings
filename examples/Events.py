# encoding: utf-8

# (Advanced) YCP example for various UI events:
#
# Create a dialog with all kinds of widgets that can generate events and
# display any event nicely formatted in a RichText widget.
#
# Most widgets have the `notify option set to demonstrate what events they can
# send.
#
# Use the "Close" button to quit the example.
import copy
from yast import import_module
import_module('UI')
from yast import *
class EventsClient:
    def main(self):


      timeout = 7 # seconds
      howto = ycpbuiltins.sformat(
        "Use the \"Close\" button to quit. " + "All other widgets will only show the event.\n" + "After %1 seconds of inactivity a timeout event will occur.", timeout
      )

      event_display = "<i>No event yet - click something (or wait for timeout)</i>"

      help_text = "<p>Please also have a look at our <a href=\"daily special\">daily special</a>.</p>" + "<p>If you have any comments about our pizza, please contact our " + "chef de cuisine <a href=\"mailto:giuseppe@mafia.it\">Giuseppe</a>.</p>"


      delivery = Tree(
        Id("delivery_service"),
        Opt("notify", "notifyContextMenu"),
        "&Delivery Service",
        [
          Item(
            Id("europe"),
            "Europe",
            True,
            [
              Item(Id("italy"), "Italy", ["Napoli", "Palermo", "Roma", "Milano"]),
              Item(Id("germany"), "Germany", ["Nuernberg", "Muenchen", "Berlin"]),
              Item(Id("czech"), "Czech Republic", ["Praha", "Brno"])
            ]
          ),
          Item(
            Id("usa"),
            "USA",
            False,
            ["New York", "Chicago", "San Francisco", "Los Angeles"]
          )
        ]
      )

      pizza = SelectionBox(
        Id("pizza"),
        Opt("notify", "immediate", "notifyContextMenu"),
        "Pi&zza",
        [
          Item(Id("napoli"), "Napoli"),
          Item(Id("funghi"), "Funghi"),
          Item(Id("salami"), "Salami"),
          Item(Id("prociutto"), "Prosciutto"),
          Item(Id("stagioni"), "Quattro Stagioni (a pizza devided into 4 parts)"),
          Item(Id("chef"), "A la Chef", True)
        ]
      )

      toppings = MultiSelectionBox(
        Id("toppings"),
        Opt("notify", "notifyContextMenu"),
        "To&ppings",
        [
          Item(Id("cheese"), "Cheese", True),
          Item(Id("tomatoes"), "Tomatoes", True),
          Item(Id("mush"), "Mushrooms", False),
          Item(Id("onions"), "Onions"),
          Item(Id("sausage"), "Salami"),
          Item(Id("ham"), "Ham")
        ]
      )

      drink = Table(
        Id("drink"),
        Opt("notify", "immediate", "multiSelection", "notifyContextMenu"),
        Header("Drink", "Contents"),
        [
          Item(Id("coke"), "Coca Cola", "Caffeine"),
          Item(Id("sprite"), "Sprite", ""),
          Item(Id("water"), "Mineral Water", ""),
          Item(Id("beer"), "Beer", "Alcohol"),
          Item(Id("wine"), "Wine", "Alcohol"),
          Item(Id("coffee"), "Coffee", "Caffeine")
        ]
      )

      lists = HBox(
        HWeight(1, delivery),
        HWeight(1, pizza),
        HWeight(1, toppings),
        HWeight(1, drink),
        HWeight(1, RichText(Id("help_text"), help_text))
      )

      buttons = HBox(
        PushButton(Id("order"), Opt("key_F2"), "&Order"),
        PushButton(Id("info"), Opt("key_F3"), "More &Info"),
        PushButton(Id("cancel"), Opt("key_F4"), "&Cancel Order"),
        MenuButton(
          Id("special"),
          "&Special...",
          [
            Item(Id("track_order"), "&Where is my last order?"),
            Term(
              "menu",
              "Send complaint",
              [
                Item(Id("pizza_cold"), "My pizza was cold when I got it!"),
                Item(Id("bad_taste"), "I didn't like the taste of that pizza!"),
                Item(Id("lost_order"), "My order got lost!"),
                Item(
                  Id("too_small"),
                  "My pizza was too small. I am still hungry!"
                )
              ]
            ),
            Item(Id("doggie_bag"), "Order doggie bag"),
            Item(
              Id("This is a dumb user who will click on everything. Nevermind."),
              "Order dog to eat the leftovers in the doggie bag"
            ),
            Item(Id("cancel_order"), "Cancel order"),
            Item(Id("caffeine"), "Give me caffeine")
          ]
        )
      )

      fields = VSquash(
        HBox(
          Top(
            ComboBox(
              Id("salutation"),
              Opt("notify", "editable"),
              "&To:",
              [
                "Mr.",
                "Mrs.",
                "Miss",
                "Dr.",
                "Don",
                "King",
                "His Royal Highness"
              ]
            )
          ), # Force height (don't use MultiLineEdit default height)
          Top(InputField(Id("name"), Opt("notify"), "&Name:")),
          MultiLineEdit(Id("address"), Opt("notify"), "&Address:"),
          VSpacing(4)
        )
      )


      payment_radio_box = VBox(
        Left(RadioButton(Id("cash"), Opt("notify"), "Cas&h on Delivery", True)),
        Left(RadioButton(Id("plastic"), Opt("notify"), "C&redit Card")),
        Left(RadioButton(Id("bill"), Opt("notify"), "&Bill me Later"))
      )

      payment = VBox(
        Left(HVSquash(Frame("Payment", RadioButtonGroup(payment_radio_box)))),
        VSpacing(0.5),
        Left(
          CheckBox(
            Id("send_mafioso"),
            Opt("notify"),
            "Send &Giuseppe over if I forget to pay",
            False
          )
        )
      )


      UI.OpenDialog(
        Opt("defaultsize"),
        VBox(
          Id("mainLayout"),
          Heading("Event Example"),
          Label(howto),
          VSpacing(),
          VWeight(
            1, # Layout trick: Lower layout priority with a weight
            lists
          ),
          VSpacing(0.2),
          VSquash(
            HBox(
              HWeight(
                60,
                VBox(fields, VSpacing(0.2), VStretch(), Left(buttons))
              ),
              HSpacing(),
              HVSquash(payment)
            )
          ),
          VSpacing(0.5),
          VWeight(1, RichText(Id("event_display"), event_display)),
          HBox(
            PushButton(Id("help"), Opt("helpButton"), "&Help"),
            HStretch(),
            PushButton(Id("close"), "C&lose")
          )
        )
      )

      UI.ChangeWidget("mainLayout", "HelpText", howto)

      #
      # Event loop
      #

      event = {}
      while True:
        event = UI.WaitForEvent(timeout * 1000)

        widget = event["ID"]

        if widget != None and UI.WidgetExists(Id(widget)):
          ycpbuiltins.y2debug(
            "Event from %1 \"%2\"",
            UI.QueryWidget(Id(widget), "WidgetClass"),
            UI.QueryWidget(Id(widget), "DebugLabel")
          )

        if event != None:
          UI.ChangeWidget("event_display", "Value", formatEvent(event))

        if event["ID"] == "bill":
          if not UI.QueryWidget("send_mafioso", "Value"):
            UI.ChangeWidget("send_mafioso", "Value", True)
        elif event["ID"] == "send_mafioso":
          if UI.QueryWidget("bill", "Value") and not UI.QueryWidget("send_mafioso", "Value"):
            UI.ChangeWidget("cash", "Value", True)
        elif event["ID"] == "order":
          UI.ChangeWidget("send_mafioso", "Value", None)
          UI.DumpWidgetTree()
        elif event["ID"] == "caffeine":
          UI.ChangeWidget("drink", "SelectedItems", ["coffee", "coke"])
        elif event["ID"] == "info":
          UI.SetFocus("bogus")
        #
        # Help text is displayed automatically (because of `opt(`helpButton)
        #
        #	else: if (  event["ID"]:nil == `help )
        #	{
        #	    string helpText = (string) UI::QueryWidget(`mainLayout, `HelpText );
        #	    UI::OpenDialog(`VBox(`MinSize( 35, 7, `RichText( helpText ) ),
        #				 `PushButton("&OK" ) ) );
        #	    UI::UserInput();
        #	    UI::CloseDialog();
        #	}
        elif event["ID"] == "cancel_order":
          ycpbuiltins.y2milestone("Cancelling order")
          UI.ChangeWidget("delivery_service", "Value", None)
          UI.ChangeWidget("pizza", "Value", None)
          UI.ChangeWidget("toppings", "CurrentItem", None)
          UI.ChangeWidget("drink", "Value", None)
        if event["ID"] == "close":
          break


      #
      # Clean up
      #

      UI.CloseDialog()


    # Nicely (HTML-) format an event map.
    #
    # param [Hash{String : Object}] event	The event map to format
    # return	html	HTML code for the formatted event
    #
def formatEvent(event):
      event = copy.deepcopy(event)
      html = "<h3>Event:</h3><p>"
      ycpbuiltins.y2milestone("formatEvent(%1)", event)
      for key, value in ycpbuiltins.foreach(event).items():
          html = html +  "<font color=blue>" + key + "</font>: " + ycpbuiltins.tostring(value) + "<br>"
      html = html + "</p>"

      return html

EventsClient().main()

