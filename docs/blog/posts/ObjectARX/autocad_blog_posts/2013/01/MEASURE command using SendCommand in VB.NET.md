---
title: "MEASURE command using SendCommand in VB.NET"
date: 2013-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
  - COM Interop
description: "Is there an example showing how to use the MEASURE command with the ActiveX SendCommand method from AutoCAD VB.NET?"
author: Autodesk
---
# MEASURE command using SendCommand in VB.NET

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/measure-command-using-sendcommand-in-vbnet.html

## 文章内容

By Fenton Webb
Issue
Is there an example showing how to use the MEASURE command with the ActiveX SendCommand method from AutoCAD VB.NET?
Solution
Below is a VB.NET example. Add the following references to the VB.NET Class Library Project:
acmgd.dll
Autodesk.AutoCAD.Interop.Common.dll
Autodesk.AutoCAD.Interop.dll 
NOTE: acdbmgd.dll is not required for this example, as it does not use any .NET database entities.
Another NOTE: be aware that whenever your reference COM interop assemblies, you are instantly tying yourself to the processor type, therefore you will need to consider x86 and x64 build types – Any CPU is not advisable.
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.Interop  
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.Interop.Common 
  <CommandMethod("MYMEASURE", "MYMEASURE", Autodesk.AutoCAD.Runtime.CommandFlags.Transparent)> _
Public Sub MYMEASURE()
  Dim app As AcadApplication = Autodesk.AutoCAD.ApplicationServices.Application.AcadApplication
  Dim obj1, obj2 As Object
      Try
    'Use ActiveX GetEntity function, as we only want to select a single entity
    app.ActiveDocument.Utility.GetEntity(obj1, obj2, "select a polyline which you want to measure")
        'Cast Object to AcadObject
    Dim tmpObj As AcadObject = CType(obj1, AcadObject)
        Dim strObjName As String
    strObjName = tmpObj.ObjectName
        '   Check its a polyline
    If strObjName = "AcDbPolyline" Then
      Dim str1 As String
          'Handle of polyline is used to identify it to MEADSURE command
      str1 = "(handent """ + tmpObj.Handle + """" + ")"
      Dim str As String
          'Insert instances of 'myblock' at 500 unit spacing along polyline
      '(replace myblock with name of your block)
      ' the polyline needs to be longer than 500
      str = "_.measure "
      str = str & str1 & vbCr & "_block" & vbCr & "myblock" & vbCr & "_Yes" & vbCr & "500" & vbCr
      app.ActiveDocument.SendCommand(str)
    End If
      Catch ex As Exception
    ' Print the exception on the command line
    Dim ed As Editor
    ed = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor
    ed.WriteMessage(ex.ToString())
  End Try
End Sub

