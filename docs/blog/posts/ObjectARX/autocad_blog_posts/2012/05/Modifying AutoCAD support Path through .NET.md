---
title: "Modifying AutoCAD support Path through .NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - COM
description: "You can use AutoCAD ActiveX API to manipulate the AutoCAD support path. Refer below code. As usual below code uses late binding technique while acc..."
author: Autodesk
---
# Modifying AutoCAD support Path through .NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/modifying-autocad-support-path-through-net.html

## 文章内容

By Virupaksha Aithal
You can use AutoCAD ActiveX API to manipulate the AutoCAD support path. Refer below code. As usual below code uses late binding technique while accessing ActiveX API.
[CommandMethod("AddSupportPath")]
static public void AddSupportPath()
{
      object acadObject = Application.AcadApplication;
      object preferences =
            acadObject.GetType().InvokeMember("Preferences",
            BindingFlags.GetProperty,
            null, acadObject, null);
      //get the files
    object files =
            preferences.GetType().InvokeMember("Files",
            BindingFlags.GetProperty,
            null, preferences, null);
      //get the support path SupportPath
    string supportPath =
            (string)files.GetType().InvokeMember("SupportPath",
            BindingFlags.GetProperty,
            null, files, null);
      Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      if (!supportPath.Contains("C:\\BatchPublish"))
    {
        supportPath = supportPath + ";" + "C:\\BatchPublish";
          object[] dataArry = new object[1];
        dataArry[0] = supportPath;
        files.GetType().InvokeMember("SupportPath",
                         BindingFlags.SetProperty,
                         null, files, dataArry);
          ed.WriteMessage(supportPath + "\n");
    }
    else
    {
        ed.WriteMessage("Support path already present\n");
    }
  }

## 评论

**内容**: Anonymoose said...
This article is either stale, or its author is not aware of the fact that as of C# 4.0, its no longer necessary to use GetType()/InvokeMember() to make late-bound calls to COM objects.
dynamic acadObject = Application.AcadApplication;
dynamic files = acadObject.Preferences.Files;
string path = files.SupportPath;
.....
Reply
05/31/2012 at 08:42 PM

---
**内容**: Virupaksha Aithal said...
Thanks for comments. But blog post code works fine on AutoCAD version which works on framework like .NET 3.5 framework. Lot of developers still uses NET 3.5 for AutoCAD 2010 & 2011.
But I should thank you for your comments.
-Viru
Reply
05/31/2012 at 09:37 PM

---
**内容**: Matus Brlit said...
this looks far more complicated than managed API
Dim pref As AcadPreferences = Autodesk.AutoCAD.ApplicationServices.Application.Preferences
Dim sp as String = pref.SupportPath
If Not sp.Contains("C:\\BatchPublish") Then pref.Files.SupportPath = sp & ";C:\\BatchPublish"
Reply
06/01/2012 at 12:26 AM

---
**内容**: Virupaksha Aithal said in reply to Matus Brlit...
Thanks for comments.
Yes you are correct; VB.net code shown by you much simpler. Blog post is in C#.

I will add the VB.net code too to blog
Thanks
Viru
Reply
06/01/2012 at 12:31 AM

---
**内容**: Anonymoose said in reply to Matus Brlit...
The Author was showing how to use AutoCAD COM apis without importing the COM type libraries, which is problematic and often undesireable, because of COM versioning issues.
In VB.NET, it is very easy to do the same (without importing the AutoCAD libraries), by simply declaring COM objects as System.Object, and using late-binding.
Reply
06/03/2012 at 01:30 AM

---
**内容**: jjj said...
object preferences = acadObject.GetType().InvokeMember("Preferences",....)
Can I use this way to create new points, like the "POINT" command.
Thanks.
Reply
12/04/2012 at 09:37 PM

---
**内容**: Viru said...
Hi,
Yes, you can use late binding to call other functions too.
regards
Viru
Reply
12/05/2012 at 02:59 AM

---
