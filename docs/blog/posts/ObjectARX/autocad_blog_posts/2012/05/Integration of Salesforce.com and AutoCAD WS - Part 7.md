---
title: "Integration of Salesforce.com and AutoCAD WS - Part 7"
date: 2012-05-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
  - DWG
  - JavaScript
  - Unicode
description: "In part 6, we transferred the DWG attachment to AutoCAD WS storage, in this post, we will try to open it in AutoCAD WS online editor."
author: Autodesk
---
# Integration of Salesforce.com and AutoCAD WS - Part 7

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/integration-of-salesforcecom-and-autocad-ws-part-7.html

## 文章内容

By Daniel Du
In part 6, we transferred the DWG attachment to AutoCAD WS storage, in this post, we will try to open it in AutoCAD WS online editor.
In part 4, we introduced how to pass parameters between visual force page and apex controller, please pay attention to the code in bold:
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
In controller:
//set openInAutocadWSUrl so that it can be
//opened in AutoCAD WS
openInAutocadWSUrl = client
     .getOpenDrawingUrl(dstRelativePath);
A command link apex tag invokes an action of apex controller. In the controller, we transferred the DWG attachment to AutoCAD WS storage, and build the URL to open in WS online editor. Once the action is completed, a JavaScript function “oncomplete” will be invoked, we just use window.open() to launch the URL in a new window. We have already transferred the DWG to AutoCAD storage, now we are going to build the launching URL.
This is the implementation of getOpenDrawingURL, it returns the URL to open DWG files in AutoCAD WS online editor:
  //===========Open drawing  begin ===============
 
  //get the url to open in AutoCAD WS
  public string getOpenDrawingUrl(string path){
   
    OpenInWSHandler openHander = new OpenInWSHandler();
    String openInAutocadWSUrl = openHander
           .Open(userName, password, path);
   
    return openInAutocadWSUrl;
  }
 
  //===========Open drawing  end ===============
I create a class OpenInWSHandler. Firstly we need to pass the username and password to AutoCAD WS authenticate URL to get the authentication token. after we get the token, we can use it to build the "AutoCAD-WS-Open-URL”. Here is the source code:
Public Class OpenInWSHandler {
      string AUTHENTICATE_URL 
        = 'https://www.autocadws.com/main/auth';
      string OPEN_IN_WS_URL 
       = 'https://www.autocadws.com/main/open';

      //return the url for open in AcadWS
      public String Open(string userName,
             string password, string relativePath){
     
        String url = '';
        string token = Authenticate(userName, password);
        //if(token.length() > 0){
          url = OPEN_IN_WS_URL + '?path=' 
              + relativePath + '&token=' + token;
        //}
         return url;
      }
     
      public string Authenticate(string userName, 
                          string password) 
      {
        // Request must contain "Authorization: Basic"
        // HTTP header
        string tok = userName + ':' + password ;
        string hash = EncodingUtil
            .base64Encode(Blob.valueOf(tok)); 
        string authorizationHeader = 'Basic ' + hash;
       
        HttpRequest req = new HttpRequest();
        req.setHeader('Authorization'
                      ,authorizationHeader );
        req.setHeader('toautocadws', 'true');
        req.setMethod('GET');
        req.setEndpoint(AUTHENTICATE_URL);
       
        Http h = new Http();
        // Send the request, and return a response
        HttpResponse res = h.send(req);
        //system.assert(false,res.getStatusCode());
        //success
        if(res.getStatusCode() >= 200 
           && res.getStatusCode() < 300) 
        {
           //system.assert(false, res.getBody());
           return String.valueOf(res.getBody()); 
            
        }
        else{
          return ''; //authenticate failed.
        }
       
      }
     
}
Since we are trying to access another remote web site https://www.autocadws.com/,  we also need to to enable Salesforce to access remote site, please check Setup->Security->Remote site settings.
We are ready to give it a run, open the visual force page(please note we need to pass a case Id to list the attachments), and click the “Open In AutoCAD WS” button, a few seconds latter, a new window will launch AutoCAD WS online editor to open this DWG file.
  In next post, I will introduce how to integer this visual force page to your case layout, so that you do not need to input the case id in URL manually.
Good luck and have fun!

## 评论

**内容**: Tushar said...
This code is not working it redirect to autoCad 360 and show page file not found
Reply
12/05/2014 at 03:43 AM

---
