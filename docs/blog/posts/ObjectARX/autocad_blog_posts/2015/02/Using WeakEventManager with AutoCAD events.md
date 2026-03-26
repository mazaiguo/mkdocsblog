---
title: "Using WeakEventManager with AutoCAD events"
date: 2015-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Recently we had a query from a developer on using WeakEventManager when subscribing to AutoCAD events. In this blog post we will look at three diff..."
author: Autodesk
---
# Using WeakEventManager with AutoCAD events

发布日期: 2015-02-01

原始链接: https://adndevblog.typepad.com/autocad/2015/02/using-weakeventmanager-with-autocad-events.html

## 文章内容

By Balaji Ramamoorthy
Recently we had a query from a developer on using WeakEventManager when subscribing to AutoCAD events. In this blog post we will look at three different versions all of which subscribe to the CommandEnded event of the Document class. The benefit of using the WeakEventManager is to prevent memory leaks when the events are left subscribed but no longer needed. The best practice is to unsubscribe the events when its no longer needed. Also, the use of WeakEventManager comes at a cost because the events are now delivered through the event manager. The additional cost of using the Weak event pattern is nicely explained in this blog post by Reed Copsey.
It is recommended to unsubscribe the AutoCAD events manually, but the following code snippets should demonstrate the use of WeakEventManager in case you need it.
 public  class  Commands  :
             IExtensionApplication ,
             System.Windows.IWeakEventListener 
 {
     void  IExtensionApplication .Initialize() { }
       void  IExtensionApplication .Terminate() { }
       #region  Version 1 (Without the use of WeakEventManager)
     // Version : 1 
     bool  bAdded1 = false ;
       [CommandMethod ("StartMonitor1" )]
     public  void  StartMonitorMethod()
     {
         Document  doc
         = Application .DocumentManager.MdiActiveDocument;
           if  (bAdded1 == false )
         {
             doc.CommandEnded
             += new  CommandEventHandler (doc_CommandEnded);
               bAdded1 = true ;
             doc.Editor.WriteMessage(
             String .Format(
             "{0} Subscribed to CommandEnded event" ,
             Environment .NewLine));
         }
     }
       [CommandMethod ("EndMonitor1" )]
     public  void  EndMonitorMethod()
     {
         Document  doc
         = Application .DocumentManager.MdiActiveDocument;
           if  (bAdded1 == true )
         {
             doc.CommandEnded
             -= new  CommandEventHandler (doc_CommandEnded);
               bAdded1 = false ;
             doc.Editor.WriteMessage(
             String .Format(
             "{0} Unsubscribed CommandEnded event" ,
             Environment .NewLine));
         }
     }
       void  doc_CommandEnded(object  sender, CommandEventArgs  e)
     {
         Document  doc
         = Application .DocumentManager.MdiActiveDocument;
         Editor  ed = doc.Editor;
           if  (bAdded3)
             ed.WriteMessage(
             String .Format("{0} (Weak event) Command Ended : {1}" ,
             Environment .NewLine, e.GlobalCommandName));
         else 
             ed.WriteMessage(
             String .Format("{0} Command Ended : {1}" ,
             Environment .NewLine, e.GlobalCommandName));
     }
     #endregion 
       //(Using WeakEventManager (non-generic version)  
     #region  Version 2
     bool  bAdded2 = false ;
       [CommandMethod ("StartMonitor2" )]
     public  void  StartMonitor2Method()
     {
         Document  doc
         = Application .DocumentManager.MdiActiveDocument;
         if  (bAdded2 == false )
         {
             CommandEndedEventManager .AddListener(doc, this );
             bAdded2 = true ;
               doc.Editor.WriteMessage(
             String .Format(
             "{0} Subscribed to CommandEnded weak event" ,
             Environment .NewLine));
         }
     }
       [CommandMethod ("EndMonitor2" )]
     public  void  EndMonitor2Method()
     {
         Document  doc
         = Application .DocumentManager.MdiActiveDocument;
         if  (bAdded2 == true )
         {
             CommandEndedEventManager .RemoveListener
                                         (doc, this );
             bAdded2 = false ;
               doc.Editor.WriteMessage(
             String .Format(
             "{0} Unsubscribed CommandEnded weak event" ,
             Environment .NewLine));
         }
     }
       bool  System.Windows.IWeakEventListener .ReceiveWeakEvent
             (Type  managerType, object  sender, EventArgs  e)
     {
         if  (managerType.Equals(
                         typeof (CommandEndedEventManager )))
         {
             Document  doc = sender as  Document ;
             CommandEventArgs  ce = e as  CommandEventArgs ;
               Editor  ed = doc.Editor;
             ed.WriteMessage(
                 String .Format("{0} (Weak event) Command Ended : {1}" ,
                 Environment .NewLine, ce.GlobalCommandName));
               return  true ;
         }
         return  false ;
     }
     #endregion 
       //(Using generic WeakEventManager from .Net framework 4.5) 
     #region  Version 3 
     bool  bAdded3 = false ;
       [CommandMethod ("StartMonitor3" )]
     public  void  StartMonitor3Method()
     {
         Document  doc 
             = Application .DocumentManager.MdiActiveDocument;
         if  (bAdded3 == false )
         {
             System.Windows.WeakEventManager
                 <Document , CommandEventArgs >
                 .AddHandler(
                 doc, 
                 "CommandEnded" , 
                 doc_CommandEnded);
               bAdded3 = true ;
             doc.Editor.WriteMessage(
                 String .Format(
                 "{0} Subscribed to CommandEnded weak event" , 
                 Environment .NewLine));
         }
     }
       [CommandMethod ("EndMonitor3" )]
     public  void  EndMonitor3Method()
     {
         Document  doc 
             = Application .DocumentManager.MdiActiveDocument;
         if  (bAdded3 == true )
         {
             System.Windows.WeakEventManager
                 <Document , CommandEventArgs >
                 .RemoveHandler(
                 doc, 
                 "CommandEnded" , 
                 doc_CommandEnded);
               bAdded3 = false ;
             doc.Editor.WriteMessage(
                 String .Format(
                 "{0} Unsubscribed CommandEnded weak event" , 
                 Environment .NewLine));
         }
     }
     #endregion 
 }
   // For Version 2  
 // Using Non-generic version of WeakEventManager 
 public  class  CommandEndedEventManager 
             : System.Windows.WeakEventManager 
 {
     public  static  CommandEndedEventManager  CurrentManager
     {
         get 
         {
             CommandEndedEventManager  manager
             = System.Windows.WeakEventManager .GetCurrentManager(
             typeof (CommandEndedEventManager ))
             as  CommandEndedEventManager ;
               if  (manager == null )
             {
                 manager = new  CommandEndedEventManager ();
                 System.Windows.WeakEventManager .SetCurrentManager
                     (typeof (CommandEndedEventManager ), manager);
             }
               return  manager;
         }
     }
       public  static  void  AddListener(
         Document  source,
         System.Windows.IWeakEventListener  listener)
     {
         CurrentManager.ProtectedAddListener
                             (source, listener);
     }
       public  static  void  RemoveListener(
         Document  source,
         System.Windows.IWeakEventListener  listener)
     {
         CurrentManager.ProtectedRemoveListener
                             (source, listener);
     }
       protected  override  void  StartListening(object  source)
     {
         try 
         {
             ((Document )source).CommandEnded
                         += deliver_CommandEnded;
         }
         catch  (System.Exception  ex)
         {
             Document  doc
               = Application .DocumentManager.MdiActiveDocument;
             Editor  ed = doc.Editor;
             ed.WriteMessage(ex.Message);
         }
     }
       void  deliver_CommandEnded(
             object  sender, CommandEventArgs  e)
     {
         this .DeliverEvent(sender, e);
     }
       protected  override  void  StopListening(object  source)
     {
         try 
         {
             ((Document )source).CommandEnded
                 -= deliver_CommandEnded;
         }
         catch  (System.Exception  ex)
         {
             System.Windows.MessageBox .Show(ex.Message);
         }
     }
 }

## 评论

**内容**: Balaji Ramamoorthy fucks goats said...
ROFL WHAT DUMB SOB POSITED THIS WORTHLESS PERICE OF CRAP
Balaji Ramamoorthy DO JUST HUMP GOATS WITH YOUR UNIT INCHER WHEN YOU COPY AND PASTE THIS CRAP ROFL
Balaji Ramamoorthy SUCK THE HOMO DIC
Reply
06/26/2023 at 07:18 AM

---
