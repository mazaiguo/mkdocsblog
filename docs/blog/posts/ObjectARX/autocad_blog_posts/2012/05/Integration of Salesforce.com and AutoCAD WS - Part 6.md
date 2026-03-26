---
title: "Integration of Salesforce.com and AutoCAD WS - Part 6"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - AutoCAD
  - COM
description: "In part3, part 4 and part 5 we introduced how to list the DWG attachments and how to debug in force.com application. in this post, we will go ahead..."
author: Autodesk
---
# Integration of Salesforce.com and AutoCAD WS - Part 6

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/integration-of-salesforcecom-and-autocad-ws-part-6.html

## 文章内容

By Daniel Du
In part3, part 4 and part 5 we introduced how to list the DWG attachments and how to debug in force.com application. in this post, we will go ahead to transfer the DWG attachment to AutoCAD WS storage.
AutoCAD WS announced its API. Currently it is still the fist step, includes connect to AutoCAD WS account, manipulate files on AutoCAD WS storage, and launch a drawing in WS online editor. These APIs rely on the industry standard http based WebDAV protocol which can be used in a variety of programming languages such as C#, C++, Java and JavaScript to access AutoCAD WS’s functionality from within web browsers, desktop applications and server-side components. Today, we will do it in Apex code.
AutoCAD WS team produced two tutorials with full source code samples showing how to use the new set of APIs using either C# or JavaScript. It may helps you to understand the mechanism so that we can create a similar one in Apex.
For our requirement, to transfer DWG attachments to AutoCAD WS and open it in WS online editor, I would not implement all functions like the one in C# or Javascript, Anther difference is the sample tutorial is trying to upload files from local drive to AutoCAD WS storage, it does apply to our scenario. What we want to do is, transfer files from one cloud to another, so we need to this part ourselves.
I created a class named as WebdavManager_WebdavClient. The constructor of the WebdavClient class expects three arguments:
url: The Webdav server addres. For example, if you want to connect to Autocad WS server, use: ‘https://dav.autocadws.com’
username: the username of your account in the Webdav server
password: the password of your account in the Webdav server
The following code creates new WebdavClient class, connecting to Autocad WS Webdav server, with the username ‘someuser’ and the password ’123456′.
WebdavManager_WebdavClient client =
  new WebdavManager_WebdavClient(
            'https://dav.autocadws.com/',
            'someuser', '123456');
Next step is to create a method to transfer DWG file stream, it uses HttpRequest object and “PUT” method. The signature is:
public boolean Put(string remoteFilePath, 
                   Attachment attach)
Here is the code to call WebdavManager_WebdavClient.Put method to transfer DWG attachment to AutoCAD WS storage. It is part of transferToWSStorage method, which is introduced in part4.
public void transferToWSStorage()
{


    //trim() is important!!!!
    //Where the hell blanks comes from?!
    //It took me almost two days to debug...
    selectedAttachmentId =  ApexPages.currentPage()
      .getParameters()
      .get('selectedAttachmentId').trim();
   
    //I have already get the selected attachment ID,
    //this is to get the attachement from map by id
    Attachment attach =
      getAttachmentById(selectedAttachmentId);
        
    string userName = '<your autocad WS username>';
    string password = '<your autocad WS password>';
    //please check Setup->Security->Remote site settings.
    string autocadWsHost = 'https://dav.autocadws.com/'; 
    string dstRelativePath = attach.Name;
   
    WebdavManager_WebdavClient client
      = new WebdavManager_WebdavClient
              (
              autocadWsHost,
              userName,
              password
              );
    client.Put(dstRelativePath, attach);   
   
    //set openInAutocadWSUrl
    //so that it can be opened in AutoCAD WS
    openInAutocadWSUrl = client
          .getOpenDrawingUrl(dstRelativePath);
   
}
Here is the complete code, I use the user credentials to generate  the Authorization header.  The Authorization header is sent to the webdav server in each request,  and the server uses this header  to authorize the user. I also set http header 'Content-Type' to 'application/x-dwg;', indicating it is a DWG file, and set the HTTP method to “PUT” and send the binary stream of DWG file. Please note that the DWG file should be less than 3MB, due to salesforce.com limit. We may need another way to transfer large files, if you have any suggestions, please do let me know, I really appreciate that.
public with sharing class WebdavManager_WebdavClient {
 
  public string host{get;set;}
  public string username {get;set;}
  public string password{get;set;}
 
  public WebdavManager_WebdavClient(
             string host,
             string username, 
             string password)
{
    this.host = host;
    this.username = username;
    this.password = password;
  } 
 

  public boolean Put(string remoteFilePath,
                     Attachment attach){

    HttpRequest req = buildWebServiceRequest
              (
                remoteFilePath, 
                attach.Body
              );
   
    // Instantiate a new http object
   
    Http h = new Http();
   
    //invoke web service call,
    // Send the request, and return a response
   
    HttpResponse res = invokeWebService(h, req);
   
    //success ?
    return WebServiceResponseSuccessful(res);
   
  }
 
  public HttpRequest buildWebServiceRequest
               (
                string remoteFilePath, 
                Blob body
               )
  {
   
    string endpoint = host+remoteFilePath;
   
    //use the user credentials to generate 
    // the Authorization header.
    //The Authorization header is sent to 
    //the webdav server in each request,
    //and the server uses this header 
    //to authorize the user.
   
    string tok = userName + ':' + password ;
    string hash = EncodingUtil
          .base64Encode(Blob.valueOf(tok)); 
    string authorizationHeader = 'Basic ' + hash;
   
    HttpRequest req = new HttpRequest();
    req.setHeader('Authorization',authorizationHeader );
    req.setHeader('Content-Type','application/x-dwg;');   
    req.setMethod('PUT'); 
   
    req.setEndpoint(endPoint);
   
    //body should less than 3MB
    //due to salesforce's limit
    req.setBodyAsBlob(body);
   
    return req;
  }
 
  public HttpResponse invokeWebService(Http h, 
                      HttpRequest req){

     //Invoke Web Service
    
     HttpResponse res = h.send(req);
     return res;
  }
 
  public boolean WebServiceResponseSuccessful
                  (HttpResponse res)
{
       
    integer statusCode = res.getStatusCode();
   
    //if status code is 2xx, success
   
    if(statusCode >= 200 && statusCode < 300){
      return true;
    }
    else{
      return false;
    }
  }
 
}
  Before you run the code, please check Setup->Security->Remote site settings to enable Salesforce to access remote site, add a new remote website to 'https://dav.autocadws.com/':
OK, with that, you can run your visual force page, and click the “Open in AutoCAD WS” button, the DWG file will be transferred to AutoCAD WS, if you open AutoCAD WS at the same time, you will see a new file is uploaded.
In next post, I will introduce how to open the DWG file in AutoCAD WS editor.
Stay tuned and have fun!

