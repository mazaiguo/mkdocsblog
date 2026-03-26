---
title: "ReadDwgFile fail on files open in another AutoCAD"
date: 2013-01-01
categories:
  - Forge
tags:
  - AutoCAD
  - DWG
  - Database
  - Forge
description: "When we want to open a DWG file that h is already open in another session of AutoCAD, any call to AcDbDatabase::readDwgFile() fails with the error ..."
author: Autodesk
---
# ReadDwgFile fail on files open in another AutoCAD

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/readdwgfile-fail-on-files-open-in-another-autocad.html

## 文章内容

By Augusto Goncalves
When we want to open a DWG file that h is already open in another session of AutoCAD, any call to AcDbDatabase::readDwgFile() fails with the error eFileAccessErr.
Basically we cannot open a DWG files in read-only state.
The problem is that readDwgFile() reads not the whole DWG file into memory. readDwgFile() opens the file and reads only some header information. Every time when we access an entity/object/symboltable... in the drawing file, AutoCAD reads another part of the DWG file. When an other instance of AutoCAD saves during your read process the drawing, it can happen that your application/AutoCAD gets an invalid file pointer.
The workaround is to copy the DWG file to a temporary location if you get eFileAccessErr on readDwgFile() and to try again to open the temporary DWG file. The following code does this.
NOTE: Don't forget that you are working on a temporary copy of the drawing. Any changes you are doing on the drawing will be lost because you have to delete the temp file.
void loadDwgReadOnly()
{
  // TODO: add your code here
  BOOL isReadOnly = FALSE;
  ACHAR dwgFileName[MAX_PATH];
  resbuf *rb = acutNewRb(RTSTR);
  if (RTNORM != acedGetFileD(L"Select File to read",
    NULL, L"dwg", 0, rb))
  {  
    acutRelRb(rb);
    return;
  }
  _tcscpy(dwgFileName, rb->resval.rstring);
  acutRelRb(rb);
  Acad::ErrorStatus es;
  AcDbDatabase db(Adesk::kFalse);
  if ((Acad::eOk != (es = db.readDwgFile(dwgFileName))))
  {   
    if (Acad::eFileAccessErr == es) 
    {     
      //   
      // Copy the file and try again    
      //       
      ACHAR tempPath[MAX_PATH], tempName[MAX_PATH];  
      // Get a temporary file name   
      GetTempPath(MAX_PATH, tempPath);
      GetTempFileNameW(tempPath, L"dwg", 0, tempName);
      if (!CopyFile(dwgFileName, tempName, FALSE))   
        return; 
      if ((Acad::eOk != (es = db.readDwgFile(tempName)))) 
        return;    
      isReadOnly = TRUE;   
      _tcscpy(dwgFileName, tempName); 
    }
  }
  // Now you can query information from the readed dwg file
  // ****
  // ****
  // ****
      // Delete the temp file
  if (isReadOnly)
  {  
    DeleteFile(dwgFileName);
  }
}

## 评论

**内容**: Rolando Hijar said...
Hi Augusto. I'm trying to open files to change some XREFs inside and save it with the same name. My problem is that sometimes a file is open and my program crash. How can ask if the file is open by someone to leave it without crash?
Reply
02/01/2013 at 06:10 AM

---
**内容**: Augusto Goncalves said in reply to Rolando Hijar...
Hi,
Is a file is already opened, then it should be a .dwl/.dwl2 file with same name at the same folder. One way can be check is the file exists.
Regards,
Augusto Goncalves
Reply
03/06/2013 at 12:12 PM

---
**内容**: Duy said...
Hello,
I think, the right solution in this case like below:
We should check whether these file is open or not, if it was opened, then we should use document iterator from Arx sdk, then get database from AcApDocument, once we have database , the job is done.
Best regards.
Reply
06/24/2019 at 09:12 PM

---
**内容**: Duy said...
I meant we can use AcApDocumentIterator to check whether this file is opened or not, if it open, we can get databse from AcApDocument.
Reply
06/24/2019 at 09:15 PM

---
