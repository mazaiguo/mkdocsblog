---
title: "Dynamic Block with Stretch Action"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Block
  - DWG
  - Database
description: "Creating a dynamic block with stretch actions is not possible through the API. A possible way to work around it is to create a set of drawings with..."
author: Autodesk
---
# Dynamic Block with Stretch Action

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/dynamic-block-with-stretch-action.html

## 文章内容

By Balaji Ramamoorthy
Creating a dynamic block with stretch actions is not possible through the API. A possible way to work around it is to create a set of drawings with the dynamic blocks as authoring elements. These drawings will need to be created using the AutoCAD UI. Such drawings can then be inserted when required in any other drawing database using the AutoCAD API.
To create drawings with authoring elements using the AutoCAD UI, follow these steps:
1) Open a new drawing and create the dynamic block (say “Door”) with few stretch actions.
2) Run the “wblock” command in AutoCAD and select the “Door” in the list box and provide the path to a new drawing file (say DoorDynBlock.dwg).
The dynamic block will then be wblocked to "DoorDynBlock.dwg" as an authoring element.
The new drawing ("DoorDynBlock.dwg") can now be inserted in any other drawing to get the dynamic block with stretch actions.
Here is a sample code and the sample drawing :
[CommandMethod("InsertDynBlock", CommandFlags.Session)]
public void InsertDynBlockMethod()
{
    try
    {
        Document activeDoc
                = Application.DocumentManager.MdiActiveDocument;
        using (DocumentLock dl = activeDoc.LockDocument())
        {
            Database db = activeDoc.Database;
            string dynBlockDwgPath
                    = @"C:\Temp\DynBlockWithStretchActions.dwg";
              using (Database dynBlkDb = new Database(false, true))
            {
                dynBlkDb.ReadDwgFile(
                                        dynBlockDwgPath,
                                        System.IO.FileShare.Read,
                                        true,
                                        ""
                                    );
                db.Insert("TestDyn", dynBlkDb, true);
            }
        }
    }
    catch (System.Exception ex)
    {
        Application.DocumentManager.MdiActiveDocument.Editor.WriteMessage(ex.Message);
    }
}
Download DynBlockWithStretchActions

