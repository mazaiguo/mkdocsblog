---
title: VS自定义项目模板,使用模板导出再处理
date: 2025-04-15
categories:
  - 开发工具
  - windows程序
tags:
  - Visual Studio
  - 项目模板
description: Visual Studio中创建自定义项目模板的详细步骤和使用方法
author: JerryMa
---

# Vs自定义项目模板

![image-20250415192756364](http://image.jerryma.xyz//images/20250416-image-20250415192756364.png)

## 先配置好项目相关文件

## 导出项目相关文件

![image-20250415192839962](http://image.jerryma.xyz//images/20250416-image-20250415192839962.png)

## 导出为项目

![image-20250415193017914](http://image.jerryma.xyz//images/20250416-image-20250415193017914.png)

![image-20250415193036748](http://image.jerryma.xyz//images/20250416-image-20250415193036748.png)

![image-20250415193112362](http://image.jerryma.xyz//images/20250416-image-20250415193112362.png)

取消，需要对压缩文件进行处理

## 处理压缩包

![image-20250415193410753](http://image.jerryma.xyz//images/20250416-image-20250415193410753.png)

修改数据

![img](http://image.jerryma.xyz//images/20250416-950dd7f78194bd3a51d761a83dfa5434.png)

## 修改完成后将压缩包放置到`Visual Studio 2022\Templates\ProjectTemplates`中

```
Visual Studio 2022\Templates\ProjectTemplates
```

![image-20250415193604984](http://image.jerryma.xyz//images/20250416-image-20250415193604984.png)

```
MyTemplate.vstemplate
<VSTemplate Version="3.0.0" xmlns="http://schemas.microsoft.com/developer/vstemplate/2005" Type="Project">
  <TemplateData>
    <Name>ZwObjectZrxNet</Name>
    <Description>ObjectZRX+WPF模板</Description>
    <ProjectType>CSharp</ProjectType>
    <ProjectSubType>
    </ProjectSubType>
    <SortOrder>1000</SortOrder>
    <CreateNewFolder>true</CreateNewFolder>
    <DefaultName>ZwObjectZrxNet</DefaultName>
    <ProvideDefaultName>true</ProvideDefaultName>
    <LocationField>Enabled</LocationField>
    <EnableLocationBrowseButton>true</EnableLocationBrowseButton>
    <Icon>__TemplateIcon.ico</Icon>
    <PreviewImage>__PreviewImage.ico</PreviewImage>
    <LanguageTag>CSharp</LanguageTag>
    <PlatformTag>Windows</PlatformTag>
    <ProjectTypeTag>Library</ProjectTypeTag>
  </TemplateData>
  <TemplateContent>
    <Project TargetFileName="$safeprojectname$.csproj" File="$safeprojectname$.csproj" ReplaceParameters="true">
      <ProjectItem ReplaceParameters="true" TargetFileName="app.config">app.config</ProjectItem>
      <ProjectItem ReplaceParameters="true" TargetFileName="Commands.cs">Commands.cs</ProjectItem>
      <Folder Name="Controls" TargetFolderName="Controls" />
      <Folder Name="Converters" TargetFolderName="Converters">
        <ProjectItem ReplaceParameters="true" TargetFileName="OptionToBooleanConverter.cs">OptionToBooleanConverter.cs</ProjectItem>
      </Folder>
      <Folder Name="Models" TargetFolderName="Models" />
      <ProjectItem ReplaceParameters="true" TargetFileName="packages.config">packages.config</ProjectItem>
      <ProjectItem ReplaceParameters="true" TargetFileName="PlugInApplication.cs">PlugInApplication.cs</ProjectItem>
      <Folder Name="Properties" TargetFolderName="Properties">
        <ProjectItem ReplaceParameters="true" TargetFileName="AssemblyInfo.cs">AssemblyInfo.cs</ProjectItem>
      </Folder>
      <Folder Name="Styles" TargetFolderName="Styles">
        <ProjectItem ReplaceParameters="true" TargetFileName="Styles.xaml">Styles.xaml</ProjectItem>
      </Folder>
      <Folder Name="ViewModel" TargetFolderName="ViewModel">
        <ProjectItem ReplaceParameters="true" TargetFileName="WpfDemoViewModel.cs">WpfDemoViewModel.cs</ProjectItem>
      </Folder>
      <Folder Name="Views" TargetFolderName="Views">
        <ProjectItem ReplaceParameters="true" TargetFileName="WpfDemo.xaml">WpfDemo.xaml</ProjectItem>
        <ProjectItem ReplaceParameters="true" TargetFileName="WpfDemo.xaml.cs">WpfDemo.xaml.cs</ProjectItem>
      </Folder>
    </Project>
  </TemplateContent>
</VSTemplate>
```

Csharp

```
$safeprojectname$.csproj
<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="15.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <Import Project="$(MSBuildExtensionsPath)\$(MSBuildToolsVersion)\Microsoft.Common.props" Condition="Exists('$(MSBuildExtensionsPath)\$(MSBuildToolsVersion)\Microsoft.Common.props')" />
  <PropertyGroup>
    <Configuration Condition=" '$(Configuration)' == '' ">Debug</Configuration>
    <Platform Condition=" '$(Platform)' == '' ">AnyCPU</Platform>
    <ProjectGuid>{$guid1$}</ProjectGuid>
    <OutputType>Library</OutputType>
    <AppDesignerFolder>Properties</AppDesignerFolder>
    <RootNamespace>$safeprojectname$</RootNamespace>
    <AssemblyName>$safeprojectname$</AssemblyName>
    <TargetFrameworkVersion>v4.7</TargetFrameworkVersion>
    <FileAlignment>512</FileAlignment>
    <Deterministic>true</Deterministic>
    <ProjectTypeGuids>{60dc8134-eba5-43b8-bcc9-bb4bc16c2548};{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}</ProjectTypeGuids>
    <NuGetPackageImportStamp>
    </NuGetPackageImportStamp>
  </PropertyGroup>
  <PropertyGroup Condition=" '$(Configuration)|$(Platform)' == 'Debug|AnyCPU' ">
    <DebugSymbols>true</DebugSymbols>
    <DebugType>full</DebugType>
    <Optimize>false</Optimize>
    <OutputPath>bin\Debug\</OutputPath>
    <DefineConstants>DEBUG;TRACE</DefineConstants>
    <ErrorReport>prompt</ErrorReport>
    <WarningLevel>4</WarningLevel>
  </PropertyGroup>
  <PropertyGroup Condition=" '$(Configuration)|$(Platform)' == 'Release|AnyCPU' ">
    <DebugType>pdbonly</DebugType>
    <Optimize>true</Optimize>
    <OutputPath>bin\Release\</OutputPath>
    <DefineConstants>TRACE</DefineConstants>
    <ErrorReport>prompt</ErrorReport>
    <WarningLevel>4</WarningLevel>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)' == 'Debug|x64'">
    <DebugSymbols>true</DebugSymbols>
    <OutputPath>..\..\Out\Debug\bin\x64\</OutputPath>
    <DefineConstants>DEBUG;TRACE</DefineConstants>
    <DebugType>full</DebugType>
    <PlatformTarget>x64</PlatformTarget>
    <LangVersion>7.3</LangVersion>
    <ErrorReport>prompt</ErrorReport>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)' == 'Release|x64'">
    <OutputPath>..\..\Out\Release\bin\x64\</OutputPath>
    <DefineConstants>TRACE</DefineConstants>
    <Optimize>true</Optimize>
    <DebugType>pdbonly</DebugType>
    <PlatformTarget>x64</PlatformTarget>
    <LangVersion>7.3</LangVersion>
    <ErrorReport>prompt</ErrorReport>
  </PropertyGroup>
  <ItemGroup>
    <Reference Include="CommunityToolkit.Mvvm, Version=8.4.0.0, Culture=neutral, PublicKeyToken=4aff67a105548ee2, processorArchitecture=MSIL">
      <HintPath>..\packages\CommunityToolkit.Mvvm.8.4.0\lib\netstandard2.0\CommunityToolkit.Mvvm.dll</HintPath>
    </Reference>
    <Reference Include="MaterialDesignColors, Version=5.2.1.0, Culture=neutral, PublicKeyToken=df2a72020bd7962a, processorArchitecture=MSIL">
      <HintPath>..\packages\MaterialDesignColors.5.2.1\lib\net462\MaterialDesignColors.dll</HintPath>
    </Reference>
    <Reference Include="MaterialDesignThemes.Wpf, Version=5.2.1.0, Culture=neutral, PublicKeyToken=df2a72020bd7962a, processorArchitecture=MSIL">
      <HintPath>..\packages\MaterialDesignThemes.5.2.1\lib\net462\MaterialDesignThemes.Wpf.dll</HintPath>
    </Reference>
    <Reference Include="Microsoft.Bcl.AsyncInterfaces, Version=8.0.0.0, Culture=neutral, PublicKeyToken=cc7b13ffcd2ddd51, processorArchitecture=MSIL">
      <HintPath>..\packages\Microsoft.Bcl.AsyncInterfaces.8.0.0\lib\net462\Microsoft.Bcl.AsyncInterfaces.dll</HintPath>
    </Reference>
    <Reference Include="Microsoft.Xaml.Behaviors, Version=1.1.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a, processorArchitecture=MSIL">
      <HintPath>..\packages\Microsoft.Xaml.Behaviors.Wpf.1.1.39\lib\net45\Microsoft.Xaml.Behaviors.dll</HintPath>
    </Reference>
    <Reference Include="PresentationCore" />
    <Reference Include="PresentationFramework" />
    <Reference Include="System.Buffers, Version=4.0.4.0, Culture=neutral, PublicKeyToken=cc7b13ffcd2ddd51, processorArchitecture=MSIL">
      <HintPath>..\packages\System.Buffers.4.6.0\lib\net462\System.Buffers.dll</HintPath>
    </Reference>
    <Reference Include="System.ComponentModel.Annotations, Version=4.2.1.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a, processorArchitecture=MSIL">
      <HintPath>..\packages\System.ComponentModel.Annotations.5.0.0\lib\net461\System.ComponentModel.Annotations.dll</HintPath>
    </Reference>
    <Reference Include="System.ComponentModel.DataAnnotations" />
    <Reference Include="System.Drawing" />
    <Reference Include="System.Memory, Version=4.0.2.0, Culture=neutral, PublicKeyToken=cc7b13ffcd2ddd51, processorArchitecture=MSIL">
      <HintPath>..\packages\System.Memory.4.6.0\lib\net462\System.Memory.dll</HintPath>
    </Reference>
    <Reference Include="System.Numerics" />
    <Reference Include="System.Numerics.Vectors, Version=4.1.5.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a, processorArchitecture=MSIL">
      <HintPath>..\packages\System.Numerics.Vectors.4.6.0\lib\net462\System.Numerics.Vectors.dll</HintPath>
    </Reference>
    <Reference Include="System.Runtime.CompilerServices.Unsafe, Version=6.0.1.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a, processorArchitecture=MSIL">
      <HintPath>..\packages\System.Runtime.CompilerServices.Unsafe.6.1.0\lib\net462\System.Runtime.CompilerServices.Unsafe.dll</HintPath>
    </Reference>
    <Reference Include="System.Threading.Tasks.Extensions, Version=4.2.0.1, Culture=neutral, PublicKeyToken=cc7b13ffcd2ddd51, processorArchitecture=MSIL">
      <HintPath>..\packages\System.Threading.Tasks.Extensions.4.5.4\lib\net461\System.Threading.Tasks.Extensions.dll</HintPath>
    </Reference>
    <Reference Include="System.Windows.Forms" />
    <Reference Include="System.Xaml" />
    <Reference Include="WindowsBase" />
    <Reference Include="WindowsFormsIntegration" />
    <Reference Include="ZcCui">
      <HintPath>$(ZrxSdk2025)\inc\ZcCui.dll</HintPath>
      <Private>False</Private>
    </Reference>
    <Reference Include="ZcWindows">
      <HintPath>$(ZrxSdk2025)\inc\ZcWindows.dll</HintPath>
      <Private>False</Private>
    </Reference>
    <Reference Include="ZdWindows">
      <HintPath>$(ZrxSdk2025)\inc\ZdWindows.dll</HintPath>
      <Private>False</Private>
    </Reference>
    <Reference Include="ZwDatabaseMgd">
      <HintPath>$(ZrxSdk2025)\inc\ZwDatabaseMgd.dll</HintPath>
      <Private>False</Private>
    </Reference>
    <Reference Include="ZwDatabaseMgdBrep">
      <HintPath>$(ZrxSdk2025)\inc\ZwDatabaseMgdBrep.dll</HintPath>
      <Private>False</Private>
    </Reference>
    <Reference Include="ZwManaged">
      <HintPath>$(ZrxSdk2025)\inc\ZwManaged.dll</HintPath>
      <Private>False</Private>
    </Reference>
    <Reference Include="System" />
    <Reference Include="System.Core" />
    <Reference Include="System.Xml.Linq" />
    <Reference Include="System.Data.DataSetExtensions" />
    <Reference Include="Microsoft.CSharp" />
    <Reference Include="System.Data" />
    <Reference Include="System.Net.Http" />
    <Reference Include="System.Xml" />
  </ItemGroup>
  <ItemGroup>
    <Compile Include="Commands.cs" />
    <Compile Include="Converters\OptionToBooleanConverter.cs" />
    <Compile Include="PlugInApplication.cs" />
    <Compile Include="Properties\AssemblyInfo.cs" />
    <Compile Include="ViewModel\WpfDemoViewModel.cs" />
    <Compile Include="Views\WpfDemo.xaml.cs">
      <DependentUpon>WpfDemo.xaml</DependentUpon>
    </Compile>
  </ItemGroup>
  <ItemGroup>
    <Folder Include="Controls\" />
    <Folder Include="Models\" />
  </ItemGroup>
  <ItemGroup>
    <Page Include="Styles\Styles.xaml">
      <SubType>Designer</SubType>
      <Generator>MSBuild:Compile</Generator>
    </Page>
    <Page Include="Views\WpfDemo.xaml">
      <SubType>Designer</SubType>
      <Generator>MSBuild:Compile</Generator>
    </Page>
  </ItemGroup>
  <ItemGroup>
    <None Include="app.config" />
    <None Include="packages.config" />
  </ItemGroup>
  <Import Project="$(MSBuildToolsPath)\Microsoft.CSharp.targets" />
  <Import Project="..\packages\MaterialDesignThemes.5.2.1\build\MaterialDesignThemes.targets" Condition="Exists('..\packages\MaterialDesignThemes.5.2.1\build\MaterialDesignThemes.targets')" />
  <Target Name="EnsureNuGetPackageBuildImports" BeforeTargets="PrepareForBuild">
    <PropertyGroup>
      <ErrorText>这台计算机上缺少此项目引用的 NuGet 程序包。使用“NuGet 程序包还原”可下载这些程序包。有关更多信息，请参见 http://go.microsoft.com/fwlink/?LinkID=322105。缺少的文件是 {0}。</ErrorText>
    </PropertyGroup>
    <Error Condition="!Exists('..\packages\MaterialDesignThemes.5.2.1\build\MaterialDesignThemes.targets')" Text="$([System.String]::Format('$(ErrorText)', '..\packages\MaterialDesignThemes.5.2.1\build\MaterialDesignThemes.targets'))" />
    <Error Condition="!Exists('..\packages\CommunityToolkit.Mvvm.8.4.0\build\CommunityToolkit.Mvvm.targets')" Text="$([System.String]::Format('$(ErrorText)', '..\packages\CommunityToolkit.Mvvm.8.4.0\build\CommunityToolkit.Mvvm.targets'))" />
  </Target>
  <Import Project="..\packages\CommunityToolkit.Mvvm.8.4.0\build\CommunityToolkit.Mvvm.targets" Condition="Exists('..\packages\CommunityToolkit.Mvvm.8.4.0\build\CommunityToolkit.Mvvm.targets')" />
</Project>
```

Csharp

![image-20250416092345724](http://image.jerryma.xyz//images/20250416-image-20250416092345724.png)

![模版参数](http://image.jerryma.xyz//images/20250416-9f6e83371677e94b8af9e10ffa87bacb.png)