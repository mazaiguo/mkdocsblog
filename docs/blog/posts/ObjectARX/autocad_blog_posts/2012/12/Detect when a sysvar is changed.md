---
title: "Detect when a sysvar is changed"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "AcEditorReactor.sysVarWillChange and AcEditorReactor.sysVarChanged  allow you to watch the events when the sysvar will change or is changed. Follow..."
author: Autodesk
---
# Detect when a sysvar is changed

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/detect-when-a-sysvar-is-changed.html

## 文章内容

By Xiaodong Liang
AcEditorReactor.sysVarWillChange and AcEditorReactor.sysVarChanged  allow you to watch the events when the sysvar will change or is changed. Following is a small demo.
class clsEditorReactor : public AcEditorReactor2
{
public:
    clsEditorReactor()
    {
        // add the reactor to editor
        acedEditor->addReactor(this);
    }
  virtual void    sysVarChanged(
    const TCHAR * varName,        
    Adesk::Boolean success)
    {
        // inform the sysvar is changed
        acutPrintf(L"[ %s ]  changed",varName);
    }
    virtual void  sysVarWillChange(
           const TCHAR * varName)
    {
        // inform the sysvar will change
        acutPrintf(L"[ %s ] will change",varName);
    }
  };
  // create a new instance of the reactor
// reactor will start
clsEditorReactor *myReactor = new  clsEditorReactor();
  In the past, there are some variables that do not generate notification if they are modified from within another command, especially transparent commands.If you meet such sysvar in the latest release, the workaround is to plant an AcEditorReactor, overriding commandWillStart() and commandEnded(). With the
Inside commandWillStart() you can cache the variables that you want to check. Inside commandEnded(), compare the cached values with the current ones. If they are different, then you can do what you want to in your sysVarChanged function.

