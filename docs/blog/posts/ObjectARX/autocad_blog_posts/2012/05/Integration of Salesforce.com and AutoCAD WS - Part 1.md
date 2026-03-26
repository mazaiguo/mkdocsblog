---
title: "Integration of Salesforce.com and AutoCAD WS - Part 1"
date: 2012-05-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
  - DWG
description: "If you are member of Autodesk Developer Network, you probably have known that our case system has been migrated to Salesforce.com(SFDC), which is a..."
author: Autodesk
---
# Integration of Salesforce.com and AutoCAD WS - Part 1

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/integration-of-salesforcecom-and-autocad-ws-part-1.html

## 文章内容

By Daniel Du
If you are member of Autodesk Developer Network, you probably have known that our case system has been migrated to Salesforce.com(SFDC), which is a cloud based CRM system. Apart from SaaS(Software as a Service), Salesforce is also a PaaS(Platform as a Service) provider. Force.com is a cloud platform, which enables developers to create applications to extend Salesforce.com and add value to your cloud based system.  At the same time, AutoCAD WS as a cloud based CAD system has gained good reputation among CAD users, it allows user to view/edit DWG drawing from a browser or even a mobile device for free, without downloading and installing the AutoCAD software.
So how about to connect the two clouds? I was assigned a task to investigate the possibilities of integrating Salesforce.com and AutoCAD WS. We have many DWG files as attachments in our SFDC based case system, What I am trying to do is, find a way to open the DWG attachment in AutoCAD WS directly, without downloading it to local disc.
In following serials of posts, I will demonstrate how to do it, this is the first part - setup the force.com development environment.
  Firstly we need to get a Free Developer Edition at developer.force.com.  Please click here to create a developer account, you will be direct to a registration page like below, just follow the instruction, you can get involved very easily.
After registration, you will get a free Developer Edition (DE) environment, you can login DE environment from developer.force.com by clicking “DE LOGIN” from the top:
Once you log in, you will be directed to the first visual force page – “start here”. It looks like below:
We need to enable development mode, so that we can start our development work. To develop with force.com, you do not need any specific tools, just a browser is good enough.
Click Your Name | Setup | My Personal Information | Personal Information, and click Edit.
Check Development Mode
You can also check Show View State in Development Mode to show “View State” tab
Click Save
After doing this and returning back to the “Start Here” page, you will see the Visualforce Development Mode Tools show up on the bottom of the page, you may need to drag it up a little if it is too narrow.
If you examine the script closer, you will notice that it is exactly the code the “start here” page. It is pretty complicated for a starter like me, so let’s create a simple one.
As always, let’s start from Hello World. Open a new tab on your browser and input following address: https://na12.salesforce.com/apex/helloworld_demo. Please notice that na12 is the instance I am working on, you may use a different one.  What I am trying to to is to access a visual force page, named as ”helloworld_demo”. Since it does not exit, you will get following error message:
We can create the page just by clicking the link in this page. You will get a very basic visual force page like below:
Now let’s do some coding work. This development tool even supports code intelligence, pretty good.
I will just copy/paste following code to script window, it is to show the account information:
<apex:page standardController="Account">
  <apex:pageBlock title=" Hello {!$User.FirstName}!"> 
    You are viewing the {!account.name} account. 
  </apex:pageBlock> 
  <apex:detail />
</apex:page>
When pressing Ctrl+S, the script will be saved and compiled, but it seems nothing happens, as we need to pass an account ID to this page.
To get an account, please click the “+” button and select “Account” from the page.
The account list will show up as below, click one of them to get the Account ID, it look like : 001U0000002NWDT
Now change the URL to https://c.na12.visual.force.com/apex/helloworld_demo?id=001U0000002NWDT, please note that your instance and account id may be different with mine. Congratulations, your first visual force page is running!
OK if you examine the snippet closely, you will see some tags starting from <apex:, they are visual force page tags. force.com will render the VFPage tags into HTML and send to browser. Here is the architecture of visual force system. Does it look like ASP.NET ?  
If you want to know more about force.com development, please refer to http://www.salesforce.com/us/developer/docs/pages/index_Left.htm
Did you follow me to setup the environment successfully? If you prefer an IDE at desktop, you can setup force.com IDE, which is an plug-in of Eclipse, I will introduce how to use it next time.
Stay tuned and have fun!

## 评论

**内容**: abiya said...
Such a great post for the Salesforce Autodesk Developer Network using probably have case systems and integrated with the Salesforce.com, and cloud based CRM systems. It's a knowledgeable post.
Reply
09/27/2016 at 12:16 AM

---
**内容**: James Burns said...
Pretty Good Article, The Way You Narrated Here Is Simply Good, Can Understand To Anyone And Like To Read More Articles From You.
Reply
01/28/2020 at 02:18 AM

---
