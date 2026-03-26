---
title: "Integration of Salesforce.com and AutoCAD WS - Part 2"
date: 2012-05-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
  - Plugin
description: "In last post, I introduced how to setup the browser based “Development Mode Tools” and how to create a helloworld visualforce page. You can get all..."
author: Autodesk
---
# Integration of Salesforce.com and AutoCAD WS - Part 2

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/integration-of-salesforcecom-and-autocad-ws-part-2.html

## 文章内容

By Daniel Du
In last post, I introduced how to setup the browser based “Development Mode Tools” and how to create a helloworld visualforce page. You can get all your job done with browser when developing applications on force.com. At the same time, I also understand some developers prefer to work on a desktop based IDE. Salesforce provides such IDE as well – force.com IDE—which is an Eclipse plugin. If you are familiar with Eclipse, force.com IDE may be a good option for you.
To install force.com IDE, please make sure you have already signed up for a free Developer Edition account, then follow the Force.com IDE installation instructions. Once installed, start up the IDE and select Window > Open Perspective > Other > Force.com to access the main interface of the Force.com IDE. You should see something similar to following screen:
The easiest way to get started is to choose File > New > Force.com Project. You will see the new Force.com Project dialogue, you are recommended to use your force.com account as project name.
You may be wondering: “what is the “Security Token”? OK, when accessing salesforce.com from outside of your company’s trusted networks, you must add a security token to your password to log in to a desktop client, such as Connect for Outlook, Connect Offline, Connect for Office, Connect for Lotus Notes, or the Data Loader, as well as Force.com IDE. New security tokens are automatically sent to you by mail when your salesforce.com password is changed or when you request to reset your security token. If you do not have the token, please visit the Setup > My Personal Information > Reset Security Token page.
Once you created your force.com project, Force.com IDE will download the schema from cloud and make a local copy.
You will see that all meta data of apex classes, pages, layouts, etc are downloaded,
In last post, we introduced to create a visual force page by inputting the page name in address bar and let the error page to create it automatically. If you prefer to use browser, you can also create a new visualforce page by clicking YourName > Setup > Develop > Pages and click “New” button.
In Force.com IDE, it can be done by File > New > Visualforce page, input the label and name and click “Finish” button, force.com IDE will communicate with server, and a new vf page is created on cloud.
Similarly, you can create apex classes in Force.com IDE and start programming. Every time you save your doc, it will be complied and save up to cloud if everything is OK. Please pay attention to the left top, you will be notified if something is wrong, and the page is just saved locally.
You can still use browser to open the visual force page to check whether it works as expected or not, in input the address  .visual.force.com/apex/">.visual.force.com/apex/">.visual.force.com/apex/">https://c.<yourinstance>.visual.force.com/apex/<yourpagename>.
To create an apex class, we choose File(or right click package explorer) > new Apex Class in Force.com IDE. It also can be done in browser, clicking YourName > Setup > Develop > Apex Classes and click “New” button.
  Force.com Apex Code is an object oriented programming language that allows developers to develop on-demand business applications on the Force.com platform. We need to create some visual force pages and some Apex classes to get our job done. I will introduce them in latter parts.
With that we are drawing to the end of this post, in next post, I will introduce how to create more useful visual force page.
Stay tuned and have fun!

