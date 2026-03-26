---
title: "Integration of Salesforce.com and AutoCAD WS - Part 3"
date: 2012-05-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
  - DWG
  - JavaScript
description: "In part 1 and part 2 we introduced how to setup the browses based development mode tool and desktop based Force.com IDE. In this post, let’s do som..."
author: Autodesk
---
# Integration of Salesforce.com and AutoCAD WS - Part 3

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/integration-of-salesforcecom-and-autocad-ws-part-3.html

## 文章内容

By Daniel Du 
In part 1 and part 2 we introduced how to setup the browses based development mode tool and desktop based Force.com IDE. In this post, let’s do some actual work.
We have some DWG attachments in a case, what I am trying to do is, to list these DWG attachments and add a button behind of each, when the button is clicked, the DWG attachment should be opened in AutoCAD WS. Let’s list the attachment first in this post.
There is a standard attachment list in case page layout, but I’d rather create my own attachment list so that I can add buttons behind, so I will create a visual force page. and we can put this visual force page to case page layout, we will discuss this in latter part. Let’s say we have 2 DWG attachments for one case. The visual force page is supposed to look like below:
Now we are going to implement this page. Firstly let’s create a visual force page, named as OpenInAutocadWS.
Developers can use Visualforce to create a Visualforce page definition. A page definition consists of two primary elements: Visualforce markup and  Visualforce controller. Visualforce markup consists of Visualforce tags, HTML, JavaScript, or any other Web-enabled code embedded within a single <apex:page> tag. The markup defines the user interface components that should be included on the page, and the way they should appear.A Visualforce controller is a set of instructions that specify what happens when a user interacts with the components specified in associated Visualforce markup, such as when a user clicks a button or link. Controllers also provide access to the data that should be displayed in a page, and can modify component behavior. A developer can either use a standard controller provided by the Force.com platform, or add custom controller logic with a class written in Apex.
In this page, we are trying to list attachment of case, so we can take advantage the “case” standard controller, we also need to create our custom controller extension to implement our custom logic.
<apex:page standardController="Case" 
  extensions="OpenInAutocadWS_Controller" >

<apex:form id="frm">
  <apex:pageBlock id="pb">
   <apex:variable value="{!0}" var="count" />
   <apex:pageBlockTable 
      value="{!listAttachment}" 
      var="item" id="pbt">
      <apex:column headerValue="Name">
         {!item.Name}
      </apex:column>
      <apex:column headerValue="Download">
        <!-- {!item.Id} –>
        <a href="https://c.na9.content.force.com
          /servlet/servlet.FileDownload?file
          ={!item.Id}">download</a>
      </apex:column>

      <apex:column id="colOpenInAcadWS"
        rendered="{!CONTAINS(item.ContentType, 
                       'application/x-dwg')}">
        <p id="{!count}.openInAcadWS"></p>
        <apex:commandLink 
             title="Open In AutoCAD WS"  
             id="btnOpenInAutoCADWs"
             value="Open In AutoCAD WS" 
             styleClass="btn"  
             style="text-decoration:none"
        </apex:commandLink>
        <apex:pageBlock id="hiddenBlock" 
              rendered="false">
        </apex:pageBlock>
        <apex:variable value="{!count+1}" 
                       var="count" />
      </apex:column>
     </apex:pageBlockTable>
    </apex:pageBlock>
</apex:form>
</apex:page>
Here is the source code of OpenInAutocadWS_Controller, which is an Apex class.
public with sharing class 
                 OpenInAutocadWS_Controller {

    public List<Attachment> listAttachment
                                  {get;set;}  
       
        //constructor
    public OpenInAutocadWS_Controller  
     (ApexPages.StandardController controller) { 

     //get the controller instance
     currentCase = (Case)controller.getRecord(); 
       
     //initialize the attachments list
     listAttachment = new List<Attachment>(); 
       
     //get all the case related DWG attachments
     listAttachment =
         [Select Id, ContentType, Name, Body  
         from Attachment  
         where ParentId = :currentCase.Id  
               and Name like '%DWG'];
       
    }
   
}
  With that code, we created a visualforce page, and bind the attachment information to this page.  In the controller, we use SOQL(Saleforce Object Query Language) to retrieve attachment from salesforce.com database and save it to a list. In Visualforce page, the list is banded to a page bloc table.
OK, are you following me? Did you create the visual force page and list out the attachment successfully? Now user can download the attachment file from following url https://c.na9.content.force.com /servlet/servlet.FileDownload?file ={!item.Id}. But for my case, is it not what I want, I would like to open it AutoCAD WS directly without downloading anything. We will discuss this in coming post.
Stay tuned and have fun!

