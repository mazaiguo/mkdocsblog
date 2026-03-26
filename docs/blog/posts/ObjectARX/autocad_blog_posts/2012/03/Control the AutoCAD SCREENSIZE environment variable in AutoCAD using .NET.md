---
title: "Control the AutoCAD SCREENSIZE environment variable in AutoCAD using .NET"
date: 2012-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "The SCREENSIZE system variable is a read-only system variable that stores the current viewport size in pixels."
author: Autodesk
---
# Control the AutoCAD SCREENSIZE environment variable in AutoCAD using .NET

发布日期: 2012-03-01

原始链接: https://adndevblog.typepad.com/autocad/2012/03/control-the-autocad-screensize-environment-variable-in-autocad-using-net.html

## 文章内容

By Gopinath Taget
The SCREENSIZE system variable is a read-only system variable that stores the current viewport size in pixels.
However, we might feel the need some times to adjust the SCREENSIZE. For instance, so you you might want to export the model space to WMF format at a specific size and aspect ratio.
One easy way to change the SCREENSIZE is to just change the active document size:
<CommandMethod("ChangeScreenSize")> _
    Public Sub changeScreenSize()
        Dim doc As Document = Application.DocumentManager.
        MdiActiveDocument
        Dim docWindow As Window = doc.Window
        Dim size As Size = docWindow.Size
          Dim ed As Editor = doc.Editor
        ed.WriteMessage(vbCrLf + "Document Size:" + vbCrLf +
          size.ToString() + vbCrLf)
          docWindow.WindowState = Window.State.Normal
          docWindow.Size = New Size(500, 500)
      End Sub
Please not that the document window size and the screen size are not exactly the same. the document window tends to be slightly bigger due to the additional non-editor parts of the drawing document window. So you will have to experiment with it a little bit to set it to the right screen size you need.

