---
title: "How to use CAdUiDockControlBar"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "CAdUiDockControlBar provided you to create dock panel. The basic steps are:"
author: Autodesk
---
# How to use CAdUiDockControlBar

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/how-to-use-caduidockcontrolbar.html

## 文章内容

By Xiaodong Liang
CAdUiDockControlBar provided you to create dock panel. The basic steps are:
- Create a dialog in the normal way.
class CMyChildDialog : public CDialog
{
// Construction
public:
    CMyChildDialog(CWnd* pParent = NULL);   // standard constructor
  // Dialog Data
    //{{AFX_DATA(CMyChildDialog)
    enum { IDD = IDD_CHILDDIALOG };
        // NOTE: the ClassWizard will add data members here
    //}}AFX_DATA
  //………
}

- Add a member variable to you DockCtrlBar class which is a pointer to the dialog class.
class CMyDockControlBar : public CAcUiDockControlBar
{
    DECLARE_DYNAMIC(CMyDockControlBar)
  public:
   CMyChildDialog *m_childDlg;
    CMyDockControlBar () ;
      //{{AFX_VIRTUAL(CMyDockControlBar)
    public:
    virtual BOOL Create(CWnd*pParent, LPCTSTR lpszTitle);
    //}}AFX_VIRTUAL
  protected:
    //{{AFX_MSG(CMyDockControlBar)
    afx_msg int OnCreate (LPCREATESTRUCT lpCreateStruct);
    afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
    afx_msg void OnSize(UINT nType, int cx, int cy);
    //}}AFX_MSG
    DECLARE_MESSAGE_MAP()
      virtual void SizeChanged (CRect *lpRect, BOOL bFloating, int flags);
} ;

- In the DockCtrlBar::OnCreate() instantiate the dialog as a child of the DockCtrlBar.
BOOL CMyDockControlBar::Create(CWnd*pParent, LPCTSTR lpszTitle) {
    CString strWndClass ;
    strWndClass =AfxRegisterWndClass (CS_DBLCLKS, LoadCursor (NULL, IDC_ARROW)) ;
    CRect rect (0, 0, 250, 200) ;
    if ( !CAcUiDockControlBar::Create (
            strWndClass,
            lpszTitle,
            WS_VISIBLE | WS_CHILD | WS_CLIPCHILDREN,
            rect,
            pParent, 0
        )
    )
        return (FALSE) ;
      SetToolID (&clsCMyDockControlBar) ;
      //----- TODO: Add your code here
      return (TRUE) ;
}
  int CMyDockControlBar::OnCreate (LPCREATESTRUCT lpCreateStruct) {
    if ( CAcUiDockControlBar::OnCreate (lpCreateStruct) == -1 )
        return (-1) ;
      // point to our resource
    CAcModuleResourceOverride resourceOverride;   
    // now create a new dialog with our stuff in it
    m_childDlg = new CMyChildDialog;
    // create it and set the parent as the dockctrl bar
    m_childDlg->Create (IDD_CHILDDIALOG, this);
    // move the window over so we can see the control lines
    m_childDlg->MoveWindow (0, 0, 100, 100, TRUE);
      return (0) ;
}

- Disable the dialog's Ok and Cancel modes by overriding the CMyChildDialog::OnCommand().
BOOL CMyChildDialog::OnCommand(WPARAM wParam, LPARAM lParam)
{
    switch (wParam)
    {
        // Enter
        case 1:
            // Esc
        case 2: return (false);
    }
      return CDialog::OnCommand(wParam, lParam);
}

- Check the Dialog properties and make sure Style=Child, Border=None and TitleBar=False.
  here is the demo project  Download _ArxDockControlBar_VS2008

## 评论

**内容**: Srini said...
I am Getting fatal error at the time of dialog is appear in autocad and unload the arxfile. how to resolve that problem.
Reply
02/11/2015 at 08:24 PM

---
**内容**: Srini said...
I am Getting fatal error at the time of dialog is appear in autocad and unload the arxfile. how to resolve that problem.
Reply
02/11/2015 at 08:24 PM

---
**内容**: Gaetano said...
I tryed this compiling in VS 2019 for AUtoCAD 2021.
It runs well... but how to implement the hide/autohide behaviour?
When docked, by clicking the arrow button near the 'x' button on the right, nothing happens.
Reply
05/11/2021 at 09:57 AM

---
