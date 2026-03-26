---
title: "Non-DWG window in AutoCAD 2015"
date: 2014-05-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - DWG
  - Dimension
description: "AutoCAD 2015 enables the creation of Non-DWG document window. The Non-DWG document window appears as a tab just as any other drawing window."
author: Autodesk
---
# Non-DWG window in AutoCAD 2015

发布日期: 2014-05-01

原始链接: https://adndevblog.typepad.com/autocad/2014/05/non-dwg-window-in-autocad-2015.html

## 文章内容

By Balaji Ramamoorthy
AutoCAD 2015 enables the creation of Non-DWG document window. The Non-DWG document window appears as a tab just as any other drawing window.
In this blog post, I have attached a C++ project to create a Non-DWG document window and demonstrate its usage.
To try it :
1. Build the sample project using Visual Studio 2012 with Platform Toolset v110.
2. Start AutoCAD 2015 and load the arx module.
3. Run "ShowMyWnd" command. This command creates a Non-DWG document window that accepts user input for the dimensions of a chain link as shown here :
                4. Create another drawing and run the "InsertLink" command. This command creates a chain link based on the values provided in the Non-DWG document window.
Now, here is a brief description of the steps to create a Non-DWG document window using C++ :
Step-1. Create a dialog class derived from CDialog. An MFC dialog can be created using the resource view of Visual Studio as usual.
Step-2. Create a custom document class derived from AcRxObject. This class will be used to hold the data that are specific to this document window. 

Step-3. Create a custom document window class derived from AcApDocWindow
- Override the "onCreate" method to instantiate the dialog that is to be shown.
- Override the "onLoad" method to associate the custom document created in step-2 with our document window class
- Override the "onDestroy" method to perform cleanup such as deleting the dialog instance.
- Override the "subRouteMessage" to perform resizing of the dialog when the document window size changes.
Step-4. Create a custom document window manager reactor derived from AcApDocWindowManagerReactor
- Override the "documentWindowActivated" method to keep our custom document updated with the values provided in the dialog.
- Override the "documentWindowCreated" method to get a pointer to our custom document window after its gets created
- Override the "documentWindowDestroyed" method so we know when our custom document window is no longer valid.
In the attached sample, the steps to associate a custom document have been commented. AutoCAD 2015 at present becomes unstable if a custom document is associated with the custom document window. This behavior has been logged in our internal database for our engineering team to analyze. So the attached sample project now stores the document data in a helper class as static variables for the "InsertLink" command to access.
Here is the sample project :
Download NonDwgWindowSample

## 评论

**内容**: Mike Robertson said...
Is this functionality exposed via .NET also?
Reply
05/01/2014 at 04:58 AM

---
**内容**: Balaji said in reply to Mike Robertson...
Hi Mike,
I have created a blog post with a .Net sample
http://adndevblog.typepad.com/autocad/2014/05/non-dwg-window-in-autocad-2015-using-net.html
Regards,
Balaji
Reply
05/01/2014 at 08:42 AM

---
**内容**: Balaji said...
Hi Mike,
Yes, this is also exposed using AutoCAD .Net API using the "DocumentWindowCollection.AddDocumentWindow" method.
Kean's blog demonstrates it usage by loading an uri.
http://through-the-interface.typepad.com/through_the_interface/2014/04/adding-a-web-page-as-a-document-tab-in-autocad-2015-using-net.html
The other variant of the "AddDocumentWindow" can accept a "DocumentWindow". A "WPFDocumentWindow" can be created and used as a document window.
Regards,
Balaji
Reply
05/01/2014 at 05:07 AM

---
**内容**: Stephan Kaiser said...
Very nice! Thanks for providing a C++ sample. I can think of several use cases.
Reply
05/06/2014 at 03:19 AM

---
**内容**: Balaji said in reply to Stephan Kaiser...
Hi Stephan,
Thanks for the update.
I am glad you are finding use cases for this feature.
Regards,
Balaji
Reply
05/06/2014 at 09:14 PM

---
**内容**: digital signature sharepoint said...
A special thanks for this informative post. I definitely learned new stuff here I wasn't aware of !
Reply
03/29/2015 at 06:56 AM

---
**内容**: chris said...
Thanks for the post Balaji.
When I add a new non-DWG window to AutoCAD, I find that the window has to be closed first before exiting AutoCAD. Otherwise the application will hang. I don't believe this has anything to do with your code but do you know why this is happening? I have noticed the same behaviour using the .NET API.
Reply
05/06/2016 at 12:01 PM

---
