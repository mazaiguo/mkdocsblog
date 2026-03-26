---
title: "VB.NET Selection Set samples"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
  - COM Interop
  - Selection
description: "The attached zip file has a VB.NET project that demonstrates how to select objects using .NET and COM Interop. It has three commands :"
author: Autodesk
---
# VB.NET Selection Set samples

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/vbnet-selection-set-samples.html

## 文章内容

By Philippe Leefsma
The attached zip file has a VB.NET project that demonstrates how to select objects using .NET and COM Interop. It has three commands :
SELSET: Demonstrates creating a selection set using AutoCAD Interop.
SELLINE: Demonstrates using the ActiveX GetEntity function to select and query a single entity (a line in this example).
NETSELECT: Shows how to select a AutoCAD entities using the native .NET Select function. Here is the code from this command:
    <Autodesk.AutoCAD.Runtime.CommandMethod("NETSELECT")> _
    Public Sub NetSel()
          Dim doc As Document = Application.DocumentManager.MdiActiveDocument
        Dim db As Database = doc.Database
        Dim ed As Editor = doc.Editor
          Dim pSelRes As PromptSelectionResult = ed.SelectAll()
          Dim dbObj As DBObject
               Using tr As Transaction = db.TransactionManager.StartTransaction
              ' Basic error handling
            Try
                If (pSelRes.Status <> PromptStatus.OK) Then
                    Return
                End If
                  Dim objIdArray() As ObjectId = pSelRes.Value.GetObjectIds()
                  For Each objId As ObjectId In objIdArray
                    dbObj = tr.GetObject(objId, OpenMode.ForRead)
                    ed.WriteMessage(dbObj.GetType.ToString + vbCrLf)
                Next
                  tr.Commit()
              Catch ex As Exception
                ed.WriteMessage(ex.ToString())
                tr.Abort()
            End Try
        End Using
    End Sub
  SelectSetSamples.zip

## 评论

**内容**: xanhnhnn280683@gmail.com said...
Hello forum, I have a small question, would the guide you
I have five single foundation construction civil pile are the same, in one drawing , so you write code that calculate the number of single foundation construction
Reply
12/29/2012 at 11:09 PM

---
**内容**: Abhilash D K said...
Hi,
Can anybody tell me what may be the equivalent code in VB.NET for the below code in ARX:
acutBuildList(RTDXF0, L"SHAPE", NULL)
I tried the following It did not work :
Dim acTypValAr(0) As TypedValue
acTypValAr.SetValue(New TypedValue(DxfCode.Start, "SHAPE"), 0)
Please help
Reply
09/24/2015 at 12:09 AM

---
**内容**: Ben said...
Hi thank you Philippe this code shows how to obtain the handle to an object - but do you know how to select the object itself to allow the user (as opposed to the .net plugin) to then manipulate it within autocad?
Reply
10/22/2016 at 11:32 PM

---
