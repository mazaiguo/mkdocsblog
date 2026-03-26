---
title: "Actual width and height of a text string"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - Database
description: "To determine the actual width of the text in an AcDbMText entity there is no direct way to get it from the AcDbMText methods. Instead, use the AcGi..."
author: Autodesk
---
# Actual width and height of a text string

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/actual-width-and-height-of-a-text-string.html

## 文章内容

By Balaji Ramamoorthy
To determine the actual width of the text in an AcDbMText entity there is no direct way to get it from the AcDbMText methods. Instead, use the AcGiTextStyle that has a method called extents() in order to obtain the actual width.
The following code samples in ObjectARX and AutoCAD .Net API demonstrate the way to obtain the string width from a user input string. AutoCAD .Net API does not expose the "fromAcDbTextStyle" method that is required to obtain the AcGiTextStyle and so a p/invoke is used.
Here is the ObjectARX code :
Acad::ErrorStatus es;
AcDbDatabase *pDb
      = acdbHostApplicationServices()->workingDatabase();
  ACHAR str[132];   
int rt = acedGetString(true, L"\nEnter a string: ", str); 
if(rt != RTNORM)  
{ 
    acutPrintf(L"\nInvalid input, try again.");  
    return;   
}   
AcGiTextStyle iStyle;
AcDbTextStyleTable* pTable = NULL;   
AcDbTextStyleTableRecord* pRecord = NULL;  
try
{  
    pDb->getTextStyleTable(pTable, AcDb::kForRead);
    const ACHAR styleName[] = L"STANDARD"; 
    es = pTable->getAt(styleName, pRecord, AcDb::kForRead);
    es = fromAcDbTextStyle(iStyle, pRecord->objectId());  
    pRecord->close();       
    pTable->close();  
} 
catch(const Acad::ErrorStatus es) 
{   
    acutPrintf(L"\nError: %s", acadErrorStatusText(es));   
    pRecord->close();  
    pTable->close();   
} 
AcGePoint2d pt = iStyle.extents (
                                    str,
                                    Adesk::kFalse,
                                    _tcslen(str),
                                    Adesk::kTrue
                                ); 
// get the width   
acutPrintf(L"\nText string width is: \t<%f>.", pt.x);
// get the height too 
acutPrintf(L"\nText string height is: \t<%f>.", pt.y);
Here is the AutoCAD .Net equivalent of the code
// To get the mangled name use dumpbin.exe. For ex :
// dumpbin.exe -headers "C:\ObjectARX 2013\lib-x64\acdb19.lib" > c:\Temp\acdb19.txt
// Open the generated acdb19.txt to find the signature
[DllImport
(
"acdb19.dll",
CharSet = CharSet.Unicode,
CallingConvention = CallingConvention.Cdecl,
EntryPoint =
"?fromAcDbTextStyle@@YA?AW4ErrorStatus@Acad@@AEAVAcGiTextStyle@@AEBVAcDbObjectId@@@Z")
]
private static extern
Autodesk.AutoCAD.Runtime.ErrorStatus
    fromAcDbTextStyle(System.IntPtr style, ref ObjectId id);
  [CommandMethod("TextStringWidth")]
public void TextStrWidthMethod()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptResult pr = ed.GetString("\nEnter a string: ");
    if (pr.Status != PromptStatus.OK)
        return;
      String textStyleName = "Standard";
    ObjectId textStyleId = ObjectId.Null;
    double width = 0.0, height = 0.0;
    using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        TextStyleTable textStyleTable = tr.GetObject
                                        (
                                            db.TextStyleTableId,
                                            OpenMode.ForRead
                                        ) as TextStyleTable;
          if (textStyleTable.Has(textStyleName))
        {
            textStyleId = textStyleTable[textStyleName];
            Autodesk.AutoCAD.GraphicsInterface.TextStyle iStyle
                = new Autodesk.AutoCAD.GraphicsInterface.TextStyle();
              if (fromAcDbTextStyle
                    (
                        iStyle.UnmanagedObject,
                        ref textStyleId
                    ) == Autodesk.AutoCAD.Runtime.ErrorStatus.OK
               )
            {
                Extents2d extents = iStyle.ExtentsBox
                                            (
                                                pr.StringResult,
                                                false,
                                                true,
                                                null
                                            );
                width  = extents.MaxPoint.X - extents.MinPoint.X;
                height = extents.MaxPoint.Y - extents.MinPoint.Y;
                  ed.WriteMessage(
                    String.Format("\nWidth - {0}\nHeight - {1}",
                                    width,
                                    height
                                 )
                               );
            }
        }
        tr.Commit();
    }
}

## 评论

**内容**: Nick G. said...
You are wright, there is no direct way to get it from the AcDbMText methods. BUT, there is a way to get it from parent class :):):). I don't think that you have to use different functions for getting extents for texts and, for example, polylines. So, the other variant is:
Acad::ErrorStatus getBoundingBox_forCurrentUCS(AcDbObjectId eId, AcGePoint3d &minPt, AcGePoint3d &maxPt, bool resptsInUCS)
{
Acad::ErrorStatus es;
AcDbExtents ext;
AcGeMatrix3d ucsMat;
AcDbEntity * pCopy;
AcDbObjectPointer pEnt(eId,AcDb::kForRead);
acedGetCurrentUCS(ucsMat);
ucsMat.invert();
if ((es = pEnt.openStatus()) != Acad::eOk) return es;
if ((es = pEnt->getTransformedCopy(ucsMat,(AcDbEntity *&)pCopy)) != Acad::eOk) return es;
es = pCopy->getGeomExtents(ext);
delete pCopy;
minPt = ext.minPoint();
maxPt = ext.maxPoint();
if (!resptsInUCS)
{
acdbUcs2Wcs(asDblArray(minPt), asDblArray(minPt), false);
acdbUcs2Wcs(asDblArray(maxPt), asDblArray(maxPt), false);
}
return es;
}
I use this variant more than 3 years. It works fine for me. And I have not to think about object type at all.
Reply
05/20/2012 at 11:40 PM

---
**内容**: Balaji said...
Hi Nick,
The code snippet that you have shared does get the extents of an MText, but that will also include any empty spaces that is part of the MText. The post is about getting the size of only the text content which is not always the same as the extents of the MText.
Regards,
Balaji
Reply
05/21/2012 at 04:03 PM

---
**内容**: Nick G. said...
Hi, Balaji,
But your code doesn't work with MText at all :) It just tells us width and height of user input string without spaces before and after text data (CString::Trim function :):):)) for textstyle STANDARD.
If you really want to know MText's width/height you have to use AcDbMText::explodeFragments function and find width/height for all of mtext's parts, and collect max and min values for output. It's quite hard job, but you'll get the right result.
Reply
05/22/2012 at 01:58 AM

---
**内容**: Anonymoose said in reply to Nick G....
explodeFragments() will not always work correctly because it doesn't account for embedded formatting within MTEXT.
Reply
06/03/2012 at 02:26 AM

---
**内容**: Anonymoose said...
For P/Invoke on an instance method of a C++ class, the CallingConvention.ThisCall should be used.
Reply
06/03/2012 at 02:29 AM

---
**内容**: ku281 said...
why not use actualHeight and actualWidth ?
Reply
08/31/2012 at 02:37 AM

---
**内容**: Hanauer said...
Works well if TextSize has the same value TextHeight. What better way to fix this?
Reply
11/07/2013 at 02:22 AM

---
