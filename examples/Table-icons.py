from __future__ import unicode_literals
# encoding: utf-8

# Advanced table example: Icon browser
from yast import import_module
import_module('UI')
from yast import *
import copy

class TableIconsClient:
    def main(self):



      iconBasePath = "/usr/share/YaST2/theme/current/icons"

      UI.OpenDialog(
        VBox(
          Heading("Icons"),
          MinSize(
            60,
            40,
            Table(Id("iconTable"), Header("Name", "22x22", "32x32", "48x48"))
          ),
          HBox(
            Label(Opt("outputField", "hstretch"), iconBasePath),
            PushButton(Id("cancel"), "&Close")
          )
        )
      )

      UI.OpenDialog(Label("Reading icon directories..."))


      iconList = readIconDir(iconBasePath + "/22x22/apps")
      iconList = ycpbuiltins.union(
          iconList,
          readIconDir(iconBasePath + "/32x32/apps"))
      iconList = ycpbuiltins.union(
          iconList,
          readIconDir(iconBasePath + "/48x48/apps"))

      itemList = []

      test = Term("icon", "22x22/apps/" + "iconName")
      test = Term("cell",test)
      print "working %s"%test.toString()
      test = Term("cell", Term("icon", "22x22/apps/" + "iconName"))
      print "not working %s"%test.toString()


      for iconName in ycpbuiltins.foreach(iconList):
        item = Item(
                Id(iconName),
                iconName,
                Term("cell", Term("icon", "22x22/apps/" + iconName)),
                Term("cell", Term("icon", "32x32/apps/" + iconName)),
                Term("cell", Term("icon", "48x48/apps/" + iconName))
                )
        # y2debug( "Item: %1", item );
        itemList = ycpbuiltins.add(itemList, item)

      UI.CloseDialog() # Close busy dialog

      UI.ChangeWidget(("iconTable"), "IconPath", iconBasePath)
      UI.ChangeWidget(("iconTable"), "Items", itemList)

      widgetID = None
      while True:
        widgetID = UI.UserInput()
        if widgetID == "cancel":
          break

      UI.CloseDialog()


    # Read a directory with icons.
    #
def readIconDir(dir):
      iconList = list(SCR.Read(Path(".target.dir"), dir))
      ycpbuiltins.y2debug("Dir %1: %2  entries", dir, ycpbuiltins.size(iconList))
#      #TODO #FIXME add ycbbuiltins.filter()
#      #TODO #FIXME add ycbbuiltins.sort()
#      iconList = ycpbuiltins.sort(ycpbuiltins.filter(iconList) do |entry|
#        ycpbuiltins.regexpmatch(entry, "^.*.(png|jpg|PNG|JPG)$")
#      end)
      filtered = []
      for entry in iconList:
          if ycpbuiltins.regexpmatch(entry, "^.*.(png|jpg|PNG|JPG)$"):
              filtered.append(entry)
      
      
      filtered.sort()
      print "returning %d items"%len(filtered)
      return copy.deepcopy(filtered)

TableIconsClient().main()

