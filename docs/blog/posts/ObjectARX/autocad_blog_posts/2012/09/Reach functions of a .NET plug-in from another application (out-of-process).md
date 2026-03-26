---
title: "Reach functions of a .NET plug-in from another application (out-of-process)"
date: 2012-09-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
  - Plugin
  - VBA
description: "I wrote a .NET plugin and created a COM interface for it to enable driving AutoCAD from my application. Some things seem to work, but e.g. MdiActiv..."
author: Autodesk
---
# Reach functions of a .NET plug-in from another application (out-of-process)

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/reach-functions-of-a-net-plug-in-from-another-application-out-of-process.html

## 文章内容

By Balaji Ramamoorthy
Issue
I wrote a .NET plugin and created a COM interface for it to enable driving AutoCAD from my application. Some things seem to work, but e.g. MdiActiveDocument is null and Editor.WriteMessage returns eNotApplicable inside my .NET functions when called from another application through its COM interface. However, when these functions are called from VBA (in-process), then everything is fine. What is the problem?
Solution
The problem is that your COM object is not in the STA. So you are trying to access AutoCAD from a thread other than its main thread. This won't work.
You have 2 ways to solve this problem:
1. Derive your COM object from System.EnterpriseServices.ServicedComponent
2. Or transition into the main thread "manually" in each method. Something like this:
control.Invoke(realMethod); Where control is any arbitrary window that was created on the main thread.
Here is the implementation of the 1st solution:
This is the plugin's code:
using Autodesk.AutoCAD.ApplicationServices;
  namespace AcadCOM
{
    [Guid("16FF7627-8439-4ea5-A533-04FEDBD27B95")]
    public interface iAcadInProc
    {
        [DispId(1)]
        string Test();
    }
      [Guid("ACC23279-97EE-4ea3-AB08-0491889DEF34"),
    ClassInterface(ClassInterfaceType.None)]
    public class AcadInProc : System.EnterpriseServices.ServicedComponent, iAcadInProc
    {
        public AcadInProc()
        {
            Document doc = Application.DocumentManager.MdiActiveDocument;
            doc.Editor.WriteMessage("\nHello world from out of process.");
        }
          public string Test()
        {
            DocumentCollection docs = Application.DocumentManager;
              Document doc = docs.MdiActiveDocument;
              Autodesk.AutoCAD.EditorInput.Editor ed = doc.Editor;
              ed.WriteMessage("Test1 in " + doc.Name);
              return doc.Name;
        }
    }
}
This is the testing application's code:
using Autodesk.AutoCAD.Interop;
using System.Runtime.InteropServices;
  private void button1_Click(object sender, EventArgs e)
{
    AcadApplication AcApp
        = (AcadApplication)Marshal.GetActiveObject("Autocad.Application");
    AcadCOM.iAcadInProc inProc
        = (AcadCOM.iAcadInProc)AcApp.GetInterfaceObject("AcadCOM.AcadInProc");
    string test = inProc.Test();
    MessageBox.Show(test);
}
The sample project is attached.
1. NetLoad CsMgdAcad1.dll into AutoCAD
2. Start MyExternalApp.exe
3. Click on the "Call Test" button
Download Sample
On a 64 bit system, registration of the COM wrapper needs an extra step. Please refer to this post for the details.

