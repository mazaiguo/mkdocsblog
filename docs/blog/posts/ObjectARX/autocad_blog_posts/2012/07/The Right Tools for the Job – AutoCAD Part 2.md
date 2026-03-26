---
title: "The Right Tools for the Job – AutoCAD Part 2"
date: 2012-07-01
categories:
  - AutoLISP
tags:
  - API
  - AutoCAD
  - AutoLISP
  - CUI
  - VBA
description: "Leading on from Part 1 - what else should you also think about before you get started with programming AutoCAD…?"
author: Autodesk
---
# The Right Tools for the Job – AutoCAD Part 2

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/the-right-tools-for-the-job-autocad-part-2.html

## 文章内容

by Fenton Webb
Leading on from Part 1 - what else should you also think about before you get started with programming AutoCAD…?
Your specific performance requirements is one thing (and I’ll get to those details soon, I promise), but I there are other considerations too when deciding on the right AutoCAD programming language to adopt.
One thing that springs to mind, especially for beginners, is the learning curve and also the cost of start up. If you are just starting out, then you will find that the time it takes you to learn the API is actually a substantial investment for any customization programming work. I think you have to carefully consider each API’s learning curve and subsequent start up costs, as well as its feature sets, before you commit to any.
I think that VBA is probably the best suited for a pure beginner because it works the same way as the Macro functionality in the Microsoft Office tools, just with an AutoCAD Object model instead. That means that almost anyone who has played with Macros in Excel will be able to get something programmed inside of AutoCAD.
AutoLISP/ Visual LISP is a little more complex to learn in my opinion because it’s so unique but it was adapted to work with AutoCAD so it integrates really nicely.
Both VBA and Visual LISP are built into AutoCAD, both are composed using built in (free) development IDE’s and as I just mentioned both are easy to learn and use, VBA being the easiest. That tells me that these languages are perfect if:
You want to just get things done quickly and effectively
You can be a master of computer science and still make really good use of VBA and LISP inside of AutoCAD
Short learning curve means you get results quicker
You are on a tight budget
No need to buy Visual Studio
All the tools you need come free with AutoCAD
Short learning curve means more time making real money
You are a beginner programmer
Short learning curve means results come quicker and you realize the concepts quicker also
Coming in 3rd place for learning curve is .NET. .NET streamlines very complex programming through lots of really cool language and Object Model development, from Microsoft. In my opinion, it is the best programming toolset out there by a mile. The integration between the all of the latest programming technologies is just breath taking-ly cool; it’s just so nice to program with. I have to say though, if you are going to utilize the native AutoCAD .NET API, which wraps the underlying ObjectARX API making it very similar, then you may find the learning curve rather steep. The API is rather low level and even though it’s .NET it can be very easy to crash if you don’t do things right. That said, one great feature of .NET is its COM Interop capabilities – this allows you to easily utilize the VBA Object Model from VB.NET (or C# if you so desire) making VB.NET almost as easy to learn as I mentioned VBA is above. One extra point about .NET that in order to developer with it, you need Visual Studio, and the professional license costs $$$’s.
Finally, ObjectARX coming in last on my learning and cost curve. ObjectARX utilizes the C++ language, which is still very popular in the programming world and is still moving forward with the likes of Microsoft and Visual Studio. The code is compiled into native machine code, making it super fast, very capable but very difficult to work with compared to .NET. It’s low level accessibility is its power, but also its pain. If you don’t know C++, I recommend that you don’t bother trying to learn ObjectARX as it takes real experience to work with and that is going to cost you time, effort, and money to get up and running with it – instead I recommend you use .NET. That said, if your application requires real performance and some really special functionality, then ObjectARX is what you need, for sure.
Read Part 3 here

## 评论

**内容**: Kerry Brown said...

Fenton,
I have difficulty reconsiling your recommendation for beginners to learn VBA with your companys dropping support of the product.
Are AutoDesk going to bring back VBA support ??
Regards
Kerry
Reply
07/13/2012 at 05:36 PM

---
**内容**: RenderMan said...
I too find it interesting the recommendation for something dead or dying through attrition (VBA), or something repeatedly, and intentionally neglected (Visual LISP/VLIDE) despite the large outcry for enhancement, when they (Autodesk) so actively continue to relegate more and more of the applications in which we work to .NET/ARX.
Visual Studio 2010 Express is also free... One just needs to also obtain, and install:
The ObjectARX SDK for their version
And, one of the many 'wizards' that allow one to launch AutoCAD and effectively debug (i.e., breakpoints, etc.)
The wizard is not necessary, provided one knows to edit the .[cs/vb]proj.user file accordingly, etc. but still.
~RM
Reply
07/14/2012 at 01:19 PM

---
**内容**: elliottpd said...
VBA...really?
Reply
07/14/2012 at 02:16 PM

---
**内容**: Loic Jourdan said...
Hi Fenton,
In my mind, cpp should be considered more often than you suggest (vs .net):
- You cannot target mac os using .net
- Building a simple application (beginner) using ObjectArx is not such a big deal
- Managing objects states is in my mind safer using oarx than using .net. for instance, disposing a transaction (C#) is quite easy to forget, it's easy for a beginner to get messed up with exception handling when code became more complex. On the other hand, cpp code now has clear-and-efficient classes such as AcDbSmartObjectPointer.
- Calling unexposed methods using P-Invoke is quite difficult for beginners
to summarize, I more or less agree with you but I would be much more moderate, especially as c++ become easier (c++11) and still as fast. I would say that people may not fear c++!
Anyway, thank you for these posts, they are very helpful for all who want to join us coding with acad.
Loic
(please excuse my english, it is often quite bad)
Reply
07/16/2012 at 04:34 AM

---
**内容**: Fenton Webb said...
The C++ comment is very valid, thanks Loic. If you do go for C++ then really, the world is in your hands because you can do pretty much anything with AutoCAD.
I totally understand all of your points on VBA.
The bottom line is though - VBA is still available for AutoCAD and in my opinion the cheapest and easiest (for a complete beginner) to start programming AutoCAD with.
Also in my opinion, as a complete beginner, starting with VBA is the easiest way to get into AutoCAD VB.NET, which should be your ultimate goal.
Please keep your comments coming!
Next post is all about Performance, and I think are you going to be surprised at some of the results!
Reply
07/16/2012 at 09:45 AM

---
**内容**: Gilles Chanteau said...
I do not agree about VBA.
IMO, AutoLISP is the best way for beginers, it's the natural continuation of autoCAD customization after scripts and command macros and the learning curve may be very fast with the help of a very large community.
If the goal is .NET, I'd say start with C# which encourage better programming practices and the strictness required with bigger applications.
I don't think VB is more easy then C#, I just would say it's more laxist...
I know there're very good codes written in VB(A), but I also know VBA allows (encourage) some 'not so good' programming practices (using of global (module) variables, hiding exceptions with On Error Resume Next, mixing static typing, implicit casts and late binding, ...). And VB.NET keeps many of these behaviors available so that the worst VBA codes can be migrated to VB.NET as they are.
So, let die VBA, start playing with LISP, and if you really enjoyed it, then, have fun with F# !
Just my 2 cents...
Reply
07/16/2012 at 01:34 PM

---
**内容**: Ben said...
Hi Fenton and readers
Times have changed. now you can get excellent functionality through Visual Studio community edition for free - which is better than the express edition of old. The community edition provides a very high level of functionality to do code almost anything. and if you want to full suite of tools you can go for the pro version too.
Reply
01/26/2016 at 01:55 PM

---
**内容**: Gabriel said...
Hi,
I learned Acad programming in c# and i am still consider myself as beginner. You can't imagine how much time i lost every time i wanted to debug! For a beginner i think its really important to start with something IDE like VBA
Reply
10/13/2016 at 12:17 PM

---
