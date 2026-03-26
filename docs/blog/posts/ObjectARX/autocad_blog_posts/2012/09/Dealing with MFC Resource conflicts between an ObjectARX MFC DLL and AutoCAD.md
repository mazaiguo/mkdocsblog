---
title: "Dealing with MFC Resource conflicts between an ObjectARX MFC DLL and AutoCAD"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "The CAcModuleResourceOverride class provides a nice way to switch the MFC resource pointer from AutoCAD’s resources to your own ARX DLL resources."
author: Autodesk
---
# Dealing with MFC Resource conflicts between an ObjectARX MFC DLL and AutoCAD

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/dealing-with-mfc-resource-conflicts-between-an-objectarx-mfc-dll-and-autocad.html

## 文章内容

by Fenton Webb
The CAcModuleResourceOverride class provides a nice way to switch the MFC resource pointer from AutoCAD’s resources to your own ARX DLL resources.
If you have to use AutoCAD User Interface functions in between your own resources, then you can still utilize the CAcModuleResourceOverride() class by relying on its destructor (which restores the MFC resource pointer back to AutoCAD)
Here’s what I mean…

class CMyDialog : public CDialog
{
…
};

void ftn()
{
  {
    // here we need to make sure we are using the dll’s resources
    CAcModuleResourceOverride resourceOverride;
    CMyDialog dlg;
    dlg.DoModal();
  } // switch back to AutoCAD’s resources
  // now safe to use this function
  acedGetFileD(...);
  // now back to our dialog
  {
    // here we need to make sure we are using the dll’s resources, so use:
    CAcModuleResourceOverride resourceOverride;
    CMyDialog dlg;
    dlg.DoModal();
  }
}

