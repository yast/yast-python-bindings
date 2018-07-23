from __future__ import unicode_literals
# encoding: utf-8

#
# Advanced MultiProgressMeter example:
# Change values interactively with sliders
# and allow tests with huge numbers
#
from yast import import_module
import_module('UI')
from yast import *
import copy
class MultiProgressMeter2Client:
    def main(self):
      #
      # Global variables
      #

      maxValueList = [950, 200, 500, 20, 100]
      valueList = [100, 30, 400, 0, 0]
      unit = 0 # exponent: powers of 2



      #
      # Check if required special widgets are available
      #

      if not UI.HasSpecialWidget("HMultiProgressMeter") or not UI.HasSpecialWidget("Slider"):
        UI.OpenDialog(
          VBox(
            Label("Error: This UI doesn't support the required widgets!"),
            PushButton(Opt("default"), "&OK")
          )
        )
        UI.UserInput()
        UI.CloseDialog()

        return


      #
      # Create dialog
      #

      radioBox = Frame(
        "Unit",
        RadioButtonGroup(
          Id("unit"),
          Opt("notify"),
          HBox(
            HSpacing(0.5),
            RadioButton(Id(Term("unit", 0)), Opt("notify"), "&Bytes"),
            HSpacing(1.5),
            RadioButton(Id(Term("unit", 10)), Opt("notify"), "&kB"),
            HSpacing(1.5),
            RadioButton(Id(Term("unit", 20)), Opt("notify"), "&MB"),
            HSpacing(1.5),
            RadioButton(Id(Term("unit", 30)), Opt("notify"), "&GB"),
            HSpacing(0.5)
          )
        )
      )

      UI.OpenDialog(
        VBox(
          HBox(
            VBox(
              Heading("MultiProgressMeter Example"),
              VSpacing(1),
              self.slidersVBox(maxValueList, valueList),
              radioBox,
              VStretch()
            ),
            HSpacing(1),
            ReplacePoint(
              Id("rep_vProgress"),
              VMultiProgressMeter(
                Id("vProgress"),
                self.scaleList(unit, maxValueList)
              )
            )
          ),
          HBox(
            ReplacePoint(
              Id("rep_hProgress"),
              HMultiProgressMeter(
                Id("hProgress"),
                self.scaleList(unit, maxValueList)
              )
            ),
            HSpacing(0.5),
            PushButton(Id("cancel"), "&Close")
          )
        )
      )

      UI.ChangeWidget(Id("unit"), "Value", Term("unit", unit))
      self.updateProgress(unit, self.values)


      #
      # Event loop
      #

      while True:
        event = UI.WaitForEvent()
        # y2debug( "Event: %1", event );
        id = event["ID"]
        widgetClass = event["WidgetClass"]

        if widgetClass == "RadioButton":
          currentUnitID = UI.QueryWidget("unit", "CurrentButton")
          print "type %s"%type(currentUnitID)
          #if Ops.is_term?(currentUnitID):
          if isinstance (currentUnitID, YCPTerm):
            unit = currentUnitID.value(0)

            ycpbuiltins.y2milestone("New unit: 2^%1", unit)
            UI.ReplaceWidget(
              "rep_vProgress",
              VMultiProgressMeter(
                Id("vProgress"),
                self.scaleList(unit, maxValueList)
              )
            )
            UI.ReplaceWidget(
              "rep_hProgress",
              HMultiProgressMeter(
                Id("hProgress"),
                self.scaleList(unit, maxValueList)
              )
            )
            self.updateProgress(unit, self.values)
        if widgetClass == "Slider":
          self.updateProgress(unit, self.values)
          self.values = self.scaleList(unit, self.getValues())
          UI.ChangeWidget("vProgress", "Values", self.values)
          UI.ChangeWidget("hProgress", "Values", self.values)

        if id == "cancel":
          break


      #
      # Clean up
      #

      UI.CloseDialog()


    # Return a VBox term with Slider widgets for each list value.
    #
    def slidersVBox(self, maxValuesList, currentValuesList):
      maxValuesList = copy.deepcopy(maxValuesList)
      currentValuesList = copy.deepcopy(currentValuesList)
      vbox = VBox()
      i = 0

      for maxVal in ycpbuiltins.foreach(maxValuesList):
        vbox = ycpbuiltins.add(
          vbox,
          Slider(
            Id(Term("slider", i)), # currentVal
            Opt("notify"),
            "", # label
            0, # minVal
            maxVal,
            currentValuesList[i]
          )
        )
        i = i + 1

      #deep_copy(vbox)
      return vbox

    # Apply unit to a list of values. Return the scaled list.
    #
    def scaleList(self, unit, values):
      self.values = copy.deepcopy(values)
      scaledValues = []

      for val in ycpbuiltins.foreach(values):
        scaledValues = ycpbuiltins.add(scaledValues, val << unit)

      # y2debug( "Values: %1	  unit: %2   scaled: %3", values, unit, scaledValues );
      return copy.deepcopy(scaledValues)


    # Get the current values from all sliders and return them as a list.
    #
    def getValues(self):
      values = []
      i = 0

      while True:
        sliderID = Term("slider", i)
        # y2debug( "Looking for %1", sliderID );

        if not UI.WidgetExists(Id(sliderID)):
          break

        values = ycpbuiltins.add(
          values,
          UI.QueryWidget(Id(sliderID), "Value")
        )
        i = i + 1

      # y2debug( "Values: %1", values );
      return copy.deepcopy(values)


    # Update progress meters with values from sliders.
    #
    def updateProgress(self, unit, values):
      self.values = self.scaleList(unit, self.getValues())
      UI.ChangeWidget("vProgress", "Values", values)
      UI.ChangeWidget("hProgress", "Values", values)


MultiProgressMeter2Client().main()

