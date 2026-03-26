---
title: "Create multi sheet PDF from ARX using DSD"
date: 2016-01-01
categories:
  - AutoCAD .NET
tags:
  - C++
  - PDF
description: "We already have a blog post on doing this from .NET, but it could take a bit of time to convert the code to ARX, so here it is."
author: Autodesk
---
# Create multi sheet PDF from ARX using DSD

发布日期: 2016-01-01

原始链接: https://adndevblog.typepad.com/autocad/2016/01/create-multi-sheet-pdf-from-arx-using-dsd.html

## 文章内容

By Adam Nagy
We already have a blog post on doing this from .NET, but it could take a bit of time to convert the code to ARX, so here it is.
It's not doing exactly the same but close enough :)
You'll have to include acplmisc.h and make sure your project links to AcPublish_crx.lib
static void plot (AcDbDatabase *pDb)
{
  CString pdfPath = "C:\\temp\\pdf\\myPDF.pdf";
  CString deviceName =  L"DWG To PDF.pc3";
  Acad::ErrorStatus es = Acad::eOk;

  const TCHAR *docName;
  es = pDb->getFilename(docName);   

  AcDbLayoutManager *layoutManager =
    acdbHostApplicationServices()->layoutManager();
  AcDbDictionary *layoutDict = NULL;
  es = pDb->getLayoutDictionary(layoutDict, AcDb::OpenMode::kForRead);

  // Start collecting info for the DSD data
  AcPlDSDEntries dsdEntries;
  AcDbDictionaryIterator *layoutIterator = layoutDict->newIterator();

  // If we only want to plot paper spaces and not the model layout
  AcDbObjectId msId = acdbSymUtil()->blockModelSpaceId(pDb);

  for (; layoutIterator && !layoutIterator->done(); layoutIterator->next())
  {
    AcDbObjectPointer<AcDbLayout> layout(
      layoutIterator->objectId(), AcDb::OpenMode::kForRead);

    if (layout->getBlockTableRecordId() == msId)
      continue;

    const ACHAR *layoutName;
    layout->getLayoutName(layoutName);

    AcPlDSDEntry dsdEntry;
    dsdEntry.setLayout(layoutName);
    dsdEntry.setDwgName(docName);
    dsdEntry.setTitle(layoutName);
    dsdEntries.append(dsdEntry);     
  }

  delete layoutIterator;
  layoutDict->close();

  AcPlDSDData dsdData;
  dsdData.setDSDEntries(dsdEntries);  

  dsdData.setProjectPath(L"c:\\temp\\pdf\\");
  dsdData.setLogFilePath(L"c:\\temp\\pdf\\logdwf.log");
  dsdData.setSheetType(AcPlDSDEntry::SheetType::kMultiPDF);
  dsdData.setNoOfCopies(1);
  dsdData.setDestinationName(pdfPath);
  dsdData.setPromptForDwfName(false);
  dsdData.setSheetSetName(L"PublisherSet");

  AcPlPlotConfig *plotConfig;
  acplPlotConfigManager->setCurrentConfig(plotConfig, deviceName);    

  // We need this for acplPublishExecute
  acedArxLoad(L"AcPublish.arx");

  acplPublishExecute(dsdData, plotConfig, false);
}

## 评论

**内容**: sudarshan d. said...
what does setCurrentConfig() method do?
and why to use devicename as a parameter to this method ?
Please explain it ?
Reply
02/02/2016 at 10:16 PM

---
**内容**: Adam Nagy said in reply to sudarshan d....
Creates the configuration object that needs to be passed to acplPublishExecute()
Reply
02/03/2016 at 03:26 AM

---
**内容**: Sudarshan d. said...
this is very slow process as acplpublishExecute metod working slowly.
please give the solution over it
Reply
02/03/2016 at 02:57 AM

---
**内容**: Adam Nagy said in reply to Sudarshan d....
This is what the publishing through the UI is using too. Maybe try setting the BACKGROUNDPLOT to 0 to speed things up - if you have not done it already.
Reply
02/03/2016 at 03:27 AM

---
**内容**: sudarshan d. said...
thank you.
Reply
02/05/2016 at 09:09 PM

---
**内容**: zhou said...
hello,i using this samp example code as a test,but can't pubulish pdf, where I am doing wrong? thank you
Reply
07/24/2017 at 08:50 PM

---
**内容**: Adam Nagy said in reply to zhou...
Without any info it's difficult to say what the problem could be.
The best would be if you asked this question on the AutoCAD API / ObjectARX forum and provide as much info as possible:
https://forums.autodesk.com/t5/objectarx/bd-p/34
Thank you
Reply
07/25/2017 at 01:30 AM

---
