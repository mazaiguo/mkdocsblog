---
title: "Accessing LDATA values from VBA"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - AutoLISP
  - C++
  - COM
  - ObjectARX
description: "A VLISP function can be used to create a dictionary just like:"
author: Autodesk
---
# Accessing LDATA values from VBA

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/accessing-ldata-values-from-vba.html

## 文章内容

By Daniel Du
Issue
A VLISP function can be used to create a dictionary just like:
(vlax-ldata-put "Test" "Helper" "Good")
And a dictionary named "Test" is created, and a (vlax-ldata-get "Test" "Helper") retrieves the return value, "Good". From VBA, how can I get the dictionary data value of "Good"?
Solution
VLISP ldata is attached to a custom object with class name "vlo_VL" and then the object is added to the Named Object Dictionary. However, a custom object is not penetrable by means of the VBA object model alone. You cannot create custom entities/objects with VBA, but you can develop custom entities with ObjectARX and create an ActiveX interface to it so that it can be used within VBA. Unfortunately, there is no direct interface (or Automation server) to a vlo_VL object.
The AutoCAD Visual LISP Automation server (an unsupported interface) can be used to bridge the gap between VBA macro and the LISP environment, though.
If the following has already been entered successfully at the command line:
(vl-load-com)
(vlax-ldata-put "Test" "Helper" "Good")
Then, with a little effort a VBA macro can use the LISP server's generalized object model:

```csharp
Function readEvalHelper(app As Object)
    ' this is a helper function
    vld = app.ActiveDocument
    Dim vlf_read As Object
    vlf_read = vld.Functions.Item("read")

    Dim vl_obj1 As Object
    vl_obj1 = vlf_read.funcall("(defun read-eval (arg)(eval (read arg)))")

    Dim vlf_eval As Object
    vlf_eval = vld.Functions.Item("eval")

    Dim vl_obj2 As Object
    vl_obj2 = vlf_eval.funcall(vl_obj1)

End Function

Public Sub vlsGetLData()
    Dim vlApp As Object
    vlApp = CreateObject("VL.Application.16")

    readEvalHelper(vlApp)
     
    Dim invokeIt As Object
    invokeIt = vlApp.ActiveDocument.Functions.Item("read-eval")
    invokeIt.funcall("(setq lDatum (vlax-ldata-get ""Test"" ""Helper""))")
     
    sym = vlApp.ActiveDocument.Functions.Item("read").funcall("lDatum")
    GetLispSym = vlApp.ActiveDocument.Functions.Item("eval").funcall(sym)
    MsgBox("Key's data is:" + Chr(13) + GetLispSym)

End Sub
```

## 评论

**内容**: Bert Piercey said...
I tried using this and it does not seem to be able to create the object vlApp = CreateObject("VL.Application.16").
Reply
11/03/2015 at 11:43 AM

---
**内容**: Joris Claassen said...
CreateObject("VL.Application.16") is available when you have a specific version (or range of versions) of AutoCAD.
To make it easier (not!) the numbering differens for a lot things:
AutoCAD   version for       first 6      version for 
program   COM access*   chars of   COM access
version     to program      dwg file     to VL
  2004             16            AC1018             ?
  2007             17            AC1021             ? 
  2010             18            AC1024           16?   
  2013             19            AC1027             ? 

*: with either CreateObject or GetObject
to be checked in
regedit.exe with:     HKEY_CLASSES_ROOT\AutoCAD.Application.##

reg.exe:
    reg query HKCR  /f "AutoCAD.Application.*"
      (likewise for VL object:
        reg query HKCR  /f "VL.Application.*")

Reply
06/10/2016 at 02:05 AM

---
