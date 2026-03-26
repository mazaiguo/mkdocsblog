---
title: "Using WblockCloneObjects to copy a Layout from the active document to a new drawing"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Block
  - DWG
description: "Another Friday afternoon, another DevNote migrated. This VB.NET sample copies a Layout from one drawing to another using CopyFrom and WblockCloneOb..."
author: Autodesk
---
# Using WblockCloneObjects to copy a Layout from the active document to a new drawing

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/using-wblockcloneobjects-to-copy-a-layout-from-the-active-document-to-a-new-drawing.html

## 文章内容

By Stephen Preston
Another Friday afternoon, another DevNote migrated. This VB.NET sample copies a Layout from one drawing to another using CopyFrom and WblockCloneObjects.
    <CommandMethod("copyLayout")> _
    Sub copyLayoutToNewDwg()
      Dim layout As New Layout
      Dim layoutNameInCurDwg As String = "Layout1"
      Dim lytMgr As LayoutManager
      Dim ed As Editor =
        Application.DocumentManager.MdiActiveDocument.Editor()
      Dim layoutId As ObjectId
      'Get orignal drawing
      Dim db As Database =
        Application.DocumentManager.MdiActiveDocument.Database
      'create a new drawing
      Dim newDb As Database = New Database(True, False)
      Using tr As Transaction = newDb.TransactionManager.StartTransaction()
        'Make the working database the new database
        HostApplicationServices.WorkingDatabase = newDb
        ' Create a new Layout
        Dim newLytMgr As LayoutManager = LayoutManager.Current()
        Dim newLayoutId As ObjectId = newLytMgr.CreateLayout("newLayout")
        Dim newLayout As Layout = tr.GetObject(newLayoutId, OpenMode.ForWrite)
        'Make the original database the working database
        HostApplicationServices.WorkingDatabase = db
        Using tr2 As Transaction = db.TransactionManager.StartTransaction()
          ' Get the dictionary of the original database
          Dim lytDict As DBDictionary =
            tr2.GetObject(db.LayoutDictionaryId, OpenMode.ForRead)
          'Make sure the layout existes in the original database
          If Not lytDict.Contains(layoutNameInCurDwg) Then
            ed.WriteMessage("Layout named ""Layout1"" does not exist in current dwg")
            Return
          End If
          'Get the layout in the original database
          lytMgr = LayoutManager.Current()
          layoutId = lytMgr.GetLayoutId(layoutNameInCurDwg)
          layout = tr2.GetObject(layoutId, OpenMode.ForRead)
          newLayout.CopyFrom(layout)
          'Get the block table record of the existing layout
          Dim blkTableRec As BlockTableRecord
          blkTableRec =
            tr2.GetObject(layout.BlockTableRecordId, OpenMode.ForRead)
          'Get the object ids of the objects in the existing block table record
          Dim objIdCol As New ObjectIdCollection()
          For Each objId As ObjectId In blkTableRec
            objIdCol.Add(objId)
          Next
          ' Clone the objects to the new layout
          Dim idMap As IdMapping = New IdMapping()
          newDb.WblockCloneObjects(objIdCol,
                                   newLayout.BlockTableRecordId,
                                   idMap,
                                   DuplicateRecordCloning.MangleName,
                                   False)
          tr2.Commit()
        End Using
        tr.Commit()
        newDb.SaveAs("c:\newLayout.dwg", DwgVersion.Newest)
      End Using
    End Sub

## 评论

**内容**: André Dagenais said...
Hi Stephen,
I use your code to create a function to import a layout from a drawing file in the current drawing. I'm working in VB .Net. But I had a problem when copying the objects on the layout. It is working but it is also copying new "bizarre" viewport in the current layout.
I change the parameter DuplicateRecordCloning from MangleName to Ignore and the problem disapears. What is the difference between these differents options?
Here you will find my function:
Public Function GetLayoutFromDWG(ByVal DWGFilename As String, ByVal LayoutName As String) As ObjectId
Dim bReturnValue As ObjectId = Nothing
Dim ed As Editor = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor()
Dim sourceDb As Database = New Database(False, True)
Dim destDb As Database = ed.Document.Database()
Dim acDoc As Document = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument
Try
''Read the DWG into a side database
sourceDb.ReadDwgFile(DWGFilename, System.IO.FileShare.Read, True, "")
Using doclock As DocumentLock = acDoc.LockDocument
Using tm1 As Transaction = destDb.TransactionManager.StartTransaction()
'Création de la nouvelle présentation
Dim newLytMgr As LayoutManager = LayoutManager.Current()
Dim newLayoutId As ObjectId = newLytMgr.CreateLayout(LayoutName)
Dim newLayout As Layout = tm1.GetObject(newLayoutId, OpenMode.ForWrite)
HostApplicationServices.WorkingDatabase = sourceDb
Using tm2 As Transaction = sourceDb.TransactionManager.StartTransaction()
''Open the layout dictionary
Dim layoutDic As DBDictionary = tm2.GetObject(sourceDb.LayoutDictionaryId, OpenMode.ForRead, False)
If Not layoutDic.Contains(LayoutName) Then
bReturnValue = Nothing
Else
Dim sourceLytMgr As LayoutManager = LayoutManager.Current()
Dim sourceLayoutId = sourceLytMgr.GetLayoutId(LayoutName)
Dim sourceLayout As Layout = tm2.GetObject(sourceLayoutId, OpenMode.ForRead)
newLayout.CopyFrom(sourceLayout)
Dim blkTableRec As BlockTableRecord
blkTableRec = tm2.GetObject(sourceLayout.BlockTableRecordId, OpenMode.ForRead)
'Get the object ids of the objects in the existing block table record
Dim objIdCol As New ObjectIdCollection()
For Each objId As ObjectId In blkTableRec
objIdCol.Add(objId)
Next
' Clone the objects to the new layout
Dim idMap As IdMapping = New IdMapping()
destDb.WblockCloneObjects(objIdCol, newLayout.BlockTableRecordId, idMap, DuplicateRecordCloning.Ignore, False)
'destDb.WblockCloneObjects(objIdCol, newLayout.BlockTableRecordId, idMap, DuplicateRecordCloning.MangleName, False)
tm2.Commit()
bReturnValue = newLayoutId
End If
End Using
If Not bReturnValue = Nothing Then tm1.Commit()
End Using
End Using
Catch ex As Autodesk.AutoCAD.Runtime.Exception
ed.WriteMessage("\nImpossible d'importer la présentation " & LayoutName & ": " & ex.Message)
Finally
HostApplicationServices.WorkingDatabase = destDb
End Try
sourceDb.Dispose()
Return bReturnValue
End Function
Regards
André
Reply
07/20/2012 at 12:23 PM

---
**内容**: Madhukar Moogala said...
Hi Andre,
Take a look at the ObjectARX documentation for AcDbDatabase::wblockCloneObjects() for an explanation of Mangle vs Ignore. This governs how AutoCAD deals with when duplicate symbol or dictionary names during the clone operation. If the Ignore option works for you, then go ahead and use it.
Can't comment on the bizarre viewport without seeing it.
Cheers,
Stephen
Reply
07/20/2012 at 01:01 PM

---
**内容**: Stephan Gumpert said...
I seam to get the same problem here.
I end up with an extra Viewport surrounding the Drawing sheet in my Exported layout.
Apart from this everything work like a dream
I can't explain why? Do you have any ideas?
Reply
05/04/2014 at 08:00 PM

---
**内容**: Anton said...
There is an example of your function in C#. Probably somebody need it.
private static void CopyLayout()
{
var curDwgLayout = "Layout1";
var ed = AcadCurrentInstances.Editor;

var db = AcadCurrentInstances.ThisDocument.Database;
var newDb = new Database(true, false);
using (var newDbTr = newDb.TransactionManager.StartTransaction())
{
//Make the working database the new database
HostApplicationServices.WorkingDatabase = newDb;

// Create a new Layout
var newLayoutMngr = LayoutManager.Current;
var newLayoutId = newLayoutMngr.CreateLayout(curDwgLayout);
var newLayout = (Layout)newDbTr.GetObject(newLayoutId, OpenMode.ForWrite);

// Make the original database the working database
HostApplicationServices.WorkingDatabase = db;
using (var dbTr = db.TransactionManager.StartTransaction() )
{
var layoutDictionary = (DBDictionary)dbTr.GetObject(db.LayoutDictionaryId, OpenMode.ForRead);
if (!layoutDictionary.Contains(curDwgLayout))
{
ed.WriteMessage("Layout named \"Layout1\" does not exist in current dwg ");
return;
}

//Get the layout in the original database
var layoutMngr = LayoutManager.Current;
var layoutId = layoutMngr.GetLayoutId(curDwgLayout);
var layout = (Layout)dbTr.GetObject(layoutId, OpenMode.ForRead);
newLayout.CopyFrom(layout);
//Get the block table record of the existing layout
var layoutTableRecord =
(BlockTableRecord) dbTr.GetObject(layout.BlockTableRecordId, OpenMode.ForRead);
//Get the object ids of the objects in the existing block table record
var objIdCol = new ObjectIdCollection();
foreach (var layoutOBjectId in layoutTableRecord)
{
objIdCol.Add(layoutOBjectId);
}
//Clone the objects to the new layout
var idMap = new IdMapping();
newDb.WblockCloneObjects(objIdCol, newLayout.BlockTableRecordId, idMap,
DuplicateRecordCloning.MangleName, false);
dbTr.Commit();
}
newDbTr.Commit();
}
}
Reply
11/25/2016 at 09:24 AM

---
