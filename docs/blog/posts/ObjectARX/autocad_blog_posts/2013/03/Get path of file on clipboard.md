---
title: "Get path of file on clipboard"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - DWG
description: "As mentioned in Kean's blog post, when you select entities in a drawing inside AutoCAD and run COPYCLIP (Ctrl+C) then AutoCAD will WBLOCK out the s..."
author: Autodesk
---
# Get path of file on clipboard

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/get-path-of-file-on-clipboard-.html

## 文章内容

By Adam Nagy
As mentioned in Kean's blog post, when you select entities in a drawing inside AutoCAD and run _COPYCLIP (Ctrl+C) then AutoCAD will WBLOCK out the selected entities into a temp DWG file. The content that's placed on the clipboard will also contain the path to that temp file. In case you would like to use that file, here is one way to find out its path:
Public Function GetClipboardFilePath() As String
  Dim dataObject As IDataObject =
    System.Windows.Clipboard.GetDataObject()
    ' Get the list of available formats
  Dim formats() As String = dataObject.GetFormats()
    For Each format As String In formats
    ' In case of AutoCAD 2013 this would be "AutoCAD.R19"
    If format.StartsWith("AutoCAD.") Then
      Using stream As MemoryStream = dataObject.GetData(format)
        ' Unicode encoding is 16 bit (2 bytes) just like ACHAR
        Using reader As TextReader =
          New StreamReader(stream, System.Text.Encoding.Unicode)
          ' 0..259 = 260
          Dim text(259) As Char
          reader.Read(text, 0, 260)
          ' There will be lots of 0 value characters in the array
          ' that we need to clean up  
          Return New String(text).TrimEnd(New Char(){Chr(0)})  
        End Using
      End Using
    End If
  Next
    Return Nothing
End Function

