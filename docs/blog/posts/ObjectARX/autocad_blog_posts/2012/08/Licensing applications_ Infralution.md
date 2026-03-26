---
title: "Licensing applications: Infralution"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Plugin
description: "This series of articles will show how to use tools available on the market to control licensing of plug-ins for Autodesk products. This is importan..."
author: Autodesk
---
# Licensing applications: Infralution

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/licensing-applications-infralution.html

## 文章内容

By Augusto Goncalves
This series of articles will show how to use tools available on the market to control licensing of plug-ins for Autodesk products. This is important to most commercial developers and if you are developing for the Autodesk Exchange Store, you noticed that no license system is provided, only a payment method. We’re not testing, validating or certifying the protection system and how hard it’s to (or not to) break it.
For this demonstration, we’ll use a .NET plug-in developed for AutoCAD, but the same idea can be applied to other .NET based APIs, like Revit and Inventor. Most of the code came from the samples available with the tool.
Now moving forward, this post will show the Infralution License System, winning of the 2009, 2010 and 2011 Members Choice of the Code Project development resource site. This tool is available for trial during 30 days and the prices start at $170 US dollars.
Between the benefits:
just a few lines of code added to any command on the plug-in, as will be shown on the sample;
single .NET reference required that will enable all license features;
supports obfuscation, although this feature is not included, but there is another tool .NET Encryptor from the same provider.
interesting sales management feature;
support trial, mandatory feature for Autodesk Exchange Store, where every plug-in must immediately work after downloaded;
authentication can be done online;
Of course, for AutoCAD environment, some cons:
the solution is .NET based and therefore will only work for Windows platform;
no C++ or Lisp support;
requires reference to Windows Form, which can affect AutoCAD console;
To test the Infralution, download the installer from here. Install it and launch it. Go to File menu, then New, then Product. Fill with your plug-in information, such as name, but note that the ‘Product Password’ field is disabled during trial, which must be a unique and hard to guess value. Then click on ‘Generate Validation Parameters’ to create the LICENSE_PARAMETERS variable value.
This sample code is based on the sample available at C:\Program Files (x86)\Infralution\Licensing System 5\Samples\VS2010\C#\LicensedApp folder and have, at the beginning, the code required to check the license. The value of the variable LICENSE_PARAMETERS must be replaced with the one generated when the product was created on the ‘Infralution License Tracker’.
Remember to adjust the TrialDays property. If you plan to deploy at the Autodesk Exchange Store, it is required to have a few days of trial, but the number is your business decision. At the bottom, the LICENSEDTESTPLUGIN custom command will require the license.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
  // Infralution namespace
using Infralution.Licensing.Forms;
  // AutoCAD namespaces
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.EditorInput;
  namespace AutoCAD_Infralution
{
  public class Commands
  {
    #region License
      /// <summary>
    /// License paramters
    /// Generated using the Infralution License
    /// Tracker (after create a new product)
    /// </summary>
    private const string LICENSE_PARAMETERS =
      @"<EncryptedLicenseParameters>
          <ProductName>AutoCAD_Infralution</ProductName>
          <RSAKeyValue>
            <Modulus></Modulus>
            <Exponent>AQAB</Exponent>
          </RSAKeyValue>
          <DesignSignature></DesignSignature>
          <RuntimeSignature></RuntimeSignature>
          <KeyStrength>7</KeyStrength>
        </EncryptedLicenseParameters>";
      /// <summary>
    /// License file
    /// </summary>
    private static string _licenseFile =
      GetPathForDLL(@"MyLicensedProduct.lic");
      /// <summary>
    /// License provider
    /// </summary>
    private static EncryptedLicenseProvider
      _licenseProvider = new EncryptedLicenseProvider(
        LICENSE_PARAMETERS, _licenseFile);
      /// <summary>
    /// Loaded license, if any
    /// </summary>
    private static EncryptedLicense _license;
      /// <summary>
    /// Helper function to get the path of the license file
    /// </summary>
    /// <param name="dllName"></param>
    /// <returns></returns>
    private static string GetPathForDLL(string dllName)
    {
      string currentAssemblyLocation =
        System.Reflection.Assembly.
        GetExecutingAssembly().Location;
      string currentAssemblyPath = System.
        IO.Path.GetDirectoryName(
        currentAssemblyLocation);
      return System.IO.Path.Combine(
        currentAssemblyPath, dllName);
    }
      public static bool Licensed
    {
      get
      {
        _license = _licenseProvider.GetLicense();
        while (_license == null)
        {
          // For this tests, I'm using the evaluation
          // version of the infralution there the
          // password cannot be changed
          EvaluationMonitor evaluationMonitor = new
            RegistryEvaluationMonitor("TEST");
          EvaluationDialog evaluationDialog = new
            EvaluationDialog();
            // Fully functional for 5 days
          // It's required for the Exchange Store that
          // any application is fully function at download
          // time, even for a short trial period
          evaluationDialog.TrialDays = 5;
            // Execution delayed after 5 days, but only
          // during 1 extra day
          evaluationDialog.ExtendedTrialDays = 1;
          evaluationDialog.ExtendedTrialDelay = new TimeSpan(10000);
            // Application name that will appear on the dialog
          // Using the same name used when creating the product
          // on the Infralution License Tracker
          evaluationDialog.ProductName = "AutoCAD_Infralution";
            // Show the license dialog
          EvaluationDialogResult dialogResult =
            evaluationDialog.ShowDialog(evaluationMonitor);
            // Exit the app
          if (dialogResult == EvaluationDialogResult.Exit)
            return false;
            // Exit the loop
          if (dialogResult == EvaluationDialogResult.Continue)
            break;
            // Install the license
          if (dialogResult == EvaluationDialogResult.InstallLicense)
          {
            EncryptedLicenseInstallForm licenseForm = new
              EncryptedLicenseInstallForm();
            _license = licenseForm.ShowDialog(_licenseProvider,
              null);
          }
        }
        return true;
      }
    }
      #endregion
      [CommandMethod("licensedTestPlugin")]
    public static void CmdMyTestCommand()
    {
      if (!Licensed) return;
        // If is licensed, show a message
      Editor ed = Application.DocumentManager.
        MdiActiveDocument.Editor;
      ed.WriteMessage("\nI'm working now");
    }
  }
} 
After NETLOAD and run the command, it will show the License dialog, like below. Although it would be possible place this license dialog on start-up (i.e. during IExtensionApplication.Initialize execution), this is not recommended. Remember that your application is one of several applications the user can have installed, and show this during AutoCAD start-up/launch can stop the process, slowing the start-up process.
Now to generate the license, go back to Infralution License Tracker, create a New Customer.
Then finally at New Sale menu, select the product and the customer, and finally click on ‘Generate’ to create the license key. This key can be sent to the user to license the application.
It is also possible to do some online activation. For that, it is required a online website running ASP.NET. Just like offline activation, when the user runs the command it will require a key, but the license framework will automatically go online and check it, avoiding duplicated activation.
Have used this solution before? Have used any other solution? Please share your experience, we can create an article on it.
Next article will discuss the Crypto tool.

## 评论

**内容**: PDOTeam said...
We've been using Intelliprotector. It's cheaper than Infran, does some encryption and does activation over the internet automatically on Intelliprotector's site.
http://intelliprotector.com/
I've been using SmartAssembly for obfuscation. While it's more expensive than Crypto, it's really easy to use with a lot of powerful features.
Reply
08/13/2012 at 07:20 PM

---
**内容**: Augusto Goncalves said in reply to PDOTeam...
Thanks, I'll look at that for a future post.
Reply
08/22/2012 at 09:57 AM

---
**内容**: LogicNP said...
Did you have a look at CryptoLicensing http://www.ssware.com/cryptolicensing/cryptolicensing_net.htm - it supports any type of .Net software including Autodesk product plug-ins, it supports a variety of license scenarios include trials, activations, machine-locking, embedded user-data and bit-features, etc, etc.
Reply
08/18/2012 at 03:01 AM

---
**内容**: Augusto Goncalves said in reply to LogicNP...
Yes, and it's actually the next tool I'll showing here. Thanks.
Reply
08/22/2012 at 09:57 AM

---
**内容**: jemue said...
You should also have a look at Licence Protector from Mirage. It is ok, has a lot of licensing options and work's with Windows and MAC Os.
On the downside, I found the Licence Protector to be sometimes a little confusing and too complicated.
http://www.mirage-systems.de/en/products/licence-protector/
Reply
09/21/2012 at 05:27 AM

---
**内容**: Augusto Goncalves said in reply to jemue...
Hi Jamue, thanks for the name, I'll consider this tool for a future post.
Regards,
Augusto Goncalves
Reply
09/21/2012 at 06:13 AM

---
**内容**: Ning Zhou said...
hi Augusto,
i'm new to this licensing stuff, just installed trial version and play w/ it, but only in Revit platform instead of AutoCAD, so my questions is:
1) where should i insert your code (#region License portion, and if (!Licensed) return; portion)?
2) should i insert multiple times for application and each command?
3) for example, below is typical Revit API stuff:
#region Namespaces
using System;
using System.Collections.Generic;
using System.Text;
using System.Linq;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Infralution.Licensing.Forms;
using Infralution.Licensing.WPF;
using Infralution.Licensing.Data;
using Infralution.Licensing.ASP;
using Infralution.Licensing.CF;
using Infralution.Licensing.CustomGenerator;
#endregion
namespace X
{
[Transaction(TransactionMode.Manual)]
public class appTest : IExternalApplication
{
public Result OnStartup(UIControlledApplication application)
{
return Result.Succeeded;
}
public Result OnShutdown(UIControlledApplication application)
{
return Result.Succeeded;
}
}
[Transaction(TransactionMode.Manual)]
public class cmdTest1 : IExternalCommand
{
public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
{
return Result.Succeeded;
}
}
[Transaction(TransactionMode.Manual)]
public class cmdTest2 : IExternalCommand
{
public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
{
return Result.Succeeded;
}
}
}
many thanks and have great weekend!
Ning
Reply
08/23/2013 at 01:47 AM

---
**内容**: Augusto Goncalves said in reply to Ning Zhou...
Sorry not replying earlier...I was out for a few days.
You can insert the #region code on any method, note the method is 'public static'. I would suggest you test at the beginning on each command, just before you start doing something with the user. That way you avoid request any data from the user when is not possible to run the command.
Hope this clarifies.
Regards,
Augusto Goncalves
Reply
09/12/2013 at 06:43 AM

---
**内容**: Elvis said...
But Only Work With AutoCad, 'Cuase I Was Trying And I Make Fail
Reply
03/15/2014 at 07:33 AM

---
**内容**: Augusto Goncalves said in reply to Elvis...
Hi Elvis,
This specific sample was designed with the Infralution API to work with AutoCAD based products. If you try with a different product, such as Revit, it can work, but you'll need to change the command part.
If that was not your question, please clarify.
Regards,
Augusto Goncalves
Reply
03/17/2014 at 10:00 AM

---
