---
title: "Exchange Apps – PayPal account setup"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "This information applies only to Apps sold for a fee on Exchange Apps. It is important to check your settings are as described in Required PayPal S..."
author: Autodesk
---
# Exchange Apps – PayPal account setup

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/exchange-apps-paypal-account-setup.html

## 文章内容

By Stephen Preston
This information applies only to Apps sold for a fee on Exchange Apps. It is important to check your settings are as described in Required PayPal Settings for Autodesk Exchange Apps below.
Recommended PayPal account types
Publishers with fee-based Apps should have either a “PayPal Business Account” or a “Premier Account”. PayPal Premier accounts allow publishers to use their individual name. PayPal Business Accounts allow publishers to conduct business under a company or group name. (See PayPal account type comparison). For Autodesk Exchange Apps PayPal accounts “PayPal Website Payment Standard” is sufficient ¾ this has no setup fees and can accept not only buyers with a PayPal account, but also anyone with a credit card even without a PayPal account.
  Required PayPal settings for Exchange apps
  Autodesk Exchange Apps uses PayPal as its payment vendor. In order for customers to be able to successfully purchase your app, you must change some settings in your PayPal account.
PayPal Settings
In your PayPal account, under My Account, click on the Profile link:
Enable Auto Return for website payments.
Click on Website Payment Preferences under Selling Preferences:
Turn On Auto return and type http://apps.exchange.autodesk.com/Payment/Success as Return URL, like this:
Save the changes clicking on the Save button at the bottom of the page. 
Enable Instant Payment Notification (IPN)
Click on Instant Payment Notification Preferences under Selling Preferences:
  You will see the IPN preferences page and click on Choose IPN Settings button:
Enable IPN messages selecting the Receive IPN messages radio button and type http://apps.exchange.autodesk.com/Payment/IPNHandler as the Notification URL, like this:
Save the changes by clicking on the Save button, and you will be redirect to IPN preferences page where you will see that IPN is now enabled:
Checking for failed purchases
If a customer reports to you that a purchase failed, look at your IPN History to get information about the transaction. On IPN history you can see all the IPN notification that were sent and their status.
To access the IPN History page, the publisher has to login to his account and under the menu history he/she is going to find the IPN History link:
In that page are all the IPN notifications sent and their state:
The retrying notification status indicates that it wasn´t successful so PayPal will try several times until success. Clicking on the message id you can see more details about the transaction.
If a customer reports a failed PayPal transaction after you have correctly set your Auto-Return and IPN settings, please email mail AppSubmissions@autodesk.com to report the problem.

