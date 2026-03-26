---
title: "remove a menu from the menubar _and_ memory"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "My application creates a custom menu and uses IAcadPopupMenus.Add. Removing it later by using RemoveMenuFromMenuBar or IAcadPopupMenu.RemoveFromMen..."
author: Autodesk
---
# remove a menu from the menubar _and_ memory

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/remove-a-menu-from-the-menubar-_and_-memory.html

## 文章内容

By Xiaodong Liang
Issue
My application creates a custom menu and uses IAcadPopupMenus.Add. Removing it later by using RemoveMenuFromMenuBar or IAcadPopupMenu.RemoveFromMenuBar works,
however, why do future attempts to add the same menu fail?
Solution
Although the custom menu can be removed from the menubar once it has been added, the popup menu itself is retained in AutoCAD's memory. This can be proven by observing the value returned by IAcadPopupMenus.GetCount() before and after removing the menu; the count remains the same because it is still effectively a
part of the popup menu collection. Please use the code demos below to test: demo adds 3 menus in the first menu group. run it again, it will removes 1 menu, and checks the menu count before & after removing.
When it is added this way, it will remain so for the remainder of the session. Any menu that has already been added during the lifetime of a loaded application can only be reinserted into the menubar. The Add method should not be called again because the program may terminate unexpectedly.
But what if your application is unloaded and the program tries to clean up solely by removing its custom menu from the menubar? The menu will remain resident in AutoCAD, but if the application is reloaded and attempts to create and add the menu back into the menubar, the program may unexpectedly terminate.
Although you might be able to avoid this problem by iterating through the popup menus to check for a menu that bears the name of the application's custom menu. If found, do not issue an Add() but instead obtain a dispatch pointer to the existing menu and use InsertMenuInMenuBar(). Unfortunately, doing this will also cause the program to terminate unexpectedly if the custom menu is
altogether inaccessible.
In this case, create your popup menus under your own menu group, which can be completely unloaded from memory upon application unload with UnLoad().
  // Enables the menu to be loaded/unloaded with the same command.
static bool bIsMenuLoaded = false;
void
demo()
{
    AutoCAD::IAcadApplication *pAcad;
    AutoCAD::IAcadMenuBar *pMenuBar;
    AutoCAD::IAcadMenuGroups *pMenuGroups;
    AutoCAD::IAcadMenuGroup *pMenuGroup;
    AutoCAD::IAcadPopupMenus *pPopUpMenus;
    AutoCAD::IAcadPopupMenu *pPopUpMenu;
    AutoCAD::IAcadPopupMenuItem *pPopUpMenuItem;
      HRESULT hr = NOERROR;
    LPUNKNOWN pUnk = NULL;
    LPDISPATCH pAcadDisp = acedGetIDispatch(TRUE);
    if(pAcadDisp==NULL)
        return;
      hr = pAcadDisp->QueryInterface(AutoCAD::IID_IAcadApplication,(void**)&pAcad);
    pAcadDisp->Release();
    if (FAILED(hr))
        return;
      pAcad->put_Visible(true);
    pAcad->get_MenuBar(&pMenuBar);
    pAcad->get_MenuGroups(&pMenuGroups);
    pAcad->Release();
    long numberOfMenus;
    pMenuBar->get_Count(&numberOfMenus);
    pMenuBar->Release();
      VARIANT index;
    VariantInit(&index);
    V_VT(&index) = VT_I4;
    V_I4(&index) = 0;
      pMenuGroups->Item(index, &pMenuGroup);
    pMenuGroups->Release();
      pMenuGroup->get_Menus(&pPopUpMenus);
    pMenuGroup->Release();
       if (!bIsMenuLoaded) {       
        // add three menus
        HRESULT hr = pPopUpMenus->Add(
            _T("myDemoMenu1"), &pPopUpMenu);
        hr = pPopUpMenus->Add(
            _T("myDemoMenu2"), &pPopUpMenu);
        hr = pPopUpMenus->Add(
           _T("myDemoMenu3"), &pPopUpMenu);
          if (hr == S_OK) {
            acutPrintf(_T("\nMenu is created."));
          } else {
            acutPrintf(_T("\nMenu not created."));
        }
         bIsMenuLoaded = true;
    }
    else // remove the menu
    {       
       long count = 0;
        pPopUpMenus->get_Count(&count);
        acutPrintf(_T("\n Before remove, count is: %d"),count) ;
          long indexOfMyMenu = -1;
        AutoCAD::IAcadPopupMenu* eachMenu = NULL;
        for (long i=0; i< count; i++)
        {
          BSTR np;
          pPopUpMenus->Item(_variant_t(i),&eachMenu);
          eachMenu->get_Name(&np);
          //remove the first menu in the group
          if (_tcscmp(np, _T("myDemoMenu1"))==0)
          {
              indexOfMyMenu = i;
              break;
          }
        }
          // remove
        if(indexOfMyMenu > -1)
        {
            HRESULT hr = pPopUpMenus->RemoveMenuFromMenuBar(_variant_t(indexOfMyMenu));
            assert (hr == S_OK);
        }
         pPopUpMenus->get_Count(&count);
         // the count is same to before removing.
        acutPrintf(_T("\n After remove, count is: %d"),count) ;
         bIsMenuLoaded = false;
    }
      pPopUpMenus->Release();
}

