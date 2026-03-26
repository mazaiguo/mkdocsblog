---
title: "Properties/OPM Window does not work in my OEM product"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - OEM
description: "When I bring up the properties window in my OEM product, it doesn't display the correct information. Why?"
author: Autodesk
---
# Properties/OPM Window does not work in my OEM product

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/propertiesopm-window-does-not-work-in-my-oem-product.html

## 文章内容

by Fenton Webb
Issue
When I bring up the properties window in my OEM product, it doesn't display the correct information. Why?
Solution
The most common causes for this are (A) missing type libraries, and (B) incorrect registry information.
If your product doesn't include any type libraries, the properties window will
correctly display the drawing's properties, but will be blank when an entity is
selected. Or it may continue to display the drawing's information when
selecting other entities.
In this case, you should go back to the OEM Make Wizard and the Automation page.
Press the "Generate GUIDs..." button to create new IDs for your product. Now
go to the Build page and build your product again. You can either rebuild the
entire product or you can just rebuild the resources, but make sure that the
"Build typeLibs" option is checked. Once you've created your type libraries,
you should follow the steps in Chapter 5 of the OEM Developer's Guide, in the
section "Testing VBA in your Product."
If you've generated the GUIDs and created the type libraries for your product
and the properties window is not functioning properly, it's almost certainly a
problem with the registry information. Here are some tips that might help you
track down the problem.
1. Be sure to follow the steps laid out in Chapt. 5 "Testing VBA in your
product" exactly and in order. The order is very important.
2. Step 1 mentions generating CLSIDs (you can't do this until you have built
the project at least once). Then you go back to the automation page and click
the Generate GUIDs button. Then go back to the build page and check "Rebuild
your resources" and "Build typeLibs". Any time you click Generate GUIDs button
you must rebuild your resources and typeLibs (as well as go through the process
for editing the REG file and registering your CLSIDs). It's an all or nothing
process. Stopping or starting in the middle will definitely cause problems.
3. The first time you launch your product, OEM will automatically create the
registry entries listed in step three all the way up to ...<Install ID>\. It is
a good idea to launch it once so that you don't accidentally make a mistake when
creating the path. In this case just double-check that those registry keys are
there. Another good check is to make sure the <prog>vba.arx app loads with the
ARX command in your stamped product. If these keys are not correct it will give
you an error message. This only has to be done once per product.
4. It should be noted that the heading in the book that says "To register
CLSIDs for your AutoCAD OEM product", begins with step 1, but you need to have
done everything under "To test VBA in your AutoCAD OEM product" (the previous
heading).
5. In step 1 (for CLSID's) it gives you the syntax for the oemguidremap
command. It may be helpful to create a batch file in the project directory and
put in the complete paths for the files. e.g. (prog name = Test)
oemguidremap c:\aoem2009\oem\Test\Testres2.dll c:\aoem2009\acadaut.reg
c:\aoem2009\projects\Test\Test.reg
Notice that the output reg file goes into the project directory so that it is
not deleted if you do a rebuild all on the project.
6. Be extremely careful about step 2. The steps were laid out specifically to
try to minimize the errors. Especially do not globally replace "AutoCAD" or
"ACAD" with anything. Follow the steps exactly. It may be a good idea to go to
the "Product Information" page of the wizard and copy and paste "Product name"
so that you don't make a typo. It also helps to refer to this because it is
easy to confuse the product name with the program name.
7. Be careful about using notepad for find and replace. It has a tendency to
truncate long strings. Especially if you have a long product path.
8. When doing the find and replace for <acad path> do not include the trailing
backslash. (i.e. the path should be: "R:\coreACAD\ntexe\debug") Obviously this
goes for the replacement string as well. (i.e. your path should look something
like: "c:\AOEM2009\oem\Test")
9. As a general rule, it works much better if you don't have any spaces in the
product name. But the documentation explains when you can and cannot have
spaces.
10. There are only two instances of acad.tlb and one instance of acad.exe. So
you don't need to globally replace acad with <prog name>.
11. As a sanity check, I usually go to the automation page of the make wizard,
click on a CLSID like the one for IDS_AoemLine, highlight it and copy it to the
clipboard. Then I go to the reg file, perform a find and then paste in the
CLSID for the search string. The find should come up with the CLSID for
"<product name> Line". If it doesn't, your reg file was not been created
properly.
12. Don't forget to double-click on the reg file to post the changes to the
registry! This should give you a message that it succeeded. When you do get
the CLSIDs registered correctly, keep the reg file. It will be a good reference
when creating the install program.

