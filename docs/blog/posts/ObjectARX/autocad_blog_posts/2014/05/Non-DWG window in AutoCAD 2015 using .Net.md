---
title: "Non-DWG window in AutoCAD 2015 using .Net"
date: 2014-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C#
  - DWG
description: "AutoCAD 2015 enables the creation of Non-DWG document window. The Non-DWG document window appears as a tab just as any other drawing window."
author: Autodesk
---
# Non-DWG window in AutoCAD 2015 using .Net

发布日期: 2014-05-01

原始链接: https://adndevblog.typepad.com/autocad/2014/05/non-dwg-window-in-autocad-2015-using-net.html

## 文章内容

By Balaji Ramamoorthy
AutoCAD 2015 enables the creation of Non-DWG document window. The Non-DWG document window appears as a tab just as any other drawing window.
In this blog post, I have attached a C# project to create a Non-DWG document window and demonstrate its usage.
To try it :
1. Build the sample project using Visual Studio 2012 with .Net framework set to 4.5.
2. Start AutoCAD 2015 and netload the dll.
3. Run "MyWnd" command. This command creates a Non-DWG document window that accepts user input for the radius of a smiley.
                  4. Create another drawing and run the "InsertSmiley" command. This command creates a smiley based on the radius value provided in the Non-DWG document window.
Now, here is a brief description of the steps to create a Non-DWG document window using .Net :
Step-1. Create a WPF usercontrol and customize it as you would create it usually.
Step-2. Create a custom document class. This class will be used to hold the data that are specific to this document window.
Step-3. Create a custom document window class derived from WPFDocumentWindow.
- Override the "OnCreate" method to know when the document window is created.
- Override the "OnLoad" method to associate the custom document with our document window class
- Override the "OnActivate" method to know when the document window gets activated.
Step-4. Create an instance of the custom document window class and add it to the DocumentWindowCollection using Application.DocumentWindowCollection.AddDocumentWindow.
In the attached sample, the steps to associate a custom document have been commented. AutoCAD 2015 at present becomes unstable if a custom document is associated with the custom document window. This behavior has been logged in our internal database for our engineering team to analyze.
So the attached sample project retrieves the document data by directly accessing the usercontrol for the "InsertSmiley" command to access.
Here is the sample project :
Download NonDwgDocWindow_Net

## 评论

**内容**: Steve Hill said...
Hi Balaji,
What would be the purpose of the Non Dwg window for CAD? I see a user could input some parameters here and then I assume this would auto draw an object in a new drawing - Is that the purpose of this? I am understanding this correctly?
Steve
Reply
05/01/2014 at 09:32 AM

---
**内容**: Madhukar Moogala said in reply to Steve Hill...
A good example is what AutoCAD uses it for now.
Reply
05/15/2014 at 07:38 PM

---
**内容**: Balaji said...
Hi Steve,
The sample project accepts an input in a Non-Dwg window only to demonstrate the access of the document associated with the Non-DWG document window. Accepting inputs is not the sole purpose of the feature.
I would leave it to the application developers to identify how this feature can help improve their end-user experience.
The possibilities are many - For example,
- A Non-DWG document window could show a table of standard pipe fittings that the user can quickly refer while working on a drawing.
- Display custom graphics to show a Finite element analysis results
- Play a short video tutorial in a Non-DWG document window which may help with the current task that the user is trying.
etc.
My thoughts may be quite limited and application developers can better identify its use in their domain / workflow.
Regards,
Balaji
Reply
05/01/2014 at 10:03 PM

---
**内容**: Web Development Company said...
Web Development Company
ASEUM INFOTECH is a global software services and IT management company. We pour our love into the things we build, take pride in the quality of the code, and measures success by customer satisfaction and happiness. Quality,Reliability and Safety.
Go to:>> http://www.aseuminfotech.com/
Reply
07/01/2014 at 01:54 AM

---
**内容**: Oscar Quintero said...
Hi Balaji,
How can you know that a Document object is a non-DWG Document using .NET?
Thanks.
Reply
02/16/2015 at 07:00 PM

---
**内容**: Balaji said...
Hi Oscar,
A document retrieved from any document window when successfully typecast as "Document" would be a regular drawing window.
Non-DWG document windows associate custom objects as their document and those cannot be derived from "Document". The "Document" class is a sealed class, so it is not possible to inherit from it. For such cases, the typecast would fail.
Also, please ensure a null check is included for the document retrieved from a document window. Non-DWG document windows can return null if there is no document associated with them.
Regards,
Balaji
Reply
02/17/2015 at 10:54 PM

---
**内容**: Ben said in reply to Balaji...
Hi Balaji,
Have you tried this example in AutoCAD 2016? I've encountered a problem when STARTMODE = 1, and you close AutoCAD with the window still open. AutoCAD hangs and i have to kill acad.exe process from the task manager. When STARTMODE = 0 the problem goes away.
Is this a known issue?
Regards
Ben
Reply
04/26/2016 at 09:53 PM

---
