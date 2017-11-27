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


      iconList = readIconDir(Ops.add(iconBasePath, "/22x22/apps"))
      iconList = ycpbuiltins.union(
          iconList,
          readIconDir(Ops.add(iconBasePath, "/32x32/apps")))
      iconList = ycpbuiltins.union(
          iconList,
          readIconDir(Ops.add(iconBasePath, "/48x48/apps")))

      itemList = []

      for iconName in ycpbuiltins.foreach(iconList):
        item = Item(
          Id(iconName),
          iconName,
          Term("cell", Term("icon", Ops.add("22x22/apps/", iconName))),
          Term("cell", Term("icon", Ops.add("32x32/apps/", iconName))),
          Term("cell", Term("icon", Ops.add("48x48/apps/", iconName)))
        )
        # y2debug( "Item: %1", item );
        itemList = ycpbuiltins.add(itemList, item)

      UI.CloseDialog() # Close busy dialog

      UI.ChangeWidget("iconTable", "IconPath", iconBasePath)
      UI.ChangeWidget("iconTable", "Items", itemList)

      widgetID = None
      while True:
        widgetID = UI.UserInput()
        if widgetID == "cancel":
          break

      UI.CloseDialog()


    # Read a directory with icons.
    #
    def readIconDir(dir)
      iconList = SCR.Read(Path(".target.dir"), dir).asList()
      ycpbuiltins.y2debug("Dir %1: %2  entries", dir, ycpbuiltins.size(iconList))
      iconList = ycpbuiltins.sort(ycpbuiltins.filter(iconList) do |entry|
        ycpbuiltins.regexpmatch(entry, "^.*.(png|jpg|PNG|JPG)$")
      end)

      copy.deepcopy(iconList)

TableIconsClient().main()

