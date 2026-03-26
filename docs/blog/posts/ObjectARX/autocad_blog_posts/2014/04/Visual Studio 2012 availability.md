---
title: "Visual Studio 2012 availability"
date: 2014-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - ObjectARX
description: "As explained in other blog posts both here and on Kean Walmsley's excellent blog (and of course in the ObjectARX 2015 documentation), AutoCAD 2015 ..."
author: Autodesk
---
# Visual Studio 2012 availability

发布日期: 2014-04-01

原始链接: https://adndevblog.typepad.com/autocad/2014/04/visual-studio-2012-availability.html

## 文章内容

By Stephen Preston
As explained in other blog posts both here and on Kean Walmsley's excellent blog (and of course in the ObjectARX 2015 documentation), AutoCAD 2015 is not binary (API) compatible with previous AutoCAD versions. This means that the Visual Studio version required to build your plug-ins has also changed. What this actually means to you depends on which API you're using.
For .NET they key requirement is .NET Framework 4.5. Both Visual Studio 2012 and 2013 support .NET Framework 4.5, so you should be able to use whichever of those two IDEs you prefer. Many .NET developers will likely go for Visual Studio 2013 because of the new 64-bit edit-and-continue feature (which is available for .NET debugging only - not native C++).
Requirements for ObjectARX (native C++) developers are a little more stringent. Because an OjectARX plug-in is a C++ DLL, it has to be compiled using the same Visual C++ compiler version as AutoCAD itself. This means that you must build your ObjectARX plug-ins using the C++ compiler that ships with Visual Studio 2012 (update 4). If you have Visual Studio 2013 installed as well, then you can use that IDE - but you must still install Visual Studio 2012 (update 4) and target the correct C++ compiler using the Platform Toolset feature.
Why is AutoCAD built using Visual Studio 2012 instead of Visual Studio 2013? Quite simply because Visual Studio 2013 was released by Microsoft too late in our development cycle to make the switch. (AutoCAD is a complex beastie, and its not trivial to convert such a large codebase to a new compiler).
This has led to a few questions to our ADN team about how to obtain a copy of Visual Studio 2012 - which is the reason for this blog post. I asked one of the Microsoft team who manages our Autodesk corporate account for a definitive statement on Visual Studio 2012 availability, which I'm posting below verbatim. Remember as you read it that this is written from a US perspective, so prices are in US dollars and programs mentioned may differ in other countries. Contact your local Microsoft reseller for full information on your local situation:
>>>
Options to acquire VS 2012
Due to the release of VS 2013 many customers need to still acquire VS 2012 for compiler compatibility.
We are currently offering an upgrade price for customers who purchased VS 2012 to VS 2013 but there is no upgrade available for older products like VS 2010.
While you can target the VS 2012 tool set in VS 2013 by setting this up in the project properties, you must already have VS 2012 to do this.
Volume License customers can purchase VS 2013 and download VS 2012 from their Volume License site.
Any customer that own VS 2013 with MSDN can download and use VS 2012.
For large customers with Volume License agreements this is probably not an issue.  Prices are approx. $450 for VS Pro license only and approx. $400/yr for VS Pro with MSDN
For smaller customers here are their choices:
If the customer does less than 2M/yr and has been in business less than 3 years they can sign up for our BizSpark program and acquire as much VS with MSDN as they need for free.  To sign up customers just need to go to www.microsoft.com/bizspark.
Customers customer can buy VS Pro with MSDN on Open Licensing (not a Volume licensing program but provides some discounts) for approx. $900/yr
Customers can purchase VS Pro with MSDN directly from Microsoft for approx. $1200/yr
Customers can acquire VS Pro 2012 box copy from sites like eBay for approx. $500
<<<
Update 4/24/14:
Following a smallish thread on this in the Twittersphere, I've updated the text above to bold an important sentence about the source of the quoted information - to make that more obvious. I'll also take this opportunity to draw your attention to the Disclaimer contained in the 'About this blog' page (link at the top of this page - just below the banner).

## 评论

**内容**: Adarsh said...
I have a AutoCAD plugins(ObjectARX) written in C++ using Visual studio 2008 32 bit and its is using 32 bit ObjectARX 2012. I am trying to migrate the same plug in to 64 bit using Visual Studio 2014 (64bit) which shoudld be using 64 ObjectARX 2014.
I am getting 300 plus Linker errors ..Some are repeated..Could any one please advise me on how to resolve these errors..
I have given few errors for your reference:
1.mismatch detected for '_MSC_VER': value '1600' doesn't match value '1700' in test.obj
2.unresolved external symbol "__declspec(dllimport) public: bool __cdecl AcRxClass::isDerivedFrom(class AcRxClass const *)const " (__imp_?isDerivedFrom@AcRxClass@@QEBA_NPEBV1@@Z)
3.error LNK2001: unresolved external symbol acedEntSel
I went thorogh all the existing posts, unfortunately i did not get relevant answer for the issue i am facing.
Reply
02/24/2015 at 01:42 PM

---
