---
title: "Override drag & drop behavior"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I want to customize drag & drop behavior of AutoCAD. I found some methods which look to be exactly the functions. But I did not know how to use."
author: Autodesk
---
# Override drag & drop behavior

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/override-drag-drop-behavior.html

## 文章内容

By Xiaodong Liang
Issue
I want to customize drag & drop behavior of AutoCAD. I found some methods which look to be exactly the functions. But I did not know how to use.
BOOL acedStartOverrideDropTarget(COleDropTarget* pTarget);
BOOL acedEndOverrideDropTarget(COleDropTarget* pTarget);
BOOL acedAddDropTarget(COleDropTarget* pTarget);
BOOL acedRemoveDropTarget(COleDropTarget* pTarget);
Solution
Firstly, you need to create a class derives from Windows class COleDropTarget. And override the functions of drag & drag.
CMyDropTarget.h
 class CMyDropTarget : public COleDropTarget
{
public:
    CMyDropTarget();
    virtual ~CMyDropTarget();
  // Attributes
public:
// Operations
public:
  // Overrides
    // ClassWizard generated virtual function overrides
    //{{AFX_VIRTUAL(CMyDropTarget)
    public:
      //return value: DROPEFFECT
    //DROPEFFECT_NONE   A drop would not be allowed.
    //DROPEFFECT_COPY   A copy operation would be
    //                    performed.
    //DROPEFFECT_MOVE   A move operation would be
    //                    performed.
    //DROPEFFECT_LINK   A link from the dropped data
    //                   to the original data would be
    //                    established.
    //DROPEFFECT_SCROLL  Indicates that a drag scroll
    //                  operation is about to occur or
    //                   is occurring in the target.
      //Called when the cursor first enters the window.
    virtual DROPEFFECT OnDragEnter(CWnd* pWnd,
         COleDataObject* pDataObject,
         DWORD dwKeyState,
         CPoint point);
    //Called when the cursor is dragged out of the window.
    virtual void OnDragLeave(CWnd* pWnd);
    //Called repeatedly when the cursor is dragged
    //over the window.
    virtual DROPEFFECT OnDragOver(CWnd* pWnd,
        COleDataObject* pDataObject,
        DWORD dwKeyState,
        CPoint point);
    //Called to determine whether the cursor is
    //dragged into the scroll region of the window.
    virtual DROPEFFECT OnDragScroll(CWnd* pWnd,
        DWORD dwKeyState,
        CPoint point);   
    //Called when data is dropped into the window,
    //default handler.
    virtual BOOL OnDrop(CWnd* pWnd,
        COleDataObject* pDataObject,
        DROPEFFECT dropEffect,
        CPoint point);
    //Called when data is dropped into the window,
    //initial handler.
    virtual DROPEFFECT OnDropEx(CWnd* pWnd,
        COleDataObject* pDataObject,
        DROPEFFECT dropDefault,
        DROPEFFECT dropList,
        CPoint point);
    //}}AFX_VIRTUAL
        // Generated message map functions
    //{{AFX_MSG(CMyDropTarget)
        // NOTE - the ClassWizard will add and remove member functions here.
    //}}AFX_MSG
      DECLARE_MESSAGE_MAP()
};
Only Drop() and DropEx() are supported. This means that you just need to implement Drop() (and/or DropEx()) method of COleDropTarget. There's difference in return value for OnDrop() & OnDropEx() methods.
OnDrop() - Return TRUE if you do not want other applications or AutoCAD to handle the drop event by filtering out the drop event from the other applications. Return FALSE if you want other applicaitons to get it.
OnDropEx() - Return -1 if you want other apps to get DropEx() event. Otherwise, return the regular DROPEFFECT value. If you do not want other applications or AutoCAD to handle the drop event,
return FALSE.
CMyDropTarget.cpp
CMyDropTarget::CMyDropTarget()
{
}
  CMyDropTarget::~CMyDropTarget()
{
} 
  BEGIN_MESSAGE_MAP(CMyDropTarget, COleDropTarget)
    //{{AFX_MSG_MAP(CMyDropTarget)
        // NOTE - the ClassWizard will add and remove mapping macros here.
    //}}AFX_MSG_MAP
END_MESSAGE_MAP()
  /////////////////////////////////////////////////////////////////////////////
// CMyDropTarget message handlers
  DROPEFFECT CMyDropTarget::OnDragEnter(CWnd* pWnd, COleDataObject* pDataObject,DWORD dwKeyState, CPoint point)
{
    //don't call base class implementation under any circumstances
    //the base delegates to the view and the view calls this function again
    //your stack will be full in no time and you crash
    //return COleDropTarget::OnDragEnter(pWnd,pDataObject, dwKeyState, point);
    return DROPEFFECT_COPY;
}
  void CMyDropTarget::OnDragLeave(CWnd* pWnd)
{
    //don't call base class implementation under any circumstances
    //the base delegates to the view and the view calls this function again
    //your stack will be full in no time and you crash
    //COleDropTarget::OnDragLeave(pWnd);
}
  DROPEFFECT CMyDropTarget::OnDragOver(CWnd* pWnd, COleDataObject* pDataObject, DWORD dwKeyState, CPoint point)
{
    //don't call base class implementation under any circumstances
    //the base delegates to the view and the view calls this function again
    //your stack will be full in no time and you crash
    //return COleDropTarget::OnDragOver(pWnd,pDataObject, dwKeyState, point);
    return DROPEFFECT_COPY;
}
  DROPEFFECT CMyDropTarget::OnDragScroll(CWnd* pWnd, DWORD dwKeyState, CPoint point)
{
    //don't call base class implementation under any circumstances
    //the base delegates to the view and the view calls this function again
    //your stack will be full in no time and you crash
    //return COleDropTarget::OnDragScroll(pWnd, dwKeyState, point);
    return DROPEFFECT_COPY;
}
  DROPEFFECT CMyDropTarget::OnDropEx(CWnd* pWnd, COleDataObject* pDataObject,DROPEFFECT dropDefault, DROPEFFECT dropList, CPoint pt)
{
    //don't call base class implementation under any circumstances
    //the base delegates to the view and the view calls this function again
    //your stack will be full in no time and you crash
    //return COleDropTarget::OnDropEx(pWnd,pDataObject,dropDefault,dropList,point);
    BOOL DoCondition = false;
    if(DoCondition)
    {
        //do anything..
        return DROPEFFECT_NONE;
    }
     //the following code shows what you might want to do upon drop. e.g. add a polyline to database.
      if (!pWnd->IsKindOf(RUNTIME_CLASS(CView)))
        return DROPEFFECT_NONE;
    //find out which document we are dropping this
    AcDbDatabase* pDb =  AcApGetDatabase((CView*)pWnd);
    AcApDocument* pDoc = acDocManagerPtr()->document(pDb);
    //activate that document
    AcApDocument* pActive = acDocManagerPtr()->mdiActiveDocument();
    if (pActive != pDoc && acDocManagerPtr()->activateDocument(pDoc)!=Acad::eOk)
        return DROPEFFECT_NONE;
    //lock it
    if (acDocManagerPtr()->lockDocument(pDoc)!=Acad::eOk)
        return DROPEFFECT_NONE;
        AcDbBlockTable* pBT;
    if (pDb->getBlockTable(pBT,AcDb::kForRead)==Acad::eOk)
    {
        AcDbBlockTableRecord* pR;
        if (pBT->getAt(strSpace,pR,AcDb::kForWrite)==Acad::eOk)
            {
//draw a rectangle
    AcDbPolyline* pPline = new AcDbPolyline(4);
   pPline->addVertexAt(0,AcGePoint2d(-0.7071,
                                      0.7071));
   pPline->addVertexAt(1,AcGePoint2d(-0.7071,
                                    -0.7071));
   pPline->addVertexAt(2,AcGePoint2d( 0.7071,
                                    -0.7071));
   pPline->addVertexAt(3,AcGePoint2d( 0.7071,
                                    0.7071));
  pPline->setClosed(Adesk::kTrue); 
  if (pR->appendAcDbEntity(pPline)==Acad::eOk)
          pPline->close();
   else
        delete pPline;
             }
           pR->close();
           pBT->close();
    }
      acDocManagerPtr()->unlockDocument(pDoc);
    pWnd->SetFocus();  
    return DROPEFFECT_COPY;
}
  BOOL CMyDropTarget::OnDrop(CWnd* pWnd, COleDataObject* pDataObject, DROPEFFECT dropEffect, CPoint point)
{
    //don't call base class implementation under any circumstances
    //the base delegates to the view and the view calls this function again
    //your stack will be full in no time and you crash
    //return COleDropTarget::OnDrop(pDataObject, dropEffect, point);
    return false;
    return TRUE;
}
  After CMyDropTarget is created, in your application, define an instance of CMyDropTarget
    CMyDropTarget g_dropTarget;
In a location you want, start custom drag & drop:
   acedStartOverrideDropTarget(&g_dropTarget);
You need to call acedEndOverrideDropTarget after your DragDrop event ends.
   acedEndOverrideDropTarget(&g_dropTarget);
  About acedAddDropTarget(COleDropTarget* pTarget), this is used to hook into AutoCAD DropTarget so that you'll get DragDrop events.However, it is not guaranteed that you will get these events because other ARX applications can hook into the DragDrop events and decide not to pass the events along with other ARX applications and AutoCAD.BOOL acedRemoveDropTarget(COleDropTarget* pTarget)
Parameters:
pTarget - custom COleDropTarget to be removed.
Remove hook to AutoCAD DragDrop Event.

## 评论

**内容**: Dan said...
I'm trying to use this to disallow dragging of my custom objects, but I don't necessarily want to override the default drag-and-drop action of AutoCAD. Similarly, I don't want to try and re-implement AutoCAD's default behaviour. Is there a way to prevent my objects from being dragged whilst leaving the standard drag-drop behaviour intact?
Reply
08/10/2016 at 03:15 PM

---
