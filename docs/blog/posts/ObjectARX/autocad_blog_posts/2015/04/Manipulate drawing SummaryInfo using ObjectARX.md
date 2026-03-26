---
title: "Manipulate drawing SummaryInfo using ObjectARX"
date: 2015-04-01
categories:
  - AutoCAD .NET
tags:
  - C++
  - ObjectARX
description: "You may want to update the "Last saved by" and "Revision number" properties and other custom properties associated with the drawing. The AcDbDataba..."
author: Autodesk
---
# Manipulate drawing SummaryInfo using ObjectARX

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/manipulate-drawing-summaryinfo-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
You may want to update the "Last saved by" and "Revision number" properties and other custom properties associated with the drawing. The AcDbDatabaseSummaryInfo class of the ObjectARX SDK will help do that. The equivalent of this class in the AutoCAD .Net API is the "DatabaseSummaryInfo" structure. But unlike the C++ API, some of the properties such as "LastSavedBy" and "RevisionNumber" are read-only in .Net. You can also use the COM API to retrieve and set the properties. This is especially useful if you are driving AutoCAD from an external application or using VBA.
After the "Last saved by" property is changed, it is important to save the database using a different name. If not, the AutoCAD's save command will automatically use the system login name and set the "Last saved by" property.
Here is the ObjectARX C++ code snippet to set the "Last saved by" and "Revision number" properties while retrieving the other properties. 
 Acad::ErrorStatus es;    
 AcDbDatabaseSummaryInfo *pInfo;    
 AcDbDatabase *pCurDb = NULL;    
 ACHAR* info;    
 ACHAR* key;    
 ACHAR* value; 
 int  customQty; 
 int  index;  
 pCurDb = acdbHostApplicationServices()->workingDatabase(); 
   // Get a pointer to the workingDatabase() 
 // summary information  
 es = acdbGetSummaryInfo(pCurDb, pInfo);   
 acutPrintf(L"\\nSummary information for this drawing:" ); 
 es = pInfo->getTitle(info);  
 if (info)
 {   
  acutPrintf(L"\\nTitle = %s" , info);   
 }    
   es = pInfo->getSubject(info);    
 if (info)    
 { 
  acutPrintf(L"\\nSubject matter = %s" , info);   
 }    
   es = pInfo->getAuthor(info);    
 if (info)
 {        
  acutPrintf(L"\\nAutor = %s" , info);    
 }    
   es = pInfo->getKeywords(info);    
 if (info)   
 {    
  acutPrintf(L"\\nKeywords = %s" , info);   
 }   
   es = pInfo->getComments(info);   
 if (info)   
 {       
  acutPrintf(L"\\nComments = %s" , info);    
 }    
   es = pInfo->setLastSavedBy(L"Captain CAD" );    
 es = pInfo->getLastSavedBy(info); 
 acutPrintf(L"\\nLast saved by = %s" , info);   
   es = pInfo->getHyperlinkBase(info);  
 if (info)   
 {
 acutPrintf(L"\\nLink Location = %s" , info);    
 }
   es = pInfo->setRevisionNumber(L"1" ); 
 es = pInfo->getRevisionNumber(info);    
 acutPrintf(L"\\nRevision number = %s" , info);    
 customQty = pInfo->numCustomInfo();    
 if (customQty > 0)    
 {        
  acutPrintf(L"\\nCustom Summary Information:\\n" );        
  acutPrintf(L"\\nKey\\t\\tValue\\n" );        
  for (index = 0; index < customQty; index++)        
  {            
   pInfo->getCustomSummaryInfo(index, key, value);            
   if (key)            
   {               
    acutPrintf(L"\\n%s" , key);            
   }            
   if (value)          
   { 
    acutPrintf(L"\\t\\t%s" , value);
   }
   acdbFree(key); 
   acdbFree(value);
  }    
 }
 else
 {
  acutPrintf(L"\\n\\nDrawing does not contain
   any Custom SummaryInformation");   
 } 
 es = acdbPutSummaryInfo(pInfo);    
 acdbFree(info); 
   pCurDb->saveAs(ACRX_T("D:\\\\Temp\\\\MyTestArx.dwg" ));
  To set the properties using COM API, here is a code snippet :
    oAcadApp.ActiveDocument.Database.SummaryInfo.LastSavedBy = "Autodesk" 
 MsgBox(oAcadApp.ActiveDocument.Database.SummaryInfo.LastSavedBy)
 oAcadApp.ActiveDocument.SaveAs("D:\\Temp\\MyTest.dwg" )

## 评论

**内容**: Mikako Harada said...
Thanks, Balaji!
This is just FYI as a related info. - I learned from the customer that there is a command in the express tool to help with this:
PROPULATE (Express Tool)
http://knowledge.autodesk.com/support/autocad/learn-explore/caas/CloudHelp/cloudhelp/2015/ENU/AutoCAD-Core/files/GUID-BD03320F-3430-4C2F-80A3-AAC1167AF019-htm.html
Reply
05/20/2015 at 08:06 AM

---
**内容**: sushil jawale said in reply to Mikako Harada...
hi,
I want to update the some of the custom properties on the document without opening file in AutoCAD.
but If I open the file using write and no share using readdwgfile I do not see the properties updated.
Please suggest how it could be done to update custom properties on same document using arx
Thanks!
Sushil
Reply
08/02/2016 at 03:40 AM

---
**内容**: Balaji said...
Thanks Mikako
Reply
05/20/2015 at 09:49 PM

---
**内容**: sushil jawale said...
hi,
I want to update the some of the custom properties on the document without opening file in AutoCAD.
but If I open the file using write and no share using readdwgfile I do not see the properties updated.
Please suggest how it could be done to update custom properties on same document using arx
Thanks!
Sushil
Reply
08/02/2016 at 03:39 AM

---
**内容**: Mikako Harada said in reply to sushil jawale...
Hi Sushil,
I'd suggest posting question to AutoCAD Customization forum:
http://forums.autodesk.com/t5/autocad-customization/ct-p/AutoCADTopic1
You can point to this post when you are describing the problem if it helps.
Balaji is no longer with Autodesk. I'm on BIM side now. I don't have brain to help you on this topic. But we have many other people who knows AutoCAD APIs.
Reply
08/02/2016 at 11:09 AM

---
