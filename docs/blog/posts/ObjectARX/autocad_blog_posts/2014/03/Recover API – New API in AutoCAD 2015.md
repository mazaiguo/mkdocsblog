---
title: "Recover API – New API in AutoCAD 2015"
date: 2014-03-01
categories:
  - AutoCAD .NET
tags:
  - API
  - AutoCAD
description: "A long time request by developer community is to recover the drawing files through API. That request has been addressed in AutoCAD 2015. Now, docum..."
author: Autodesk
---
# Recover API – New API in AutoCAD 2015

发布日期: 2014-03-01

原始链接: https://adndevblog.typepad.com/autocad/2014/03/recover-api-new-api-in-autocad-2015-1.html

## 文章内容

By Virupaksha Aithal
A long time request by developer community is to recover the drawing files through API. That request has been addressed in AutoCAD 2015. Now, document collection class has a new API “AppContextRecoverDocument” which takes the name of the drawing file to recover. This API is present in ObjectARX and in .NET. In ObjectARX use AcApDocManager::appContextRecoverDocument() API.
[CommandMethod("RecoverTest", CommandFlags.Session)]
publicvoid RecoverTest() // This method can have any name
{
    Document doc =
        Application.DocumentManager.MdiActiveDocument;
    DocumentCollection docs = Application.DocumentManager;
    Editor ed = doc.Editor;

    OpenFileDialog file =
        newOpenFileDialog("Select file to recover", null,
                            "dwg;dxf", "Recover",
          OpenFileDialog.OpenFileDialogFlags.DoNotTransferRemoteFiles);
             
    //show the dialog and take the dwg input
    System.Windows.Forms.DialogResult dr =  file.ShowDialog();
    if (dr != System.Windows.Forms.DialogResult.OK)
           return;
    try
    {
        //call  AppContextRecoverDocument to revover the selected DWG.
        docs.AppContextRecoverDocument(file.Filename);
    }
    catch
    {
        ed.WriteMessage("Unable to recover the drawing\n");
    }
}

## 评论

**内容**: Z Graff said...
This is a nice addition, however it doesn't appear to work! AppContextRecoverDocument wont seem to take any of the paths I can come up with. A path that will work with docs.Open wont work with docs.AppContextRecoverDocument
Any ideas?
Reply
08/04/2015 at 03:00 PM

---
**内容**: Z Graff said in reply to Z Graff...
In fact I omitted the CommandFlags.Session, which appears to be a necessary component.
Problem solved.
Reply
08/06/2015 at 11:01 AM

---
**内容**: CAD bloke said...
but this doesn't exist in RealDwg because there is no implementation of ApplicationServices but the docs don't mention that (they do mention this functionality, just as a tease) so if you paid for RealDwg just forget you ever saw this ok?
Reply
06/12/2016 at 04:58 PM

---
**内容**: Alok said...
I am using your above code as it is, to recover a corrupt file, but it giving 'eNotApplicable' error. Could you please help me.
Reply
11/05/2016 at 05:46 AM

---
**内容**: James Cameron said...
The command only works in SDI 1
Reply
12/07/2016 at 07:54 AM

---
**内容**: Mike Hutchinson said...
Well... interesting, having just moved to AutoCAD 2017, this explains why 'our' third party's objects get reduced to Proxy objects when RECOVER is used. Although, we were previously on 2016... I think RECOVER worked then. Why does it not work now?
Reply
01/12/2017 at 09:31 AM

---
**内容**: Hassan said...
Hi
Could this APIruns on CAD2014?
Reply
08/22/2017 at 06:42 AM

---
**内容**: Hassan said...
Hi
I have no idea about this language I am coding using lisp, So
Could this API runs on CAD2014? and How?
Reply
08/22/2017 at 06:44 AM

---
