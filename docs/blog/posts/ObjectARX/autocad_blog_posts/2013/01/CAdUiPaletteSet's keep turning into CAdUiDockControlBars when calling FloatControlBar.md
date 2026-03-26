---
title: "CAdUiPaletteSet's keep turning into CAdUiDockControlBars when calling FloatControlBar"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - Palette
description: "You might find that instances of CAdUiPaletteSet's keep turning into CAdUiDockControlBars when called with FloatControlBar method."
author: Autodesk
---
# CAdUiPaletteSet's keep turning into CAdUiDockControlBars when calling FloatControlBar

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/caduipalettesets-keep-turning-into-caduidockcontrolbars-when-calling-floatcontrolbar.html

## 文章内容

By Gopinath Taget
You might find that instances of CAdUiPaletteSet's keep turning into CAdUiDockControlBars when called with FloatControlBar method.
Applications normally manage the state of docking windows (CControlBars) using the standard MFC methods CFrameWnd::DockControlBar(), CFrameWnd::FloatControlBar() and CFrameWnd::ShowControlBar() (Docking windows should not be shown/hidden using calls to CWnd::ShowWindow()). 
Applications can continue to call CFrameWnd::DockControlBar() and CFrameWnd::ShowControlBar() normally. However, when calling CFrameWnd::FloatControlBar(), applications will need to "swap" the floating frame class if the control bar passed to FloatControlBar() is a kind of CAdUiPaletteSet. Applications can perform this "swap" by calling the new method AdUiSetFloatingFrameClass() before and after the call to FloatControlBar():
CRect mRect(100,100, 300, 600);
GetPaletteSet()->InitFloatingPosition(&mRect);
CMDIFrameWnd* pAcadFrame = acedGetAcadFrame();
CRuntimeClass* pCurrentFloatingFrameClass = AdUiSetFloatingFrameClass(RUNTIME_CLASS(CAdUiPaletteSetDockFrame));
acedGetAcadFrame()->FloatControlBar(GetPaletteSet(),CPoint(mRect.left, mRect.top),CBRS_ALIGN_TOP );
AdUiSetFloatingFrameClass(pCurrentFloatingFrameClass);
Why is all of this necessary? MFC's CFrameWnd class caches a pointer to the floating frame class used as a private member of the class. This class pointer is used to instantiate a floating frame for dock control bars when they are floating by CFrameWnd::FloatControlBar(). AdUi needs to continue to support for custom dialogs derived directly from CAdUiControlBar. So AdUi host applications need to use two different floating frame classes, one for those derived from CAdUiControlBar and another for those derived from CAdUiPaletteSet. 
Unfortunately FloatControlBar() is not a virtual method so it is not possible to override it in the application frame class to automatically detect the control bar class and use the correct floating frame. Instead applications must detect the control bar class themselves and manually swap the floating frame class before calling CFrameWnd::FloatControlBar().

## 评论

**内容**: Nick Gorlov said...
CRuntimeClass* pCurrentFloatingFrameClass = AdUiSetFloatingFrameClass(RUNTIME_CLASS(CAdUiPaletteSetDockFrame));
This code won't work fine within my AutoCAD2013, but it works fine within previous versions :-)
So it's better to use
CRuntimeClass* pCurrentFloatingFrameClass = AdUiSetFloatingFrameClass(AdUiGetRegisteredPaletteSetFloatingFrameClass());
For more info, arx online help with mistakes in code :-) :
http://docs.autodesk.com/ACDMAC/2011/ENU/ObjectARX%20Reference/index.html?frmname=topic&frmfile=AdUiSetFloatingFrameClass@CRuntimeClass_.html
RUNTIME_CLASS( - useless code there
Reply
01/23/2013 at 12:36 AM

---
