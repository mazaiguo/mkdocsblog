---
title: "AutoCAD.NET API is now on Nuget.org"
date: 2014-12-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - NuGet
description: "The long waited enhancement is rolled out , I’m personally very happy that our API package is available on Nuget ."
author: Autodesk
---
# AutoCAD.NET API is now on Nuget.org

发布日期: 2014-12-01

原始链接: https://adndevblog.typepad.com/autocad/2014/12/autocadnet-api-is-now-on-nugetorg.html

## 文章内容

By Madhukar Moogala
The long waited enhancement is rolled out , I’m personally very happy that our API package is available on Nuget .
So what is big deal about Nuget ?
NuGet is the package manager for the Microsoft development platform including .NET. The NuGet client tools provide the ability to produce and consume packages. The NuGet Gallery is the central package repository used by all package authors and consumers.Nuget
How it is going to help us ?
Very simply ,now you need not download sdk and  manually add references to your project ,after installing package from nuget search available with in Visual Studio IDE ,it copies the library files to your solution and automatically updates your project (add references, change config files, etc.). If you remove a package, NuGet reverses whatever changes it made so that no clutter is left.
  How should I install a package from Nuget ?
Go to Tools\Library Package Manager \ Manage Nuget Packages
Search for AutoCAD .NET API

## 评论

**内容**: Norman said...
If one uses VS2013, the NuGet Package Manager dialog box is not able to find the AutoCAD.NET package. One has to use NuGet command line to install in ("install-package AutoCAD.NET"). With VS2012, though, the package can be found in NuGet Package Manager dialog box.
After package is installed, all the referenced DLLs are correctly set with "COPY LOCAL" being "False", except for the reference to acdbmgdbreb.dll: its "COPY LOCAL" is set to "TRUE", which is wrong.
Reply
12/11/2014 at 10:27 AM

---
**内容**: Madhukar Moogala said...
Hi Norman , thanks for commenting , yes copy local should be set to false , I have reported this to developer.
If one uses VS2013, the NuGet Package Manager dialog box is not able to find the AutoCAD.NET package
Do you mean you were not able to see Manage Nuget Packages in Nuget Package Manager ?
I checked on Vs2013 , I can find package and installed too.
Reply
12/11/2014 at 09:01 PM

---
**内容**: Mike said...
I also don't see it in the nuget package manager in 2013. Screenshot here:
http://imgur.com/a5FzA4V
If I extend the search from "AutoCAD" to "AutoCAD .NET API" it simply returns every hit with .Net or API in the name, none of which seem to be AutoCAD related.
Reply
12/29/2014 at 01:18 PM

---
**内容**: Madhukar Moogala said in reply to Mike...
Hi Mike ,
Happy new year :) , sorry for delayed reply , I just came from 15 Day vacation :),
I can find AutoCAD .NET on NuGet on VS2013 too , I'm using VS2013 Professional, you check on this image
http://a360.co/1wPywJY
Reply
01/05/2015 at 02:20 AM

---
**内容**: Maxence said in reply to Mike...
@mike You need to add nuget.org to the sources
Reply
04/07/2015 at 10:28 AM

---
**内容**: Alex Fielder said...
Hi Madhukar,
I don't suppose it's possible for the ADN team to do the same with the Inventor .NET API?
Thanks,
Alex.
Reply
01/15/2015 at 08:29 AM

---
**内容**: bshanwar said...
I am using VS2012, and when trying to download the package I got this error

The element 'metadata' in namespace 'http://schemas.microsoft.com/packaging/2011/08/nuspec.xsd' has invalid child element 'developmentDependency' in namespace 'http://schemas.microsoft.com/packaging/2011/08/nuspec.xsd'. List of possible elements expected: 'releaseNotes, frameworkAssemblies, tags, copyright, summary, iconUrl, dependencies, references, language, description, title' in namespace 'http://schemas.microsoft.com/packaging/2011/08/nuspec.xsd'.

Reply
01/17/2015 at 03:46 AM

---
**内容**: Андрей Бушман said...
I have looked the newest AutoCAD.Net (Version 21.0.1). It doesn't set `CopyLocal` to `false` for each its assembly. It is bad. Also current naming creates the problem of forced updating. I.e. by default the package will update the assemblies to newer AutoCAD versions even if you don't want to use newer AutoCAD version for your project. Therefore user are to use `-Version` key and be very attentive. So, current naming of the package is bad too... Also, Autodesk didn't create the packages for older AutoCAD versions (2009-2014 are interesting for me too).
Please, test your packages before you will publish them on NuGet feed. To solve the problems mentioned by me I created own packages here: https://www.nuget.org/profiles/Bush
Reply
07/21/2016 at 01:17 PM

---
