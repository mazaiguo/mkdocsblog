---
title: "Model-View-Controller Design Pattern"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
description: "The Model-view-controller design pattern is a pretty important pattern to learn and understand if you are interested in Web/cloud and mobile progra..."
author: Autodesk
---
# Model-View-Controller Design Pattern

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/model-view-controller-design-pattern.html

## 文章内容

By Gopinath Taget
The Model-view-controller design pattern is a pretty important pattern to learn and understand if you are interested in Web/cloud and mobile programming. This design pattern allows you to architect your applications by dividing them into three main components:
1) The Model – Which represents the data
2) The View – Which provides a visual, graphic or any other kind of “view” of the data
3) The Controller – Which controls the view
The Model and View components do not directly talk to each other. They always communicate via the controller. This separation between the data and the view makes it very easy to manage the application and add/modify functionality. For instance if your data is represented as a bar chart, then the data would be the model and the bar chart would be the view. Also, the Bar Chart would be rendered and managed by a controller object or component. Now if you need to represent your data as a Pie chart instead, all you have to do is create a new view (for the pie chart) and/or a controller to manage the pie chart. The model component does not have to change.
This powerful design pattern is used very extensively in web programming technologies including ASP .NET. It is also a  very central architecture used in iOS programming.

## 评论

**内容**: Viktor K said...
It took me a while to switch over to OOP from my young days vba spaghetti, and wpf has definitely helped grasp the concept of MVC or MVVM by utilizing bindings. But i still seem to struggle where does the autocad portion of the code belong?
For example, my app displays a list of special entities, so the view is the UI, and the list is the Model. The controller glues it together. But when I have methods that deal with autocad api, like selecting objects for example, does that belong in the controller? or the model?
Reply
06/04/2012 at 03:36 PM

---
