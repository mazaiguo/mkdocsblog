---
title: "A simple alternative to accessing the COM Preferences object in AutoCAD"
date: 2012-06-01
categories:
  - AutoLISP
tags:
  - AutoCAD
  - AutoLISP
  - COM
  - Plot
description: "Recently, a developer ran into an issue with some LISP code where he was trying to add multiple paths to the PrinterStyleSheetPath property… The co..."
author: Autodesk
---
# A simple alternative to accessing the COM Preferences object in AutoCAD

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/a-simple-alternative-to-accessing-the-com-preferences-object-in-autocad.html

## 文章内容

by Fenton Webb
Recently, a developer ran into an issue with some LISP code where he was trying to add multiple paths to the PrinterStyleSheetPath property… The code looked something like this:
(defun c:xx()
  (vl-load-com)
  (setq
    acad (vlax-get-acad-object)
    prefs (vla-get-preferences *acad)
    files (vla-get-files prefs)
  )
  (vla-put-PrinterStyleSheetPath files "c:\\fenny;c:\\temp")
)
The problem is that behind the scenes, as with other Preference variables, the put-PrinterStyleSheetPath does not handle the semi colon’s and just fails because the path is invalid.
The solution is simply to use getenv and/or setenv.
If you are not familiar with these functions, basically they have a two stage process… First, check the FixedProfile in the registry for the required system setting, and second, if an entry is not found then the Windows System environment is searched.
Here’s the code to set the PrinterStyleSheetPath to multiple paths in LISP…
(setenv "PrinterStyleSheetDir" "c:\\fenton;c:\\temp")
Here’s the code to set the PrinterStyleSheetPath to multiple paths in ARX…
acedSetEnv(_T("PrinterStyleSheetDir"), _T("c:\\fenton;c:\\temp"));
  Now for .NET, it seems there is no native way to call acedSetEnv()… I can see why that is actually (it’s because the ObjectARX API’s, which .NET is built around, AcDbHostApplicationServices class only exposes a GetEnvironmentVariable(), not a Set) so you will have to PInvoke acedSetEnv… Not difficult, here’s how…
  [DllImport("acad.exe", CallingConvention = CallingConvention.Cdecl,
      CharSet = CharSet.Auto, EntryPoint = "acedGetEnv")]
extern static private Int32 acedGetEnv(string var,
        [Out] System.Text.StringBuilder val);
[DllImport("acad.exe", CallingConvention = CallingConvention.Cdecl,
      CharSet = CharSet.Auto, EntryPoint = "acedSetEnv")]
extern static private Int32 acedSetEnv(string var, string val);
  // test acedGet and acedSetEnv by Fenton Webb, DevTech, 05/06/2012
[CommandMethod("testenv")]
static public void testenv()
{
  System.Text.StringBuilder buf = new System.Text.StringBuilder("", 1024);
  acedGetEnv("PATH", buf);
  buf.Append(";"); buf.Append(@"c:\temp");
  acedSetEnv("PATH", buf.ToString());
}
To finish off, I personally think that one other great advantage of using getenv/acedGetEnv() and setenv/acedSetEnv() instead of the COM Preferences in .NET is that you reduce the need to bring in the COM Interop reference DLLs into your project references – namely Autodesk.AutoCAD.Interop.dll and/or Autodesk.AutoCAD.Interop.Common.dll. To explain why I’m bringing this up; so when you bring in these DLL’s as references you can no longer rely on the “Any CPU” setting in your project build settings working universally across 32bit and 64bit AutoCAD, thus possibly making you have to consider creating separate 32bit and 64bit versions of your application. Don’t worry too much though, it really all depends on which parts of the COM Interop libraries you are using; my advise is, if you are using these COM Interop libs, and you are compiling as “Any CPU” make sure you test your application on both 32bit and 64bit… If it fails, you know you have to create separate 32bit and 64bit versions. If it works, then great!! Actually, a good first test is to simply set your CPU build type to Win32 and recompile, do the same for x64 – if you get any compiler errors, you know you definitely have a problem…

## 评论

**内容**: Kerry Brown said...

>>> Testing for DevTech 2012 <<
You obviously weren't using ACAD2013
Regards
Reply
06/05/2012 at 02:42 PM

---
**内容**: Fenton Webb said...
Yes, I was using 2013 - what is obvious exactly? Sorry... :-)
Reply
06/05/2012 at 03:04 PM

---
**内容**: Kerry Brown said in reply to Fenton Webb...

Hi Fenton,
I thoght that the acedGetEnv and acedSetEnv
were declared in the acCore.dll not in the acad.exe for 2013.
Regards
kdub
Reply
06/05/2012 at 05:20 PM

---
**内容**: Fenton Webb said...
ah you are right :-) I just double checked my debugger, and it did startup 2012, not 2013 - been a long day. Thanks for pointing that out.
Anyway, I hope you like my work other than that?
Reply
06/05/2012 at 05:24 PM

---
**内容**: Kerry Brown said in reply to Fenton Webb...

>>Anyway, I hope you like my work other than that?<<
Yes, thanks :-D
The blog will be a goldmine for anyone starting out.
I still think that it would be a good idea adding the builds that the code/posts are relevant for (similar to the knowledgebase at ADN)
kdub
Reply
06/05/2012 at 06:32 PM

---
**内容**: Account Deleted said...
Hi, Fenton!
Very similar and adopted with AutoCAD 2007...2013: http://goo.gl/xMAjn
Reply
06/06/2012 at 01:19 PM

---
**内容**: Fenton Webb said...
That's really nice work, Alexander.
Reply
06/07/2012 at 09:45 AM

---
**内容**: Андрей Бушман said...
For this .NET code working there is no need to connect the libraries Autodesk.AutoCAD.Interop.dll and Autodesk.AutoCAD.Interop.Common.dll.
Reply
12/11/2013 at 11:27 PM

---
**内容**: R.K. McSwain said...
Strange, I've been using (vla-put-ToolPalettePath.....) with a semicolon delimited list of multiple paths for a while. I wonder why (vla-put-PrinterStyleSheetPath...) can't handle it.
Thanks.
Reply
12/15/2015 at 06:57 AM

---
**内容**: rajesh said...
ActCAD https://actcad.com/download-actcad-intellicad-software.php” target="_blank" rel=”nofollow”>intellicad Software.One of the best AutoCAD alternative cad software at affordable price.
Reply
03/03/2021 at 03:04 AM

---
**内容**: Mia said...
CADHOBBY IntelliCAD has revolutionized the way I approach my hobby. Its user-friendly interface and advanced features have made 3D printing and design much more accessible to me.
https://www.cadhobby.com/
Reply
07/09/2023 at 03:12 AM

---
