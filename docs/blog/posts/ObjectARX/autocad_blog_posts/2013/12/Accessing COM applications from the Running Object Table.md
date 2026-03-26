---
title: "Accessing COM applications from the Running Object Table"
date: 2013-12-01
categories:
  - AutoCAD .NET
tags:
  - C#
  - COM
description: "Here is a topic that comes up every now and then: how do you access a specific instance of a COM application if several instances are running with ..."
author: Autodesk
---
# Accessing COM applications from the Running Object Table

发布日期: 2013-12-01

原始链接: https://adndevblog.typepad.com/autocad/2013/12/accessing-com-applications-from-the-running-object-table.html

## 文章内容

By Philippe Leefsma
Here is a topic that comes up every now and then: how do you access a specific instance of a COM application if several instances are running with a similar ProgId? The GetActiveObject(progId) approach can only return a single object, so there is no way to differentiate or select any specific instance.
The workaround for that goal is to use the ROT (Running Object Table), which can provide you access to every COM instance running on the machine.
Here is a C# sample that illustrates how to achieve that:
[DllImport("ole32.dll")]
static extern int CreateBindCtx(
    uint reserved,
    out IBindCtx ppbc);
  [DllImport("ole32.dll")]
public static extern void GetRunningObjectTable(
    int reserved,
    out IRunningObjectTable prot);
  // Requires Using System.Runtime.InteropServices.ComTypes
// Get all running instance by querying ROT
private List<object> GetRunningInstances(string[] progIds)
{
    List<string> clsIds = new List<string>();
      // get the app clsid
    foreach (string progId in progIds)
    {
        Type type = Type.GetTypeFromProgID(progId);
          if(type != null)
            clsIds.Add(type.GUID.ToString().ToUpper());
    }
      // get Running Object Table ...
    IRunningObjectTable Rot = null;
    GetRunningObjectTable(0, out Rot);
    if (Rot == null)
        return null;
      // get enumerator for ROT entries
    IEnumMoniker monikerEnumerator = null;
    Rot.EnumRunning(out monikerEnumerator);
      if (monikerEnumerator == null)
        return null;
      monikerEnumerator.Reset();
      List<object> instances = new List<object>();
      IntPtr pNumFetched = new IntPtr();
    IMoniker[] monikers = new IMoniker[1];
      // go through all entries and identifies app instances
    while (monikerEnumerator.Next(1, monikers, pNumFetched) == 0)
    {
        IBindCtx bindCtx;
        CreateBindCtx(0, out bindCtx);
        if (bindCtx == null)
            continue;
          string displayName;
        monikers[0].GetDisplayName(bindCtx, null, out displayName);
                        foreach (string clsId in clsIds)
        {
            if (displayName.ToUpper().IndexOf(clsId) > 0)
            {
                object ComObject;
                Rot.GetObject(monikers[0], out ComObject);
                  if (ComObject == null)
                    continue;
                  instances.Add(ComObject);
                break;
            }
        }
    }
      return instances;
}
  void TestROT()
{
    // Look for acad 2009 & 2010 & 2014
    string[] progIds =
    {
        "AutoCAD.Application.17.2",
        "AutoCAD.Application.18",
        "AutoCAD.Application.19.1"
    };
      List<object> instances = GetRunningInstances(progIds);
      foreach (object acadObj in instances)
    {
        try
        {
            // do some stuff ...  
        }
        catch
        {
                    }
    }
}

## 评论

**内容**: Peter Ferber said...
I've been trying in vain to return a list of running Access application objects; and I had a hunch that this code might help me do that, with the changed parameter 'string[] progIds = {"Access.Application"}'. The code, as written, gets as far as "if (displayName.ToUpper().IndexOf(clsId) > 0)", but it does not return Access objects. Any notion of how might be changed to achieve that objective?
Reply
05/01/2014 at 02:40 PM

---
**内容**: Philippe Leefsma said...
Hi Peter, I don't have Access installed, so I cannot test it directly. Did you try specifying the version, eg. Access.Application.11?
Does the Type.GetTypeFromProgId return a valid type?
Reply
05/01/2014 at 07:53 PM

---
**内容**: Peter Ferber said...
Hi, Philippe, and thanks very much for your response.
I tried what you suggested, with the following command:
Dim myType As Type = Type.GetTypeFromProgID("Access.Application")
The procedure does yield a valid type.
Type.FullName = "Microsoft.Office.Interop.Access.ApplicationClass"
Type.Asssembly.FullName = "Microsoft.Office.Interop.Access, Version=14.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c"
I open 3 copies of Access; and using "Access.Application.14" as a parameter, I got an Instances count of 1. When going through the foreach process, acadObj does return a valid Access object! That is just excellent. My concern, now, is why it is returning only one object when two or more instances are open. If you can help me solve that riddle, you will have solved a problem that's been plaguing me for nearly a week.
Superb work on this, by the way. I'm very grateful to have you as a resource. ~Peter Ferber
Reply
05/02/2014 at 09:28 AM

---
**内容**: rvcristiand said in reply to Peter Ferber...
Hi Peter !
At this moment I'm trying do an Application like you, but I can't use the Type Class. What did you do for VBA recognize this Class.
Thank you so much for you advice !
Reply
06/25/2018 at 08:56 AM

---
**内容**: Philippe Leefsma said...
Hi Peter, I'm afraid I don't have a suggestion for the multiple instances running question... the issue was raised in the past and we couldn't find a solution for that behavior. It seems the ROT only returns the same instance if they are similar.
You may want to approach Microsoft support or some Windows API dedicated forums where more expert people on those APIs may be able to help you.
Sorry for the bad news...
Reply
05/04/2014 at 08:58 PM

---
**内容**: Peter Ferber said...
Fair enough. Thanks for taking the time to respond to my inquiry. I will pursue with Tech support.
Reply
05/05/2014 at 02:14 PM

---
**内容**: Philippe Leefsma said...
You're welcome. Feel free to let us know if you can sort this out.
Thanks,
Philippe.
Reply
05/05/2014 at 06:06 PM

---
**内容**: cestleswampthing@gmail.com said...
is it posible to post the code in VB.net format?
i'm having the same problem with inventor
Reply
06/13/2014 at 12:00 AM

---
**内容**: Limin Ma said...
I want to have a VB.NET version of this code too, for Inventor.
Reply
06/24/2014 at 05:11 AM

---
**内容**: Philippe said in reply to Limin Ma...
Sorry, we don't write code 'on-demand'. If you cannot convert that sample by yourself, either hire a programmer or find somebody who is willing to do that for fun. I'm happy to help if you have a precise question on how to convert a specific line into Vb.Net.
Reply
06/24/2014 at 05:17 AM

---
**内容**: Philippe said in reply to Philippe...
By the way, that approach doesn't apply to Inventor as-is. I wrote the following post on Inventor, and you will be happy to notice it's in Vb.Net:
http://adndevblog.typepad.com/manufacturing/2013/05/running-programmatically-a-specific-version-of-inventor.html
Reply
06/24/2014 at 05:20 AM

---
**内容**: Shamil said...
@Peter Ferber:
Try the following code:
using System;
using System.Runtime.InteropServices;
using System.Runtime.InteropServices.ComTypes;
namespace ROT.TestConsole
{
///
/// Enumerate opened MS Access projects via ROT
///
public class OpenedAccessProjects2
{
[DllImport("ole32.dll")]
static extern int CreateBindCtx(uint reserved, out IBindCtx ppbc);
[DllImport("ole32.dll")]
public static extern void GetRunningObjectTable(int reserved, out IRunningObjectTable prot);
public static void Enum()
{
string progId = "Access.Application";
Type type = Type.GetTypeFromProgID(progId);
var clsId = type.GUID.ToString().ToUpper();
// get Running Object Table ...
IRunningObjectTable Rot;
GetRunningObjectTable(0, out Rot);
// get enumerator for ROT entries
IEnumMoniker monikerEnumerator = null;
Rot.EnumRunning(out monikerEnumerator);
IntPtr pNumFetched = new IntPtr();
IMoniker[] monikers = new IMoniker[1];
IBindCtx bindCtx;
CreateBindCtx(0, out bindCtx);
int index = 1;
while (monikerEnumerator.Next(1, monikers, pNumFetched) == 0)
{
string applicationName = "";
dynamic application = null;
try
{
Guid IUnknown = new Guid("{00000000-0000-0000-C000-000000000046}");
object ppvResult;
monikers[0].BindToObject(bindCtx, null, ref IUnknown, out ppvResult);
application = ppvResult;
applicationName = application.Name;
}
catch { }
if (applicationName == "Microsoft Access")
System.Console.WriteLine("{0}. '{1}' '{2}'", index, application.Name, application.CurrentDB.Name);
index++;
}
}
}
}

P.S. Code lines indenting is removed to avoid code lines wrapping AMAP...
Reply
11/01/2014 at 02:08 PM

---
**内容**: Shamil said...
Here is a refactored streamlined code snippet:
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Runtime.InteropServices.ComTypes;
namespace ROT.TestConsole
{
///
/// Use Running Object Table (ROT) to get
/// MS Access application instances
/// with opened databases/projects
///
public class MSAccessRunningInstances
{
[DllImport("ole32.dll")]
static extern int CreateBindCtx(uint reserved, out IBindCtx ppbc);
[DllImport("ole32.dll")]
public static extern void GetRunningObjectTable(int reserved, out IRunningObjectTable prot);
public static IEnumerable Enum()
{
// get Running Object Table ...
IRunningObjectTable Rot;
GetRunningObjectTable(0, out Rot);
// get enumerator for ROT entries
IEnumMoniker monikerEnumerator = null;
Rot.EnumRunning(out monikerEnumerator);
IntPtr pNumFetched = new IntPtr();
IMoniker[] monikers = new IMoniker[1];
IBindCtx bindCtx;
CreateBindCtx(0, out bindCtx);
while (monikerEnumerator.Next(1, monikers, pNumFetched) == 0)
{
string applicationName = "";
dynamic application = null;
try
{
Guid IUnknown = new Guid("{00000000-0000-0000-C000-000000000046}");
monikers[0].BindToObject(bindCtx, null, ref IUnknown, out application);
applicationName = application.Name;
}
catch { }
if (applicationName == "Microsoft Access") yield return application;
}
}
}
}
Reply
11/01/2014 at 03:02 PM

---
**内容**: Matt Garrett said...
Hi Philippe,
Thank you for posting this. It really helps to have an example when learning to use the ROT! Unfortunately, it doesn't seem to work for me, with the following actions:
1. I started two instances of AutoCAD, opening a different dwg in each: A.dwg and B.dwg. Both are in SDI mode.
2. I added debug code to the monikerEnumerator.Next loop to print the moniker displayname for each moniker.
3. I added debug code to the foreach clsId loop to cast ComObject as AcadApplication acApp, then print acApp.ActiveDocument.Name.
4. When I run the example, it prints "A.dwg" (the dwg opened in the first instance) 4 times, for 2 unique displaynames. (I'm assuming these correspond to acad.exe and AcBrowserHost.exe.)
The problem, of course, is that all four ComObjects appear to point to the AutoCAD instance that opened A.dwg. I can't seem to connect to the instance that opened B.dwg.
I note in Process Explorer that the B.dwg instance is a child process of the A.dwg instance, which I started first.
Any idea why this isn't working?
Thank you,
Matt Garrett
Reply
01/29/2015 at 09:54 AM

---
**内容**: Harold Reuvers said...
Somebody any idea why my .NET program is getting an error when trying to open a DWG in an active AutoCAD 2013 application? (works fine an active AutoCAD 2015)
Problem remains also with the COM Marshal method...
//ObjectARX_2015:
//Autodesk.AutoCAD.Interop.dll
//Autodesk.AutoCAD.Interop.Common.dll
using Autodesk.AutoCAD.Interop;
...
// Look for acad 2013 & 2015
string[] progIds = {
"AutoCAD.Application.19",
"AutoCAD.Application.20"
};
List instances = GetRunningInstances(progIds);
foreach (object acadObj in instances)
{
try
{
AcadApplication acApp = (AcadApplication) acadObj;
acApp.Documents.Open(FullPathOpenDWG, false);
}
catch
{
MessageBox.Show("error");
}
}
Reply
05/26/2015 at 12:24 PM

---
**内容**: Vladimir Kozlov (aienabled) said...
Hello!
Unfortunately this code returns for me the same instance of Visual Studio instead of all running instances. I mean if I had X running instances, it X times return only the first instance.
The code from there http://www.codeproject.com/Articles/7984/Automating-a-specific-instance-of-Visual-Studio-NE works flawless for me (and it could be adapted for not only Visual Studio processes).
Regards!
Reply
01/30/2016 at 06:05 AM

---
**内容**: Gary Puerini said in reply to Vladimir Kozlov (aienabled)...
i'm running into the same problem. Were you able to convert the Visual Studio to use with autoCAD ? It looks like it uses basically the same approach?
thanks
Reply
01/06/2017 at 02:02 PM

---
**内容**: NDOH said...
Hi,
This was useful. I am not utilizing COM access to manipulate AutoCAD, instead of using Lisp. Now, can you create COM object with Revit?
Thanks,
Andy
Reply
02/17/2016 at 12:19 PM

---
**内容**: Philippe Leefsma said...
I don't think Revit has a COM API, but I'm not a Revit expert so you may want to ask this kind of questions on... a Revit forum:
http://forums.autodesk.com/t5/revit-api/bd-p/160
Regards,
Philippe.
Reply
02/17/2016 at 01:48 PM

---
**内容**: Naren said...
using the above could i able to get the running instance of Internet Explorer object.
Reply
09/17/2017 at 06:03 AM

---
**内容**: rvcristiand said...
Hi !
At this moment I'm doing an VBA Excel application and I want manage many AutoCAD Applications Instances. I'm searching in the web and I don't find any way to get the ROT (Running Object Table) with VBA. Do you any suggestion ?
Thank you so much for the help !
Reply
06/23/2018 at 03:47 PM

---
**内容**: Swetha said...
Hello Philippe!!
I noticed that calling a specific CATIA Application this way throws an error.I tried calling a catia interface library as reference and it still does not work. Is there any specific dll that i need to use inorder to create an ROT for the CATIA application in a similar way. Your reply will be really helpful as I have been trying to create a running object table for CATIA instances. Thank you very much in advance!
Regards,
Swetha
Reply
09/03/2020 at 06:14 AM

---
