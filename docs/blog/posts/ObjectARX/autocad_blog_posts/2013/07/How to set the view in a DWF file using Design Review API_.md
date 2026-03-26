---
title: "How to set the view in a DWF file using Design Review API?"
date: 2013-07-01
categories:
  - AutoCAD .NET
tags:
  - API
  - C#
  - Dimension
  - Plot
description: "Setting the View using Design Review API takes two different approach based on whether you want to set View for a 2D DWF or 3D DWF."
author: Autodesk
---
# How to set the view in a DWF file using Design Review API?

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/how-to-set-the-view-in-a-dwf-file-using-design-review-api.html

## 文章内容

By Partha Sarkar
Setting the View using Design Review API takes two different approach based on whether you want to set View for a 2D DWF or 3D DWF.
Using EPlotSection.SetView() function we can set a view for the current section (page) of the DWF file based on the specified paper-based coordinates. Please note, this API is available only for 2D sections i.e. 2D DWF files.
Here is a relevant C# code snippet:
CompositeViewer = (ECompositeViewer.IAdECompositeViewer) axCExpressViewerControl1.ECompositeViewer;
SectionChk = (ECompositeViewer.IAdSection) CompositeViewer.Section;
SectionTypeChk = (ECompositeViewer.IAdSectionType) SectionChk.SectionType; 
  if (SectionTypeChk.Name == "com.autodesk.dwf.ePlot")
  {
  PlotSection = (EPlotViewer.IAdEPlotSection) CompositeViewer.Section;
  View = (AdCommon.IAdPageView)PlotSection.View; 
  //Set View - interchange Left with Bottom and Top with Right
  PlotSection.SetView (View.Bottom, View.Left, View.Top,  View.Right);
}
  In 3D, using EModelSection.Camera property, we can access the camera object of a specific 3D section in the DWF that is currently loaded in the canvas. Then it can be modified using the EModelCamera object, to access various properties of the camera.
EModelCamera.Position property -> Returns the current position of the camera. We can use [set] method of this property to set the position of the camera to a known set of coordinates (represented by IAdPoint object).

## 评论

**内容**: Stephen Grisez said...
Partha,
Is it possible to view a DWF using Auotlisp/Visual Lisp and DCL?
Reply
06/19/2015 at 09:16 AM

---
**内容**: David said...
Partha,
I can change the current view of a DWF but the changes are not saved when I call axCExpressViewerControl1.SaveAs(newDwfName);
Is there a way to set the current view, and save the file so that when the file is opened again, my new view is used?
Reply
07/21/2015 at 07:16 AM

---
