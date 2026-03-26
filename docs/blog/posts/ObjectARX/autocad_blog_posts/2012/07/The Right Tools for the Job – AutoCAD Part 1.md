---
title: "The Right Tools for the Job – AutoCAD Part 1"
date: 2012-07-01
categories:
  - AutoLISP
tags:
  - API
  - AutoCAD
  - AutoLISP
description: "Recently, Stephen posted this great blog entry on Performance – perception versus reality and then asked me if I could tell you all the tricks I ha..."
author: Autodesk
---
# The Right Tools for the Job – AutoCAD Part 1

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/the-right-tools-for-the-job-autocad-part-1.html

## 文章内容

by Fenton Webb
Recently, Stephen posted this great blog entry on Performance – perception versus reality and then asked me if I could tell you all the tricks I have learnt over the years to produce the fastest, leanest AutoCAD code on the planet!!  
In fact, as Stephen mentioned in his post, I presented this exact topic at Autodesk University so I’ll present the topics inside of that presentation here in a few different blog entry parts.
So for Part 1, way before I start talking about the performance topic, let’s start with a quick look at which APIs are currently available inside of AutoCAD, along with what I consider to be their Pros and Cons…
First we have:
AutoLISP/Visual LISP… For those that don’t know, LISP is a scripting language inside of AutoCAD
Pros
Quick and Easy to write code with
There is an integrated Development IDE accessed via the “VLIDE” command
Lots of Sample Code
Can Access all parts of the DWG file
Runs inside of Menus/CUI Commands
This is extremely useful in my opinion
Integrated Supported Language
It’s not going away because the AutoCAD development team use LISP in their test harnesses
Automatic memory management
Works same every year
Not affected by product changes and updates
You can compile LISP modules
thus making your source code secure
Cons
Limited ongoing investment from Autodesk
We are focusing more on the newer languages these days as they provide the most bang for your buck
Limited/Outdated UI
All we have is the aging DCL (Dialog Control Language)
Not easy to read and/or maintain the code
obviously up for discussion, but in my opinion, it’s true.
Not Object Oriented
Slow Performance
This is really task dependent. Some operations can be extremely fast though, for instance, creating objects (due to most of the work being done internally by AutoCAD)
Limited Interoperability
I would say that LISP’s interoperability capabilities aren’t bad though, you can very easily interoperate with ObjectARX and .NET, and visa versa using the acedEvaluateLisp() function.
Not a skill you can really use outside of the AutoCAD world
Next we have:
VBA…  Microsoft VBA Macros inside of AutoCAD, similar to Outlook Macros
Pros
Quick and Easy to write code with
Like LISP, there is an integrated Development IDE which can be accessed via the command “VBAIDE”
Lots of Sample Code
Object Based
Easy and Nice UI APIs
Works same every year
Generally, not affected by product changes and updates
Code Saved with DWG file
Automatic Memory Management
VBA skills are recognized outside of Autodesk
Cons
Limited ongoing investment from Autodesk
Slow Performance
task dependent, of course
Bad Source code security
password encrypted macros can easily be hacked
64bit version runs Out of Process
Tricky and extremely slow
Limited Access to AutoCAD
No built in Interoperability
Now onto:
ObjectARX – our awesome C++ API
Pros
Totally Interoperable!
Mix and match APIs
Not easy to implement though
Lots of sample code
Object Oriented
Very powerful
the most powerful API we have
Low level
gain access to almost anything going on inside of AutoCAD
Fastest API we have
Secure
Compiled machine code
Advanced technology features
still being updated by the likes of Microsoft
Full Access to AutoCAD
Powerful UI API capabilities
Recognized inside of AutoCAD world as a top notch programming skill
Recognized outside of AutoCAD world too
Cons
Pro software engineers needed to write it
Expensive!
No built in Memory Management
UI capabilities are powerful, but error prone and difficult
Powerful, Low level – is this really an advantage???
Its power can be its downfall
Tied to platform 32bit and 64bit
Binary break every 3 years
Is affected by product changes and updates
AutoCAD .NET – our even more awesome AutoCAD .NET API
Pros
Quick and Easy to write code with
VB.NET provides an easy way to port over from VBA
Easy and Nice UI APIs
Built into the latest Visual Studio tools
Totally interoperable
and easy with it
Lots of sample code
Not tied to platform
as long as you steer away from ObjectARX and COM interoperability
Object Oriented
Very powerful
Low Level, but at the same time High level!
Very Fast
but not compared with ObjectARX
Latest and most Advanced programming language on Windows
New features being added all the time
Automatic memory management
Recognized inside of AutoCAD world as a very good programming skill
Recognized outside of AutoCAD world too
Cons
Code Security can be an issue, be careful
Difficult for LISP and VBA people to migrate to pure .NET
Using VB.NET via COM Interop makes life easy though
Cannot unload DLLs very easily while AutoCAD is running
Read The Right Tools for the Job - Part 2

## 评论

**内容**: jeff said...
I think it's a bit cheeky calling out ObjectARX for breaking every three years when .NET breaks more often.
(given the changing set of assemblies to link against, and the hacks required to run .NET 2.0 modules in a .NET 4.0 environment)
And when you say "cannot unload DLLs very easily", you mean "cannot unload DLLs at all", don't you?
Reply
07/16/2012 at 09:35 PM

---
**内容**: Anonymoose said...
Ok, so what about the performance ? :D
Reply
07/17/2012 at 01:14 AM

---
**内容**: Anonymoose said...
What scripting APIs are available on both Windows and MAC AutoCAD ?
Reply
07/17/2012 at 01:15 AM

---
**内容**: Smith011 said...
objectarx: Lots of sample code? where?
Reply
02/04/2020 at 10:14 PM

---
**内容**: Megha Pendse said...
Thanks for sharing information. Good Initiative. 
Top Employment Consultants in Mumbai for jobs
Reply
04/19/2021 at 01:20 AM

---
