---
title: "Why does the app.config file not work for my AutoCAD .NET DLL?"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Plugin
description: "I'm developing a .NET add-in (dll) for AutoCAD."
author: Autodesk
---
# Why does the app.config file not work for my AutoCAD .NET DLL?

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/why-does-the-appconfig-file-not-work-for-my-autocad-net-dll.html

## 文章内容

By Marat Mirgaleev
Issue
I'm developing a .NET add-in (dll) for AutoCAD.
I'd like to store some settings for the dll, for this purpose, I've added an app.config file to my project.
When the project builds, the config file is copied to mydll.dll.config in the output folder. 
But when I netload the dll in AutoCAD, the dll can't get the settings from the config file. Why?
Solution
The cause of the problem is that the application config file is associated with the exe file, not a dll:
      http://msdn.microsoft.com/en-us/library/ms229689.aspx
Thus, try to place the settings into the AutoCAD's config file (depending on the AutoCAD’s version, it can be \Program Files\Autodesk\AutoCAD 2013\acad.exe.config or \Program Files\AutoCAD 2010\acad.exe.config).

## 评论

**内容**: Ed Jobe said...
It works for me if you add settings from the Settings tab of your project's Properties.
Reply
07/20/2012 at 09:31 AM

---
**内容**: Diego said in reply to Ed Jobe...
How did you read this information?
Thank you.
Reply
01/07/2015 at 08:02 AM

---
**内容**: BJHuffine said...
You're right that the .Net configuration file framework sees the host exe for the dll, but there are ways around this rather than using the acad.exe.config. If you just used the acad.exe.config for all your development, things can get pretty messy. You can still use the Visual Studio settings, or the older 2.0 config appSettings elements, or even create your own custom elements. You can even create an auxiliary config and merge it with your application config. And yes all these can be retrieved from your dll. I taught on this at AU last year. You can look for Jason Huffine as the speaker in the AU Online Classes by going to au.autodesk.com. You can also click on this link http://au.autodesk.com/?nd=class&session_id=9611, but keep in mind you have to sign on to see the information. It's no big deal to register though. In this I give plenty of examples in the document and I also give plenty of sample code with ReadMe.txt files to explain how to setup. If you listen to the presentation, forgive me. That was my first time talking at AU and I was a bit nervous :-). Hope that helps.
Reply
07/31/2012 at 06:12 AM

---
**内容**: Michael J. Smith said...
Thanks for the great resource Mr. Huffine!!!!
Reply
02/15/2013 at 06:43 AM

---
**内容**: Ben said...
Bloody brilliant Jason!
Reply
03/21/2016 at 04:07 AM

---
**内容**: Ben said...
Bad news,
I added some config settings by going to Visual studio ---> Settings tab of my project's Properties. I then batch built my dll and took the release version of my dll onto another computer. *****ERROR****** could not find database at: C:\incorrectpath\etc ........oops: I'll have to change my connection string in the config file, which should be located on this new computer (as opposed to the computer i developed the plugin on). the connection string should be in the config file so i should just change it to point to where the database exists on this new computer.
The config file should be called acad.exe.config. So I go to my Program files folder and I find acad.exe.config, and i click on the XML file: but there is no connection string.txt copied in there! Where then is this fabled connection string located? Acad is obviously storing it somewhere because the Acad error reports that the connection string could not be found at that particular path - which means that the connection string is being held in an XML file somewhere.
The question is: Where? Becauase i really need to point it to the new location of the database.
Reply
03/21/2016 at 04:19 AM

---
**内容**: Besanttech1 said...
Thanks for sharing informative post. QTP Training in Chennai
Reply
04/20/2016 at 11:39 PM

---
