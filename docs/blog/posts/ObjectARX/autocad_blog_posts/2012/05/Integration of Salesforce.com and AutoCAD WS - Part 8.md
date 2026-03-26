---
title: "Integration of Salesforce.com and AutoCAD WS - Part 8"
date: 2012-05-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
description: "Until last post, we have already implemented of salesforce.com and AutoCAD WS. We need to pass the case Id to the visual force page, the URL is sim..."
author: Autodesk
---
# Integration of Salesforce.com and AutoCAD WS - Part 8

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/integration-of-salesforcecom-and-autocad-ws-part-8.html

## 文章内容

By Daniel Du
Until last post, we have already implemented of salesforce.com and AutoCAD WS. We need to pass the case Id to the visual force page, the URL is similar like : https://c.na12.visual.force.com/apex/OpeninAutocadWS?id=500U0000001yRc4
In this post, I would introduce how to integrate this visual force page to our case layout, so that we do not need to input the case ID manually.
Refer to Your Name > Setup > App Setup > Customize > Cases > Page Layouts,  Edit “Case layout”.
select “VisualForce Pages ”, all visual force pages applying to case will show up, drag the one we created “ OpenInAutocadWS” to somewhere below, you can get a WYSIWYG interface.  Click “Quick Save”  or “Save” when you are done.
Here is what I did, When you open one case from salesforce.com, you will see the visual force page is embedded in case layout.
So far we are finishing this serials of post. It is just a prototype and many stuffs need to be done to make it more practical. Anyway, it is really a good experiences to investigate those two cloud based applications. If you have any suggestions to make it better, please do let me know.
Have fun !

