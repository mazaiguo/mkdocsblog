---
title: "Combobox/mouse over/disappear and text size in docked bar"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - CUI
  - Unicode
description: "After successfully following the the CAcUiDockControlBar sample, I place a combo box or a CAcUiXXXComboBox at the bottom portion the dockbar. If I ..."
author: Autodesk
---
# Combobox/mouse over/disappear and text size in docked bar

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/comboboxmouse-overdisappear-and-text-size-in-docked-bar.html

## 文章内容

By Xiaodong Liang
Issue
After successfully following the the CAcUiDockControlBar sample, I place a combo box or a CAcUiXXXComboBox at the bottom portion the dockbar. If I expand the combobox so the items are expanded, I can select an entry, but when I move the mouse cursor over the expanded portion, it disappears. The text size in the color combobox is larger than the tree control in the docked bar.
Solution
If you use CAcUiXXXComboBox(s), you'll need to make sure the following combobox styles are set:
- Type: Drop List
- Owner draw: Fixed
- Enable the "Has strings" option, and clear "Sort" and enable 
                    "Vertical scroll".
When the expanded portion disappears, it is by design. When you move the mouse cursor outside a docked bar, the cursor needs to be changed to be an Acad cursor type. Therefore, if you have a combo box that expands over any Acad's properties, Acad will get its cursor back. At the time when CAcUiDockControlBar is created, this issue existed.
There is a undocumented function CanFrameworkTakeFocus() of the CAcUiDockControlBar (comes with the SDK), which controls the behavior. To change it, override it and return false.
class CSampDialogBar : public CAcUiDockControlBar
//class CSampDialogBar : public CAcUiDialogBar
{
    DECLARE_DYNAMIC(CSampDialogBar);
// Construction
public:
    CSampDialogBar();   // standard constructor
      CTreeCtrl    m_tree;
    CComboBox   m_MyCombo;
    CAcUiColorComboBox   m_combo;
      void PaintControlBar(CDC* pDC);
  // Overrides
    // ClassWizard generated virtual function overrides
    //{{AFX_VIRTUAL(CSampDialogBar)
    public:
    virtual BOOL Create(CWnd*pParent, LPCTSTR  lpszTitle);
    //}}AFX_VIRTUAL
private:
    // this override is to make the any control
    // that extends beyond the dockbar to be
    // selectable. Otherwise, the default
    // is to restore Acad cursor so the portion
    // is repainted immediately.
   bool CanFrameworkTakeFocus() { return false;}
  // Implementation
protected:
      // Generated message map functions
    //{{AFX_MSG(CSampDialogBar)
    afx_msg int OnCreate (LPCREATESTRUCT lpCreateStruct);
    //}}AFX_MSG
    DECLARE_MESSAGE_MAP()
      virtual void SizeChanged (CRect *lpRect, BOOL bFloating, int flags);
  };
Now you should be able to select the expanded items out of the combobox.
3. In regards to combobox's text size, it is too big because it will be whatever default is out there since itself doesn't have a font size set. To overcome it, just get a font you want from something and set to it, for example, in your OnCreate().
  int
CSampDialogBar::OnCreate (LPCREATESTRUCT lpCreateStruct)
{
     // …. other codes
        // this will make the font size the same as in the tree control
    // otherwise it is a bigger one
    m_MyCombo.SetFont(m_tree.GetFont());
    m_combo.SetFont(m_tree.GetFont());
    return 1;
}
Please refer to the attached project. Download Combobox-mouse-hover-VS2008

