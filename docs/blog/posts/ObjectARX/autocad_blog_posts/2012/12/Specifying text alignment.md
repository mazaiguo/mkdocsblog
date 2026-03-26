---
title: "Specifying text alignment"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "How do I set up or change a text entity's alignment?"
author: Autodesk
---
# Specifying text alignment

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/specifying-text-alignment.html

## 文章内容

By Daniel Du
Issue
How do I set up or change a text entity's alignment?
Solution
When aligning text you need to use the TextAlignmentPoint property as shown in
the following sample code:
Public Sub test()
   Dim Text As AcadText
   Dim curnam As String
   Dim inpt(0 To 2) As Double
   Dim ht As Double
   
   curnam = "This is a string"
   inpt(0) = 5
   inpt(1) = 5
   inpt(2) = 0
  
   ht = 0.5
   
   Set Text = ThisDrawing.ModelSpace.AddText(curnam, inpt, ht)
   Text.Alignment = acAlignmentMiddleCenter
   Text.TextAlignmentPoint = inpt
End Sub
  For .net API, you can use DBText.AlignmentPoint property.Following information comes from the .net API document:
This function sets pt to be the alignment point for the text object.
If vertical mode is AcDb::kTextBase and horizontal mode is either AcDb::kTextLeft, AcDb::kTextAlign, or AcDb::kTextFit, then the position point (DXF group code 10) is the insertion point for the text object and, for AcDb::kTextLeft, the alignment point is automatically calculated based on the other parameters in the text object. Any setting made by this function are replaced by the newly calculated value.
For all other vertical and horizontal mode combinations, the alignment point is used as the insertion point of the text and the position point is automatically calculated based on the other parameters in the text object.
The alignment point value is the WCS equivalent of DXF group code 11.
Returns Acad::eOk if successful, or Acad::eNotApplicable if the text object's horizontal mode is AcDb::kTextLeft and vertical mode is AcDb::kTextBase.
Here is the code in .net API:
public void MyCommand() // This method can have any name
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
    Database db = doc.Database;
 
    //align point
    Point3d pt = new Point3d(15, 15, 0);
 
    using (DBText text = new DBText())
    {
        text.TextString = "This is a db text";
 
        text.VerticalMode = TextVerticalMode.TextVerticalMid;
        text.HorizontalMode = TextHorizontalMode.TextCenter;
        text.AlignmentPoint = pt;
                
        AddToModelSpace(text, db);
    }
          
}
 
private static void AddToModelSpace(Entity ent, Database db)
{
    using (Transaction trans = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = (BlockTable)trans.GetObject(
            db.BlockTableId, OpenMode.ForRead);
        BlockTableRecord modelSpace = trans.GetObject(
            bt[BlockTableRecord.ModelSpace], 
            OpenMode.ForWrite) as BlockTableRecord;
 
        modelSpace.AppendEntity(ent);
        trans.AddNewlyCreatedDBObject(ent, true);
        trans.Commit();
    }
}
Hope this helps!

## 评论

**内容**: Jason DeVore said...
Thank you!
Reply
11/21/2013 at 11:57 AM

---
**内容**: Jason DeVore said...
This post single-handedly helped me figure out why I was getting exceptions when attempting to align my text in AutoCAD using the .NET API. It seems that there is a conflict when attempting to set both position and alignmentpoint properties. (Only alignmentpoint needs to be set, apparently.) The developer's guide doesn't give much detail to this tidbit!
Reply
11/21/2013 at 12:02 PM

---
**内容**: Prakash B Bajaj said...
Danial Du
Thank you so much for specifying text alignment
Reply
02/21/2023 at 11:58 PM

---
