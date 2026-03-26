---
title: "Adding Custom Menu to AutoCAD Application Frame"
date: 2016-06-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Plugin
description: "AutoCAD 2016 introduced a new class AdApplicationFrame which has exposed a bunch of API to access the application frame."
author: Autodesk
---
# Adding Custom Menu to AutoCAD Application Frame

发布日期: 2016-06-01

原始链接: https://adndevblog.typepad.com/autocad/2016/06/adding-custom-menu-to-autocad-application-frame.html

## 文章内容

By Madhukar Moogala
AutoCAD 2016 introduced a new class AdApplicationFrame which has exposed a bunch of API to access the application frame.
In this blog post we will see how we can create and add our custom menu replacing the existing ‘MENUBAR’.
With help of AdApplicationFrame instance we can do our major MFC kind of UI elements in our AutoCAD.
Adding Custom menu:
  void testAddCustomMenu()
  {
  Acad::ErrorStatus error = Acad::eOk;
  AdApplicationFrame* pNewAppFrame = acedGetApplicationFrame();
  pNewAppFrame != NULL ? error = Acad::eOk : error = Acad::eNullPtr;
  HMENU hDefaultMenu = NULL;  /*Needed to restore to Default ACAD Menu*/
  HMENU hNewMenu = NULL;
  CString strDirName;
  HMODULE hm = NULL;
    /*Switch Acad Resource to Our's*/
  CAcModuleResourceOverride hResources(AcadFrameDLL.ModuleResourceInstance());
  if (eOkVerify(error))
  {
  /*To retrieve pointer to Menubar*/
  AdMenuBar* pMenuBar = NULL;
  pMenuBar = pNewAppFrame->GetMenuBar();
  pMenuBar != NULL ? error = Acad::eOk : error = Acad::eNullPtr;
  if (eOkVerify(error))
  {
    hDefaultMenu = pMenuBar->GetMenuHandle();
  if (hDefaultMenu != 0)
  {
    strDirName = _T("D:\\Temp\\AcadFrame\\x64\\Debug\\madAcadFrame.arx");
  hm = GetModuleHandle(strDirName);
  if (hm != NULL)
  {
  // Set custom menu
  hNewMenu = LoadMenu(hm, MAKEINTRESOURCE(IDR_MENU1));
  if (hNewMenu != NULL)
  {
  bool bOk = pMenuBar->SetMenuHandle(hNewMenu);
  if(bOk)
  pMenuBar->UpdateMenu();
  else
  error = (Acad::ErrorStatus)Acad::eFailed;
  }
  else
  {
  error = Acad::eNullHandle;
  }
  // To Revert back to default menu
  /* if (pMenuBar->SetMenuHandle(hDefaultMenu))
  pMenuBar->UpdateMenu();
  else
  error = (Acad::ErrorStatus)Acad::eFailed;*/
  }
  else
  error = Acad::eNullHandle;
      }
  else
  error = Acad::eNullHandle;
  }
  else
  error = Acad::eUnrecoverableErrors;
    /*We will enable MenuBar visibility*/
  if(!pNewAppFrame->IsMenuBarVisible())
  pNewAppFrame->EnableMenuBar(true);
  }
  else
  error = Acad::eNullPtr;
    acutPrintf(_T("\n%s"), acadErrorStatusText(error));
  }
  Getting User Credentials:
If we user logged in to AutoCAD with A360, we can get user ID and user name using following API’s
Earlier it was possible to get same information with CLI ONLINEUSERID and ONLINEUSERNAME
void getUserCredentials()
{
Acad::ErrorStatus error = Acad::eOk;
AdApplicationFrame* pNewAppFrame = acedGetApplicationFrame();
pNewAppFrame != NULL ? error = Acad::eOk : error = Acad::eNullPtr;
if (eOkVerify(error))
{
CString userId;
CString userName;
  int bOK = -1;
/*Check if user Logged in to A360*/
if (pNewAppFrame->IsLoggedIn())
{
/*Same can be retrieved using ONLINEUSERID and ONLINEUSERNAME*/
bOK = pNewAppFrame->GetLoginUserId(userId.GetBuffer(BUFSIZE), BUFSIZE);
acutPrintf(_T("\n user id : [%s]"), userId);
userId.ReleaseBuffer();
bOK = pNewAppFrame->GetLoginUserName(userName.GetBuffer(BUFSIZE), BUFSIZE);
acutPrintf(_T("\n user name : [%s]"), userName);
userName.ReleaseBuffer();
int server = pNewAppFrame->GetServer();
acutPrintf(_T("\n Server Port : [%d]"), server);
  }
  }
}

## 评论

**内容**: Jamie said...
Where do I find additional information about the usage of this new class?
There are lots of methods I would like to use but the arx documentation (arxref.chm) is pretty much useless for this.
For instance the bool Initialize(); method will lock up AutoCAD.
Reply
02/02/2017 at 08:31 AM

---
**内容**: Tom DiVittis said in reply to Jamie...
I'll second the request. ;)
Reply
02/27/2017 at 12:52 PM

---
