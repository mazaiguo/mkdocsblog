---
title: "Integrating AutoCAD with Twitter using RESTSharp – Part 1"
date: 2013-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Unicode
description: "In my last posts on integrating AutoCAD with Evernote I mentioned that, with hindsight, I would have preferred to start my experimentation using a ..."
author: Autodesk
---
# Integrating AutoCAD with Twitter using RESTSharp – Part 1

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/integrating-autocad-with-twitter-using-restsharp-part-1.html

## 文章内容

By Stephen Preston
In my last posts on integrating AutoCAD with Evernote I mentioned that, with hindsight, I would have preferred to start my experimentation using a REST API that allows Out Of Band authentication. The Twitter API allows that, so I decided to move to Twitter for my next experiments.
The downside of this is that I had to create a Twitter account for myself ;-).
I also mentioned an interesting .NET library I’d found called RESTSharp, so I’m going to use that in this post to construct my REST calls. I’m leaving authentication until a later post so I can focus for now on learning the RESTSharp basics.
First, let’s compare the code for making the same REST call using ‘standard’ .NET Framework classes (HttpWebRequest and HttpWebResponse) and with RESTSharp. I’m using synchronous calls for simplicity.
In the following example, I’m using the Wolfram Alpha API, because I was originally considering writing an app to integrate Wolfram Alpha with AutoCAD, but changed to the Twitter API because Wolfram Alpha doesn’t require OAuth (and I couldn’t think of something useful to do with it :-). I’m running a query on the search term ‘copper’ and filtering for output that is an image (not plaintext or HTML).
Here is the ‘standard’ .NET code:
      public static void test1()
      {
        HttpWebRequest req =
          WebRequest.Create(http://api.wolframalpha.com/v2/query?input=copper&format=image&appid=XXXX)
            as HttpWebRequest;
          HttpWebResponse response = req.GetResponse()
                  as HttpWebResponse;   
        StreamReader reader =
            new StreamReader(response.GetResponseStream());
        String result = reader.ReadToEnd();
        response.Close();
        //I'm not doing anything with the result
      }
And here is the same call made using RESTSharp:
      [CommandMethod("TEST2")]
      public static void test2()
      {
        String query = "input=copper&format=image";
        var client = new RestClient("http://api.wolframalpha.com");
        var request = new RestRequest("v2/query");
        request.AddParameter("input", "copper");
        request.AddParameter("format", "image");
        request.AddParameter("appid", "XXXX");
          IRestResponse response = client.Execute(request);
        String result = response.Content;
        //I'm not doing anything with the result
      }
In both examples, I’ve replaced my personal API key with XXXX – you’ll have to request your own from Wolfram if you want to run the sample code.
When making a single REST API call (and especially when not doing anything with the response from the REST API call) there’s not really than much benefit in using RESTSharp, But it should be immediately obvious that the way RESTSharp separates the base URL, the ‘resource’ path, and the query parameters will make it much easier to use for any more involved use of the REST APIs from a particular vendor. That’s just the very basics of RESTSharp – you’ll see a bit more in the next code snippet.
In case you’re interested, the data returned from those calls looks like this:
<?xml version="1.0" encoding="UTF-8" ?>
- <queryresult success="true" error="false" numpods="12" datatypes="Element,Isotope,MatterPhase" timedout="" timedoutpods="" timing="4.332" parsetiming="0.19" parsetimedout="false" recalculate="" id="MSPa57731a4ede43c16dc15i00003bbd6a0ie8322b62" auth="" host="http://www4c.wolframalpha.com" server="47" related="http://www4c.wolframalpha.com/api/v2/relatedQueries.jsp?id=MSPa57741a4ede43c16dc15i00000d5gg8c35075hf5a&s=47" version="2.6">
- <pod title="Input interpretation" scanner="Identity" id="Input" position="100" error="false" numsubpods="1">
- <subpod title="">
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57751a4ede43c16dc15i00002h5e5bhid39c20a3?MSPStoreType=image/gif&s=47" alt="copper (chemical element)" title="copper (chemical element)" width="177" height="18" />
  </subpod>
  </pod>
- <pod title="Periodic table location" scanner="Data" id="PeriodicTableLocation:ElementData" position="200" error="false" numsubpods="1">
- <subpod title="">
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57761a4ede43c16dc15i00005f7e7hhe6b9ccdi2?MSPStoreType=image/gif&s=47" alt="" title="" width="320" height="240" />
  </subpod>
  </pod>
- <pod title="Image" scanner="Data" id="Image:ElementData" position="300" error="false" numsubpods="1">
- <subpod title="">
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57771a4ede43c16dc15i000045i9i9h8i4h9gifb?MSPStoreType=image/gif&s=47" alt="" title="" width="150" height="150" />
  </subpod>
  </pod>
- <pod title="Basic elemental properties" scanner="Data" id="Elemental2:ElementData" position="400" error="false" numsubpods="1">
- <subpod title="">
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57781a4ede43c16dc15i000044g5ei51d6a52168?MSPStoreType=image/gif&s=47" alt="symbol | Cu atomic number | 29 atomic weight | 63.546" title="symbol | Cu atomic number | 29 atomic weight | 63.546" width="193" height="100" />
  </subpod>
- <states count="1">
  <state name="More" input="Elemental2:ElementData__More" />
  </states>
  </pod>
- <pod title="Thermodynamic properties" scanner="Data" id="Thermal:ElementData" position="500" error="false" numsubpods="1">
- <subpod title="">
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57791a4ede43c16dc15i00006415584gib5816de?MSPStoreType=image/gif&s=47" alt="phase at STP | solid melting point | 1084.62 °C (rank: 43rd) boiling point | 2927 °C (rank: 35th) (properties at standard conditions)" title="phase at STP | solid melting point | 1084.62 °C (rank: 43rd) boiling point | 2927 °C (rank: 35th) (properties at standard conditions)" width="280" height="121" />
  </subpod>
- <states count="2">
  <state name="More" input="Thermal:ElementData__More" />
  <state name="Use Fahrenheit" input="Thermal:ElementData__Use Fahrenheit" />
  </states>
  </pod>
- <pod title="Material properties" scanner="Data" id="Material:ElementData" position="600" error="false" numsubpods="1">
- <subpod title="">
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57801a4ede43c16dc15i00006a58b54e855cgc31?MSPStoreType=image/gif&s=47" alt="density | 8.96 g/cm^3 (rank: 33rd) Mohs hardness | 3 (~~ calcite) Young's modulus | 130 GPa (rank: 16th) sound speed | 3570 m/s (rank: 25th) thermal expansion | 1.65×10^-5 K^(-1) (rank: 18th) thermal conductivity | 400 W/(m K) (rank: 2nd) (properties at standard conditions)" title="density | 8.96 g/cm^3 (rank: 33rd) Mohs hardness | 3 (~~ calcite) Young's modulus | 130 GPa (rank: 16th) sound speed | 3570 m/s (rank: 25th) thermal expansion | 1.65×10^-5 K^(-1) (rank: 18th) thermal conductivity | 400 W/(m K) (rank: 2nd) (properties at standard conditions)" width="356" height="217" />
  </subpod>
- <states count="1">
  <state name="More" input="Material:ElementData__More" />
  </states>
- <infos count="1">
- <info>
- <units count="5">
  <unit short="g/cm^3" long="grams per cubic centimeter" />
  <unit short="GPa" long="gigapascals" />
  <unit short="K^(-1)" long="reciprocal kelvins difference" />
  <unit short="m/s" long="meters per second" />
  <unit short="W/(m K)" long="watts per meter kelvin difference" />
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57811a4ede43c16dc15i00003hhec830bcfdbc64?MSPStoreType=image/gif&s=47" width="262" height="116" />
  </units>
  </info>
  </infos>
  </pod>
- <pod title="Electromagnetic properties" scanner="Data" id="Electromagnetic:ElementData" position="700" error="false" numsubpods="1">
- <subpod title="">
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57821a4ede43c16dc15i00004be6027g0g3bfbi6?MSPStoreType=image/gif&s=47" alt="electrical type | conductor resistivity | 1.7×10^-8 Omega m (ohm meters) magnetic type | diamagnetic color | (copper)" title="electrical type | conductor resistivity | 1.7×10^-8 Omega m (ohm meters) magnetic type | diamagnetic color | (copper)" width="320" height="132" />
  </subpod>
- <states count="1">
  <state name="More" input="Electromagnetic:ElementData__More" />
  </states>
  </pod>
- <pod title="Reactivity" scanner="Data" id="Chemical:ElementData" position="800" error="false" numsubpods="1">
- <subpod title="">
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57831a4ede43c16dc15i000069c59867ceb435gf?MSPStoreType=image/gif&s=47" alt="valence | 2 electronegativity | 1.9 electron affinity | 1.227 eV (molar electronvolts) ionization energies | 7.727 eV | ..." title="valence | 2 electronegativity | 1.9 electron affinity | 1.227 eV (molar electronvolts) ionization energies | 7.727 eV | ..." width="365" height="132" />
  </subpod>
- <states count="3">
  <state name="Show energy plot" input="Chemical:ElementData__Show energy plot" />
  <state name="Show all energies" input="Chemical:ElementData__Show all energies" />
  <state name="Show metric" input="Chemical:ElementData__Show metric" />
  </states>
- <infos count="1">
- <info>
- <units count="1">
  <unit short="eV" long="molar electronvolts" />
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57841a4ede43c16dc15i000031gf8bh0h0ei2265?MSPStoreType=image/gif&s=47" width="165" height="26" />
  </units>
  </info>
  </infos>
  </pod>
- <pod title="Atomic properties" scanner="Data" id="Atomic:ElementData" position="900" error="false" numsubpods="1">
- <subpod title="">
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57851a4ede43c16dc15i00005658580g7b61hi3g?MSPStoreType=image/gif&s=47" alt="term symbol | ^2S_(1/2) atomic radius | 135 pm (electronic ground state properties)" title="term symbol | ^2S_(1/2) atomic radius | 135 pm (electronic ground state properties)" width="191" height="91" />
  </subpod>
- <states count="2">
  <state name="More" input="Atomic:ElementData__More" />
  <state name="Spectrum" input="Atomic:ElementData__Spectrum" />
  </states>
- <infos count="1">
- <info>
- <units count="1">
  <unit short="pm" long="picometers" />
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57861a4ede43c16dc15i0000110h7h333bh70f56?MSPStoreType=image/gif&s=47" width="124" height="26" />
  </units>
  </info>
  </infos>
  </pod>
- <pod title="Abundances" scanner="Data" id="Abundance:ElementData" position="1000" error="false" numsubpods="1">
- <subpod title="">
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57871a4ede43c16dc15i000012e1cg07h2801h1i?MSPStoreType=image/gif&s=47" alt="universe abundance | 6×10^-6% (rank: 27th) crust abundance | 0.0068% (rank: 24th) human abundance | 1×10^-4% (rank: 20th)" title="universe abundance | 6×10^-6% (rank: 27th) crust abundance | 0.0068% (rank: 24th) human abundance | 1×10^-4% (rank: 20th)" width="318" height="100" />
  </subpod>
- <states count="1">
  <state name="Show atomic abundances" input="Abundance:ElementData__Show atomic abundances" />
  </states>
- <infos count="1">
- <info>
- <units count="1">
  <unit short="%" long="mass percent" />
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57881a4ede43c16dc15i00002iebd8d79b915338?MSPStoreType=image/gif&s=47" width="126" height="26" />
  </units>
  </info>
  </infos>
  </pod>
- <pod title="Nuclear properties" scanner="Data" id="Nuclear:ElementData" position="1100" error="false" numsubpods="1">
- <subpod title="">
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57891a4ede43c16dc15i00003045b3694i7ha1c8?MSPStoreType=image/gif&s=47" alt="half-life | (stable) stable isotopes | Cu-63 (69.17%) | Cu-65 (30.83%) unstable isotopes | Cu-67 (61.83 h) | ..." title="half-life | (stable) stable isotopes | Cu-63 (69.17%) | Cu-65 (30.83%) unstable isotopes | Cu-67 (61.83 h) | ..." width="379" height="100" />
  </subpod>
- <states count="2">
  <state name="More" input="Nuclear:ElementData__More" />
  <state name="All isotopes" input="Nuclear:ElementData__All isotopes" />
  </states>
- <infos count="1">
- <info>
- <units count="5">
  <unit short="h" long="hours" />
  <unit short="min" long="minutes" />
  <unit short="ms" long="milliseconds" />
  <unit short="ns" long="nanoseconds" />
  <unit short="s" long="seconds" />
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57901a4ede43c16dc15i00000f5ad28d4f2ea445?MSPStoreType=image/gif&s=47" width="140" height="110" />
  </units>
  </info>
  </infos>
  </pod>
- <pod title="Identifiers" scanner="Data" id="Identifier:ElementData" position="1200" error="false" numsubpods="1">
- <subpod title="">
  <img src="http://www4c.wolframalpha.com/Calculate/MSP/MSP57911a4ede43c16dc15i000065c1b63ch8526fd2?MSPStoreType=image/gif&s=47" alt="CAS number | 7440-50-8 PubChem CID number | 23978" title="CAS number | 7440-50-8 PubChem CID number | 23978" width="270" height="68" />
  </subpod>
  </pod>
- <assumptions count="1">
- <assumption type="Clash" word="copper" template="Assuming "${word}" is ${desc1}. Use as ${desc2} instead" count="5">
  <value name="Element" desc="a chemical element" input="*C.copper-_*Element-" />
  <value name="DietaryReference" desc="a dietary reference" input="*C.copper-_*DietaryReference-" />
  <value name="Color" desc="a color" input="*C.copper-_*Color-" />
  <value name="Language" desc="a language" input="*C.copper-_*Language-" />
  <value name="Word" desc="a word" input="*C.copper-_*Word-" />
  </assumption>
  </assumptions>
- <sources count="3">
  <source url="http://www.wolframalpha.com/sources/AtomicSpectrumDataSourceInformationNotes.html" text="Atomic spectrum data" />
  <source url="http://www.wolframalpha.com/sources/ElementDataSourceInformationNotes.html" text="Element data" />
  <source url="http://www.wolframalpha.com/sources/IsotopeDataSourceInformationNotes.html" text="Isotope data" />
  </sources>
  </queryresult>
Now let’s move on to the Twitter REST API. I decided to start off with something easy and use the Twitter search API, because this doesn’t require authentication. (I’ll look at a Twitter API that requires authentication next time). My test app asks the user to enter a search string on the AutoCAD commandline and then display the five most recent (English) tweets that match that search string.
Here is the code. If you add this to your own project, you’ll have to also reference the RESTSharp assembly. (I’ll leave it as an exercise for the reader to add error handling ;-).
using System;
using System.Collections.Generic;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.EditorInput;
using RestSharp;
  //Twitter search documentation:
// https://dev.twitter.com/docs/api/1/get/search
//RestSharp documentation:
// https://github.com/restsharp/RestSharp/wiki
  namespace AcadTwitterTest1
{
    public class TwitterTestClass
    {
      //Number of requests to return per page
      private const string k_rpp = "5";
      //REturn most recent requests
      private const string k_result_type = "recent";
      //Base and resource URLs.
      // Used to create RestSharp objects
      private const string k_BaseUrl = "http://search.twitter.com";
      private const string k_RequestUrl = "search.json";
        [CommandMethod("SEARCHTWEETS")]
      public static void test()
      {
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        //Ask user to enter search string
        PromptStringOptions opts = new PromptStringOptions("\nEnter Twitter search text:");
        opts.AllowSpaces = true;
        PromptResult res = ed.GetString(opts);
        if (res.Status != PromptStatus.OK)
          return;
        string strQuery = res.StringResult.Trim();
        if (strQuery == "")
          return;
        //Build Twitter search query
        //Query URL is of form:
        // http://search.twitter.com/search.json?q=strQuery&rpp=k_rpp&result_type=k_result_type
        var client = new RestClient(k_BaseUrl);
        var request = new RestRequest("search.json");
        request.AddParameter("q", strQuery);
        request.AddParameter("rpp", k_rpp);
        request.AddParameter("result_type", k_result_type);
        request.AddParameter("lang", "en");
        //Response is returned as JSON.
        //This call uses JSON Deserializer and classes I've defined below
        // (TwitterResponse, TwitterResult, and TwitterMetaData)
        // to populate response.Data for easy access.
        RestResponse<TwitterResponse> response =
          client.Execute<TwitterResponse>(request)
                as RestResponse<TwitterResponse>;
        //If responses were returned, we display them on commandline
        // response.Data is now populated with the Twitter* classes I defined below
        if (response.Data.results.Count == 0)
        {
          ed.WriteMessage("\nNo recent tweets match that search term.\n");
        }
        else
        {
          //Iterate all responses
          foreach (TwitterResult tRes in response.Data.results)
          {
            //Write to commandline
            ed.WriteMessage("\n" + tRes.from_user + " tweeted: " +
                tRes.text);
          }
          ed.WriteMessage("\n");
        }
      }
    }
    //The following class definitions are used by JSON Deserializer
  // Fields should be the same as the parameters in the returned JSON
  public class TwitterResponse
  {
    public double completed_in { get; set; }
    public long max_id { get; set; }
    public string max_id_str { get; set; }
    public string next_page { get; set; }
    public int page { get; set; }
    public string query { get; set; }
    public string refresh_url { get; set; }
    public List<TwitterResult> results { get; set; }
  }
    public class TwitterResult
  {
    public string created_at { get; set; }
    public string from_user { get; set; }
    public long from_user_id { get; set; }
    public string from_user_id_string { get; set; }
    public string geo { get; set; }
    public long id { get; set; }
    public string id_str { get; set; }
    public string iso_language_code { get; set; }
    public TwitterMetaData metadata {get; set;}
    public string profile_image_url { get; set; }
    public string source { get; set; }
    public string text { get; set; }
    public long to_user_id { get; set; }
    public string to_user_id_str { get; set; }
  }
    public class TwitterMetaData
  {
    public int recent_retweets { get; set; }
    public string result_type { get; set; }
  }
}
Being new to deserializers, I’m really impressed with the deserialization mechanism. (I know WCF has a similar mechanism).
My call to ‘client.Execute<TwitterResponse>(request)’ (marked in bold in the code above) deserializes the JSON-formatted response from the REST API call and populates response.Data with the classes I defined in my code (TwitterResponse, TwitterResult and TwitterMetaData) to match the JSON data structure. All I have to do is ensure that the fields in those classes match the fields in the JSON data. Then I use this deserialized data to greatly simplify accessing the part of the response that I want.
Very cool :-).
That’s all for this now. In this post I learned how easy it is to use the basic RESTSharp APIs to call a REST API, and to deserialize the response into an easy to use format. Next time I’ll look at a Twitter API that requires authentication to see how RESTSharp handles that.

