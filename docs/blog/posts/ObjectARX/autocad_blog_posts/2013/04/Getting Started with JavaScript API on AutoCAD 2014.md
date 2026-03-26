---
title: "Getting Started with JavaScript API on AutoCAD 2014"
date: 2013-04-01
categories:
  - AutoCAD .NET
tags:
  - API
  - AutoCAD
  - JavaScript
description: "As you may have seen already, AutoCAD 2014 is coming with a brand new JavaScript API that will allow a new wave of programmers to interact with it."
author: Autodesk
---
# Getting Started with JavaScript API on AutoCAD 2014

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/getting-started-with-javascript-api-on-autocad-2014.html

## 文章内容

By Philippe Leefsma
As you may have seen already, AutoCAD 2014 is coming with a brand new JavaScript API that will allow a new wave of programmers to interact with it.
Whether you are an experienced web developer or a complete newbie in that area, this DevTv will take you through the steps required to get started programming AutoCAD in JavaScript. A previous experience with one of the existing AutoCAD API, such as ObjectARX or .Net is however a plus.
Here are the topics I cover during the presentation:
I. Introduction to JavaScript
II. JavaScript API in AutoCAD
III. Extending AutoCAD JavaScript API
You will also find the samples that I am demo-ing as part of the attached material below. Note: Firefox or Chrome are recommended browsers if you are playing the video using the html link, IE may behave strangely.
Download AutoCAD_2014_Getting_started_with_JavaScript_API

## 评论

**内容**: Jeff Evans said...
Hi, the video is very interesting. As for the API document mentioned in the video, I took a look at http://www.autocadws.com/jsapi/v1/docs/Acad_Application.html. An very interesting thing is that classes in the document have no details, just a constructor, such as "Acad.Vector2d".
Without member methods, how could we use them? Could you explain this?
Reply
01/02/2014 at 02:33 PM

---
**内容**: Philippe said in reply to Jeff Evans...
Hi Jeff,
Thanks for your interest in the JavaScript API. Make sure you scroll down the page, so the documentation link you mentioned does have a description of the properties for each object. Talking about Acad.Vector2d, here is what I can see:
Name: x
Type: Number
Description: Returns the X property value
Condition: Read-write
Name: y
Type: Number
Description: Returns the Y property value
Condition: Read-write
I hope it helps,
Philippe.
Reply
01/03/2014 at 06:16 AM

---
**内容**: Jeff Evans said in reply to Philippe...
Thank you very much, Philippe.
Take the Vector2d as the example, I know that there are X and Y properties. However, there is no methods, like rotation, dotProduct, crossProduct etc, which are available in ARX's AcGeVector2d documentation.
Thanks.
Reply
01/03/2014 at 08:26 AM

---
**内容**: Philippe Leefsma said in reply to Jeff Evans...
The 2014 version of the JavaScript API has to be considered as a "tech-preview". The real v1.0 should be released in the next version of AutoCAD.
It is however in no point the equivalent or a replacement for the powerful ARX API.
Acad.Vector2d has no methods, it's simply a structure holding X,Y coordinates. If needed, methods should be implemented on your own.
To get an idea about what is doable at the moment using JS, take a look at the samples coming along, they are pretty exhaustive in term of functionality. You can also extend the JS API using .Net or ARX also as illustrated in that material.
I hope it clarifies thing a bit.
Reply
01/03/2014 at 08:55 AM

---
**内容**: Jeff Evans said in reply to Philippe Leefsma...
Thanks!
Reply
01/04/2014 at 05:38 AM

---
**内容**: Иван Цукев said...
Hi,
In your demo video you use "adnjsdemo" to load the html files.
Is this a separate app that we can download from somewhere? Or is there an alternative way to load the html file?
If I understand the help files correctly, webload loads only JavaScript files.
Reply
03/28/2014 at 03:42 AM

---
**内容**: Philippe said...
Hi, everything is included in the package. ADNJSDEMO is a custom command created by a .Net plug-in. You need to use custom code to load html files, you are correct webload loads only js.
Reply
03/28/2014 at 10:09 AM

---
**内容**: Иван Цукев said in reply to Philippe...
Thank you for your clarification.
I found a file called JavascriptLoader.dll in the package and I assumed it is something similar to yout ADNJSDEMO command, but NETLOAD returns error on load: "Cannot load assembly. Error details: System.BadImageFormatException...."
Is there any way to create a HTML5 palette without having to learn and compile C# code?
Reply
04/08/2014 at 07:10 AM

---
**内容**: Philippe said in reply to Иван Цукев...
You are getting that error most likely because the dll is compiled against another version of the SDK than the AutoCAD version you are using. Unfortunately the only way at the moment to display a custom html page in a palette is to load it using custom .Net code (C# or VB.Net). We have resources that can help you getting started with AutoCAD.Net programming:
http://usa.autodesk.com/adsk/servlet/index?id=18162650&siteID=123112
Reply
04/09/2014 at 10:53 PM

---
**内容**: George Endrulat said...
Does anyone have a compiled ADNJSDEMO, or whatever lib contains it, or just anything that can point me in the right direction to obtaining it?
Reply
05/30/2014 at 06:03 AM

---
**内容**: Philippe Leefsma said in reply to George Endrulat...
Hi George, the complete source code is provided in the link, what is holding you back to build it yourself?
Reply
06/04/2014 at 04:05 AM

---
**内容**: Бакыт Оморов said...
Hi, the article is very interesting.
I'm a designer (AutoCAD user) i can programming on JS, but i dont know ObjectARX C# .NET VB.net C++ etc.
Could you briefly describe how can I create a command as ADNJSdemo?
I think it will be very interesting and very useful for people like me.
We hope for your help... Thanks!
Reply
03/19/2015 at 10:28 PM

---
**内容**: Balaji said in reply to Бакыт Оморов...
Hello,
The ADNJSDemo is available in the sample code and you can compile it using Visual Studio. Express edition of Visual Studio will also do.
This tutorial will help you get started with the AutoCAD .Net API :
http://usa.autodesk.com/adsk/servlet/index?siteID=123112&id=18162650
Regards,
Balaji
Reply
03/20/2015 at 02:13 AM

---
**内容**: Бакыт Оморов said in reply to Balaji...
Hello Balaji.
Thank you very much!
Now everything clicked into place.
Reply
04/06/2015 at 04:10 AM

---
**内容**: oba said in reply to Бакыт Оморов...
In addition,
The following article is very useful for create a command as ADNJSdemo:
http://through-the-interface.typepad.com/through_the_interface/2013/03/implementing-an-autocad-palette-using-html5-and-javascript.html
Reply
05/13/2015 at 04:38 AM

---
**内容**: Jose Antonio Mateos said...
Is there any function I could use to get the points from a polyline?
I thought that once your select one Entity Id (like a Polyline) you could get info like its vertex and so on.
I use your ADNJSDEMO script to load my HTML and I only need to be able to click on every Entity in the DWG and store the vertex of each polyline into the database.
Is there any example I could use?
Reply
03/18/2016 at 12:14 PM

---
**内容**: Philippe Leefsma said...
I don't think you can do this from the JavaScript API, you would need to use the C++ or .Net API inside AutoCAD to achieve that. Getting the vertices from .Net is fairly straightforward: http://through-the-interface.typepad.com/through_the_interface/2007/04/iterating_throu.html
You could load a custom .Net dll in AutoCAD that expose a toolkit of features and invoke that from js. There is an example in that material that illustrates calling .net from js.
Hope that helps
Philippe.
Reply
03/18/2016 at 01:47 PM

---
**内容**: Rudolffo Lemos said...
Hi Philippe,
I note on my application that the acwebbrowser.exe process is left running after i remove it from palletset. I run your example ADNJSDEMO and the same problem happened when i call it more than one time. Its a Bug ? Do you know how can i fix it?
Regards,
Rudolffo
Reply
08/30/2016 at 12:17 PM

---
**内容**: Philippe said in reply to Rudolffo Lemos...
Here is the feedback from a colleague about that:
"This issue can happen with older versions of the AcWebBrowser when it gets in a hung state, or if the UI frame is still active. Is the host palette set really shutdown, or just hidden? Did you dispose it yet?"
Hope that helps
Philippe.
Reply
08/31/2016 at 08:17 PM

---
**内容**: Rudolffo Lemos said in reply to Philippe...
Thanks Philippe for yours feedback. Some aditional information.
Product name Autodesk Browser Components
Company name Autodesk
File description Chromium host executable
Internal name acwebbrowser.exe
Original filename acwebbrowser.exe
Legal copyright Copyright (C) 2013, Autodesk
Product version 2.0.0.0
File version 2.0.0.0
Basically the code is:
_ps = new PaletteSet("", new Guid("229E43DB-E76F-48F9-849A-CC8D726DF257"));
_ps.Style = ...
...
_ps.Visible = false;
_ps.Add(objLabel, uri); // process created.
_ps.Remove(0);
_ps.Visible = true;
I re-use this palette and show an other URI. I do this because i want to keep the palette position.
Reply
09/01/2016 at 07:21 AM

---
**内容**: Athanasius said...
Hi,
I'm having some issues to get AcHTML running. For now I've created the ACHTML.dll file with Visual Studio 2012, 4.5 .NET. Running it with AutoCAD 2016.
I can load the .dll into AutoCAD and I can also open the html file with the adnjsdemo command, as i.e. the DBReactors.html. From there on the window opens in autocad, but I cannot Add Listeners or anything else. Also tried all the other html examples. Do I still have to add a javascript loader or anything else? It seems, that the html file cannot call the .js files.
Many thanks in advance,
Athanasius
Reply
02/21/2017 at 02:02 PM

---
**内容**: Athanasius said in reply to Athanasius...
Maybe this helps to come closer to the solution. Starting AutoCAD I get the following errors:
AutoCAD menu utilities loaded.*Cancel*
Command: *Cancel*
_RIBBON
*Cancel*
COMMANDLINE
Layer
*Cancel*
JavaScript Unknown command "JAVASCRIPT". Press F1 for help.
Demo
Unknown command "DEMO". Press F1 for help.
Reply
02/21/2017 at 02:34 PM

---
**内容**: Athanasius said in reply to Athanasius...
Slowly answering my own questions... I had to change the Autodesk.AutoCAD.js to

Probably that's due to AutoCAD 2016. However I think I still need to change parts in the .js File, because I cannot get the interaction right between the AutoCad objects and the .html file. Any ideas about that?
Reply
02/22/2017 at 04:58 AM

---
**内容**: Athanasius said in reply to Athanasius...
src="https://www.autocadws.com/jsapi/v2/Autodesk.AutoCAD.js"
Reply
02/22/2017 at 04:59 AM

---
**内容**: Бакыт Оморов said...
I think they have suspended support. It was not a successful attempt to introduce JS to the Autocad
Reply
05/17/2018 at 03:27 AM

---
