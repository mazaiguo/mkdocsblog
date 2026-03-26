---
title: "Audit API - New in AutoCAD 2015"
date: 2014-03-01
categories:
  - AutoCAD .NET
tags:
  - API
  - AutoCAD
description: "From AutoCAD 2015, you can programmatically audit the drawing file using the new Database API “Audit” . You can also try fixing the issues in the d..."
author: Autodesk
---
# Audit API - New in AutoCAD 2015

发布日期: 2014-03-01

原始链接: https://adndevblog.typepad.com/autocad/2014/03/audit-api-new-in-autocad-2015.html

## 文章内容

By Virupaksha Aithal
From AutoCAD 2015, you can programmatically audit the drawing file using the new Database API “Audit” . You can also try fixing the issues in the drawing file using API’s argument. This API is present in ObjectARX and .NET.
In ObjectARX – use Acad::ErrorStatus acedAudit(AcDbDatabase* , bool , bool ) API.
[CommandMethod("AuditTest")]
publicvoid AuditTest() // This method can have any name
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;

    try
    {
        //to fix the error or not
        bool bFixErrors = true;
        //to show the message in commandline or not
        bool becho = true;
               
        //call audit API
        doc.Database.Audit(bFixErrors, becho);
    }
    catch
    {
        ed.WriteMessage("Unable to audit the drawing\n");
    }

}

## 评论

**内容**: Jonathan said...
I can't seem to find the database.Audit function.
Could I be missing a dll reference, or using statement?
I have Acad 2015 + the hotfix that came out this month
Thanks
Reply
06/23/2014 at 11:00 AM

---
**内容**: Jonathan said in reply to Jonathan...
Found it. Needs a reference to:
Autodesk.AutoCAD.ApplicationServices.DatabaseExtension
Reply
06/24/2014 at 07:15 AM

---
**内容**: Curtis Linville said...
Sorry for the necropost. Is there a way to get back the number of items fixed/found? Essentially I want a way to programmatically call Audit and get all the same text as when I run Audit manually in AutoCAD for logging purposes.
Reply
01/03/2017 at 09:42 AM

---
**内容**: viru said...
Hi,
You can get the text outputted to command line using becho variable (second bool) but i do not think you can get back the number of error fixed in terms of count.
regards
Viru
Reply
01/04/2017 at 12:28 AM

---
