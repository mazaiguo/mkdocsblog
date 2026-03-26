---
title: "Create a new sheet using COM SheetSet API"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - COM
  - COM Interop
description: "This example will add a sheet to an existing Sheetset (DST file), on this sample c:\temp\test.dst. The "Sheet Creation Template" property needs to ..."
author: Autodesk
---
# Create a new sheet using COM SheetSet API

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/create-a-new-sheet-using-com-sheetset-api.html

## 文章内容

By Augusto Goncalves
This example will add a sheet to an existing Sheetset (DST file), on this sample c:\temp\test.dst. The "Sheet Creation Template" property needs to be set on the sheetset for this example to work properly. The code uses .NET COM interoperability to program COM objects with .NET.
Update: a reference to AcSmComponents Type Library is required. Choose it at the COM tab of Visual Studio.
[CommandMethod("testSheet")]
static public void CmdTestSheet()
{
  Editor ed = Application.DocumentManager.
    MdiActiveDocument.Editor;
  string dstFile = "C:\\temp\\test.dst";
  AcSmSheetSetMgr mgr = new AcSmSheetSetMgr();
  AcSmDatabase db = new AcSmDatabase();
    // try open the database
  try
  {
    db = mgr.OpenDatabase(dstFile, true);
  }
  catch (System.Exception ex)
  {
    ed.WriteMessage(ex.ToString());
    return;
  }
    // lock to perform the operations
  db.LockDb(db);
  try
  {
    IAcSmSheetSet mySheetSet;
    IAcSmSheet newSheet;
    mySheetSet = db.GetSheetSet();
      // check the name and location
    if ((mySheetSet.GetDefDwtLayout().GetFileName() == "")
      || (mySheetSet.GetNewSheetLocation() == null))
    {
      ed.WriteMessage("\nCannot add sheet." +
        " Manually set the Sheet Creation Template");
      return;
    }
    else
    {
      AcSmAcDbLayoutReference lytRef2 =
        mySheetSet.GetDefDwtLayout();
      ed.WriteMessage("\nAdding a sheet using Layout1 in"
        + lytRef2.GetFileName().ToString());
        IAcSmFileReference fileRef2 =
        mySheetSet.GetNewSheetLocation();
      ed.WriteMessage("\nNew drawing will be created in "
        + fileRef2.GetFileName().ToString());
        newSheet = mySheetSet.AddNewSheet(
        "Layout1", "Some Description");
      newSheet.SetTitle("testTitle");
      mySheetSet.InsertComponent(newSheet, null);
    }
  }
  catch (System.Exception ex)
  {
    ed.WriteMessage(ex.ToString());
  }
  finally
  {
    db.UnlockDb(db, true);
    mgr.Close(db);
  }
}

## 评论

**内容**: Jason Huffine said...
I hate to ask an ignorant question here... but where is the SheetSet API? What do I reference in my project?
Reply
09/05/2012 at 08:27 AM

---
**内容**: Augusto Goncalves said in reply to Jason Huffine...
Hi Jason,
Thanks for your question. Actually the post is missing this information. It is required to add reference to AcSmComponents Type Library.
Regards,
Augusto Goncalves
Reply
09/05/2012 at 08:43 AM

---
