---
title: "VB.NET or C# – a personal perspective"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C#
description: "Kean and I were recently interviewed by Andrew Roe for his Cadalyst series on programming AutoCAD. As part of the discussion (not all of which appe..."
author: Autodesk
---
# VB.NET or C# – a personal perspective

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/vbnet-or-c-a-personal-perspective.html

## 文章内容

By Stephen Preston
Kean and I were recently interviewed by Andrew Roe for his Cadalyst series on programming AutoCAD. As part of the discussion (not all of which appeared in his article), he asked us our opinions on which programming language was best for beginner programmers new to AutoCAD .NET development.
The quick answer to this is that it really doesn’t matter. All .NET programming languages are ‘compiled’ to a common intermediate language (Microsoft’s Common Intermediate Language, or CIL for short). This means that I can use any .NET programming language I like to access the AutoCAD .NET API. I can even mix and match – for example by writing part of my code in C# and extending it in VB.NET. There is a huge range of .NET programming languages to choose from, and (in theory) you can use any of those. However, as for anything in the real world, there are practical considerations.
The most common choice is VB.NET or C# (or F# if you’re a big fan of Kean’s blog ). Factors that will affect your choice between VB.NET and C# include:
Company standards – No point learning VB.NET if your coding standards require everything to be in C#.
Friends and colleagues – Your best programming resource is someone you know who’s willing to spend time answering all your noobish questions. They can help you so much more easily if you’re learning the language they are most familiar with.
Your background – If you’ve already dabbled in VBA or VB6, then VB.NET will be a shallower learning curve. If you’re a C++ programmer, then you’ll likely choose C# (so you can keep your semicolons ).
Code samples – What language are most of the available code samples available in?
My choice of.NET language is slightly unusual considering my background. My first exposure to programming was through being a computer geek as a kid. My parents bought a BBC Micro to help my brother with his Computer Studies homework. My brother used it mostly to play games; I used it to learn BBC BASIC and later FORTRAN. I studied Physics as an undergraduate, which included modules on programming – in Pascal on NeXT boxes. For my post-graduate study, I variously programmed in FORTRAN (on an IBM mainframe), Object Pascal and C on Mac OS 7 – writing simulations to model the results of my plasma physics experiments. Then I got bored one day when the laser in our lab was offline for repairs and read through a teach yourself C++ book. Finally (and embarrassingly since I’d already been using Object Pascal), I understood what Object-Oriented Programming was all about. From there on in it was C++ only until Microsoft launched .NET.
Which is why – of course – when faced with a choice between C# and VB.NET, I chose VB.NET.
My reasoning was simple: If any language complies down to the same CIL code, then it really doesn’t matter which language you choose. All my C++ programmer friends were learning C# and feeling superior because they weren’t VB programmers – so I went for VB.NET to prove my point. (I can be a bit contrary sometimes).
[BTW That’s another factor to consider in your choice of programming languages – some C# programmers still look down their noses at VB.NET. As a VB.NET programmer, you quickly learn to smile knowingly and get on with writing great code ].
That was about eight years ago. (AutoCAD 2005 included our first .NET (preview) API). I still stand by that early decision – I’ve not yet found anything I wanted to do that I couldn’t do in VB.NET. (Hmm - That statement could open up a can of worms ). However, just before talking to Andrew, I’d started dabbling with iOS and Android development. That caused me to answer Andrew’s question slightly differently than I had in the past …
The four factors I list above are still the main issues to consider when starting .NET development. For example, if I were programming Revit, I’d definitely go for C# because there are very few VB.NET samples available. You can translate C# to VB.NET using online translators, such as http://www.developerfusion.com/tools/convert/csharp-to-vb/, but it’s a bit of a pain having to do it for every code sample. There’s a better balance between VB.NET and C# in the AutoCAD .NET world, so the choice there depends more on the other three factors.
But now I’ve added a fifth factor to consider – your future plans.
If you’re happy that you’ll only ever be programming on Windows, and if you have little programming experience (or if you’ve dabbled in VBA or VB6), then VB.NET is an obvious choice for you. After all, BASIC was originally designed as a language for beginners.  If, on the other hand, you have ambitions to join the revolution and try your hand at mobile or cloud computing development, then my recommendation is to accept the steeper learning curve of C# because its going to make it easier to learn the native programming languages for those platforms:
iOS (Apple’s iPhone/iPad operating system) uses Objective-C – like C++, this is a C derivative. (And in my humble opinion and limited experience is an extremely ugly programming language).
Android uses Java – and derives much of its syntax from C/C++.
Java is also extremely widely used for cloud/web programming, and JavaScript is a mainstay of scripts on webpages.
I’ve been particularly enjoying dabbling with Android development in recent weeks. As I’ve been hacking around, I started wondering just how easy it is to convert C# code into Java, so I decided to test by writing an AutoCAD .NET plug-in in C# and then converting it to an Android app. I’ll be writing up my findings in a series of posts, but I’m starting with this article because one thing has become very clear to me as I’ve been playing around:
I’ve struggled the most in this project because my preference for VB.NET has left my C# skills very rusty. The hardest part for me was translating my VB.NET knowledge to C#. Once I’d written the C# code, migrating it to Java was disconcertingly easy - which is why my advice for beginners has now changed.
Just how easy the migration was will be the subject of a future post. For now, feel free to add a comment to stake your position in the great VB/C# debate …

## 评论

**内容**: Veli V. said...
I like to code with VB.NET most of cases but I have to give my only vote to C#.NET because it has better preprocessor directives than VB.NET. There are some cases when you need those directives that C# has. I don´t know the reason why VB.NET compiler doesn´t support those.
And thanks for the very good blog cause it is a timesaver for us. =)
Cheers
Veli V.
Reply
05/23/2012 at 11:38 PM

---
**内容**: Kyle B. said...
Great posting... I just wish you had posted this a couple months ago. I just started working with ObjectARX, having done all my previous code in either Visual Lisp or VBA, I was faced with this decision very recently.
Reply
05/24/2012 at 03:48 AM

---
**内容**: Roland said...
I started years ago with VBA. When AutoCAD introduced .NET I started to learn C#. Now I like C# more than VB. For me it is better to read and it is not really a problem to learn it.
Reply
05/24/2012 at 06:34 AM

---
**内容**: Account Deleted said...
My career in programming began with Russian analog of IBM/370 (EC-1045) - FORTRAN, PL / 1, Assembler.
I'm programming with AutoCAD since 1989: AutoLisp-> ADS-> ADSRX-> ARX-> ObjectARX and a bit of C#. VB / VBA went past me. Perhaps that is why I do not like VB.NET
P.S.: It is incomprehensible why the old topics in blog are closed to commenting. I think this is wrong - if after a certain time will be found inaccuracies or errors in the code or inconsistency the newest versions of AutoCAD will not report it to the author.
Reply
05/24/2012 at 12:26 PM

---
**内容**: Madhukar Moogala said in reply to Account Deleted...
Hi Alexander,
Oops! Looks like Typepad defaults to closing commenting on posts after one month. I've fixed that now - they should now stay open forever.
Cheers,
Stephen
Reply
05/24/2012 at 01:16 PM

---
**内容**: Account Deleted said in reply to Madhukar Moogala...
>>...they should now stay open forever...
That is good news! :-)
Reply
05/24/2012 at 01:37 PM

---
**内容**: David Marshall said...
http://channel9.msdn.com/Series/Windows-Store-apps-for-Absolute-Beginners-with-C-/Part-1-Series-Introduction
Bob Tabor: "While I began with VB, I haven't seen a lot of docs / videos / articles / books using VB for Win8 or other recent technologies. Increasingly, it feels to me *personally* like C# would be a good investment."
Sounds like Bob thinks VB.NET is on the way out.
Reply
05/08/2013 at 02:28 PM

---
**内容**: Carl Richard Dumdum said...
Sir, I want to learn programming in a deeper sense. Please contact me with my email.. thank you.. I need your suggestions or any help.
Reply
11/27/2014 at 05:43 AM

---
**内容**: nini said...
thankyou for your post visit us to see article about anything
Reply
03/10/2023 at 03:58 AM

---
