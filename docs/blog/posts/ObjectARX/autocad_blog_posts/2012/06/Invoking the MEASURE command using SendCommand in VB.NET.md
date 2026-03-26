---
title: "Invoking the MEASURE command using SendCommand in VB.NET"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Block
  - C++
description: "There are several ways to invoke an AutoCAD command from a .NET plugin:"
author: Autodesk
---
# Invoking the MEASURE command using SendCommand in VB.NET

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/invoking-the-measure-command-using-sendcommand-in-vbnet.html

## 文章内容

By Stephen Preston
There are several ways to invoke an AutoCAD command from a .NET plugin:
The native .NET SendStringToExecute method is asynchronous, which makes it fiddly to use.
P/Invoking the ObjectARX acedCommand/acedCmd function can cause problems because AutoCAD makes use of Fibers than are not supported in .NET (although it usually works ok).
Invoking the ActiveX SendCommand API introduces a dependency on the COM Interop assemblies, which introduces a platform dependency into your code that you may otherwise not have had in your .NET plug-in. (And read this blog post on some synchronous/asynchronous issues).
You pays your money and you takes your chance!
The following code demonstrates the use of SendCommand to invoke the AutoCAD MEASURE command to insert an instance of a block along a lightweight polyline. You’ll need a drawing containing a polyline over 10 units long and a block called ‘myblock’ to test the code. Make sure you reference the Autodesk.AutoCAD.Interop and Autodesk.AutoCAD.Interop.Common assemblies from the inc-win32 or inc-x64 directories of your ObjectARX SDK (depending on whether you’re working on a 32- or 64- bit platform).
    <CommandMethod("MYMEASURE")> _
    Public Sub MYMEASURE()
      Dim app As AcadApplication = Application.AcadApplication
      Dim obj1, obj2 As Object
      'Use ActiveX GetEntity function, as we only want to select a single entity
      app.ActiveDocument.Utility.GetEntity(obj1, obj2,
                        "select a polyline which you want to measure")
      'Cast Object to AcadObject
      Dim tmpObj As AcadObject = CType(obj1, AcadObject)
      Dim strObjName As String
      strObjName = tmpObj.ObjectName
      '   Check its a polyline
      If strObjName = "AcDbPolyline" Then
        Dim str1 As String
        'Handle of polyline is used to identify it to MEASURE command
        str1 = "(handent """ + tmpObj.Handle + """" + ")"
        Dim str As String
        'Insert instances of 'myblock' at 10 unit spacing along polyline
        '(replace myblock with name of your block)
        ' the polyline needs to be longer than 10
        str = "_measure "
        str = str & str1 & vbCr & "_block" & vbCr & "myblock" &
                                    vbCr & "_Y" & vbCr & "10" & vbCr
        app.ActiveDocument.SendCommand(str)
      End If
    End Sub

