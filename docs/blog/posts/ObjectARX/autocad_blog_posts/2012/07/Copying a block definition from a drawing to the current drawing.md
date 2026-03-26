---
title: "Copying a block definition from a drawing to the current drawing"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "I'm trying to copy a block definition from one drawing to the current drawing using wblock method but the it’s returning “eFileInternalErr” error. ..."
author: Autodesk
---
# Copying a block definition from a drawing to the current drawing

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/copying-a-block-definition-from-a-drawing-to-the-current-drawing.html

## 文章内容

By Philippe Leefsma
Q:
I'm trying to copy a block definition from one drawing to the current drawing using wblock method but the it’s returning “eFileInternalErr” error. What am I doing wrong?
A:
The wblock function is meant for writing out database contents. What you are trying to do is the opposite, i.e. reading the contents of an external file into the current database. You should be using the insert function for this.
The code snippet below shows how to use one of the overloaded insert functions to copy a block definition from an external file to the current database:
void AdskCopyBlockDef()
{
        struct resbuf *rb;
        TCHAR *fname;
        AcDbObjectId blockId;
        rb = acutNewRb(RTSTR);
        Acad::ErrorStatus es;
          acedGetFileD(
            L"Pick drawing containing block def", NULL, _T("dwg"), 0, rb);
        if(acutNewString(rb->resval.rstring, fname) != Acad::eOk )
        {
                acutPrintf(L"\nString memory allocation failed");
                acutRelRb(rb);
                return;
        }
          acutRelRb(rb);
          AcDbDatabase *pSourceDb = new AcDbDatabase(Adesk::kFalse);
        pSourceDb->readDwgFile(fname);
          TCHAR SourceBlockdefName[132];
        acedGetString(
            0, L"Enter block def. name in source DWG: ", SourceBlockdefName);
          TCHAR DestBlockdefName[132];
        acedGetString(
            0, L"Enter destination block def. name: ", DestBlockdefName);
          //Get current database 
        AcDbDatabase *pCurDb =
            acdbHostApplicationServices()->workingDatabase();
          //Insert the chosen block definition
        es = pCurDb->insert(
            blockId, SourceBlockdefName, DestBlockdefName, pSourceDb); 
        if (es != Acad::eOk)
        {
                acutPrintf(_T("\nBlock Def copy  failed. Error: %d"), es);
                return;
        }
          acutDelString(fname);
}

