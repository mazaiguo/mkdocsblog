---
title: "Customizing CAdUiListCtrl"
date: 2014-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "If you are using CAdUiListCtrl and wish to customize it more, you can do it by using custom draw. This is same as customizing any other MFC control..."
author: Autodesk
---
# Customizing CAdUiListCtrl

发布日期: 2014-09-01

原始链接: https://adndevblog.typepad.com/autocad/2014/09/customizing-caduilistctrl.html

## 文章内容

By Balaji Ramamoorthy
If you are using CAdUiListCtrl and wish to customize it more, you can do it by using custom draw. This is same as customizing any other MFC controls and a nice article on customizing a CListCtrl is here :
Neat Stuff to Do in List Controls Using Custom Draw
Following the custom drawing on list control derived from CAdUiListCtrl, here is a code snippet for displaying color values.
 // MyListCtrl.h 
 #pragma  once 
   class  MyListCtrl : public  CAdUiListCtrl 
 {
  DECLARE_DYNAMIC(MyListCtrl)
 private :
  // Helper method 
  CString ColorNameFromIndex(int  colorIndex);
   public :
  MyListCtrl();
  virtual  ~MyListCtrl();
   protected :
  DECLARE_MESSAGE_MAP()
    // Custom draw 
  afx_msg void  OnCustomDraw 
   ( NMHDR* pNMHDR, LRESULT* pResult );
 };
   // MyListCtrl.cpp : implementation file 
   #include  "stdafx.h" 
 #include  "MyListCtrl.h" 
   IMPLEMENT_DYNAMIC(MyListCtrl, CAdUiListCtrl)
   MyListCtrl::MyListCtrl(){}
   MyListCtrl::~MyListCtrl(){}
   BEGIN_MESSAGE_MAP(MyListCtrl, CAdUiListCtrl)
  ON_NOTIFY_REFLECT ( NM_CUSTOMDRAW, OnCustomDraw)
 END_MESSAGE_MAP()
   // Custom draw  
 afx_msg void  MyListCtrl::
  OnCustomDraw ( NMHDR* pNMHDR, LRESULT* pResult)
 {
  NMLVCUSTOMDRAW* pLVCD 
   = reinterpret_cast <NMLVCUSTOMDRAW*>(pNMHDR);
       // Take the default processing unless we  
     // set this to something else below. 
     *pResult = CDRF_DODEFAULT;
       // First thing - check the draw stage.  
  // If's the's prepaint 
     // stage, then tell Windows we want messages  
  // for every item. 
     if  ( CDDS_PREPAINT 
   == pLVCD->nmcd.dwDrawStage )
  {
         *pResult = CDRF_NOTIFYITEMDRAW;
     }
     else  if  ( CDDS_ITEMPREPAINT 
   == pLVCD->nmcd.dwDrawStage )
  {
   *pResult = CDRF_NOTIFYPOSTPAINT;
  }
  else  if  ( CDDS_ITEMPOSTPAINT 
   == pLVCD->nmcd.dwDrawStage )
  {
   LVITEM rItem;
   int     nItem = 
    static_cast <int >( pLVCD->nmcd.dwItemSpec);
   CDC*  pDC = CDC::FromHandle ( pLVCD->nmcd.hdc);
   CRect rcIcon;
     // RGB color treating item row as a color index 
   long  acirgb, r,g,b;
         acirgb = acedGetRGB ( nItem );
         r = ( acirgb & 0xffL );
         g = ( acirgb & 0xff00L ) >> 8;
         b = acirgb >> 16; 
   CBrush brush(RGB(r,g,b));
     CRect rcItem;
   GetSubItemRect(nItem, 1, rcItem);
     int  w = rcItem.Width();
   int  h = rcItem.Height();
     CRect clrBox((int )rcItem.left + 0.1 * h, 
       (int )rcItem.top + 0.1 * h, 
       (int )rcItem.left + 0.9 * h, 
       (int )rcItem.top + 0.9 * h);
       CBrush* pOldBrush = pDC->SelectObject(&brush);
     // create and select a thick, black pen 
   CPen penBlack;
   penBlack.CreatePen(PS_SOLID, 1, RGB(0, 0, 0));
   CPen* pOldPen = pDC->SelectObject(&penBlack);
     pDC->Rectangle(clrBox);
   pDC->TextOutW(clrBox.right + 0.1*h, 
      (int )rcItem.top + 0.1 * h, 
      ColorNameFromIndex(nItem));
     // put back the old objects 
   pDC->SelectObject(pOldBrush);
   pDC->SelectObject(pOldPen);
     *pResult = CDRF_DODEFAULT;
  }
 }
   // Helper method 
 CString MyListCtrl::ColorNameFromIndex
        (int  colorIndex)
 {
  switch (colorIndex)
  {
   case  0:
    return  _T("Black" );
   case  1:
    return  _T("Red" );
   case  2:
    return  _T("Yellow" );
   case  3:
    return  _T("Green" );
   case  4:
    return  _T("Cyan" );
   default  :
   {
    CString str;
    str.Format(_T("%d" ), colorIndex);
    return  str;
   }
  }
 }
  To use the List control in a dialog, insert an MFC List control and add a member variable for it. Replace the CListCtrl with the custom List control class. Here is a code snippet :
 // SampleDlg.h 
 // Member variable for the List control 
 MyListCtrl mMyList;
   // SampleDlg.cpp 
 BOOL SampleDlg::OnInitDialog()
 {
  CDialog::OnInitDialog();
    // Insert two columns 
  mMyList.InsertColumn(
   0, 
   _T("Layer Name" ), 
   LVCFMT_LEFT, 90);
    mMyList.InsertColumn(
   1, 
   _T("Color" )
   , LVCFMT_LEFT, 90);
    // Contents of column-1 will be  
  // customized at runtime 
  // so provided as empty 
  int  nIndex = 
   mMyList.InsertItem(0, _T("Layer 0" ));
  mMyList.SetItemText(nIndex, 1, _T(" " ));
    nIndex 
   = mMyList.InsertItem(1, _T("Layer 1" ));
  mMyList.SetItemText(nIndex, 1, _T(" " ));
    nIndex 
   = mMyList.InsertItem(2, _T("Layer 2" ));
  mMyList.SetItemText(nIndex, 1, _T(" " ));
    nIndex 
   = mMyList.InsertItem(3, _T("Layer 3" ));
  mMyList.SetItemText(nIndex, 1, _T(" " ));
    nIndex
   = mMyList.InsertItem(4, _T("Layer 4" ));
  mMyList.SetItemText(nIndex, 1, _T(" " ));
    return  TRUE;  
 }
  Here is the customized list control displaying color values

