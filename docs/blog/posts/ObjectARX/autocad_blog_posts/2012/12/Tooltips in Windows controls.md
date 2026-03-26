---
title: "Tooltips in Windows controls"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - CUI
  - Unicode
description: "This is actually a question of Windows, but may help for some developers. There are several approaches for showing a tooltip for Windows' control i..."
author: Autodesk
---
# Tooltips in Windows controls

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/tooltips-in-windows-controls.html

## 文章内容

By Xiaodong Liang
This is actually a question of Windows, but may help for some developers. There are several approaches for showing a tooltip for Windows' control in AutoCAD. The code you write depends on the level of complexity.
The other blog post introduces add tooltip for CAcUiBitmapButton. Those methods are implemented by CAcUiBitmapButton.
In this post, we introduce the native way of Windows. The project could be downloaded at: Download Create-tooltip-VS2008
First, to generate tooltips from the parent dialog for a given control, you need to add message definition in the head file of your dialog:
    afx_msg BOOL OnNotify_ToolTipText(UINT id,
                                     NMHDR *pNMHDR,
                               LRESULT *pResult);
   
Then in the map field of dialog implement file, add notification.
BEGIN_MESSAGE_MAP(CSampDialog, CAcUiDialog)
     ON_NOTIFY_EX(TTN_NEEDTEXT, 0,  
                 OnNotify_ToolTipText)
END_MESSAGE_MAP()
Next, remember to enable the tooltip in initializing of the dialog:
void CSampDialog::OnInitDialogFinish()
{
    CAcUiDialog::OnInitDialogFinish();
    AutoLoadControl(&m_bmpbtn1);
   EnableToolTips(TRUE);
}
Finally, implement the function: OnNotify_ToolTipText
BOOL CSampDialog::OnNotify_ToolTipText (UINT id, NMHDR *pNMHDR, LRESULT
*pResult)
{
   // Process a Windows request for Tool Tip Text.
   TOOLTIPTEXT *ttt = (TOOLTIPTEXT *)pNMHDR;
   HWND hWnd;
   UINT idFrom;
   BOOL handled = FALSE;
     if (ttt)
   {
    idFrom = pNMHDR->idFrom;
    if (idFrom && (ttt->uFlags & TTF_IDISHWND))
    {
        hWnd = (HWND)idFrom;
        idFrom = ::GetDlgCtrlID(hWnd);
        if (idFrom)
        {
        // At this point it's determined that the notification's
        // ID is really an HWND and the true control ID is known. The
        // following turns the ToolTipText request into an internal
        // notification. The control ID and notification code are
        // passed in WParam and the address of a CString buffer that
        // will receive the text is passed in LParam. If the request
        // is handled (i.e. reply is non-zero) then the CString's
        // contents are copied back to the ToolTipText buffer.
        CString u;
        CPoint p;
        WPARAM wp;
        LPARAM lp;
        LRESULT res = 0;
        if (GetCursorPos(&p))
        {
            wp = MAKEWPARAM(idFrom, kAdUiNotify_GetTipSupport);
            lp = (LPARAM)&p;
            res = SendMessage(AdUiMessage(), wp, lp);
        }
        if (res == kAdUiReply_ToolTip)
        {
            wp = MAKEWPARAM(idFrom, kAdUiNotify_GetTipText);
            lp = (LPARAM)&u;
            res = SendMessage(AdUiMessage(), wp, lp);
            handled = (res == kAdUiReply_Ok);
            if (handled)
            {
            _tcsncpy(ttt->szText, u, 80);
            ttt->szText[79] = '\0';
            return (TRUE) ;
            }
        }
        // if not handle by the control itself,
        // the dialog decides for a tooltip
        switch ( idFrom )
        {
            case IDC_BUTTON3:// the control we want to show tooltip
            _tcscpy(ttt->szText, _T("This is a tooltip text"));
            return (TRUE) ;
        }
        }
    }
   }
   return (FALSE) ;
}

