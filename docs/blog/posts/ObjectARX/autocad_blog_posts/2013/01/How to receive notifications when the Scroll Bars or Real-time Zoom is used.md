---
title: "How to receive notifications when the Scroll Bars or Real-time Zoom is used"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
description: "There are a few ways you can make sure you are notified when the screen is updated with the mouse-wheel, or when the scroll bars are adjusted."
author: Autodesk
---
# How to receive notifications when the Scroll Bars or Real-time Zoom is used

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-receive-notifications-when-the-scroll-bars-or-real-time-zoom-is-used.html

## 文章内容

By Gopinath Taget
There are a few ways you can make sure you are notified when the screen is updated with the mouse-wheel, or when the scroll bars are adjusted.
The most straightforward way may be to subclass the AutoCAD drawing window, and catch any WM_VSCROLL, WM_HSCROLL or WM_MOUSEWHEEL messages. You know that the screen will be updated when AutoCAD receives these, and you can monitor or filter AutoCAD messages by implementing an AutoCAD message monitor or filter. But there is a catch. Your custom message monitor “monitors” AutoCAD messages *before* they are handled by AutoCAD. And there is really no clean way to monitor AutoCAD messages immediately after they have been handled by AutoCAD. So the simplest solution would be for you to set a timer for some arbitrarily small value to be used as a notification (this assumes that the AutoCAD screen will update within this time, so you may need to adjust this value).
Within the WindowProc, you can kill the timer, and reset it for every subsequent message that is received so that you only get one timer update. Here is the relevant code:
WNDPROC dwgWndProc = NULL;
virtual AcRx::AppRetCode On_kInitAppMsg (void *pkt) {
 // TODO: Load dependencies here
   // You *must* call On_kInitAppMsg here
AcRx::AppRetCode retCode =AcRxArxApp::On_kInitAppMsg (pkt) ;
   // TODO: Add your initialization code here
pReactor = new asdkEditorReactor(true);
dwgWndProc = (WNDPROC)::SetWindowLong(acedGetAcadDwgView()->m_hWnd,
  GWL_WNDPROC, // Use GWLP_WNDPROC for x64 platforms
  (long)myWndProc);
   return (retCode) ;
}
LRESULT CALLBACK myWndProc(HWND hwnd, UINT uMsg,
WPARAM wParam,LPARAM lParam)
{
 if(uMsg==WM_VSCROLL || uMsg==WM_HSCROLL ||
  uMsg==WM_MOUSEWHEEL)
{
  acedGetAcadFrame()->KillTimer(10);
  acedGetAcadFrame()->SetTimer(10,100,TimerProc);
}
   return ::CallWindowProc(dwgWndProc,hwnd,uMsg,wParam,lParam);
}
void CALLBACK TimerProc(HWND hWnd,UINT nMsg,
UINT_PTR nIDEvent,DWORD dwTime)
{
screenUpdated();
acedGetAcadFrame()->KillTimer(10);
}
  void screenUpdated()
{
acutPrintf(L"Display Updated\n");
}
You can also use an editor reactor to handle the regular zoom commands, as well as the toolbar version of Realtime Zoom. Here is a sample snippet:
  void asdkEditorReactor::commandEnded(const ACHAR* cmdStr)
{
 if(!wcscmp(cmdStr,L"ZOOM") || !wcscmp(cmdStr,L"PAN"))
  screenUpdated();
}

