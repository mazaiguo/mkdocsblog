---
title: "Programmatically Creating SaveAs Dialog"
date: 2015-11-01
categories:
  - AutoCAD
tags:
  - Plot
description: "This blog work is result of a query resulted from customer, in this blog we ‘ll see a simple implementation of save drawing as dialog."
author: Autodesk
---
# Programmatically Creating SaveAs Dialog

发布日期: 2015-11-01

原始链接: https://adndevblog.typepad.com/autocad/2015/11/programmatically-creating-saveas-dialog.html

## 文章内容

By Madhukar Moogala
This blog work is result of a query resulted from customer, in this blog we ‘ll see a simple implementation of save drawing as dialog.
Though we have acedGetNavDialog, we don’t have much control over combo list specifying all drawing formats.
void SaveDialog()
{
     acutPrintf(L"TEST\n");

     AcApDocument *pDoc = acDocManager->mdiActiveDocument();

     acDocManager->lockDocument(pDoc);
    
     AcDbDatabase *pDB = pDoc->database();
     AcDbBlockTable *pBT = NULL;
     ErrorStatus es = pDB->getBlockTable(pBT,AcDb::kForRead);
     AcDbBlockTableRecord *pBTR =NULL;

     pBT->getAt(ACDB_MODEL_SPACE,pBTR,AcDb::kForWrite);
    

     ::AcDbLine *pLine = new AcDbLine(AcGePoint3d(0,0,0), AcGePoint3d(10,10,0));
     pBTR->appendAcDbEntity(pLine);
     pLine->close();

     pBT->close();
     pBTR->close();

     acDocManager->unlockDocument(pDoc);
  // Create an Save Dialog
  CFileDialog fileDlg(FALSE, NULL,NULL,
     OFN_FILEMUSTEXIST | OFN_HIDEREADONLY |OFN_EXTENSIONDIFFERENT, NULL);
  DWORD dwSelItem;
  /*Setting Dialog Comboxitems to Index, it will help to get aware of user choice*/
  fileDlg.m_pOFN->nFilterIndex = 1;
  /*A buffer containing pairs of null-terminated filter strings. 
  The last string in the buffer must be terminated by two NULL characters. */
  fileDlg.m_pOFN->lpstrFilter = L"AutoCAD 2013 Drawing(*.dwg)\0*.DWG\0
     AutoCAD 2012 Drawing(*.dwg)\0*.DWG\0
     AutoCAD 2010 Drawing(*.dwg)\0*.DWG\0
     AutoCAD 2008 Drawing(*.dwg)\0*.DWG\0
     AutoCAD 2007 Drawing(*.dwg)\0*.DWG\0
     AutoCAD 2007 DXF(*.dxf)\0*.DXF\0\0";


   // Display the file dialog. When user clicks OK, fileDlg.DoModal() 
   // returns IDOK.
   if(fileDlg.DoModal() == IDOK)
   {
     
    CString pathName = fileDlg.GetPathName();
   /*User selection choice*/
 dwSelItem = fileDlg.m_pOFN->nFilterIndex;

 switch(dwSelItem)
 {
 case 1:
  acutPrintf(L"AutoCAD 2013 Drawing(*.dwg) is selected");
 
  /*Write custom save fromat logic*/
  break;
 case 2:
  acutPrintf(L"AutoCAD 2012 Drawing(*.dwg) is selected");
  break;
 case 3:
  acutPrintf(L"AutoCAD 2010 Drawing(*.dwg) is selected");
  break;
 case 4:
  acutPrintf(L"AutoCAD 2008 Drawing(*.dwg) is selected");
  break;
 case 5:
  acutPrintf(L"AutoCAD 2007 Drawing(*.dwg) is selected");
  break;
 case 6:
  acutPrintf(L"AutoCAD 2007 DXF(*.dxf) is selected");
  break;
 default:
  acutPrintf(L"Nothin");
  break;
 }

  acutPrintf(L"\nFile name returned: %s\n", pathName);
     pDoc->database()->saveAs(pathName, true);
     
   }
     
   acedPostCommandPrompt();


}

