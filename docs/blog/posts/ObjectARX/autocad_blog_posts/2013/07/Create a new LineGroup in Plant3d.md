---
title: "Create a new LineGroup in Plant3d"
date: 2013-07-01
categories:
  - Plant 3D
tags:
  - Database
  - Plant 3D
description: "When creating a new LineGroup, the PipingObjectAdder should already create line groups or take an existing one. However, here’s some code which sho..."
author: Autodesk
---
# Create a new LineGroup in Plant3d

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/create-a-new-linegroup-in-plant3d.html

## 文章内容

by Fenton Webb
When creating a new LineGroup, the PipingObjectAdder should already create line groups or take an existing one. However, here’s some code which shows how to do it manually:
int CreateUnassignedLineGroup(PipingProject prjpart)
{
    // Create a new line group in project database
    //
    DataLinksManager dlm = prjpart.DataLinksManager;
    PnPDatabase db = dlm.GetPnPDatabase();
      PnPTable tbl = db.Tables["P3dLineGroup"];
           PnPRow row = tbl.NewRow();
    tbl.Rows.Add(row);
      return row.RowId;
}
  void AssignToLineGroup(PipingProject prjpart, ObjectId partId, int cacheId, int groupId)
{
    // Assign an entity's row to line group
    //
    DataLinksManager dlm = prjpart.DataLinksManager;
    PnPDatabase db = dlm.GetPnPDatabase();
      // Relate objects to line group
    //
    dlm.Relate("P3dLineGroupPartRelationship",
               "LineGroup", groupId,
               "Part", cacheId);
      // Also relate drawing to line group
    //
    Database acdb = partId.Database;
    int dwgId = dlm.GetDrawingId(acdb);
    if (dwgId != -1)
    {
        dlm.Relate("P3dDrawingLineGroupRelationship",
                    "Drawing", dwgId,
                    "LineGroup", groupId);
    }
}

## 评论

**内容**: Jason said...
Please explain what the variable "cacheID" in "AssignToLineGroup" is supposed to contain. I am trying to assign a selection set to an existing Line Group and thought I could use this as an example but can't quite get it together. Thanks!
Reply
07/20/2013 at 11:57 AM

---
**内容**: Norbert Meier said...
This blog and the blog “Setting the Line Number Tag in AutoCAD Plant3d”
helped me to solve the customer request: Add the Line Number Tag of the pipe to the newly created pipe supports of your 3rd Party application.
The method “AssignLineGroupOfPipeToSupport” shows how it’s done. The parameter pipe and support are used to perform the necessary steps.
1. Getting the LineGroup(s) from the Pipe object
2. Assigning the found LineGroup(s) to the support object
Option Explicit On
Imports System
Imports System.Math
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.ApplicationServices.Application
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.Geometry
Imports System.Collections.Specialized
Imports Autodesk.AutoCAD.EditorInput
Imports Microsoft.VisualBasic
Imports Autodesk.ProcessPower.PnP3dDataLinks
Imports Autodesk.ProcessPower.P3dProjectParts
Imports Autodesk.ProcessPower.ProjectManager
Imports Autodesk.ProcessPower.PlantInstance
Imports Autodesk.ProcessPower.DataObjects
Imports Autodesk.ProcessPower
Imports LISEGA.Licad4Plant3D.SupportClasses
Imports Autodesk.ProcessPower.PnP3dObjects
Imports Autodesk.AutoCAD.ApplicationServices.DocumentCollectionExtension
Imports Autodesk.AutoCAD.ApplicationServices.DocumentExtension
'//////////////////////////////////////////////////////////////////////////////////////////////////////////////
'// Refer to:
'// http://adndevblog.typepad.com/autocad/2012/08/setting-the-line-number-tag-in-autocad-plant3d.html
'// http://adndevblog.typepad.com/autocad/2013/07/create-a-new-linegroup-in-plant3d.html
'//
'//////////////////////////////////////////////////////////////////////////////////////////////////////////////
Public Shared Class LineGroupAssignmentHelper
'///////////////////////////////////////////////////////////////////////////////////////////////
'//
'// Adding the Line Number Tag information of pipe to a custom support
'//
'///////////////////////////////////////////////////////////////////////////////////////////////
Public Shared Sub AssignLineGroupOfPipeToSupport(ByRef Pipe As Pipe, ByRef sup As PnP3dObjects.Support)
'// Getting access to the project database
Dim currentProj As PlantProject = PlantApplication.CurrentProject
Dim pipeProj As PipingProject = currentProj.ProjectParts("Piping")
Dim dlm As Autodesk.ProcessPower.DataLinks.DataLinksManager = pipeProj.DataLinksManager
'// Editor is used for writing status information
Dim ed As Editor = Application.DocumentManager.MdiActiveDocument.Editor
'// get the 3d data links manager
Dim dlm3d As DataLinksManager3d = pipeProj.DataLinksManager3d
'// and then get the row id for the selected object (Pipe)
Dim PipeRowId As Integer = dlm.FindAcPpRowId(Pipe.ObjectId)
'// Parts are related to pipe line group via P3dLineGroupPartRelationship.
'// So we need to traverse this relationship to get line group row id
Dim lgid As PnPRowIdArray = dlm.GetRelatedRowIds("P3dLineGroupPartRelationship", "Part",
PipeRowId, "LineGroup")
If (lgid Is Nothing) Or (lgid.Count = 0) Then
'// line group was not found. May happen, for example, if Equipment is picked.
ed.WriteMessage(vbNewLine & "No LineGroup relation to pipe defined!")
Else
'// this is line group row in the data. (PnPRowIdArray is in fact list)
Dim enumerator As IEnumerator = lgid.GetEnumerator()
While (enumerator.MoveNext())
Dim lgRowId As Integer = enumerator.Current
' Get the rowid of the support
Dim SupportRowId As Integer = dlm.FindAcPpRowId(sup.ObjectId)
' and assign the line group of the pipe also to the support
dlm.Relate("P3dLineGroupPartRelationship", "LineGroup", lgRowId, "Part", SupportRowId)
End While
End If
End Sub
End Class
Reply
07/31/2013 at 11:31 PM

---
**内容**: Wjasonhudson@gmail.com said in reply to Norbert Meier...
Thanks for the help! So 'cacheid' is simply the rowid of the object. :)
Reply
08/05/2013 at 04:39 PM

---
