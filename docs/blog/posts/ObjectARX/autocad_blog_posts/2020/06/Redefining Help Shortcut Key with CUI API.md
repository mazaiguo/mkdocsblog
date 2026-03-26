---
title: "Redefining Help Shortcut Key with CUI API"
date: 2020-06-01
categories:
  - AutoCAD
tags:
  - API
  - CUI
  - Selection
description: "There is common need to change shortcut assigned for Help from F1 to some other key, if you look at keypad layout F1 and ESC keys are adjacent to e..."
author: Autodesk
---
# Redefining Help Shortcut Key with CUI API

发布日期: 2020-06-01

原始链接: https://adndevblog.typepad.com/autocad/2020/06/redefining-help-shortcut-key-with-cui-api.html

## 文章内容

By Madhukar Moogala
There is common need to change shortcut assigned for Help from F1 to some other key, if you look at keypad layout F1 and ESC keys are adjacent to each other, designers often use ESC to cancel running command, or deselect the objects from selection. As the F1 key is adjacent chances of pressing this key accidently is quite high, F1 pops up a Help window, which in said cases is counter productive.
To avoid this, we can assign F1 to a Cancel command and CTRL+ALT+F1 to Help.


 public static void RedefineHelpKey()
{
string mainCuiFile = (string)Application.GetSystemVariable("MENUNAME");
mainCuiFile += ".cuix";
var doc = Application.DocumentManager.MdiActiveDocument;
var db = doc.Database;
var ed = doc.Editor;
CustomizationSection cs = new CustomizationSection(mainCuiFile);
AcceleratorCollection acCollection = cs.MenuGroup.Accelerators;

//This is to get Help menu macro.
var macros = from MacroGroup mg in cs.MenuGroup.MacroGroups
        from MenuMacro mm in mg.MenuMacros
        where mm.ElementID.Equals("ID_Help") || mm.ElementID.Equals("ID_Cancel")
        select mm;
foreach(MenuMacro menuMacro in macros)
{
if (menuMacro.ElementID.Equals("ID_Help"))
{

MenuAccelerator macHelp = new MenuAccelerator(menuMacro,
                            /*ShortCutKeyCombination*/"CTRL+ALT+H",
                                cs.MenuGroup);
if (acCollection.Contains(macHelp))
{
    ed.WriteMessage($"\n True MenuAccelerator Contains.");
}
else
{
    acCollection.Add(macHelp);
}
                    

}
if (menuMacro.ElementID.Equals("ID_Cancel"))
{
//Assigning Cancel to F1
MenuAccelerator macCancel = new MenuAccelerator(menuMacro,
                                        /*ShortCutKeyCombination*/"F1",
                                        cs.MenuGroup);
if (acCollection.Contains(macCancel))
{
    ed.WriteMessage($"\n True MenuAccelerator Contains.");
}
else
{
    acCollection.Add(macCancel);
}                 

}
}


//This will create backup CUIX!
cs.Save(true);
            

}             
Note:
If the changes don't reflect immediately, a restart of AutoCAD is needed, this is because, we are attempting to change the main CUI.
A utility function to list shortcut keys we have redefined
[CommandMethod("LISTMAC")]
public static void ListMenuAccelerators()
{
var doc = Application.DocumentManager.MdiActiveDocument;
var db = doc.Database;
var ed = doc.Editor;
string mainCuiFile = (string)Application.GetSystemVariable("MENUNAME");
mainCuiFile += ".cuix";
CustomizationSection cs = new CustomizationSection(mainCuiFile);
AcceleratorCollection acCollection = cs.MenuGroup.Accelerators;
var q = from MenuAccelerator menuAcltr in acCollection
        where menuAcltr.Name.Contains("Help") || 
       menuAcltr.Name.Contains("Cancel")
        select menuAcltr;
if (q != null && q.ToList().Count > 0)
{


    foreach (var m in q.ToList())
    {
        ed.WriteMessage($"\n Name: {m.Name}\n\tAccerlerator ShortcutKey: {m.AcceleratorShortcutKey}");
    }

                
}
}
Demo

## 评论

**内容**: Greg said...
The ESC function needs updating. In current versions of Civil 3D if your cursor is in the drawing area (cross-hairs active) and you hit Esc it will cancel a command or deselect as it is supposed to and then often the cross-hairs are replaced by a mouse cursor. Presumably as some tool palette or other UI element is activated.
The other associated problem is constantly starting a crossing window just because you are clicking to [re-]activate the drawing window. All you are doing is trying to activate the cross-hairs so you can do something or type a command so it changes the mouse from an arrow to the cross-hairs and starts a crossing window all in one click which it should not do.
Reply
07/23/2020 at 04:51 PM

---
