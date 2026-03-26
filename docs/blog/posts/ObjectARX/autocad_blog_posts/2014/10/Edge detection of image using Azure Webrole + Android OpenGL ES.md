---
title: "Edge detection of image using Azure Webrole + Android OpenGL ES"
date: 2014-10-01
categories:
  - AutoCAD
tags:
  - API
description: "In the recently concluded Apps Hackathon, DevTech teams worked on different cloud and mobile based projects of their choice. The DevTech team in In..."
author: Autodesk
---
# Edge detection of image using Azure Webrole + Android OpenGL ES

发布日期: 2014-10-01

原始链接: https://adndevblog.typepad.com/autocad/2014/10/edge-detection-of-image-using-azure-webrole-android-opengl-es.html

## 文章内容

By Balaji Ramamoorthy, Madhukar Moogala, Virupaksha Aithal
In the recently concluded Apps Hackathon, DevTech teams worked on different cloud and mobile based projects of their choice. The DevTech team in India chose to work on an image edge detection web service by creating a Microsoft Azure Webrole that exposes REST API and to create an Android client for it to display the edges. In this blog post, we are sharing the work that we did. Most of the webrole had already been created as a hobby project and a significant portion of the work during the Apps Hackathon went into consuming the web service in an Android OpenGL ES project.
Here is a sample image that was uploaded and the edges in an Android tablet
As a basis for the algorithm needed for image edge detection, we converted the code from this excellent blog post into a Azure web role and provided REST access to it.
Canny edge detection of images
The Azure webrole project, android client project, a sample image and a screenshot of the output in an Android tablet can be downloaded here :
Download EDServiceAzureWebRole
Download EDAndroidClient
Download DS1
Here are some details about the files provided for download :
EDServiceAzureWebRole.zip includes source code for a Azure web role that does edge detection of images and provides output as lines. Canny edge detection algorithm as implemented in the blog post is used as a basis for this web service. REST API has been provided to upload an image and get access to the edge detected output. Here are some details about the webrole.
After the EDService Webrole is hosted in Azure, you will get a URL similar to this : http://168.63.186.125:8080/EDService.svc/
The REST API exposed by the web role are :
1) GET : http://168.63.186.125:8080/EDService.svc/Datasets
Provides the id of all the image datasets that have been uploaded for edge detection
2) GET : http://168.63.186.125:8080/EDService.svc/Dataset/{id}
Gets the edge information of a dataset that is identified using {id}
A sample edge information obtained for a dataset is provided in "DS1.ogl" file.
3) POST : http://168.63.186.125:8080/EDService.svc/Image/{id}
Uploads the image as a JSON data represented by "ImageData" class.
Please refer to IEDService.cs for the contents of ImageData class that represents an image
4) GET : http://168.63.186.125:8080/EDService.svc/ClearDataset/{id}
Clears the dataset identified by the id. If you no longer need the edge detected image to be stored at the server, this will help clear it.
DS1.ogl : A sample file that contains the edge information as obtained for the sample image from the webrole. This sample data is used in the Android application for display.
EDAndroidClient.zip includes an Android project that uses OpenGL ES 2.0 for displaying the edges as obtained from the webrole.
SampleImage.png : A sample image that was uploaded to the Webrole for edge detection. The edges were displayed in an Android application using OpenGL ES 2.0
Screenshot_AndroidClientOutput.png : A screenshot of the Android client as it displays the edges as obtained from the webrole.

