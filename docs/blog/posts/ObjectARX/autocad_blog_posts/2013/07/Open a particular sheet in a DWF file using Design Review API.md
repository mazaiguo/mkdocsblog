---
title: "Open a particular sheet in a DWF file using Design Review API"
date: 2013-07-01
categories:
  - AutoCAD
tags:
  - API
description: "If you want to open a particular sheet in a DWF file which has many sheets in it (e.g. - Model, A1, A2, A3 etc) and you want to show only the A2 sh..."
author: Autodesk
---
# Open a particular sheet in a DWF file using Design Review API

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/open-a-particular-sheet-in-a-dwf-file-using-design-review-api.html

## 文章内容

By Partha Sarkar
If you want to open a particular sheet in a DWF file which has many sheets in it (e.g. - Model, A1, A2, A3 etc) and you want to show only the A2 sheet when the DWF file is loaded using the Design Review API, in that situation we can use the AdCommon.IAdCollection Sections collection to get and set the named section as demonstrated in the code snippet below :
  ECompositeViewer.IAdECompositeViewer compvwr = (ECompositeViewer.IAdECompositeViewer)axCExpressViewerControl1.ECompositeViewer;
AdCommon.IAdCollection Sections = (AdCommon.IAdCollection)compvwr.Sections;
  // Loop through the section collections and set the current
foreach (ECompositeViewer.IAdSection sec in Sections)
{
  //Set section
  if (sec.Title.ToString() == "A2") // Get the specific section of the DWF file
  {
    compvwr.Section = sec;
    //MessageBox.Show(sec.Title);
  }
  }

