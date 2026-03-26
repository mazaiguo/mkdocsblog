---
title: "Disabled event handlers"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Plugin
description: "A post on the AutoCAD .NET forum the other day reminded me of an issue I wasted a lot of time debugging when I was developing my DigSigStamp Plugin..."
author: Autodesk
---
# Disabled event handlers

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/disabled-event-handlers.html

## 文章内容

By Stephen Preston
A post on the AutoCAD .NET forum the other day reminded me of an issue I wasted a lot of time debugging when I was developing my DigSigStamp Plugin of the Month. Everything was working fine until Kean cleaned up my code ready for posting to the Labs website. Then my event handlers would suddenly stop being called the second time my code ran.
It turned out that the code cleanup had introduced a small bug in my event handler that was causing an exception to be thrown - which I wasn't catching. (Slap my wrist for shoddy error handling technique:-). This led to a conversation with Albert Szilvasy - the Architect for the AutoCAD .NET API - who explained slowly and patiently to me that letting a managed exception pass up to AutoCAD from your event handler was a really silly thing to do. Make sure you handle exceptions thrown in your event handler in the event handler to stop them bubbling up to AutoCAD. (Of course, its good practice to always handle any exceptions you can handle in all the code you write).
So if your event handlers suddenly stop working, go to Debug -> Exceptions and set Visual Studio to stop when exceptions are thrown. It might just show you your 'smoking gun'.

