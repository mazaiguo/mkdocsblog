---
title: "Maximize document window in mdi environment"
date: 2012-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "How do I maximize an active document window in AutoCAD environment?"
author: Autodesk
---
# Maximize document window in mdi environment

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/maximize-document-window-in-mdi-environment.html

## 文章内容

By Xiaodong Liang
Issue
How do I maximize an active document window in AutoCAD environment?
Solution
The sample code that follows maximizes an active document window. Before proceeding, be sure that the project supports MFC and .DLL as file extensions.
    static void test(void)
    { 
     CMDIChildWnd   *m_pWnd;
     CMDIFrameWnd    *m_pWndFrame; 
    //   get the pointer to AutoCAD's main frame window.
    m_pWndFrame = acedGetAcadFrame();
    // get the handle of the active window
    m_pWnd         = m_pWndFrame->MDIGetActive();
    // maximize it
    m_pWnd->ShowWindow(SW_MAXIMIZE); 
    }

