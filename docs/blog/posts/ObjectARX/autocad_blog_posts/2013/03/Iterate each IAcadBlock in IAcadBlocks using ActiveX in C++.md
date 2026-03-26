---
title: "Iterate each IAcadBlock in IAcadBlocks using ActiveX in C++"
date: 2013-03-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - Block
  - C++
  - COM
description: "In C++, I don't seem to be able to iterate the IAcadBlocks to access each IAcadBlock. Is there sample code that does this?"
author: Autodesk
---
# Iterate each IAcadBlock in IAcadBlocks using ActiveX in C++

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/iterate-each-iacadblock-in-iacadblocks-using-activex-in-c.html

## 文章内容

Issue
In C++, I don't seem to be able to iterate the IAcadBlocks to access each IAcadBlock. Is there sample code that does this?
Solution
The following two approaches iterate the IAcadBlocks to access each IAcadBloc. This assumes that you have set up your skeleton ARX/MFC project, importing the tlb of AutoCAD COM library already.
void test()
{
    try
    {
        // get application
        IAcadApplicationPtr pIAcad =
            acedGetAcadWinApp()->GetIDispatch(TRUE);
        // get blocks collection
        IAcadBlocksPtr pIBlks =
            pIAcad->GetActiveDocument()->GetBlocks();
          // count of blocks
        long nCnt =pIBlks->GetCount();
        for(long i=0; i<nCnt; i++)
        {
            _variant_t var(i);
            // each block
            IAcadBlockPtr pIBlk =
                pIBlks->Item(var);
            BSTR str;
            // get block name
            pIBlk->get_Name(&str);
            _bstr_t bstr(str);
            // pop out the block name
            AfxMessageBox(bstr);
            ::SysFreeString(str);
        }
    }
    catch(_com_error& err)
    {
        AfxMessageBox(err.ErrorMessage());
    }
}
  If you want to use the #import generated files that come ObjectARX, do it as the following code shows:
static void test()
{
    try
    {
        // get application
        IDispatch* pDisp =
            acedGetAcadWinApp()->GetIDispatch(TRUE);
        if(!pDisp) _com_issue_error(E_POINTER);
        CComPtr<IAcadApplication> pIAcad;
        pDisp->QueryInterface(IID_IAcadApplication, (void**)&pIAcad);
          // get current document
        CComPtr<IAcadDocument> pIDoc;
        pIAcad->get_ActiveDocument(&pIDoc);
          // get blocks collection
        CComPtr<IAcadBlocks> pIBlks;
        pIDoc->get_Blocks(&pIBlks);
          long blksCnt;
        pIBlks->get_Count(&blksCnt);
        CComPtr<IAcadBlock> pIBlk;
        // iterate each block
        for(long i=0; i<blksCnt; i++)
        {
            _variant_t x(i);
            pIBlks->Item(x, &pIBlk);
            BSTR str;
            pIBlk->get_Name(&str);
            char buf[256];
            buf [0] =0 ;
            if(WideCharToMultiByte (CP_ACP,
                0,
                str,
                -1,
                buf,
                256,
                NULL,
                NULL))
       acutPrintf(_T("\nBlock name %d is: %s"), i, buf);
            ::SysFreeString(str);
        }
    }
    catch(_com_error& err)
    {
        AfxMessageBox(err.ErrorMessage());
    }
}

## 评论

**内容**: Alexander Rivilis said...
Hi, Xiaodong!
As far as I remember calling WideCharToMultiByte was only required for AutoCAD up to version 2006. acutPrintf requires not char *, but wchar_t * since AutoCAD 2007 for %s format.
Reply
03/04/2013 at 01:29 AM

---
