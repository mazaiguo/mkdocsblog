---
title: "Access Object Properties and control visibility using Design Review API"
date: 2013-06-01
categories:
  - AutoCAD .NET
tags:
  - API
  - C#
  - Plot
description: "Autodesk Design Review is a viewer application which allows us to view, print, annotate, and compare 2D and 3D DWF files. It has a set of public AP..."
author: Autodesk
---
# Access Object Properties and control visibility using Design Review API

发布日期: 2013-06-01

原始链接: https://adndevblog.typepad.com/autocad/2013/06/access-object-properties-and-control-visibility-using-design-review-api.html

## 文章内容

By Partha Sarkar
Autodesk Design Review is a viewer application which allows us to view, print, annotate, and compare 2D and 3D DWF files. It has a set of public API which allows us to create custom application focused on viewing DWF files, Object properties, Printing etc. You can get more details on Autodesk Design Review API from the Developer Center Page. 
In this blog post, I am sharing some code snippet using Design Review / DWF Viewer API which shows how to load a DWF file, how to get the object properties of the components of DWF object model, how to control visibility of a component in the DWF file and access the DWF file properties. Here is the screenshot of the sample Windows Forms application which embedding Design Review / DWF Viewer control and few buttons for specific task -
    And here is the relevant C# code snippet for each task -
privatevoid button1_Click(object sender, EventArgs e)
{
    // Option 2 - Using OpenFileDialog
    OpenFileDialog oFileDialog = newOpenFileDialog();
  oFileDialog.ShowDialog();
  axCExpressViewerControl1.SourcePath = oFileDialog.FileName;      
  }
    privatevoid DWF_Property_Click(object sender, EventArgs e)
{
    ECompositeViewer.IAdECompositeViewer CompositeViewer;
  AdCommon.IAdCollection Sections;
    CompositeViewer = (ECompositeViewer.IAdECompositeViewer)axCExpressViewerControl1.ECompositeViewer;
  Sections = (AdCommon.IAdCollection)CompositeViewer.Sections;
  MessageBox.Show("Pages Count : " + Sections.Count);
      //Loop through Sections Collection using foreach
  foreach (ECompositeViewer.IAdSection Section in Sections)
  {       
    MessageBox.Show(Section.Title);
    MessageBox.Show("Order of the section \"" + Section.Title + "\" is " + Section.Order);
  }
}
    privatevoid button_ObjProp_Click(object sender, EventArgs e)
{
  try
  {
    ECompositeViewer.IAdECompositeViewer compvwr =
(ECompositeViewer.IAdECompositeViewer)axCExpressViewerControl1.ECompositeViewer;
      ECompositeViewer.IAdSection sec = (ECompositeViewer.IAdSection)compvwr.Section;
    ECompositeViewer.IAdContent con = (ECompositeViewer.IAdContent)sec.Content;
      AdCommon.IAdCollection adobj = (AdCommon.IAdCollection)con.get_Objects(1); //for selected object
    AdCommon.IAdObject obj = (AdCommon.IAdObject)adobj[1];
      string str = "";
    foreach (AdCommon.IAdProperty prop in (AdCommon.IAdCollection)obj.Properties)
    {
      str = str + "Name: " + prop.Name + " Value: " + prop.Value + Environment.NewLine;
    }
    // Properties of the selected object will be displayed in a Text Box 
    textBox1.Text = str;
    }
  catch
  {
    // TODO: Add your error handling here.
  }
  } //
  privatevoid button_hideObj_Click(object sender, EventArgs e)
{
  try
  {
    ECompositeViewer.IAdECompositeViewer compvwr =
(ECompositeViewer.IAdECompositeViewer)axCExpressViewerControl1.ECompositeViewer;
      ECompositeViewer.IAdSection sec = (ECompositeViewer.IAdSection)compvwr.Section;
    ECompositeViewer.IAdContent con = (ECompositeViewer.IAdContent)sec.Content;
      AdCommon.IAdCollection adobj = (AdCommon.IAdCollection)con.get_Objects(1); //for selected object
    AdCommon.IAdObject obj = (AdCommon.IAdObject)adobj[1];
      compvwr.ExecuteCommand("HIDE");       
    }
  catch
  {
    // TODO: Add your error handling here.
  }
}
  Hope this is useful to you!
  [ Updated on 20/Nov/2013 ]
I am updating this blog post with the following notes and screenshot to show what all components you need to reference from Autodesk Design Review to build this C# .NET code sample.
Autodesk Design Review 2013 API Reference document has a topic - "Setting References in C# .NET" which lists the Autodesk Design Review components you need to reference in your project to build this sample.
  Here is the screenshot of the Design Review components I have used in my project -
You can also download this C# .NET sample application from here ADR2013WinFormAppCS.

## 评论

**内容**: Jeremy Tammik said...
Dear Partha,
Where can I find the full source code for this sample, please?
Are all the required components and all referenced .NET assembly DLLs provided by the DWF developer centre that you point to?
http://www.autodesk.com/developdwf
If so, can you please tell us which components are required, since it includes a quite substantial list to explore.
Thank you!
Cheers, Jeremy.
Reply
11/19/2013 at 09:24 AM

---
**内容**: Partha Sarkar said...
Dear Jeremy,
This code snippet is not part of the Sample codes posted in DWF developer centre http://www.autodesk.com/developdwf
However, I have now updated the blog post with details of all components you need to reference from Autodesk Design Review to build this C# .NET project.
Hope this helps.
Cheers,
Partha
Reply
11/19/2013 at 09:12 PM

---
**内容**: Matthew Johnson said...
Hi Partha,
Is there any chance you can upload a buildable version as i cant get this to work. Based on your sample and references i can try and open a dwf but i get an error as below. The code sample doesn't seem to include how the CExpressViewerControl is added to the form?
Retrieving the COM class factory for component with CLSID {A662DA7E-CCB7-4743-B71A-D817F6D575DF} failed due to the following error: 80040154 Class not registered (Exception from HRESULT: 0x80040154 (REGDB_E_CLASSNOTREG)).
Reply
11/20/2013 at 08:16 AM

---
**内容**: Partha Sarkar said...
Hi Matthew,
I have attached the project here. See the link in the last line of this post.
Hope this helps to you !
Thanks,
Partha
Reply
11/20/2013 at 08:49 PM

---
**内容**: Matthew Johnson said in reply to Partha Sarkar...
Great thanks!
Reply
11/21/2013 at 02:00 AM

---
**内容**: Matthew Johnson said...
Unfortunately this wont build as the files AxExpressViewerDll and ExpressViewerDll are missing from the references. Do you know where i can get get hold of these files please?
Thanks
Matt
Reply
11/21/2013 at 06:22 AM

---
**内容**: lee said...
I have question about the code 'compvwr.ExecuteCommand("HIDE");'
the ExecuteCommand has one string type parameter bstrCommand.
what is bstrCommand? what kind of command? do you have any document about this?
Reply
10/29/2014 at 10:15 PM

---
**内容**: edu pastor said...
Partha,
I used the code and it has worked perfect. But it can be done in reverse. That is locate an object in the DWF PnPID
Thank you
Reply
11/11/2014 at 05:57 AM

---
**内容**: Po said in reply to edu pastor...
You mentionned that it is possible to locate (=select) a 3d-object in the dwf by using the PnpID . Can you tell me how
Thanks in advance
Reply
07/04/2017 at 09:16 AM

---
**内容**: shiba said...
Thanks a ton..very useful post..Its Perfect
Reply
10/25/2015 at 01:13 AM

---
