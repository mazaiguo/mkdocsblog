---
title: "Integration of Salesforce.com and AutoCAD WS - Part 4"
date: 2012-05-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
  - JavaScript
  - Unicode
description: "In part 3, I have already list the attachments in visual force page, and add one command link behind each attachment. Now I want to pass parameters..."
author: Autodesk
---
# Integration of Salesforce.com and AutoCAD WS - Part 4

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/integration-of-salesforcecom-and-autocad-ws-part-4.html

## 文章内容

By Daniel Du
In part 3, I have already list the attachments in visual force page, and add one command link behind each attachment. Now I want to pass parameters to Apex class controllers from visual force page. I need to know which attachment should be opened in AutoCAD WS when user clicks the command link, I am passing the attachment ID as parameter.
<script type="text/javascript"> 
 function openInWS(url){
   window.open(url);
 }
</script>
<apex:column id="colOpenInAcadWS" 
       rendered="{!CONTAINS(item.ContentType, 'application/x-dwg')}">
    <p id="{!count}.openInAcadWS"></p>
    <apex:commandLink action="{!transferToWSStorage}" 
         title="Open In AutoCAD WS"   
         id="btnOpenInAutoCADWs"
         value="Open In AutoCAD WS" 
         styleClass="btn"  style="text-decoration:none"
         oncomplete="openInWS('{!openInAutocadWSUrl}');" >
        <apex:param name="selectedAttachmentId" 
              value="{!item.Id}"/>
    </apex:commandLink>
    <apex:pageBlock id="hiddenBlock" rendered="false">
    </apex:pageBlock>
</apex:column>
Here I assign an action “transferToWSStorage” to command link, it is defined in controller, it will be executed when command link is clicked. Another visual force tag <apex: param> is added to pass parameters.
To avoid query database twice, I store the attachments into a map, so that it can be retrieved by ID without query database again.
Here is the controller code:
public with sharing class 
                  OpenInAutocadWS_Controller {

    public List<Attachment> listAttachment 
    {get;set;}

    public Map<String, Attachment> mapAttachment  
    {get; set;}

    public Case currentCase {get; set;}
   
    public string openInAutocadWSUrl{get;set;} 
       
     //constructor 
     public OpenInAutocadWS_Controller 
      (ApexPages.StandardController controller) {

        //get the controller instance
        currentCase = (Case)controller
                           .getRecord();
       
         //initialize the attachments list
        listAttachment = new List<Attachment>();
       
        //get all the case related attachments
        listAttachment =
           [Select Id, ContentType, Name, Body  
           from Attachment  
           where ParentId = :currentCase.Id  
           and Name like '%DWG'];
       
        //save into a map for latter use
        mapAttachment =
              new Map<String, Attachment>();
        for(Attachment item : listAttachment ) { 
          //trim() is important!!!!  
          //Where the hell blanks comes from?!  
          //It took me almost two days to debug...
            mapAttachment.put(
                   String.valueOf(item.Id).trim(), 
                   item);
            System.Debug('ID=' + item.Id 
                       + 'Name=' + item.name 
                       + ' is added to map');
        }
        
    }
   
   
    public string selectedAttachmentId
    {get; set; }
   
    public void transferToWSStorage()
    {
   
        //trim() is important!!!! 
        //Where the hell blanks comes from?! 
        //It took me almost two days to debug...
        selectedAttachmentId =  
            ApexPages.currentPage()
            .getParameters()
            .get('selectedAttachmentId').trim();
       
        //I have already get the selected attachment ID,
        //this is to get the attachement from map by id
        Attachment attach = 
          getAttachmentById(selectedAttachmentId);
       
        //TO DO: Transfer the attachment to AutoCAS WS 
       // and get file open url in AutoCAD WS
     
        //TO DO: set openInAutocadWSUrl 
        //so that it can be opened in AutoCAD WS
        openInAutocadWSUrl = ‘https://www.autocadws.com/…’;
       
    }
   
    //get the attachment from map by id
    public Attachment getAttachmentById
                      (String attachmentId){

       //This blocks me almost 2 days, 
       //just because the trim() issue!
        Attachment att = mapAttachment
                    .get(attachmentId);
        return att;
       
    }
}
You probably have known, to access Apex objects from visual force page, we can use {! apexPublicVarible}. For example, I will open the DWG file in AutoCAD WS, after get the file URL I will open it with JavaScript.
An attribute is defined in Apex Class:
public string openInAutocadWSUrl{get;set;}
To get the value from apex class controller and use as parameter of JavaScript:
oncomplete="openInWS('{!openInAutocadWSUrl}');"
Please pay attention to the singe quote in parameter.
I am using an <Apex : param> tag to pass attachment ID to Apex class controller. 
<apex:param name="selectedAttachmentId"
value="{!item.Id}"/>
The value can be retrieved from Apex class by following code:
selectedAttachmentId =
ApexPages.currentPage()
.getParameters()
.get('selectedAttachmentId').trim();
Actually the code is pretty simple, but a very small bug blocked me almost 2 days! As careless as me, I accidentally type a SPACE in value, so the value passed to the controller is not correct, no wander I cannot get the correct item by mapAttachment (attchemendId);
<apex:param name="selectedAttachmentId" 
                    value="[SPACE]{!item.Id}"/>
It is not a big deal, but is very difficult to debug! I will talk about debug in next post.
Stay tuned and have fun!

