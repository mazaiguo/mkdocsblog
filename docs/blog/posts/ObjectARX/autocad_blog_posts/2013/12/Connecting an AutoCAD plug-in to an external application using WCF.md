---
title: "Connecting an AutoCAD plug-in to an external application using WCF"
date: 2013-12-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
  - Plugin
description: "We have many references on how to connect an AutoCAD plug-in to an external executable using COM, but as it becomes an antique technology as years ..."
author: Autodesk
---
# Connecting an AutoCAD plug-in to an external application using WCF

发布日期: 2013-12-01

原始链接: https://adndevblog.typepad.com/autocad/2013/12/connecting-an-autocad-plug-in-to-an-external-application-using-wcf.html

## 文章内容

By Philippe Leefsma
We have many references on how to connect an AutoCAD plug-in to an external executable using COM, but as it becomes an antique technology as years are passing I though it would be useful to illustrate how to achieve the same (and potentially much more) using WCF.
The idea is to have a WCF server that is hosted by an AutoCAD .Net plug-in. One or several client executables running on the same machine will be able to connect to that server and exchange data. Eventually the server can also dispatch data send by one client to the other.
To make the thing more fun I created a little chat application where clients can send messages between each other. You will find the complete code attached with the download at the bottom of that blog post. For more details about the implementation, take a look at the initial post I created on our Cloud & Mobile blog:
Inter-process communication using WCF
The AcadServer plug-in is net-loaded in AutoCAD and can start processing requests from the clients:
ADN Pipe Demo.zip

## 评论

**内容**: Taher said...
Hi Philippe Leefsma,
I'm beginner to autocad & .net . I try to make my first program in vb.net2012 I add reference the two dll file (Acdbmgd.dll, Acmgd.dll) and add the following import
Imports Autodesk.AutoCAD.Runtime
Imports Autodesk.AutoCAD.ApplicationServices
Imports Autodesk.AutoCAD.DatabaseServices
Imports Autodesk.AutoCAD.Geometry
It give me message.
(Debugger detected - please close it down and restart!
Window NT users: Please note that having the WinIce/ SoftIce service installed means the you are running a debugger !)

I hope to find a solution to my problem
taherhamdy_76@yahoo.com
Reply
12/30/2013 at 11:02 PM

---
**内容**: Madhukar Moogala said in reply to Taher...
Hi Taher,
I've deleted your numerous comments identical to this. Please refrain from spamming the same question on multiple posts.
As Philippe already mentioned, please post your technical support questions to the AutoCAD .NET Discussion Group and someone there will help you.
Regards,
Stephen
Reply
01/01/2014 at 01:14 PM

---
**内容**: Ben said in reply to Taher...
Hello Taher,
perhaps i shouldn't indulge you here in this particular post. but i was curious: are you using genuine software or pirate software?
regards
Ben
Reply
03/17/2016 at 04:56 PM

---
**内容**: Philippe said...
Hi Taher,
Your question has nothing to do with the topic discussed in that post. You can take a look at my first plug-in if you are starting with the API:
http://usa.autodesk.com/adsk/servlet/index?id=18162650&siteID=123112
In the future please post this kind of question on the forum:
http://forums.autodesk.com/t5/AutoCAD-Customization/ct-p/AutoCADTopic1
Thank you,
Philippe.
Reply
12/31/2013 at 01:01 AM

---
**内容**: Konstantin said...
Hello Philippe,
Is it possible to have the WCF server hosted by an AutoCAD .Net plug-in on one machine and several WCF client executables running on different machines within a LAN or WAN ?
If yes what should be changed in the provided code ?
Best Regards
Konstantin
Reply
01/09/2014 at 08:34 AM

---
**内容**: Philippe Leefsma said in reply to Konstantin...
Hi Konstantin,
Yes it's possible, if you want to use WCF/SOAP then you would need (according to the chart) to use netTcpBinding. I wrote an article on it already:
http://adndevblog.typepad.com/cloud_and_mobile/2012/08/creating-a-cloud-based-viewerpart-iv.html
If you are not familiar with WCF, you may actually want to check the whole series on the same blog:
Creating a cloud based viewer – Part I to X
Cheers,
Philippe.
Reply
01/09/2014 at 08:43 AM

---
**内容**: Konstantin said in reply to Philippe Leefsma...
Hello Philippe,
many thanks, i will go through them...
Regards
Konstantin
Reply
01/10/2014 at 03:57 AM

---
**内容**: Konstantin said...
Hi Phillipe,
i have been working through the current and your 2 articles
Creating a cloud based viewer – Part I
Creating a cloud based viewer – Part II
and everything is setup and running !
I was able to use WCF Server and Clients on different mashines using netTcpBinding.
Fine indeed !
I would like to replace the client application (WCF client) in the current article
by the Client Viewer from "Creating a cloud based viewer – Part II" !
****************
I just want to test transferring a DWG stream from a DWG open in AutoCAD on the server
or just being on the Server disk using the ACADserver plug-in and display it in the Client DWG Viewer.
****************
I don't have any clue how to transfer and display a DWG Stream in the WCF Client DWG Viewer !
How can i view DWG in a WCF Client Viewer ?
Could you please describe how to proceed or extend the current article showing
how to transfer a DWG Stream from the WCF ACADserver to a WCF Client DWG Viewer ?
Many thanks in advance .
Best Regards
Konstantin
Reply
01/17/2014 at 03:32 AM

---
**内容**: Philippe Leefsma said in reply to Konstantin...
You can find numerous resources over the internet that illustrates how to transfer a stream using WCF.
Here is one for example:
http://www.codeproject.com/Articles/166763/WCF-Streaming-Upload-Download-Files-Over-HTTP
To display a dwg the solutions are pretty limited. You can use either AutoCAD, your own viewer based on RealDWG or the AcCtrl control as illustrated below:
http://through-the-interface.typepad.com/through_the_interface/2008/03/embedding-autoc.html
Reply
01/20/2014 at 05:33 AM

---
**内容**: Konstantin said in reply to Philippe Leefsma...
OK ! Thanks Philippe
I'll go through these materials...
Reply
01/22/2014 at 01:12 AM

---
