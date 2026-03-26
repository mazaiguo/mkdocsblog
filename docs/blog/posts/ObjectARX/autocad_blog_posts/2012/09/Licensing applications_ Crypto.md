---
title: "Licensing applications: Crypto"
date: 2012-09-01
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
# Licensing applications: Crypto

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/licensing-applications-crypto.html

## 文章内容

By Augusto Goncalves
This series of articles will show how to use tools available on the market to control licensing of plug-ins for Autodesk products. This is important to most commercial developers and if you are developing for the Autodesk Exchange Store, you noticed that no license system is provided, only a payment method. We’re not testing, validating or certifying the protection system and how hard it’s to (or not to) break it.
For this demonstration, we’ll use a .NET plug-in developed for AutoCAD, but the same idea can be applied to other .NET based APIs, like Revit and Inventor. Most of the code came from the samples available with the tool.
Here will be shown the Crypto Licensing for .NET, winning of the 2012 Members Choice of the Code Project development resource site. This tool is available for trial during 30 days and the prices start at $149 US dollars.
Between benefits:
just a few lines of code added to any command on the plug-in, as will be shown on the sample;
single .NET reference required that will enable all license features;
supports obfuscation, although this feature is not included, but they offer a tool called Crypto Obsfucator for .NET starting at $149.
support trial, mandatory feature for Autodesk Exchange Store, where every plug-in must immediately work after downloaded;
serial or license code feature;
authentication can be done online;
Of course, for AutoCAD environment, some cons:
the solution is .NET based and therefore will only work for Windows platform;
requires reference to Windows Form, which can affect AutoCAD console;
To test the Crypto solution, download it from here. After install it, launch it, the default new project will have the option to create a new validation key, like described on the image below.
The validation key will be used on the code below, which was based on the sample available at the C:\Program Files (x86)\LogicNP Software\CryptoLicensing For .Net 2012\Samples\C#\AppLicensing folder. On the code, the CryptoLicense object have a ValidationKey property that will receive the value obtained above.
The next step is to create a LicenseCode that will go embed on the code. On this case, let’s set it to run up to 5 days after first run. To create this code, select the number of days, as described on 1 at the image below. Then click on Generate, as shown on 2 and then finally get the code on 3.
Finally place the validation key and license code at the code, like shown at the sample code below. Compile and NETLOAD on AutoCAD.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
  // Crypto licensing namespace
using LogicNP.CryptoLicensing;
  // AutoCAD namespaces
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.EditorInput;
  namespace AutoCAD_Crypto
{
  public class Commands
  {
    public static bool Licensed
    {
      get
      {
        // Create the object to check the license
        CryptoLicense license = new CryptoLicense();
          // Get the validation key using Ctrl+K in the Generator UI.
        license.ValidationKey = "";
          // The license will be loaded from/saved to the registry
        license.StorageMode = LicenseStorageMode.ToRegistry;
          // Load the license from the registry
        if (!license.Load())
        {
          // When app runs for first time, the load will
          // fail, so specify an evaluation code....
          // This license code was generated from the Generator
          // UI with a "Limit Usage Days To" setting to some days.
          license.LicenseCode = "";
            // Save it so that it will get loaded
          // the next time app runs
          license.Save();
        }
          // ShowEvaluationInfoDialog shows the dialog only
        // if the license specifies evaluation limits
        bool licensed = license.ShowEvaluationInfoDialog(
          "AutoCAD_Crypto",
          "http://www.companyname.com/buy");
          // it is possible check if the application
        // still in evaluation mode using the following code
        if (license.IsEvaluationLicense())
        {
        }
          // Be sure to call Dispose when done
        // using the CryptoLicense object.
        // The 'using' keywork is not a option
        // as this object do not implement IDisposable
        license.Dispose();
          return licensed;
      }
    }
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
Once we NETLOD and run the command, will show a warning like below. Notice that it still showing ‘30 days of trial’, but this is because I’m using the trial version of Crypton solution.
As the trial version do not allow generate other types of code, I will stop here, but if the user clicks on ‘Enter License’ button, it’ll prompt for another license key that can be generated like the before, but specifying another usage restriction.
The ‘Purchase’ button will open the URL specified on the code, which is the website where the user can buy the application.
Have used this solution before? Have used any other solution? Please share your experience, we can create an article on it.
Next article will discuss the IntelliProtector, as suggested on this comment.

## 评论

**内容**: Rajibyadev123 said...
I see absolutely nothing really difficult to apply the intents: The certification webserver need its very own private as well as public key pairs. Then chances are you need to create.
Reply
12/14/2012 at 07:13 AM

---
**内容**: Augusto Goncalves said in reply to Rajibyadev123...
Hi,
Not sure what you mean here...can you clarify?
Regards,
Augusto Goncalves
Reply
12/14/2012 at 08:21 AM

---
**内容**: Ben said...
Hello thank you for your excellent article!
The crpto program..."requires reference to Windows Form, which can affect AutoCAD console;"
How will a windows forms reference affect the autocad console? Are there any work-around solutions?
Reply
03/02/2016 at 03:32 AM

---
**内容**: Augusto Goncalves said in reply to Ben...
Hi Ben,
Indeed AutoCAD Console cannot have windows Forms, it's a console application... therefore use these references will make the plugin DLL incompatible.
Regards,
Augusto Goncalves
Reply
03/02/2016 at 03:54 AM

---
**内容**: Keith Brown said...
If you don't use their dialog then I believe that you can use it without Systems.Windows.Forms.
For instance, just check to see if the product is licensed and if not then cancel out of the console. You could create a separate .exe to license the application.
Reply
03/02/2016 at 08:20 AM

---
**内容**: Ben said in reply to Keith Brown...
thanks Keith that will come in very useful
Reply
03/03/2016 at 02:47 PM

---
**内容**: Sam Porter said...
If you're looking to protect an AutoCAD app, you might want to check out Quick License Manager by Soraco Technologies at https://soraco.co
Reply
08/24/2017 at 09:24 AM

---
