# encoding: utf-8

from yast import *

# Because we don't have access to Directory.themedir
themedir = "/usr/share/YaST2/theme/"

class TimezoneSelectorClient:
    def main(self):

      # Build a dialog with a "special" widget - one that may not be supported
      # by all UIs.

      examples = {
        "Europe/Amsterdam"    : "Netherlands",
        "Europe/Athens"       : "Greece",
        "Europe/Berlin"       : "Germany",
        "Europe/Bratislava"   : "Slovakia",
        "Europe/Brussels"     : "Belgium",
        "Europe/Helsinki"     : "Finland",
        "Europe/Istanbul"     : "Turkey",
        # time zone
        "Europe/Kaliningrad"  : "Russia (Kaliningrad)",
        "Europe/Kiev"         : "Ukraine",
        "Europe/Malta"        : "Malta",
        # time zone
        "Europe/Minsk"        : "Belarus",
        "Europe/Monaco"       : "Monaco",
        # time zone
        "Europe/Moscow"       : "Russia (Moscow)",
        "Europe/Oslo"         : "Norway",
        "Europe/Paris"        : "France",
        "Europe/Prague"       : "Czech Republic",
        "Europe/Riga"         : "Latvia",
        "Europe/Rome"         : "Italy",
        # time zone
        "Europe/San_Marino"   : "San Marino",
        # time zone
        "Europe/Samara"       : "Russia (Samara)",
        "Europe/Sarajevo"     : "Bosnia & Herzegovina",
        "US/Aleutian"         : "Aleutian",
        "US/Arizona"          : "Arizona",
        "US/Central"          : "Central",
        "US/East-Indiana"     : "East Indiana",
        "US/Hawaii"           : "Hawaii",
        "US/Indiana-Starke"   : "Indiana Starke",
        "US/Michigan"         : "Michigan",
        "US/Mountain"         : "Mountain",
        "US/Pacific"          : "Pacific",
        "US/Samoa"            : "Samoa",
        "US/Eastern"          : "Eastern",
        "Europe/London"       : "United Kingdom",
        "America/New_York"    : "Eastern",
        "Australia/Darwin"    : "Northern Territory--Darwin",
        "Australia/Brisbane"  : "Queensland--Brisbane",
        "Australia/South"     : "South Australia--Adelaide",
        "Australia/Sydney"    : "New South Wales--Sydney",
        "Australia/ACT"       : "Australian Capital Territory--Canberra",
        "Australia/Hobart"    : "Tasmania--Hobart",
        "Australia/Melbourne" : "Victoria--Melbourne",
        "Australia/Perth"     : "Western Australia--Perth"
      }


      # Ask the UI whether or not it supports this widget.

      if UI.HasSpecialWidget("TimezoneSelector"):
        # Only create a dialog with this kind of widget if it is supported
        UI.OpenDialog(
          VBox(
            TimezoneSelector(
              Id("timezone"),
              Opt("notify"),
              #Directory.themedir + "/current/worldmap/worldmap.jpg",
              themedir + "/current/worldmap/worldmap.jpg",
              examples
            ),
            PushButton(Id("ok"), Opt("default"), "&Close"),
            ComboBox(
              Id("combozone"),
              Opt("notify"),
              "",
              [
                Item(Id("london"), "Europe/London"),
                Item(Id("prag"), "Europe/Prague"),
                Item(Id("ny"), "America/New_York")
              ]
            )
          )
        )
        # preselect something
        UI.ChangeWidget(Id("timezone"), "CurrentItem", "Europe/London")
      else:
        # Always provide a fallback: Either try to create a simpler dialog
        # without the special widget, or terminate with an error message.
        UI.OpenDialog(
          VBox(
            Label("Timezone Selector not supported!"),
            PushButton(Opt("default"), "&Oops!")
          )
        )

      while True:
        button = UI.UserInput()
        if button == "ok" or button == "cancel":
          break

        if button == "combozone":
          zone = UI.QueryWidget(Id("combozone"), "Value")
          if zone == "london":
            UI.ChangeWidget(Id("timezone"), "Value", "Europe/London")
          if zone == "prag":
            UI.ChangeWidget(Id("timezone"), "Value", "Europe/Prague")
          if zone == "ny":
            UI.ChangeWidget(Id("timezone"), "Value", "America/New_York")

        if button == "timezone":
          zone = UI.QueryWidget(Id("timezone"), "Value")
          UI.ChangeWidget(Id("combozone"), "Value", zone)

      UI.CloseDialog()


TimezoneSelectorClient().main()

