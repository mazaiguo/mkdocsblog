---
title: "Copy a layout with its entities from one drawing to another"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "One simply approach to copy a layout with its entities is use “SendCommand”. Below code shows the procedure where code using command line implement..."
author: Autodesk
---
# Copy a layout with its entities from one drawing to another

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/copy-a-layout-with-its-entities-from-one-drawing-to-another.html

## 文章内容

By Virupaksha Aithal
One simply approach to copy a layout with its entities is use “SendCommand”. Below code shows the procedure where code using command line implementation of layout (layout command) coping.
        <CommandMethod("ImportLayout", CommandFlags.Session)> _
        Public Shared Sub ImportLayout()
              Dim fd As Object = _
                        Application.GetSystemVariable("FILEDIA")
            Application.SetSystemVariable("FILEDIA", 0)
              Dim acadapp As Object = Application.AcadApplication
            'start layout command
            acadapp.ActiveDocument.SendCommand("-Layout" + vbCr)
            'say wants to import from tamplate
            acadapp.ActiveDocument.SendCommand("Template" + vbCr)
            'provide the file path
            acadapp.ActiveDocument.SendCommand("c:\temp\test.dwt" _
                                                            + vbCr)
            'provide the template name
            acadapp.ActiveDocument.SendCommand("TestLayout" + vbCr)
            Application.SetSystemVariable("FILEDIA", fd)
        End Sub

## 评论

**内容**: Ronald said...
Hi Virupuksha,
not really helpfull to use VBA interop Com - Objects which are not supplied any longer by Autodesk. There is also a real .NET solution for this issue possible.
Reply
06/14/2012 at 08:52 AM

---
**内容**: Madhukar Moogala said in reply to Ronald...
Hi Ronald,
What do you mean by "not supplied any longer by Autodesk"? We still provide the COM Interop assemblies as part of the ObjectARX SDK. We just stopped installing them in the GAC as of AutoCAD 2013. You just need to reference the versions from the ObjectARX SDK and turn on type embedding for your project.
Cheers,
Stephen
Reply
06/14/2012 at 12:46 PM

---
