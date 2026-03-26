---
title: "Read / Write custom drawing properties without opening drawing in AutoCAD"
date: 2014-11-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Database
  - Plugin
description: "In some cases, it might be required to read / write custom properties for AutoCAD drawings without having to open the drawing in AutoCAD. If you al..."
author: Autodesk
---
# Read / Write custom drawing properties without opening drawing in AutoCAD

发布日期: 2014-11-01

原始链接: https://adndevblog.typepad.com/autocad/2014/11/read-write-custom-drawing-properties-without-opening-them-in-autocad.html

## 文章内容

By Balaji Ramamoorthy
In some cases, it might be required to read / write custom properties for AutoCAD drawings without having to open the drawing in AutoCAD. If you already have AutoCAD installed in the system, using accoreconsole.exe provides an easy way to achieve this. Here are the steps :
1) Create a .Net plugin that only references acdbmgd.dll and accoremgd.dll and implement a custom command with this code snippet :
 Document activeDoc = 
     Autodesk.AutoCAD.ApplicationServices.Core.
     Application.DocumentManager.MdiActiveDocument;
 Database db = activeDoc.Database;
 DatabaseSummaryInfoBuilder builder 
                 = new  DatabaseSummaryInfoBuilder();
 builder.Author = "GoCAD" ;
 builder.CustomPropertyTable.Add
                         ("Machine Type" , "Milling" );
 builder.CustomPropertyTable.Add("Model" , "Vertical" );
 builder.CustomPropertyTable.Add("Year" , "2014" );
 db.SummaryInfo = builder.ToDatabaseSummaryInfo();
  2) Create a AutoCAD script file to load the plugin and invoke the custom command. Save the script as a scr file.
 //Script starts here
 ; Load the custom plugin
 (command "_.Netload"  "D:\\\\Temp\\\\Test.dll" )
 ; Run the command
 (command "WriteCustomProp" )
 save
   //Script ends here
  3) Run AccoreConsole.exe found in the AutoCAD 2015 install folder and provide the drawing to which custom properties are to be added.
 accoreconsole.exe /i "D:\\Temp\\Test.dwg"  
                   /s "D:\\Temp\\WriteProp.scr" 
                   /l en-US
  If you do not have AutoCAD installed in the system, it is possible to read the custom properties using the COM API provided by DwgPropX ActiveX control. But this activeX does not provide write access to the properties. You can read about this approach in this blog post :
Access drawing properties outside AutoCAD

## 评论

**内容**: Will Parker said...
Is there any way to read drawing properties without using any autocad api? I want to be able to access this data through the windows command prompt and by the same means as windows explorer is able to access it.
Reply
11/25/2014 at 12:38 PM

---
**内容**: Balaji said in reply to Will Parker...
Hi Will,
Sorry, My apologies for failing to notice your comment to this blog post and the long delay in getting back to you.
Please have a look at the DWG Properties ActiveX control from ADN Utilities. This should provide read-only access to some of the drawing properties even without AutoCAD installed in the system.
This ActiveX can be downloaded as part of ADN Utilites from here :
http://adndevblog.typepad.com/autocad/2012/08/adn-autocad-utilities.html/
Regards,
Balaji
Reply
12/22/2014 at 10:02 PM

---
**内容**: Cado Magenge said...
Excellent ! it is very useful post. Keep it up .
Reply
05/06/2015 at 09:12 PM

---
**内容**: Aarun Poojary said...
Dear Balaji Sir, I am able to add Custom Properties to a Autocad file , but the metadata is not displaying in the field list view on the document explorer page . Can you kindly help.
Reply
12/11/2015 at 05:09 AM

---
**内容**: Aarun Poojary said...
Dear Balaji Sir, I am able to add Custom Properties to a Autocad file , but the metadata is not displaying in the field list view on the document explorer page . Can you kindly help. Would appreciate if the reply is also marked to My Email id is arunsepl@gmail.com as i am not a regular visitor to this page , Thanks in advance. With Regards Aarun Poojary , Mumbai India
Reply 12
Reply
12/11/2015 at 05:11 AM

---
