---
title: "Converting C# to Java – An Experiment (Part 2)"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - AutoCAD
  - C#
  - Plugin
description: "In part 1, I created a C# application for AutoCAD. Other than a small amount of logic/UI separation, I didn't do anything to make the code easier t..."
author: Autodesk
---
# Converting C# to Java – An Experiment (Part 2)

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/converting-c-to-java-an-experiment-part-1-1.html

## 文章内容

By Stephen Preston
In part 1, I created a C# application for AutoCAD. Other than a small amount of logic/UI separation, I didn't do anything to make the code easier to port to Java. (How could I? - I didn't know anything about Java!).
Next I'm going to take the core business logic and get it to compile as Java code. I'll migrate the Item class today, and PrioritizerCore in the next installment. I won't worry about any subtleties of how the code runs - testing and tweaking that will come later. And I'm going to migrate my C# to Java inside an Android app project.
The 'standard' development environment for Android is Eclipse. My main computer is an Apple MacBook Pro running BootCamp, so I have Eclipse Indigo installed on Mac OSX. Eclipse is also available for Windows. I chose to install the MacOS version partly because someone pointed out to me that most of the Google evangelists in their online screencast recordings are using MacBooks (so perhaps they care about the development experience a little more on MacOS ), but mostly because my Windows disk partition is almost full. This does have the disadvantage that I keep typing Ctrl-C to copy stuff instead of Command-C :-(.
I'm not going to document the steps for installing Eclipse and the Android SDK and ADT Plugin for Eclipse - you can find that here. Let's go straight into creating our project in Eclipse and adding/migrating our C# code to the.
In Eclipse, select File->New->Android Project and specify the Project name, Android SDK version, Application name and Package name. I also left the default choice to create an Activity, because we'll need that eventually when we start on our Android UI.



In the Eclipse Package Explorer, open the src-folder for your project, right-click on the <package> folder, and select New->Class.
In the New Class dialog, set the Name to Item, and keep all other settings at their default.


Do the same again to create a PrioritizerCore class. Then open each class in turn by double clicking on the file created in the Package Explorer and paste your C# code into the file (obviously you copy the Item class to the Item,java file, and PrioritizerCore to PrioritizerCore.java).
Don't copy the using statements at the top of the C# code.
Don't copy the C# namespace declaration and associated brackets.
Keep the 'package <namespace>;' line at the top of the Java file.
Now its time to start migrating the C# syntax to Java. We're only fixing the Item class today ...
Eclipse has some pretty good Intellisense. It highlights an error with a red symbol in the margin, and underlines the error. Hovering over the marked error will often display a tooltip offering options to automatically fix the error.
Our first error is right at the start of the class. My blog editor is more limited than Eclipse, so I'm highlighting errors in yellow. 
  [Serializable()]
  public class Item : IEquatable<Item>
Java doesn't recognize the C# attributes, but the same functionality is available by implementing the Serializable interface for a class. And Java doesn't have an equivalent of IEquatable. Fortunately we don't need it, so we can remove it. The fixed code looks like this:
  //[Serializable()]
  public class Item implements Serializable
Serializable will be underlined in red when you type it, but when you hover over it, the Intellisense tooltip gives you the option to import the java.io.Serializable package.
The next error is that I used 'string' (with a lowercase 's') in my C# code. The Java string class is 'String', so I next do a global search and replace of 'string' to 'String'.
Next is the .NET  'List<T>' class. I decided to replace this with the Java 'ArrayList<T>':
    private ArrayList<Item> m_BetterThanList;
I also imported the java.utils.ArrayList package and changed all other occurrences of List to ArrayList. (There is also a java.util.List class - can't recall now why I preferred ArrayList).
The next error is simple too - change all occurrences of the C# 'bool' type to the Java 'boolean' type.
Now we come to a more significant difference. Java doesn't have concept of properties as used in C#. Instead, you're expected to implement get and set functions. So this code:
    public String ItemText
    {
      get { return m_strItemText; }
      set { m_strItemText = value; }
    }
becomes
    public String getItemText() {
       return m_strItemText;
    }
    public void setItemText(String value) {
      m_strItemText = value; 
    }
Do that for all your C# properties.
The rest of the compilation errors in Item.java are due to another small syntax difference between .NET and Java. In .NET, method names all begin with uppercase characters, whereas in Java they all begin with lowercase.  The remaining errors are all for our ArrayList class - m_BetterThanList. Change the first character of the method calls flagged as errors to lowercase - with the exception of the Count property, which changes to 'size()', and '[index]', which changes to 'get(index)'.
Now there are two more changes to make before we're done.
Firstly, there is a 'warning' flag on the class declaration line. This is because it is recommended to implement a SerialVersionUID for a Serializable class. Use the Intellisense tooltip over the underlined-in-yellow 'Item' and select 'Add default serial version Id' to create:
    private static final long serialVersionUID = 1L;
Secondly, our C# of Item.Equals() finction was specifically implementing the .NET Iserializable<T>.Equals(T) method. Knowing how my code is going to end up, I change this function to instead override the java.lang.Object.Equals(Object) method (for which I've edited some boilerplate from the Java documentation, so it diverges more from the C# than it might have):
   @Override
    public boolean equals(Object o) {
      // Return true if the objects are identical.
      // (This is just an optimization, not required for correctness.)
      if (this == o) {
        return true;
      }
      // Return false if the other object has the wrong type.
      // This type may be an interface depending on the interface's specification.
      if (!(o instanceof Item)) {
        return false;
      }
      // Cast to the appropriate type.
      // This will succeed because of the instanceof, and lets us access private fields.
      Item lhs = (Item) o;
 
      // Items considered equal if their text is equal
      if (this.getItemText() == lhs.getItemText()) {
      //if (txt1 == txt2) {
        return true;
      }
      return false;
    }
That's our basic migration finished. I'll have to come back later and add a few bits and bobs because I'm going to implement a little more functionality in my Android app than I did in AutoCAD. Item.java now looks like this:
package Preston.Stephen.Prioritizer;
 
import java.io.Serializable;
import java.util.ArrayList;
 
  //Item class stores info on each item that you want to prioritize
  //Implements IEquatable interface so we can use this class with 
  // a custom comparator - see PrioritizerCore.Sort() method.
  //[Serializable()]
  public class Item implements Serializable
  {
 

    //The text describing this Item - also used to ensure uniqueness
    private String m_strItemText;
    //The list of Items this Item is more important than
    private ArrayList<Item> m_BetterThanList;

    //Constructor
    public Item()
    {
      m_BetterThanList = new ArrayList<Item>();
    }

    //For our  purposes, Items are equal if their names match
    @Override
    public boolean equals(Object o) {
      // Return true if the objects are identical.
      // (This is just an optimization, not required for correctness.)
      if (this == o) {
        return true;
      }
      // Return false if the other object has the wrong type.
      // This type may be an interface depending on the interface's specification.
      if (!(o instanceof Item)) {
        return false;
      }
      // Cast to the appropriate type.
      // This will succeed because of the instanceof, and lets us access private fields.
      Item lhs = (Item) o;

      // Items considered equal if their text is equal
      if (this.getItemText() == lhs.getItemText()) {
      //if (txt1 == txt2) {
        return true;
      }
      return false;
    }

    //Read-write property
    //The name of this Item
    public String getItemText() {
       return m_strItemText;
    }
    public void setItemText(String value) {
      m_strItemText = value; 
    }

    //Read-only property
    //Number of Items this Item is rated higher than
    // in binary comparisons
    public int getScore()
    {
      return m_BetterThanList.size();
    }

    //Returns true if item successfully added
    //Returns false if item was already in the list, or we try to add 
    // an Item to its own BetterThanList
    public boolean AddBetterThanItem(Item anItem)
    {
      if (anItem == this)
        return false;

      if (this.IsBetterThan(anItem))
      {
        return false;
      }
      else
      {
        m_BetterThanList.add(anItem);
        //If anItem had already been selected as better than this Item
        // then we remove this Item from anItem's BetterThan list
        if (anItem.IsBetterThan(this))
        {
          anItem.Remove(this);
        }
        return true;
      }
    }

    //Returns true if this Item is better than the supplied Item
    public boolean IsBetterThan(Item anItem)
    {
      return m_BetterThanList.contains(anItem);
    }

    //Removes an Item from the list
    //Returns true if successful, false if Item wasn't in list
    public boolean Remove(Item anItem)
    {
      return m_BetterThanList.remove(anItem);
    }

    //Returns Item at position 'index' in this Item's BetterThanList
    //Returns null if index is outside list bounds
    public Item GetBetterThanItem(int index)
    {
      if (index >= 0 & index < m_BetterThanList.size())
      {
        return m_BetterThanList.get(index);
      }
      else
      {
        return null;
      }
    }
  }
  That was a pretty easy migration from one language to another, and you can see why I'm recommending learning C# if you want to later extend your AutoCAD .NET skills to Android programming. If I were migrating VB.NET, I'd probably translate it to C# first.
Here is a summary of our findings so far:
'string' in C# becomes 'String' in Java - we cound have saved a search and replace by using String in C# too.
'bool' becomes 'boolean' - simple find and replace
.NET properties have to be rewritten in Java as get/set functions.
Java has a powerful Serialization mechanism - just like C#. But you enable it by implementing an interface instead of adding an attribute.
Java has template (generic) collection classes - just like C#. In this case, we used an ArrayList, where most of the method names are the same as in C# (but starting with a lowercase character).
See you next time with the additional migration steps for PrioritizerCore class ...

## 评论

**内容**: Marvil said...
hello...
I need to make an application for android autocad incorporating ...
Reply
02/13/2014 at 02:11 PM

---
**内容**: Madhukar Moogala said in reply to Marvil...
Are you talking about AutoCAD 360 Mobile for Android? (https://play.google.com/store/apps/details?id=com.autodesk.autocadws).
If so - sorry - this product does not curently expose an API.
If not - please would you provide more information on what you're looking for, because I don't understand the question?
Reply
02/13/2014 at 02:24 PM

---
