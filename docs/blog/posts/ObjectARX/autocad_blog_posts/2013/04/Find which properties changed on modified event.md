---
title: "Find which properties changed on modified event"
date: 2013-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
description: "This is common request: identify what have changed on Modified event of entities. In fact this feature is not available on the API, mainly because ..."
author: Autodesk
---
# Find which properties changed on modified event

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/find-which-properties-changed-on-modified-event.html

## 文章内容

By Augusto Goncalves
This is common request: identify what have changed on Modified event of entities. In fact this feature is not available on the API, mainly because it can potentially represent a big use of memory. But a (partial) workaround may help in some cases!
The main thing is that is not easy to track everything that change on a entity, mainly because one can refer to another, or even contain internal data not easily exposed. Also, in complex scenarios like this, a generic approach may not capture everything.
So I decided to do a quick try with .NET properties, basically using reflection mechanism to store the data and compare back. Below is a common code that track changes with Modified event, but it has a few extra lines (marked in yellow) enabled by .NET Extension mechanism.
[CommandMethod("monitorEntity")]
public void CmdMonitorEntity()
{
  // select an entity
  Editor ed = Application.DocumentManager.
    MdiActiveDocument.Editor;
  PromptEntityResult resEnt = ed.GetEntity(
    "Select an entity: ");
  if (resEnt.Status != PromptStatus.OK) return;
    // and register the event
  MonitorEntity(resEnt.ObjectId);
}
private void MonitorEntity(ObjectId objectId)
{
  Database db = Application.DocumentManager.
    MdiActiveDocument.Database;
  using (Transaction trans = db.
    TransactionManager.StartTransaction())
  {
    Entity ent = trans.GetObject(objectId,
      OpenMode.ForRead) as Entity;
      // start the monitor this object
    ent.MonitorPropertyChanges();
      // as usual, register for 'Modified' event
    ent.Modified += new EventHandler(ent_Modified);
  }
} 
  void ent_Modified(object sender, EventArgs e)
{
  Entity ent = sender as Entity;
  if (ent == null) return;
    // list of what changed
  string[] propsModified = ent.GetModifiedProperties();
  if (propsModified.Length == 0) return;
    Editor ed = Application.DocumentManager.
    MdiActiveDocument.Editor;
    // write the values that changed
  ed.WriteMessage("\nProperties were modified:");
  foreach (string propName in propsModified)
  {
    ed.WriteMessage("\n{0}, previous value {1}",
      propName, ent.GetPreviousValue(propName));
  }
}
The code above should look very common, no extra feature other than those in yellow. As a side note, that is the beauty of .NET Extension: we can add new methods for certain types of object and the syntax is quite sharp.
At the image below, note how the properties changed are tracked after the user change the layer using the Property palette. Please test this and make sure the properties you’re tracking are listed with this mechanism. Things like nodes of a polyline will not appear.
Ok, to enable this extension methods, simply create a new class and mark as ‘static’ in C# or create as a ‘Module’ on VB.NET (where an additional metadata is required: <Extension()>).
public static class DBObjectMonitor
{
  private static Dictionary<ObjectId,
    Dictionary<string, object>> _monitorList;
    // list of properties for objects monitored
  private static Dictionary<ObjectId,
    Dictionary<string, object>> MonitorList
  {
    get
    {
      if (_monitorList == null) _monitorList =
        new Dictionary<ObjectId,
          Dictionary<string, object>>();
      return _monitorList;
    }
  }
    /// <summary>
  /// Prepare the object to monitor what have changed
  /// </summary>
  public static void MonitorPropertyChanges(this DBObject dbObj)
  {
    dbObj.OpenedForModify +=
      new EventHandler(dbObj_OpenedForModify);
  }
    private static void dbObj_OpenedForModify(
    object sender, EventArgs e)
  {
    StorePropeties((DBObject)sender);
  }
    private static void StorePropeties(DBObject dbObj)
  {
    Dictionary<string, object> objPropBefore =
      new Dictionary<string, object>();
      System.Reflection.PropertyInfo[] props =
      dbObj.GetType().GetProperties();
    foreach (System.Reflection.PropertyInfo prop in props)
    {
      try
      {
        // if we cannot write,
        // let's not monitor it
        if (!prop.CanWrite) continue;
          // save the value of the propery
        objPropBefore.Add(prop.Name,
          prop.GetValue(dbObj, null));
      }
      catch
      {
        // get the value through reflection
        // cannot be safe...
      }
    }
      // store all the properties based
    // on the objectId
    MonitorList.Remove(dbObj.ObjectId);
    MonitorList.Add(dbObj.ObjectId, objPropBefore);
  }
    /// <summary>
  /// List of properties changed on the Modified event
  /// </summary>
  public static string[]
    GetModifiedProperties(this DBObject dbObj)
  {
    // is on the list?
    if (!MonitorList.ContainsKey(dbObj.ObjectId))
      return null;
      // get the list of values
    Dictionary<string, object> objPropBefore =
      MonitorList[dbObj.ObjectId];
      // this will store the name of what was changed
    List<String> propList = new List<String>();
      // list of properties
    System.Reflection.PropertyInfo[] props =
        dbObj.GetType().GetProperties();
    foreach (System.Reflection.PropertyInfo prop in props)
    {
      try
      {
        // if we cannot write,
        // let's not monitor it
        if (!prop.CanWrite) continue;
          // save the value of the propery
        object valueBefore = objPropBefore[prop.Name];
        object valueAfter = prop.GetValue(dbObj, null);
          if (valueBefore.Equals(valueAfter))
          // remove from the original list
          objPropBefore.Remove(prop.Name);
        else
          propList.Add(prop.Name);
      }
      catch
      {
        // get the value through reflection
        // may not be safe...
      }
    }
      return propList.ToArray<string>();
  }
    /// <summary>
  /// Get the value for the property
  /// before this current change
  /// </summary>
  /// <param name="propertyName">
  /// Name of the property</param>
  /// <returns>The previous value</returns>
  public static object
    GetPreviousValue(
    this DBObject dbObj,
    string propertyName)
  {
    // get the list
    Dictionary<string, object> objPropBefore =
      MonitorList[dbObj.ObjectId];
      // this property exist?
    if (!objPropBefore.ContainsKey(propertyName))
      return null;
      return objPropBefore[propertyName];
  }
}

## 评论

**内容**: Tony Tanzillo said...
  MonitorList.Remove(dbObj.ObjectId);
  MonitorList.Add(dbObj.ObjectId, objPropBefore);
Hi Augusto.
Are you familiar with the .NET Dictionary?
How about:
  MonitorList[dbObj.ObjectId] = objPropBefore;
??????????
Reply
04/19/2013 at 08:54 AM

---
**内容**: Augusto Goncalves said in reply to Tony Tanzillo...
Hi Tony,
If I just call MonitorList[dbObj.ObjectId] the code will throw KeyNotFoundException exception at the first time.
So I used Remove to clear any previous data, if any, then Add to add it again. That will will store only the last version (before the current edit of the object).
Simply call Add will also throw an exception if already exist.
Hope that make sense.
Regards,
Augusto Goncalves
Reply
04/19/2013 at 09:16 AM

---
**内容**: Tony Tanzillo said in reply to Augusto Goncalves...
Hi Augusto.
Sorry, but I think that's incorrect.
The indexer 'set' does not require the key to exist, and it if the key doesn't exist, it adds the key and value, otherwise, it sets the value of the existing entry with that key to the supplied value.
Reply
04/19/2013 at 09:58 AM

---
**内容**: Augusto Goncalves said in reply to Tony Tanzillo...
Tony,
Sounds like you are right...I just saw the list of exceptions, which led to my conclusion, now reading the whole thing it says: "If the specified key is not found, a get operation throws a KeyNotFoundException, and a set operation creates a new element with the specified key" (http://msdn.microsoft.com/en-us/library/9tee9ht2.aspx?cs-save-lang=1&cs-lang=csharp )
Good point, thanks again.
What about the whole code/idea, have you tried? Helped you? :)
Regards,
Augusto Goncalves
Reply
04/19/2013 at 10:04 AM

---
**内容**: BlackBox said in reply to Augusto Goncalves...
Augusto,
Conceptually, this seems very valuable to me for a specific plug-in I was working on regarding *Modified event... I'll know better when I have a chance to implement & test for myself.
Just wanted to say thanks for discussing the topic, generally.
Cheers
Reply
04/20/2013 at 03:12 PM

---
**内容**: Tony Tanzillo said in reply to BlackBox...
I wouldn't recommend this solution if there are potentially many entities that must be observed, unless you can tolerate AutoCAD's performance being slowed a painful crawl. A generic solution like Augusto has proposed here will have that problem when used with many objects.
You can solve the general problem more easily and without taking a major performance hit, using ObjectOverrule.
For a tracking changes to a potentially-large number of entites, this is about the worst-possible way to go about it.
Reply
04/21/2013 at 07:55 AM

---
**内容**: Tony Tanzillo said in reply to Augusto Goncalves...
Hi Augusto. I haven't tried your code, but knowing that Reflection is painfully slow, I would say that it can be useful in the case you only have to observe a small number of objects.
With many objects, the performance penalty would be very hard to justify.
Reply
04/21/2013 at 07:58 AM

---
**内容**: Augusto Goncalves said in reply to Tony Tanzillo...
Yes that will depend on the performance trade off you're willing to take, as usual.
For any case, I would recommend testing on real work scenario.
Cheers,
Augusto Goncalves
Reply
04/22/2013 at 05:24 PM

---
**内容**: BlackBox said...
Thanks for the feedback, Tony.
My interest stems from this thread:
http://www.theswamp.org/index.php?topic=43356.msg485953#msg485953
... Where you've offered me an ObjectOverrule sample, that I simply must not understand how to implement for my purposes:
http://www.theswamp.org/index.php?topic=43356.msg486228#msg486228
I was hoping Augusto's example would offer some means by which to fill the gap between Database.ObjectModified, and EnteringQuiescentState (i.e., immediately following Properties Pane change(s) given an entity selection)... As obviously there's no CommandEnded event raised in this scenario.
Reply
04/21/2013 at 10:09 AM

---
**内容**: Tony Tanzillo said in reply to BlackBox...
The events you mention aren't a very good way to solve the sort of problem, IMO.
The ObjectOverrule does solve the problem very cleanly and without introducing other problems.
You can post questions about it in that thread if you're not sure how to implement it for what you need.
Reply
04/22/2013 at 11:11 AM

---
**内容**: Augusto Goncalves said in reply to BlackBox...
Hope you had change to try my suggestion with the property palette.
Also, as mentioned by Tony, the Reflection can be slow, but you can avoid part of that getting the specific properties you need, instead the whole object like I did (which is a generic approach).
Cheers,
Augusto
Reply
04/22/2013 at 05:30 PM

---
**内容**: vyx01695 said...
Guys..
My friend ask me to help on his concern regarding tracking events on the elements..
I found this solutions..
but how could i integrate it on my revit application..
I know a little bit in c# but not much how to integrate it..
The objective is how to integrate that code in Revit to trace the changes
Thanks best regards.
Vyx
Reply
09/03/2014 at 12:35 AM

---
**内容**: Augusto Goncalves said in reply to vyx01695...
Vyx,
This post applies to AutoCAD, not to Revit.
For Revit, there is an event called DocumentChanged that is similar: http://knowledge.autodesk.com/support/revit-products/downloads/caas/CloudHelp/cloudhelp/2015/ENU/Revit-API/files/GUID-288EF636-4EBF-4B5D-8E3F-246C810C2720-htm.html
Regards,
Augusto Goncalves
Reply
09/03/2014 at 07:56 AM

---
**内容**: Alexander said...
Guys,
Are you aware of the status of EnteringQuiescentState in AutoCAD 2015 - the code that appended the reactor
currentDocument.Editor.EnteringQuiescentState += new System.EventHandler(OnEnteringQuiescentState);
and was working fine in 2013/2014 now throwing an eDuplicatedKey exception?
Thank you
=Alexander
Reply
12/03/2014 at 05:50 PM

---
**内容**: Augusto Goncalves said in reply to Alexander...
Alexander,
I'm trying this code on my end and it's working fine. Is there any other step to repro? Also, can post the question on our forum?
Thanks!
Regards,
Augusto Goncalves
Reply
12/08/2014 at 12:52 PM

---
