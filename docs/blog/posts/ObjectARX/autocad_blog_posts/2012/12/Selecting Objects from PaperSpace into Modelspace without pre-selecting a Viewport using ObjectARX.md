---
title: "Selecting Objects from PaperSpace into Modelspace without pre-selecting a Viewport using ObjectARX"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "There is an undocumented function in ObjectARX which you can use called acedNEntSelPEx() which does exactly this. It even allows you to supply a pi..."
author: Autodesk
---
# Selecting Objects from PaperSpace into Modelspace without pre-selecting a Viewport using ObjectARX

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/selecting-objects-from-paperspace-into-modelspace-without-pre-selecting-a-viewport-using-objectarx.html

## 文章内容

by Fenton Webb
There is an undocumented function in ObjectARX which you can use called acedNEntSelPEx() which does exactly this. It even allows you to supply a picked point via the ‘pickflag’ parameter so you can supply your own programmatically supplied PS points…
Here’s some sample code for you…
extern int acedNEntSelPEx ( const TCHAR *str, ads_name entres,
                            ads_point ptres, int pickflag,
                            ads_matrix xformres,
                            struct resbuf **refstkres,
                            unsigned int uTransSpaceFlag,
                            int* gsmarker);
static void asdkSelectEnt_sel(void)
{
  int     gsmarker = -1;
  ads_name  ename;
  struct resbuf *rbChain;
  ads_point  selPt;
  ads_matrix tranMat;
    // Select a single object. If it's a block reference or a sub-entity
  // within a block reference, rbChain will not be null.
  unsigned int uTransSpaceFlag = 1;
  // set uTransSpaceFlag to 0, if the current layout is in model space
  struct resbuf rb;
  acedGetVar(_T("CVPORT"), &rb);
  if (rb.resval.rint != 1)
    uTransSpaceFlag = 0;  // Model space
    // now do the entity select
  int stat = acedNEntSelPEx(_T("\nPick entity : "), ename,
           selPt, 0, tranMat, &rbChain, uTransSpaceFlag, &gsmarker);
  // if everything worked ok
  if (RTNORM == stat)
  {
    // open the selected entity for
    AcDbObjectId objId;
    acdbGetObjectId(objId,ename);
    AcDbObjectPointer<AcDbEntity> pEnt(objId,AcDb::kForRead);
    if (pEnt.openStatus() == Acad::eOk)
      pEnt->list();
  }
}

## 评论

**内容**: design2@expodirect.com.au said...
Could you give us the same code in vb.net We realy need it :-)
Reply
11/04/2013 at 06:36 PM

---
**内容**: Alexander Rivilis said in reply to design2@expodirect.com.au...
In order to use acedNEntSelPEx with VB.NET you have to P/Invoke it such as: http://www.theswamp.org/index.php?topic=22963.msg345716#msg345716
Also you have remember that code working with AutoCAD 2007...2009 x86, so you have to do some changes
Reply
11/06/2013 at 01:31 PM

---
