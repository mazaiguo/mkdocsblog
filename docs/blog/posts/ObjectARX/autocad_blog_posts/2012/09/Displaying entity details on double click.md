---
title: "Displaying entity details on double click"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - Selection
description: "On double click of an entity I wish to show its details on a custom form. Can you show me how to do this ?"
author: Autodesk
---
# Displaying entity details on double click

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/displaying-entity-details-on-double-click.html

## 文章内容

By Balaji Ramamoorthy
Issue
On double click of an entity I wish to show its details on a custom form. Can you show me how to do this ?
Solution
Doing this involves two steps :
1) Creating a double click action which invokes a command to display the custom form.
2) Retrieving the selected entity that was double-clicked using the Implied selection.
Here is the sample code to create a double-click action that invokes the custom command :
// Add reference to AcCui.dll
using Autodesk.AutoCAD.Customization;
[CommandMethod("RegisterDCA")]
public void RegisterDoubleClickActionMethod()
{
    string mainCuiFile
    = (string)Application.GetSystemVariable("MENUNAME") + ".cuix";
    CustomizationSection cs = new CustomizationSection(mainCuiFile);
      int index = 0;
    DoubleClickAction circleDoubleClickAction = null;
    foreach (DoubleClickAction dca in cs.MenuGroup.DoubleClickActions)
    {
        if (dca.Name.Equals("My Double click"))
        {
            cs.MenuGroup.DoubleClickActions.Remove(index);
            break;
        }
        index++;
    }
      index = 0;
    MacroGroup myMacroGroup = null;
    foreach (MacroGroup mg in cs.MenuGroup.MacroGroups)
    {
        if (mg.Name.Equals("myMacroGroup"))
        {
            cs.MenuGroup.MacroGroups.Remove(index);
            break;
        }
        index++;
    }
      if (circleDoubleClickAction == null && myMacroGroup == null)
    {
        DoubleClickAction dblClickAction
        = new DoubleClickAction(cs.MenuGroup, "My Double click", -1);
          dblClickAction.Description = "Double Click Customization";
        dblClickAction.ElementID = "EID_mydblclick";
        dblClickAction.DxfName = "Circle";
        DoubleClickCmd dblClickCmd = new DoubleClickCmd(dblClickAction);
          MenuMacro macroMyForm;
        MacroGroup myMacGroup
                = new MacroGroup("myMacroGroup", cs.MenuGroup);
        macroMyForm
        = myMacGroup.CreateMenuMacro
                            (
                                "testMyForm",
                                "^C^C_MyForm ",
                                "ID_MyFormCmd",
                                "My Form help",
                                MacroType.Any,
                                "TESTMYFORM_BMP",
                                "TESTMYFORM_BMP",
                                "Test MyForm label"
                            );
          dblClickCmd.MacroID = macroMyForm.ElementID;
        dblClickAction.DoubleClickCmd = dblClickCmd;
          if (cs.IsModified)
            cs.Save();
    }
}

