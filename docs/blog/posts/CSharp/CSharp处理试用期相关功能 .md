---
title: CSharp处理试用期相关功能
date: 2025-09-26
categories:
  - windows程序
tags:
  - CSharp
  - JSON
description: 该授权系统适用于试用版本管理，系统支持中英文切换的试用期功能，不适用于高安全级别的商业软件保护
author: JerryMa
---

# CSharp处理试用期相关功能

## TrialLicenseManager.cs

???success  "TrialLicenseManager"

    ```csharp
        namespace GalleryUI
        {
            /// <summary>
            /// 试用期授权管理器
            /// 提供完整的试用期管理功能，包括版本控制、硬件绑定、安全存储等
            /// </summary>
            public class TrialLicenseManager
            {
                #region 配置常量 - 在其他项目中使用时请修改这些值
    
                // ====== 项目配置 - 在新项目中使用时请修改以下常量 ======
                private const string PROJECT_NAME = "GalleryUI";           // 项目名称
                private const string PROJECT_SHORT_NAME = "glui";          // 项目短名称
                private const string COMPANY_NAME = "YourCompany";         // 公司名称
    
                // 版本管理 - 修改此版本号将自动重置所有用户的试用期
                private const string CURRENT_VERSION = "1.0.0";
                private const int TRIAL_DAYS = 30;                         // 试用天数
    
                // 语言设置 - true:英文, false:中文
                private const bool USE_ENGLISH = true;                    // 界面语言
                // ====== 项目配置结束 ======
    
                #endregion
    
                #region 系统常量定义 - 通常不需要修改
    
                private static readonly string REGISTRY_KEY = $@"SOFTWARE\{PROJECT_NAME}";
                private const string REGISTRY_KEY_BACKUP = @"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}\Count";
                private const string FIRST_RUN_VALUE = "FirstRunDate";
                private const string HARDWARE_ID_VALUE = "HardwareId";
                private const string ENCRYPTED_DATA_VALUE = "TrialData";
                private const string VERSION_VALUE = "Version";
                private static readonly string ENCRYPTION_KEY = $"{PROJECT_NAME}#{DateTime.Now.Year}#TrialProtection";
                private const string RESET_COMMAND = "RESET_TRIAL_2024";
    
                private static readonly string HIDDEN_FILE_PATH = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), 
                    $".{PROJECT_SHORT_NAME}", "trial.dat");
                private static readonly string BACKUP_FILE_PATH = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), 
                    "Temp", $".{PROJECT_SHORT_NAME}_t.tmp");
                private static readonly string RESET_FLAG_FILE = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.Desktop), 
                    $"RESET_{PROJECT_NAME.ToUpper()}_TRIAL.txt");
    
                #endregion
    
                #region 本地化字符串
    
                /// <summary>
                /// 获取本地化字符串
                /// </summary>
                private static string GetLocalizedString(string chineseText, string englishText)
                {
                    return USE_ENGLISH ? englishText : chineseText;
                }
    
                /// <summary>
                /// 清理版本字符串，移除无效字符防止乱码
                /// </summary>
                private static string CleanVersionString(string version)
                {
                    if (string.IsNullOrWhiteSpace(version))
                        return "Unknown";
    
                    var cleanChars = new System.Text.StringBuilder();
                    foreach (char c in version)
                    {
                        // 只保留可打印的ASCII字符、数字、点、连字符和下划线
                        if (char.IsLetterOrDigit(c) || c == '.' || c == '-' || c == '_' || c == ' ')
                        {
                            cleanChars.Append(c);
                        }
                    }
    
                    string cleaned = cleanChars.ToString().Trim();
                    return string.IsNullOrEmpty(cleaned) ? "Unknown" : cleaned;
                }
    
                /// <summary>
                /// 常用本地化消息
                /// </summary>
                private static class Messages
                {
                    public static string WelcomeMessage => GetLocalizedString(
                        $"欢迎使用 {PROJECT_NAME} {CURRENT_VERSION}！",
                        $"Welcome to {PROJECT_NAME} {CURRENT_VERSION}!");
    
                    public static string VersionUpdateMessage(string oldVersion, string newVersion)
                    {
                        // 清理版本字符串，防止乱码
                        string cleanOldVersion = CleanVersionString(oldVersion);
                        string cleanNewVersion = CleanVersionString(newVersion);
    
                        return GetLocalizedString(
                            $"检测到版本更新：{cleanOldVersion} → {cleanNewVersion}\n试用期已自动重置为30天，感谢您使用新版本！",
                            $"Version update detected: {cleanOldVersion} → {cleanNewVersion}\nTrial period has been reset to 30 days. Thank you for using the new version!");
                    }
    
                    public static string TrialResetMessage => GetLocalizedString(
                        "试用期已重置为30天！",
                        "Trial period has been reset to 30 days!");
    
                    public static string FirstRunMessage => GetLocalizedString(
                        $"欢迎使用！您有 {TRIAL_DAYS} 天的试用期。",
                        $"Welcome! You have {TRIAL_DAYS} days of trial period.");
    
                    public static string RemainingDaysMessage(int days) => GetLocalizedString(
                        $"试用期剩余 {days} 天，请及时联系开发商获取正式版本。",
                        $"Trial period remaining: {days} days. Please contact the developer for the full version.");
    
                    public static string TrialExpiredMessage => GetLocalizedString(
                        "试用期已过期！请联系开发商获取正式版本。\n\n插件将无法正常使用。",
                        "Trial period has expired! Please contact the developer for the full version.\n\nThe plugin will not function properly.");
    
                    public static string TrialErrorMessage(string error) => GetLocalizedString(
                        $"试用期检测出现错误：{error}",
                        $"Trial period detection error: {error}");
    
                    public static string TrialDataClearedMessage => GetLocalizedString(
                        $"试用期数据已清除，重置时间：{DateTime.Now:yyyy-MM-dd HH:mm:ss}",
                        $"Trial data cleared, reset time: {DateTime.Now:yyyy-MM-dd HH:mm:ss}");
    
                    public static string ResetErrorMessage(string error) => GetLocalizedString(
                        $"重置试用期时发生错误：{error}",
                        $"Error occurred while resetting trial period: {error}");
                }
    
                #endregion
    
                #region 试用期状态信息
    
                /// <summary>
                /// 试用期检查结果
                /// </summary>
                public class TrialResult
                {
                    /// <summary>
                    /// 是否在试用期内
                    /// </summary>
                    public bool IsValid { get; set; }
    
                    /// <summary>
                    /// 剩余天数
                    /// </summary>
                    public int RemainingDays { get; set; }
    
                    /// <summary>
                    /// 是否为首次运行
                    /// </summary>
                    public bool IsFirstRun { get; set; }
    
                    /// <summary>
                    /// 是否为版本升级
                    /// </summary>
                    public bool IsVersionUpgrade { get; set; }
    
                    /// <summary>
                    /// 旧版本号
                    /// </summary>
                    public string OldVersion { get; set; }
    
                    /// <summary>
                    /// 当前版本号
                    /// </summary>
                    public string CurrentVersion { get; set; }
    
                    /// <summary>
                    /// 提示消息
                    /// </summary>
                    public string Message { get; set; }
                }
    
                #endregion
    
                #region 公开方法
    
                /// <summary>
                /// 检查试用期状态
                /// </summary>
                /// <returns>试用期检查结果</returns>
                public static TrialResult CheckTrialPeriod()
                {
                    var result = new TrialResult
                    {
                        CurrentVersion = CURRENT_VERSION
                    };
    
                    try
                    {
                        // 检查是否需要重置试用期（手动重置）
                        if (CheckForTrialReset())
                        {
                            ResetTrialPeriod();
                            result.Message = Messages.TrialResetMessage;
                        }
    
                        // 检查版本号，如果版本不匹配则自动重置试用期
                        string storedVersion = GetStoredVersion();
                        if (!string.Equals(storedVersion, CURRENT_VERSION, StringComparison.OrdinalIgnoreCase))
                        {
                            result.IsVersionUpgrade = !string.IsNullOrEmpty(storedVersion);
                            result.OldVersion = storedVersion;
                            ResetTrialPeriod();
    
                            if (result.IsVersionUpgrade)
                            {
                                result.Message = Messages.VersionUpdateMessage(storedVersion, CURRENT_VERSION);
                            }
                            else
                            {
                                result.Message = Messages.WelcomeMessage;
                            }
                        }
    
                        // 获取硬件指纹
                        string hardwareId = GetHardwareFingerprint();
    
                        // 从多个位置读取试用信息
                        DateTime? registryDate = ReadFromRegistry();
                        DateTime? fileDate = ReadFromHiddenFile();
                        DateTime? backupDate = ReadFromBackupLocation();
    
                        // 检测时间篡改
                        if (DetectTimeManipulation())
                        {
                            result.IsValid = false;
                            result.Message = Messages.TrialExpiredMessage;
                            return result;
                        }
    
                        DateTime firstRunDate;
                        bool isFirstRun = false;
    
                        // 确定首次运行时间（使用最早的记录）
                        List<DateTime> dates = new List<DateTime>();
                        if (registryDate.HasValue) dates.Add(registryDate.Value);
                        if (fileDate.HasValue) dates.Add(fileDate.Value);
                        if (backupDate.HasValue) dates.Add(backupDate.Value);
    
                        if (dates.Count == 0)
                        {
                            // 首次运行
                            firstRunDate = DateTime.Now;
                            isFirstRun = true;
                            result.IsFirstRun = true;
    
                            // 保存到所有位置
                            SaveTrialData(firstRunDate, hardwareId);
                        }
                        else
                        {
                            // 使用最早的日期，防止通过删除部分记录来延长试用期
                            firstRunDate = dates.Min();
    
                            // 验证硬件指纹
                            if (!ValidateHardwareFingerprint(hardwareId))
                            {
                                result.IsValid = false;
                                result.Message = Messages.TrialExpiredMessage;
                                return result;
                            }
    
                            // 更新缺失的记录位置
                            if (registryDate == null || fileDate == null || backupDate == null)
                            {
                                SaveTrialData(firstRunDate, hardwareId);
                            }
                        }
    
                        TimeSpan elapsed = DateTime.Now - firstRunDate;
                        int remainingDays = TRIAL_DAYS - (int)elapsed.TotalDays;
                        result.RemainingDays = remainingDays;
    
                        if (remainingDays > 0)
                        {
                            result.IsValid = true;
                            if (string.IsNullOrEmpty(result.Message))
                            {
                                if (isFirstRun)
                                {
                                    result.Message = Messages.FirstRunMessage;
                                }
                                else
                                {
                                    result.Message = Messages.RemainingDaysMessage(remainingDays);
                                }
                            }
                        }
                        else
                        {
                            result.IsValid = false;
                            result.Message = Messages.TrialExpiredMessage;
                        }
    
                        return result;
                    }
                    catch (Exception ex)
                    {
                        // 发生错误时采用更严格的策略
                        result.IsValid = true; // 仍然允许使用，但记录错误
                        result.Message = Messages.TrialErrorMessage(ex.Message);
                        return result;
                    }
                }
    
                /// <summary>
                /// 手动重置试用期
                /// </summary>
                public static void ManualResetTrial()
                {
                    ResetTrialPeriod();
                }
    
                /// <summary>
                /// 获取当前版本号
                /// </summary>
                public static string GetCurrentVersion()
                {
                    return CURRENT_VERSION;
                }
    
                #endregion
    
                #region 私有方法
    
                /// <summary>
                /// 获取硬件指纹
                /// </summary>
                private static string GetHardwareFingerprint()
                {
                    try
                    {
                        string cpuId = GetCpuId();
                        string motherboardId = GetMotherboardId();
                        string diskId = GetDiskSerialNumber();
    
                        // 组合硬件信息并生成哈希
                        string combined = $"{cpuId}|{motherboardId}|{diskId}";
                        return ComputeSha256Hash(combined);
                    }
                    catch
                    {
                        // 如果获取硬件信息失败，使用机器名作为备选
                        return ComputeSha256Hash(Environment.MachineName + Environment.UserName);
                    }
                }
    
                private static string GetCpuId()
                {
                    try
                    {
                        using (var searcher = new ManagementObjectSearcher("SELECT ProcessorId FROM Win32_Processor"))
                        {
                            foreach (ManagementObject obj in searcher.Get())
                            {
                                return obj["ProcessorId"]?.ToString() ?? "";
                            }
                        }
                    }
                    catch { }
                    return "";
                }
    
                private static string GetMotherboardId()
                {
                    try
                    {
                        using (var searcher = new ManagementObjectSearcher("SELECT SerialNumber FROM Win32_BaseBoard"))
                        {
                            foreach (ManagementObject obj in searcher.Get())
                            {
                                return obj["SerialNumber"]?.ToString() ?? "";
                            }
                        }
                    }
                    catch { }
                    return "";
                }
    
                private static string GetDiskSerialNumber()
                {
                    try
                    {
                        using (var searcher = new ManagementObjectSearcher("SELECT SerialNumber FROM Win32_PhysicalMedia"))
                        {
                            foreach (ManagementObject obj in searcher.Get())
                            {
                                string serial = obj["SerialNumber"]?.ToString();
                                if (!string.IsNullOrWhiteSpace(serial))
                                    return serial.Trim();
                            }
                        }
                    }
                    catch { }
                    return "";
                }
    
                /// <summary>
                /// 从注册表读取试用信息
                /// </summary>
                private static DateTime? ReadFromRegistry()
                {
                    try
                    {
                        using (var key = Registry.CurrentUser.OpenSubKey(REGISTRY_KEY))
                        {
                            if (key != null)
                            {
                                string encryptedData = key.GetValue(ENCRYPTED_DATA_VALUE) as string;
                                if (!string.IsNullOrEmpty(encryptedData))
                                {
                                    string decrypted = DecryptString(encryptedData);
                                    if (DateTime.TryParse(decrypted, out DateTime date))
                                        return date;
                                }
                            }
                        }
                    }
                    catch { }
                    return null;
                }
    
                /// <summary>
                /// 从隐藏文件读取试用信息
                /// </summary>
                private static DateTime? ReadFromHiddenFile()
                {
                    try
                    {
                        if (File.Exists(HIDDEN_FILE_PATH))
                        {
                            string fileContent = File.ReadAllText(HIDDEN_FILE_PATH);
    
                            // 处理新格式（包含版本号）
                            if (fileContent.Contains("|"))
                            {
                                string[] parts = fileContent.Split('|');
                                if (parts.Length >= 1)
                                {
                                    string decrypted = DecryptString(parts[0]);
                                    if (DateTime.TryParse(decrypted, out DateTime date))
                                        return date;
                                }
                            }
                            else
                            {
                                // 处理旧格式（仅日期）
                                string decrypted = DecryptString(fileContent);
                                if (DateTime.TryParse(decrypted, out DateTime date))
                                    return date;
                            }
                        }
                    }
                    catch { }
                    return null;
                }
    
                /// <summary>
                /// 从备份位置读取试用信息
                /// </summary>
                private static DateTime? ReadFromBackupLocation()
                {
                    try
                    {
                        using (var key = Registry.CurrentUser.OpenSubKey(REGISTRY_KEY_BACKUP))
                        {
                            if (key != null)
                            {
                                string encryptedData = key.GetValue($"{PROJECT_NAME}_Trial") as string;
                                if (!string.IsNullOrEmpty(encryptedData))
                                {
                                    string decrypted = DecryptString(encryptedData);
                                    if (DateTime.TryParse(decrypted, out DateTime date))
                                        return date;
                                }
                            }
                        }
                    }
                    catch { }
                    return null;
                }
    
                /// <summary>
                /// 检测时间篡改
                /// </summary>
                private static bool DetectTimeManipulation()
                {
                    try
                    {
                        // 检查系统时间是否合理（不能早于2020年）
                        if (DateTime.Now.Year < 2020)
                            return true;
    
                        // 可以添加更多时间篡改检测逻辑
                        return false;
                    }
                    catch
                    {
                        return false;
                    }
                }
    
                /// <summary>
                /// 保存试用数据到所有位置
                /// </summary>
                private static void SaveTrialData(DateTime firstRunDate, string hardwareId)
                {
                    string dateString = firstRunDate.ToString("yyyy-MM-dd HH:mm:ss");
                    string encryptedDate = EncryptString(dateString);
                    string encryptedHardware = EncryptString(hardwareId);
                    string encryptedVersion = EncryptString(CURRENT_VERSION);
    
                    // 保存到注册表
                    try
                    {
                        using (var key = Registry.CurrentUser.CreateSubKey(REGISTRY_KEY))
                        {
                            key?.SetValue(ENCRYPTED_DATA_VALUE, encryptedDate);
                            key?.SetValue(HARDWARE_ID_VALUE, encryptedHardware);
                            key?.SetValue(VERSION_VALUE, encryptedVersion);
                        }
                    }
                    catch { }
    
                    // 保存到隐藏文件
                    try
                    {
                        string dirPath = Path.GetDirectoryName(HIDDEN_FILE_PATH);
                        if (!Directory.Exists(dirPath))
                            Directory.CreateDirectory(dirPath);
    
                        // 保存多个值到文件，用分隔符分开
                        string fileContent = $"{encryptedDate}|{encryptedVersion}";
                        File.WriteAllText(HIDDEN_FILE_PATH, fileContent);
                        File.SetAttributes(HIDDEN_FILE_PATH, FileAttributes.Hidden | FileAttributes.System);
                    }
                    catch { }
    
                        // 保存到备份位置
                        try
                        {
                            using (var key = Registry.CurrentUser.CreateSubKey(REGISTRY_KEY_BACKUP))
                            {
                                key?.SetValue($"{PROJECT_NAME}_Trial", encryptedDate);
                                key?.SetValue($"{PROJECT_NAME}_Hardware", encryptedHardware);
                                key?.SetValue($"{PROJECT_NAME}_Version", encryptedVersion);
                            }
                        }
                        catch { }
    
                    // 保存到备份文件
                    try
                    {
                        string dirPath = Path.GetDirectoryName(BACKUP_FILE_PATH);
                        if (!Directory.Exists(dirPath))
                            Directory.CreateDirectory(dirPath);
    
                        string fileContent = $"{encryptedDate}|{encryptedVersion}";
                        File.WriteAllText(BACKUP_FILE_PATH, fileContent);
                        File.SetAttributes(BACKUP_FILE_PATH, FileAttributes.Hidden);
                    }
                    catch { }
                }
    
                /// <summary>
                /// 验证硬件指纹
                /// </summary>
                private static bool ValidateHardwareFingerprint(string currentHardwareId)
                {
                    try
                    {
                        // 从注册表读取保存的硬件指纹
                        using (var key = Registry.CurrentUser.OpenSubKey(REGISTRY_KEY))
                        {
                            if (key != null)
                            {
                                string encryptedHardware = key.GetValue(HARDWARE_ID_VALUE) as string;
                                if (!string.IsNullOrEmpty(encryptedHardware))
                                {
                                    string savedHardwareId = DecryptString(encryptedHardware);
                                    return string.Equals(currentHardwareId, savedHardwareId, StringComparison.OrdinalIgnoreCase);
                                }
                            }
                        }
                    }
                    catch { }
                    return true; // 如果无法验证，允许继续使用
                }
    
                /// <summary>
                /// 获取存储的版本号
                /// </summary>
                private static string GetStoredVersion()
                {
                    try
                    {
                        // 首先从注册表读取
                        using (var key = Registry.CurrentUser.OpenSubKey(REGISTRY_KEY))
                        {
                            if (key != null)
                            {
                                string encryptedVersion = key.GetValue(VERSION_VALUE) as string;
                                if (!string.IsNullOrEmpty(encryptedVersion))
                                {
                                    return DecryptString(encryptedVersion);
                                }
                            }
                        }
    
                        // 从隐藏文件读取
                        if (File.Exists(HIDDEN_FILE_PATH))
                        {
                            string fileContent = File.ReadAllText(HIDDEN_FILE_PATH);
                            if (fileContent.Contains("|"))
                            {
                                string[] parts = fileContent.Split('|');
                                if (parts.Length >= 2)
                                {
                                    return DecryptString(parts[1]);
                                }
                            }
                        }
    
                        // 从备份位置读取
                        using (var key = Registry.CurrentUser.OpenSubKey(REGISTRY_KEY_BACKUP))
                        {
                            if (key != null)
                            {
                                string encryptedVersion = key.GetValue($"{PROJECT_NAME}_Version") as string;
                                if (!string.IsNullOrEmpty(encryptedVersion))
                                {
                                    return DecryptString(encryptedVersion);
                                }
                            }
                        }
    
                        // 从备份文件读取
                        if (File.Exists(BACKUP_FILE_PATH))
                        {
                            string fileContent = File.ReadAllText(BACKUP_FILE_PATH);
                            if (fileContent.Contains("|"))
                            {
                                string[] parts = fileContent.Split('|');
                                if (parts.Length >= 2)
                                {
                                    return DecryptString(parts[1]);
                                }
                            }
                        }
                    }
                    catch { }
    
                    return null; // 没有找到版本信息
                }
    
                /// <summary>
                /// 检查是否需要重置试用期
                /// </summary>
                private static bool CheckForTrialReset()
                {
                    try
                    {
                        // 方法1：检查桌面上的重置标志文件
                        if (File.Exists(RESET_FLAG_FILE))
                        {
                            string content = File.ReadAllText(RESET_FLAG_FILE).Trim();
                            if (string.Equals(content, RESET_COMMAND, StringComparison.OrdinalIgnoreCase))
                            {
                                // 删除标志文件
                                File.Delete(RESET_FLAG_FILE);
                                return true;
                            }
                        }
    
                        // 方法2：检查环境变量（临时）
                        string envReset = Environment.GetEnvironmentVariable($"{PROJECT_NAME.ToUpper()}_RESET_TRIAL");
                        if (string.Equals(envReset, RESET_COMMAND, StringComparison.OrdinalIgnoreCase))
                        {
                            // 清除环境变量
                            Environment.SetEnvironmentVariable($"{PROJECT_NAME.ToUpper()}_RESET_TRIAL", null);
                            return true;
                        }
    
                        // 方法3：检查特殊注册表项
                        try
                        {
                            using (var key = Registry.CurrentUser.OpenSubKey($@"SOFTWARE\{PROJECT_NAME}_Dev"))
                            {
                                if (key != null)
                                {
                                    string resetValue = key.GetValue("ResetTrial") as string;
                                    if (string.Equals(resetValue, RESET_COMMAND, StringComparison.OrdinalIgnoreCase))
                                    {
                                        // 删除重置标志
                                        using (var writeKey = Registry.CurrentUser.OpenSubKey($@"SOFTWARE\{PROJECT_NAME}_Dev", true))
                                        {
                                            writeKey?.DeleteValue("ResetTrial", false);
                                        }
                                        return true;
                                    }
                                }
                            }
                        }
                        catch { }
    
                        return false;
                    }
                    catch
                    {
                        return false;
                    }
                }
    
                /// <summary>
                /// 重置试用期 - 清除所有试用期数据
                /// </summary>
                private static void ResetTrialPeriod()
                {
                    try
                    {
                        // 清除主注册表项
                        try
                        {
                            Registry.CurrentUser.DeleteSubKey(REGISTRY_KEY, false);
                        }
                        catch { }
    
                        // 清除备份注册表项
                        try
                        {
                            using (var key = Registry.CurrentUser.OpenSubKey(REGISTRY_KEY_BACKUP, true))
                            {
                                if (key != null)
                                {
                                    key.DeleteValue($"{PROJECT_NAME}_Trial", false);
                                    key.DeleteValue($"{PROJECT_NAME}_Hardware", false);
                                    key.DeleteValue($"{PROJECT_NAME}_Version", false);
                                }
                            }
                        }
                        catch { }
    
                        // 删除隐藏文件
                        try
                        {
                            if (File.Exists(HIDDEN_FILE_PATH))
                            {
                                File.SetAttributes(HIDDEN_FILE_PATH, FileAttributes.Normal);
                                File.Delete(HIDDEN_FILE_PATH);
                            }
    
                            // 删除文件夹（如果为空）
                            string dirPath = Path.GetDirectoryName(HIDDEN_FILE_PATH);
                            if (Directory.Exists(dirPath) && !Directory.EnumerateFileSystemEntries(dirPath).Any())
                            {
                                Directory.Delete(dirPath);
                            }
                        }
                        catch { }
    
                        // 删除备份文件
                        try
                        {
                            if (File.Exists(BACKUP_FILE_PATH))
                            {
                                File.SetAttributes(BACKUP_FILE_PATH, FileAttributes.Normal);
                                File.Delete(BACKUP_FILE_PATH);
                            }
                        }
                        catch { }
                    }
                    catch (Exception)
                    {
                        // 忽略重置过程中的错误
                    }
                }
    
                /// <summary>
                /// 加密字符串
                /// </summary>
                private static string EncryptString(string plainText)
                {
                    try
                    {
                        byte[] data = Encoding.UTF8.GetBytes(plainText);
                        byte[] key = Encoding.UTF8.GetBytes(ENCRYPTION_KEY.PadRight(32).Substring(0, 32));
    
                        using (var aes = Aes.Create())
                        {
                            aes.Key = key;
                            aes.GenerateIV();
    
                            using (var encryptor = aes.CreateEncryptor())
                            {
                                byte[] encrypted = encryptor.TransformFinalBlock(data, 0, data.Length);
                                byte[] result = new byte[aes.IV.Length + encrypted.Length];
                                Array.Copy(aes.IV, 0, result, 0, aes.IV.Length);
                                Array.Copy(encrypted, 0, result, aes.IV.Length, encrypted.Length);
                                return Convert.ToBase64String(result);
                            }
                        }
                    }
                    catch
                    {
                        return Convert.ToBase64String(Encoding.UTF8.GetBytes(plainText));
                    }
                }
    
                /// <summary>
                /// 解密字符串
                /// </summary>
                private static string DecryptString(string cipherText)
                {
                    try
                    {
                        if (string.IsNullOrWhiteSpace(cipherText))
                            return "";
    
                        byte[] data = Convert.FromBase64String(cipherText);
                        byte[] key = Encoding.UTF8.GetBytes(ENCRYPTION_KEY.PadRight(32).Substring(0, 32));
    
                        using (var aes = Aes.Create())
                        {
                            aes.Key = key;
    
                            if (data.Length < aes.IV.Length)
                                return ""; // 数据太短，无效
    
                            byte[] iv = new byte[aes.IV.Length];
                            byte[] encrypted = new byte[data.Length - iv.Length];
    
                            Array.Copy(data, 0, iv, 0, iv.Length);
                            Array.Copy(data, iv.Length, encrypted, 0, encrypted.Length);
    
                            aes.IV = iv;
    
                            using (var decryptor = aes.CreateDecryptor())
                            {
                                byte[] decrypted = decryptor.TransformFinalBlock(encrypted, 0, encrypted.Length);
                                string result = Encoding.UTF8.GetString(decrypted);
    
                                // 验证解密结果是否包含有效字符
                                if (IsValidDecryptedString(result))
                                    return result;
                                else
                                    return "";
                            }
                        }
                    }
                    catch
                    {
                        try
                        {
                            string fallback = Encoding.UTF8.GetString(Convert.FromBase64String(cipherText));
                            return IsValidDecryptedString(fallback) ? fallback : "";
                        }
                        catch
                        {
                            return "";
                        }
                    }
                }
    
                /// <summary>
                /// 验证解密后的字符串是否有效
                /// </summary>
                private static bool IsValidDecryptedString(string text)
                {
                    if (string.IsNullOrEmpty(text))
                        return false;
    
                    // 检查是否包含过多的控制字符或无效字符
                    int invalidCharCount = 0;
                    foreach (char c in text)
                    {
                        if (char.IsControl(c) && c != '\r' && c != '\n' && c != '\t')
                        {
                            invalidCharCount++;
                        }
                    }
    
                    // 如果无效字符超过30%，认为解密失败
                    return (double)invalidCharCount / text.Length < 0.3;
                }
    
                /// <summary>
                /// 计算SHA256哈希
                /// </summary>
                private static string ComputeSha256Hash(string input)
                {
                    try
                    {
                        using (var sha256 = SHA256.Create())
                        {
                            byte[] bytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(input));
                            StringBuilder builder = new StringBuilder();
                            foreach (byte b in bytes)
                            {
                                builder.Append(b.ToString("x2"));
                            }
                            return builder.ToString();
                        }
                    }
                    catch
                    {
                        return input.GetHashCode().ToString();
                    }
                }
    
                #endregion
            }
        }
    
    ```

## 使用方式如下所示：

在`IExtensinApplication`中检测试用期状态

```csharp
 public class PlugInApplication : IExtensionApplication
 {
     public void Initialize()
     {
         // 检查试用期状态
         var trialResult = TrialLicenseManager.CheckTrialPeriod();
         
         // 显示试用期信息
         if (!string.IsNullOrEmpty(trialResult.Message))
         {
             var editor = AcadApp.DocumentManager.MdiActiveDocument?.Editor;
             editor?.WriteMessage($"{trialResult.Message}\n");
         }
         
         if (!trialResult.IsValid)
         {
             // 试用期已过期，不执行初始化
             return;
         }

         try
         {
             // Add your initialize code here.
             Document doc = AcadApp.DocumentManager.MdiActiveDocument;
             if (doc != null)
             {
                 using (doc.LockDocument())
                 {
                     doc.SendStringToExecute("tldxk ", false, false, false);
                 }
             }
         }
         catch (ZwSoft.ZwCAD.Runtime.Exception ex)
         {
             var editor = AcadApp.DocumentManager.MdiActiveDocument?.Editor;
             editor?.WriteMessage($"插件初始化时发生错误：{ex.Message}\n");
         }
     }

     public void Terminate()
     {
         // Add your uninitialize code here.
     }
 }
```

## 使用说明

`使用说明`

1. 复制 TrialLicenseManager.cs 到您的项目中
2. 修改配置常量（在文件顶部的"配置常量"区域）：
   - PROJECT_NAME: 项目名称（如 "MyApp"）
   - PROJECT_SHORT_NAME: 项目短名称（如 "myapp"）
   - COMPANY_NAME: 公司名称（如 "MyCompany"）
   - CURRENT_VERSION: 当前版本号（如 "1.0.0"）
   - TRIAL_DAYS: 试用天数（如 30）
   - USE_ENGLISH: 界面语言（true:英文, false:中文）
3. 在程序入口点调用 TrialLicenseManager.CheckTrialPeriod()
4. 根据返回结果决定是否继续执行程序逻辑

`项目配置示例`

```csharp
// ====== 项目配置 - 在新项目中使用时请修改以下常量 ======
private const string PROJECT_NAME = "MyAwesomeApp";        // 项目名称
private const string PROJECT_SHORT_NAME = "myapp";         // 项目短名称  
private const string COMPANY_NAME = "MyCompany";           // 公司名称

// 版本管理 - 修改此版本号将自动重置所有用户的试用期
private const string CURRENT_VERSION = "2.1.0";
private const int TRIAL_DAYS = 30;                         // 试用天数

// 语言设置 - true:英文, false:中文
private const bool USE_ENGLISH = true;                     // 界面语言
// ====== 项目配置结束 ======
```

配置后，系统将自动使用：
- 注册表路径: SOFTWARE\MyAwesomeApp

- 隐藏文件夹: %AppData%\.myapp\

- 环境变量: MYAWESOMEAPP_RESET_TRIAL

- 重置文件: RESET_MYAWESOMEAPP_TRIAL.txt

- 界面语言: 英文提示信息

  

`多语言支持`

系统支持中英文切换：

**中文模式** (USE_ENGLISH = false):
- "欢迎使用！您有 30 天的试用期。"
- "试用期剩余 15 天，请及时联系开发商获取正式版本。"
- "试用期已过期！请联系开发商获取正式版本。"

**英文模式** (USE_ENGLISH = true):
- "Welcome! You have 30 days of trial period."
- "Trial period remaining: 15 days. Please contact the developer for the full version."
- "Trial period has expired! Please contact the developer for the full version."

` 版本管理 `

发布新版本时：
1. 修改 TrialLicenseManager.cs 中的 CURRENT_VERSION 常量
2. 编译并发布新版本
3. 所有用户首次运行新版本时会自动重置试用期

`迁移现有项目`

如果要将此授权系统集成到现有项目：
1. 修改 PROJECT_NAME 为您的项目名称
2. 修改 PROJECT_SHORT_NAME 为适合的短名称
3. 修改 COMPANY_NAME 为您的公司名称
4. 设置合适的 CURRENT_VERSION 和 TRIAL_DAYS
5. 测试确保所有功能正常工作

` 注意事项`

- 该授权系统适用于试用版本管理
- 不适用于高安全级别的商业软件保护
- 建议配合其他安全措施使用
- 支持 .NET Framework 和 .NET Core
- 只需修改顶部的配置常量，系统自动适配