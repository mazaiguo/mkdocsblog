---
title: "Integration of Salesforce.com and AutoCAD WS - Part 5"
date: 2012-05-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - Block
  - COM
description: "In last post, I said I was blocked by a small bug for quite a lot time. In this post, let’s talk about how to debug in force.com. Actually I do not..."
author: Autodesk
---
# Integration of Salesforce.com and AutoCAD WS - Part 5

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/integration-of-salesforcecom-and-autocad-ws-part-5.html

## 文章内容

By Daniel Du
In last post, I said I was blocked by a small bug for quite a lot time. In this post, let’s talk about how to debug in force.com. Actually I do not find a very convenient way to debug Apex code, I cannot set break point and trace the code step by step, so I have to use System.Debug() to write log. If you know a convenient way to debug, please do let me know, it would be really appreciated!
I uses following code to add log to checked whether the correct attached is added to map or not :
//save into a map for latter use
mapAttachment = new Map<String, Attachment>();
for(Attachment item : listAttachment ) { 

  mapAttachment.put(
     String.valueOf(item.Id).trim(),
     item);
  System.Debug('ID=' + item.Id
             + 'Name=' + item.name
             + ' is added to map'); 
}
A convenient way to check log is to use Developer Console. Click Your Name > Developer Console to open. Actually it is concentrated place to write code and debug, can be used as an IDE.
The Developer Console looks like below:
In Logs tab, the log is listed, developer can open one log item to examine the detailed log. It may contains the very detailed log, we can set filter to “USER_DEBUG” to show the log we set.
If you prefer to use Developer Console as IDE to write code, all pages/classed can be accessed from “Repository” tab, we can edit the visual force page to apex classes directly.
Another way to examine the value of object is to use System.Assert(false, object): For example, I add following code in the constructor to example the value of mapAttachment:
System.Assert(false, mapAttachment);
I will get the output as below at runtime for debug:
It helps developer to debug.
Ok, in next post, I will dive into the core part, to transfer DWG attachment to AutoCAD WS storage.
Stay tuned and have fun!
  PS. I just find a very useful video about Developer Console, it introduces many features I don’t know before, please check it out here.

