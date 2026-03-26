---
title: "PAUSE \ waits longer than before in case of m2p/mtp"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I have a Macro for one of my commands and it worked fine before, but in AutoCAD 2010 the PAUSE seems to wait longer, not only for a single point aq..."
author: Autodesk
---
# PAUSE \ waits longer than before in case of m2p/mtp

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/pause-waits-longer-than-before-in-case-of-m2pmtp.html

## 文章内容

By Wayne Brill
Issue
I have a Macro for one of my commands and it worked fine before, but in AutoCAD 2010 the PAUSE seems to wait longer, not only for a single point aquisition as in AutoCAD 2009.
I have this Macro:
^C^C_line m2p;endp;\endp;
In AutoCAD 2010 if Object Snap is turned off and you start the above macro then you can see that the first end point acquisition of m2p is going well (the end point of the entities under the cursor are shown), but during the second end point acquisition of m2p the end points are not highlighted. It seems that the PAUSE is still on, and so the second endp has not been reached.
How could I make this work as before, so that \ would only wait for a single point acquisition?
Solution
In case of the new behaviour PAUSE \ waits for the whole m2p to finish, instead of waiting for just a single intermediate point acquisition. This is more consistent with other similar functions like tan/appint.
If you use the following Lisp code then the result will always be predictable in AutoCAD 2010 and above - PAUSE will wait for the first point acqusition of the LINE command to finish no matter how the user aquires it:
(command "_.line" pause "5,5" "")
Run the above Lisp code
Type in m2p
Pick the first point for m2p >> in AutoCAD 2009 the LINE command will exit without creating a line entity, whereas in the newer releases the LINE command will continue by passing in "5,5" as the second point of the line, and the entity will be created successfully
As a workaround your Macro could set the OSMODE value directly:
^C^C(setq osm (getvar "OSMODE"));(setvar "OSMODE" 1);_line m2p;\\;(setvar "OSMODE" osm);
This switches on End Point Snap temporarily, instead of using endp.

