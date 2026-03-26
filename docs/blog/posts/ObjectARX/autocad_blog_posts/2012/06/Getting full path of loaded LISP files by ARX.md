---
title: "Getting full path of loaded LISP files by ARX"
date: 2012-06-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoLISP
  - C++
  - ObjectARX
description: "How can I get the full path of loaded LISP applications?"
author: Autodesk
---
# Getting full path of loaded LISP files by ARX

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/getting-full-path-of-loaded-lisp-files-by-arx.html

## 文章内容

By Xiaodong Liang
Issue
How can I get the full path of loaded LISP applications?
Solution
There are two APIs on the AcApDocument class in ObjectARX that you can use to get this information.
The following is more information on these functions:
virtual int GetCountOfLispList() const;
Returns the number of load LISP files.
virtual AcLispAppInfo* GetItemOfLispList(int nIndex) const;
Returns the descriptor structure for the LISP application designated by nIndex.
Paramters:
nIndex - integer between 0 and GetCountOfLispList()
class AcLispAppInfo
{
     public: TCHAR appFileName[_MAX_PATH];
     bool bUnloadable;
};
Returned by the GetItemOfLispList.
appFileName - full path of the lisp application
bUnloadable - specifies if the lisp application is unloadable
  static void getLISPFullPathByARX()
{
AcApDocument* pActiveDoc =
     acDocManager->mdiActiveDocument();
  // count of LISP files
int lispCount = pActiveDoc->GetCountOfLispList();
  CString msg;
msg.Format(L"count of LISP file: %d",lispCount);
MessageBox(NULL,msg,msg,0);
   // each LISP info
 for(int index = 0 ;
     index < lispCount;
     index++)
{
       TCHAR msg1[256] = {0};
     AcLispAppInfo *pEachInfo =
         pActiveDoc->GetItemOfLispList(index);
       _tcscat( msg1,pEachInfo->appFileName);
       if(pEachInfo->bUnloadable)
        _tcscat(msg1,L"\nloadable\n");
     else
        _tcscat(msg1,L"\nunloadable\n");
      MessageBox(NULL,msg1,msg1,0);
}
  }

