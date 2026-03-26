---
title: "Deleting xdata"
date: 2013-01-01
categories:
  - AutoCAD VBA
tags:
  - VBA
description: "How do I delete Xdata that is attached to an entity?"
author: Autodesk
---
# Deleting xdata

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/deleting-xdata.html

## 文章内容

By Xiaodong Liang
Issue
How do I delete Xdata that is attached to an entity?
Solution
The following sample code demonstrates how to delete an Entity's Extended Entity data.
VBA:
Sub test()
   Dim obj As Object
   Dim xtype(0) As Integer
   Dim xvalue(0) As Variant
   xtype(0) = 1001
   'MyApp is assumed to be the registered application.
   xvalue(0) = "MyApp"
   'select an entity
   ThisDrawing.Utility.GetEntity obj, pt, "Pick: "
   ' remove the xdata
   obj.SetXData xtype, xvalue
End Sub
C#:
[CommandMethod("REMXDATA")]
static public void RemoveXdata()
{
    Document doc =
        Autodesk.AutoCAD.ApplicationServices.Application.
        DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Transaction tr =
        db.TransactionManager.StartTransaction();
      using (tr)
    {
        Editor ed =             Application.DocumentManager.MdiActiveDocument.Editor; 
        try
        {
            // Prompt the user to select an entity
            PromptEntityResult ers;
            ers = ed.GetEntity("Pick entity ");
            // Open the selected entity
            Entity ent =
                (Entity)tr.GetObject(ers.ObjectId,
                OpenMode.ForWrite);
            // This call would ensure that the Xdata of the entity
            // associated with ADSK application name only would be removed
            ent.XData = new ResultBuffer(
                new TypedValue(1001, "ADSK"));
            tr.Commit();
        }
        catch (System.Exception ex)
        {
       ed.WriteMessage("Exception while removing Xdata: "
                + ex.Message);
            tr.Abort();
        }
        finally
        {
        }
    }
}

## 评论

**内容**: Ben said...
Hello,
I have two questions:
(1) I am presuming from the above code it is not possible to delete the xdata directly but to merely replace it?
(2) i noticed something in the code: suppose an exception was caught in the try bracket, would the transaction be automatically disposed if it was not cleaned up (with the tr.Abort() call in the catch statement)?
with kind regards,
Ben
Reply
01/18/2016 at 05:25 PM

---
**内容**: Xiaodong Liang said in reply to Ben...
Hi Ben,
1) have you tried to run the code? That will exactly remove the Xdata of the specific app named 'MyApp'.
2) Abort is to terminate this transaction, it does not responsible to dispose the transaction object.
In addition, I’d suggest you could post question on AutoCAD API board. There are many gurus of AutoCAD API there. You would be able to get answer timely. You can enclose the blog url there.
http://forums.autodesk.com/t5/autocad-customization/ct-p/AutoCADTopic1
Reply
01/22/2016 at 10:26 PM

---
