---
title: "Positioning AcPane in StatusBar"
date: 2015-04-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
  - Unicode
description: "I’ve recently received a query from an ADN partner about positioning AcPane, I will show sample code to achieve the same."
author: Autodesk
---
# Positioning AcPane in StatusBar

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/positioning-acpane-in-statusbar.html

## 文章内容

By Madhukar Moogala
I’ve recently received a query from an ADN partner about positioning AcPane, I will show sample code to achieve the same.
Before getting in to the code, just want to inform you that with Acad 2015 support for showing text labels on the buttons in the status bar is not available.
Earlier we can switch between text labels and icons of status bar panes, now only icons.
I got an opportunity to migrate a very old sample on status bar which was shipped with ObjectARX SDK 2007  to current AutoCAD 2014/15.
void testPane()
{
int result;
AcApDocument *pDoc=acDocManager->curDocument();
AcApStatusBar* pStatus = acedGetApplicationStatusBar(); 
if (pStatus) 
{ 
/*Get pane count*/
int iCnt = pStatus->GetPaneCount();
/*Get default pane to position our custom pane */
AcPane* pdfltPane =
pStatus->GetDefaultPane(ACSBPANE_APP_ORTHO);
int index =
pStatus->GetIndex(pdfltPane);
int iStyle=
pdfltPane->GetStyle(); 
CPaneItem* pPaneItem = new CPaneItem();
result=
pPaneItem->SetToolTipText(
        _T("Pane Icon Item Tooltip"));
pPaneItem->Enable(TRUE);
result=pPaneItem->SetStyle(iStyle);
pPaneItem->SetVisible(TRUE);
HICON hIcon =
(HICON)::LoadImage(_hdllInstance,
                    MAKEINTRESOURCE(IDI_WORLD),
                    IMAGE_ICON, 16, 16, 0);
result=pPaneItem->SetIcon(hIcon);   
result = pStatus->Insert(index+1, pPaneItem); 
  } 
pStatus->Update(); 
  SDK migrated sample

## 评论

**内容**: WolframKuss said...
Thank you for migrating it to 2014 and 2015 and for publishing it! It works very nicely on 2014.
However, we are now switching to 2016 and I wonder whether "SetStyle" with "ACSB_NORMAL" / "ACSB_POPOUT" still makes a difference and the user can see the state of the button (on or off) or whether this has to be achieved by setting two different icons?
Wolfram.
Reply
04/23/2015 at 07:12 AM

---
**内容**: Madhukar Moogala said...
Thanks Wolfram for comment,
No, single icon would be sufficient. enable and disable can be employed to status bar button following way, assuming CPaneItem is derived from AcPane
void CPaneItem::OnLButtonDown(UINT nFlags, CPoint point)
{
m_Enable=!m_Enable;
if(m_Enable)
{
SetStyle(ACSB_NORMAL);
AfxMessageBox(_T("Pane Item Enabled"));
}
else
{
/*To ensure menu pop up on right click MB*/
SetStyle(ACSB_POPOUT);
AfxMessageBox(_T("Pane Item Disabled"));
}
acDocManager->curDocument()->drawingStatusBar()->Update();

}
Reply
04/23/2015 at 11:59 PM

---
**内容**: Jef said...
Hi!
I have the same problem as WolframKuss.
The calls to SetStyle(ACSB_ACTIVE); do not change anything.
The icon stays 'inactive'.
Changing the icon though works fine.
I used AutoCAD 2021.
Regards,
Jef
Reply
02/26/2021 at 08:24 AM

---
