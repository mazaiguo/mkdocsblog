---
title: "List of extensible tab dialogs in AutoCAD"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "What are the dialog names that are extensible In AutoCAD 2007 through the TabExtensionManager?"
author: Autodesk
---
# List of extensible tab dialogs in AutoCAD

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/list-of-extensible-tab-dialogs-in-autocad.html

## 文章内容

By Xiaodong Liang 
Issue
What are the dialog names that are extensible In AutoCAD 2007 through the TabExtensionManager?
Solution
There are three tabbed dialogs that are extensible in AutoCAD e..g.
- Options dialog ("OptionsDialog")
- Drawing Aids dialog ("DrawingSettingsDialog")
- Mtext editor ("MTextEditor")
You need to pass the name in () is the string to acedRegisterExtendedTab() function.
BOOL acedRegisterExtendedTab(
    LPCTSTR szAppName, 
    LPCTSTR szDialogName
);
This function lets AutoCAD know that the calling application, identified by szAppName, wants to add tabs to the dialog whose published name is szDialogName.
The calling application should call this function from the AcRx::kInitAppMsg case of its acrxEntryPoint() function.
in the previous ObjectARX SDK, there is a sample called ExtendTabs. In current SDKs, it is removed. Here is the updated version of the sample. Download ExtendTabs-VS2010-Acad2013
The core code is as below:
  CTab1 gTab1;
CTab1 gTab2;
void addMyTabs(CAdUiTabExtensionManager* pXtabManager)
// Add the tabs here.
{
    // When resource from this ARX app is needed, just
    // instantiate a local CAcModuleResourceOverride
    CAcModuleResourceOverride resOverride;
      // Add our tabs to the 'OPTIONS' dialog
    BOOL flag = pXtabManager->AddTab(_hdllInstance, IDD_TAB1,_T("My Tab1"), &gTab1);
    gTab1.StretchControlXY(IDC_EDIT1, 50, 50);
    gTab1.StretchControlXY(IDC_EDIT2, 50, 50);
    gTab1.MoveControlX(IDC_EDIT2, 100);
    gTab1.MoveControlX(IDC_STATIC2, 100);
    flag =  pXtabManager->AddTab(_hdllInstance, IDD_TAB2,_T("My Tab2"), &gTab2);
    gTab2.StretchControlXY(IDC_LIST1, 50, 100);
    gTab2.MoveControlX(IDC_RADIO1, 100);
    gTab2.MoveControlX(IDC_RADIO2, 100);
    gTab2.MoveControlX(IDC_RADIO3, 100);
    gTab2.MoveControlX(IDC_STATIC1, 100);
    gTab2.StretchControlXY(IDC_LIST2, 50, 100);
    gTab2.MoveControlX(IDC_LIST2, 100);
    gTab2.MoveControlY(IDC_STATIC3, 100);
    gTab2.MoveControlY(IDC_EDIT1, 100);
    gTab2.MoveControlY(IDC_BUTTON, 100);
  }
//----- ObjectARX EntryPoint
class CExtendTabsApp : public AcRxArxApp {
  public:
    CExtendTabsApp () : AcRxArxApp () {}
      // need to override On_kInitDialogMsg which initializes
    // dialogs
    virtual AcRx::AppRetCode On_kInitDialogMsg(void *pkt)
    {
        // You *must* call On_kInitDialogMsg here
         AcRx::AppRetCode retCode
              =AcRxArxApp::On_kInitDialogMsg (pkt) ;
         // add my tabs
          addMyTabs((CAdUiTabExtensionManager*)pkt);
         return (retCode) ;
      }
    virtual AcRx::AppRetCode
            On_kInitAppMsg (void *pkt)
   { 
        // You *must* call On_kInitAppMsg here
        AcRx::AppRetCode retCode
            =AcRxArxApp::On_kInitAppMsg (pkt) ;
          // TODO: Add your initialization code here   
          // Express interest in adding tabs to the OPTIONS dialog.
        // The name of the OPTIONS dialog in AutoCAD is "OptionsDialog".
         acedRegisterExtendedTab(
            _T("EXTENDTABS.ARX"),
            _T("OptionsDialog"));
        acutPrintf(
            _T("\nCommand is \"ExtendTabs\"."));         return (retCode) ;
    }
      virtual AcRx::AppRetCode
                 On_kUnloadAppMsg (void *pkt) {
        // You *must* call On_kUnloadAppMsg here
        AcRx::AppRetCode retCode =AcRxArxApp::On_kUnloadAppMsg (pkt) ;
          // TODO: Unload dependencies here 
        return (retCode) ;
    }
      virtual void RegisterServerComponents () {
    }
      static void MyGroupMyCommand () {
        // Put your command code here
      } 
} ;

