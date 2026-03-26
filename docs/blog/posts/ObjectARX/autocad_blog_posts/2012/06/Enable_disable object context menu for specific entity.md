---
title: "Enable/disable object context menu for specific entity"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "As mentioned my one of previous post you can add a object specific context menu which will be appended to AutoCAD context menu when that object typ..."
author: Autodesk
---
# Enable/disable object context menu for specific entity

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/enabledisable-object-context-menu-for-specific-entity.html

## 文章内容

By Virupaksha Aithal
As mentioned my one of previous post you can add a object specific context menu which will be appended to AutoCAD context menu when that object type is selected. But there are scenarios where you may have to control the visibility/accessibility of this context menu on different conditions. Below code shows a simple approach which shows the context menu only when selected entity contains a particular XDATA.
[CommandMethod("XDataContextMenuTest")]
static public void XDataContextMenuTest()
{
    ContextMenuExtension contextMenu =
                                new ContextMenuExtension();
      MenuItem item0 = new MenuItem("Line context menu");
    contextMenu.MenuItems.Add(item0);
    MenuItem Item1 = new MenuItem("Test1");
    Item1.Click += new EventHandler(Item1_Click);
    item0.MenuItems.Add(Item1);
    MenuItem Item2 = new MenuItem("Test2");
    Item1.Click += new EventHandler(Item2_Click);
    item0.MenuItems.Add(Item2);
      //ADD the popup item
    contextMenu.Popup += new EventHandler(contextMenu_Popup);
      //for custom entity, replace the "Line" with .NET
    //(managed) wrapper of custom entity
    Application.AddObjectContextMenuExtension(
                Line.GetClass(typeof(Line)), contextMenu);
  }
static void Item1_Click(object sender, EventArgs e)
{
    Application.ShowAlertDialog("Item 1 clicked\n");
}
static void Item2_Click(object sender, EventArgs e)
{
    Application.ShowAlertDialog("Item 2 clicked\n");
}
  static void contextMenu_Popup(object sender, EventArgs e)
{
    try
    {
        ContextMenuExtension contextMenu =
                                      sender as ContextMenuExtension;
          if (contextMenu != null)
        {
            Document doc =
                       Application.DocumentManager.MdiActiveDocument;
            Editor ed = doc.Editor;
            // This is the "Root context menu" item
            MenuItem rootItem = contextMenu.MenuItems[0];
              PromptSelectionResult acSSPrompt = ed.SelectImplied();
              bool bEnable = false;
              if (acSSPrompt.Status == PromptStatus.OK)
            {
                SelectionSet set = acSSPrompt.Value;
                ObjectId[] ids = set.GetObjectIds();
                  //if only one selected
                if (ids.Length == 1)
                {
                    //get the selection
                    ObjectId id = ids[0];
                    Database db = doc.Database;
                    using (Transaction tx =
                            db.TransactionManager.StartTransaction())
                    {
                        DBObject ent =
                                  tx.GetObject(id, OpenMode.ForRead);
                          using (ResultBuffer result =
                           ent.GetXDataForApplication("CONTEXTMENU"))
                        {
                            if (result != null)
                            {
                                bEnable = true;
                            }
                        }
                          tx.Commit();
                    }
                }
            }
              rootItem.Enabled = bEnable;
        }
    }
    catch
    {
    }
}

## 评论

**内容**: BlackBox said...
Hi Viru,
If I have implemented multiple context menus, but am having a problem with only two.
Specifically, one for BlockReference, and one for Table. How to I prevent them both from being displayed when a Table is selected?
Example:

RXClass blockRx = BlockReference.GetClass(typeof(BlockReference));
acApp.AddObjectContextMenuExtension(blockRx , blockMenu);
RXClass tableRx = Table.GetClass(typeof(Table));
acApp.AddObjectContextMenuExtension(tableRx , tableMenu);
My implementation works well for all other Types, having to only call AddObjectContextMenuExtension() once, but the two I mention are the only ones that show both context menus as described above.
I'm trying to avoid having to repeated calls to AddObjectContextMenuExtension(), and RemoveObjectContextMenuExtension() to prevent this undesired behavior.
Thanks
Reply
04/06/2013 at 10:48 AM

---
**内容**: BlackBox said...
After some testing, I learned that the issue was due to Table deriving from BlockReference. Instead of having two separate context menus (one for each) I only need one context menu for both (specifically for BlockReference), and a logical test of a non-Null cast 'as Table' within the Popup Event to Remove()/Add() the appropriate MenuItems.
Reply
04/08/2013 at 06:44 AM

---
**内容**: Viru said...
Hi,
Thanks for letting us know. Yes ,Table is also a type of block reference.
regards
Viru
Reply
04/09/2013 at 12:13 AM

---
