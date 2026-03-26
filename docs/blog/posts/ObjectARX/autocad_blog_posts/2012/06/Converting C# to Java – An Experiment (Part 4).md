---
title: "Converting C# to Java – An Experiment (Part 4)"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - C#
  - Migration
description: "(Links to previous installments: Part 1; Part 2; Part 3)."
author: Autodesk
---
# Converting C# to Java – An Experiment (Part 4)

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/converting-c-to-java-an-experiment-part-4.html

## 文章内容

By Stephen Preston
(Links to previous installments: Part 1; Part 2; Part 3).
Its time to hook up our migrated Item.java and PrioritizerCore.java classes to a simple Android UI. No bells and whistles - or even editing for that matter - just enough to display some items in a ListView.
The core of an Android app is an Activity. An Activity represents a single screen displayed by the Android app. The display you see on the screen is composed of View Groups and Views, and you transfer control between Activities by creating an Intent. Each app includes a manifest file, which documents the various components that make up the app. Read more about the Android basics here.
We've already created our basic Android Activity - when we created our Android project. This project was imaginatively named CSMigrationTest, and so our one and only Activity is called CSMigrationTestActivity:
The default code looks like this:
package Preston.Stephen.Prioritizer;
 
import android.app.Activity;
import android.os.Bundle;

public class CSMigrationTestActivity extends Activity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
    }
}
Notice the call to "setContentView(R.layout.main);" - this is creating our screen display. Go to the Eclipse Project Explorer and open the res->layout folder and you'll see a file called main.xml. This is the XML that describes the screen layout, and which is being referenced by SetContentView:
  Double-click on that file to open it. The window displaying the file has tabs at the bottom to switch between the XML view and the WYSIWYG editor view. Replace the existing XML with this:
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="fill_parent"
    android:layout_height="fill_parent"
    android:orientation="vertical" >
    <ListView
        android:id="@+id/ItemList"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" android:clickable="true">
    </ListView>
</LinearLayout>
This inserts a ListView in your default view. The WYSIWYG view now looks like this:
  If you've already setup your Android virtual machine or setup some real Android hardware for debugging, you can go ahead and test your app now, but it doesn't do anything yet. (I'll talk more about running the app once we've added some code).
To hook up a data source to a ListView, we use an Adapter class. An Adapter class is an interface between your data and the ListView. It retrieves the data item corresponding to an particular element in the List View, and it also provides the sub-View to be inserted in each element of the ListView. There are a number of pre-defined Adapters for various data types, but we're going to create a custom adapter derived from BaseAdapter.
(The simple Item class we're using could easily (and more simply) have been handled by storing items in a SQLite database and using a SimpleCursorAdaptor, but we're looking at the more general case of accesing data stored in a class and also migrating code from C#).
Right click on your package folder in the src folder and selct New...Class. In the dialog that appears, click the Browse button by the Superclass editbox and choose the BaseAdapter class
  Give the class a name (I called mine 'MyAdapter') and click 'Finish'.
Now open MyAdapter.java and replace the default code with the following:
package Preston.Stephen.Prioritizer;
 
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;
 
public class MyAdapter extends BaseAdapter {
  
  private PrioritizerCore m_prioritizer;
  private LayoutInflater m_inflater;
  private Context m_cxt;

  //Constructor - instantiates our PrioritizerCore class,
  // and also creates an Inflater class that we use to create sub-Views in the 
  // getView function.
  public MyAdapter(Context c) {
    m_cxt = c;
    m_prioritizer = new PrioritizerCore();
    m_inflater = (LayoutInflater)m_cxt.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
  }

  //Number of data items
  @Override
  public int getCount() {
    return m_prioritizer.getItemCount();
  }

  //Get item for a particular position
  @Override
  public Object getItem(int position) {
    return m_prioritizer.getAtIndex(position);
  }

  //Get row Id for a particular position in list its the same in this case
  @Override
  public long getItemId(int position) {
    return position;
  }

  //Return View to be used as sub-View for ListView element.
  //For efficiency, we re-use convertView if its not null.
  @Override
  public View getView(int position, View convertView, ViewGroup parent) {
    if (convertView == null) {
      convertView = m_inflater.inflate(R.layout.listentry, null);
    }
    //Load View with Item data
    TextView txtView = (TextView)convertView;
    Item i = m_prioritizer.getAtIndex(position);
    txtView.setTag(i);
    txtView.setText(i.getItemText());
    return txtView;
  }
  
  //These other functions have nothing to do with the ListView - they just relay
  // function calls to PrioritizerCore so our main Activity doesn't have to know 
  // about PrioritizerCore.
  
  public boolean add(String itemText) {
    return m_prioritizer.addItem(itemText);
  }
  
  public boolean hasPriorities() {
    return m_prioritizer.hasPriorities();
  }
  
  public void sort() {
    m_prioritizer.sort();
  }
  
}
There are certain base class functions we have to override. The overrides we've supplied are marked with the "@Override" annotation. The comments explain what's going on - it turns out that our Adapter is just a really shallow wrapper on top of what we'd already implemented in PrioritizerCore. We could have simply edited PrioritizerCore to derive from BaseAdapter and added the additional required functions, but we don't want to pollute our PrioritizerCore code with Android specific code - just like we avoided polluting our C# versopn with AutoCAD-specific code.
Once you've copied the above code, you'll see there's an error in it - because we've not yet created the 'listentry' layout the LayoutInflater uses to create the View. The LayoutInflator is simply using an XML layout definition to instantiate the corresponding Android View classes.
You'll recall that layouts are defined by XML files in the res->layout folder. Right click on that folder and seelct New->Android XML File, set the filename to 'listentry' and click Finish. Then open the XML file and replace the default XML with this:
<?xml version="1.0" encoding="utf-8"?>
<TextView xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="fill_parent"
    android:layout_height="fill_parent" android:textSize="20pt">
    android:text="Large Text" android:textAppearance="?android:attr/textAppearanceLarge" />
</TextView>
(The textSize and textAppearance attributes aren't required. I put them there to make the text appear at a reasonable size on my 10"tablet).
Now we have our Adapter defined, its time to go back to our Activity, hook the Adapter up to the ListView, and hardcode a few Items to put in the list. Open CSMigrationTestActivity.Java and replace the code you had with the code below:
package Preston.Stephen.Prioritizer;
 
import Preston.Stephen.Prioritizer.MyAdapter;
import Preston.Stephen.Prioritizer.R;
import android.app.Activity;
import android.os.Bundle;
import android.widget.ListView;

public class CSMigrationTestActivity extends Activity {
    /** Called when the activity is first created. */
  
  //Member variables
  ListView m_listView;
  MyAdapter m_adapter;
  
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        //Store ListView for this activity in a member variable for convenience 
        m_listView = (ListView)this.findViewById(R.id.ItemList); 
        //Create our Adapter and attach it to our ListView
        m_adapter = new MyAdapter(this);
        m_listView.setAdapter(m_adapter);
        //Add some items to the list
        m_adapter.add("Fix the roof");        
        m_adapter.add("Paint the spare bedroom");        
        m_adapter.add("Paint the house exterior");
        m_adapter.add("Dig up the lawn");
        m_adapter.add("Build a fence");
    }
}
All this code is doing so far is adding five items to our list (via MyAdapter.add). We've not implemented any of the functionality we need to add/edit/or remove items from the list, or to set priorities, or to sort by priority. But this post is getting quite long now so it's time to run this code in the debugger to make sure it works. 
If you don't have an Android device, then follow these instructions for creating a virtual device. If you have an Android phone or tablet, then you may prefer to setup your hardware for debugging instead. I'm using an Asus Transformer Pad TF300 for debugging. I find that debugging on a hardware device is a lot faster than using the software emulator. And when I read the instructions on setting up the device for debugging, I was really pleased I'd arbitrarily decided to install Eclipse on my MacOS, and not on my Windows partition, because of the text I've highlighted in the Android hardware setup instructions I've copied below:
Set up your system to detect your device.
If you're developing on Windows, you need to install a USB driver for adb. For an installation guide and links to OEM drivers, see the OEM USB Drivers document.
If you're developing on Mac OS X, it just works. Skip this step.
If you're developing on Ubuntu Linux, you need to add a udev rules file that contains a USB configuration for each type of device you want to use for development. In the rules file, each device manufacturer is identified by a unique vendor ID, as specified by the ATTR{idVendor} property. For a list of vendor IDs, see USB Vendor IDs, below. To set up device detection on Ubuntu Linux:
(Gopinath was really unhappy when I told him this. He has a MacBook, but decided to use Windows for his Android debugging. He spent ages finding and installing the right driver for his device :-). 
Whatever device you do use, make sure you selected a compatible Android SDK version when you first created your project. My Tablet is running Ice Cream Sandwich, so I just chose the the latest API (level 15) for mine.
To Run or Debug your app, right click on your project in the Package Explorer, and select either Run As... or Debug As... and then Android Application.


If you've setup your hardware or virtual device correctly, your app should be loaded to the device ready to use. (BTW I've noticed that I often have to perform the Run As or Debug As operation twice before my app gets loaded onto the device - I'm not sure if that's a bug or something I'm doing wrong).
Start up the app on the device and it will look something like this:

(I'm using the emulator here because I had to take a screenshot. The text is very big because I deliberately hardcoded large text in listentry.xml so it would be a reasonable size on my 10" tablet. I've not made any allowance for smaller screen sizes so it looks a bit cramped on the default emulator screen size).
You can click on an item on the list and it will be highlighted, but we've not implemented any code to respond to those clicks yet. That's what we'll look at next time.

