using System.Diagnostics;
using System.Media;
using System.Reflection;
using System.Text.Json;
using System.Text.RegularExpressions;

namespace SpicetifyUpdater;

public class Program {
    private static bool _debug, _showBeginningAsciiArt = true;
    public static bool IsWindows, IsPlayerRunning;
    public static readonly SoundPlayer Player = new("Resources\\Littleroot Town.wav");
    private static DateTime _dateTime;
    private static string _lastOutput;
    private static readonly ConsoleColor DefaultColor = Console.ForegroundColor;

    private static bool IsSpicetifyUpToDate(bool showResult = true) {
        var http = new HttpClient();
        Api apiResponseJson;
        try {
            http.DefaultRequestHeaders.Add("User-Agent", $"Spicetify Updater/{Assembly.GetExecutingAssembly().GetName().Version}");
            var output = http.GetStringAsync("https://api.github.com/repos/spicetify/spicetify-cli/releases/latest").GetAwaiter().GetResult();
            apiResponseJson = JsonSerializer.Deserialize<Api>(output)!;
        }
        catch (Exception e) {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("An error occurred while checking for Spicetify's GitHub API response.");
            Console.WriteLine(e.Message);
            Console.WriteLine(e.StackTrace);
            Console.ForegroundColor = DefaultColor;
            return false;
        }
        var latestVersion = apiResponseJson?.tag_name.Split('v')[1].Trim() ?? "null";
        http.Dispose();
        
        RunSpicetifyCommand("-v", false, showResult);
        Thread.Sleep(500);
        
        if (showResult || _debug) {
            Console.WriteLine($"Latest version: {latestVersion}");
            Console.WriteLine($"Current version: {_lastOutput.Trim()}");
        }

        return latestVersion == _lastOutput.Trim();
    }

    private static bool IsSpicetifyInstalled() => Directory.Exists(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "Spicetify"));

    public static void Main(string[]? args) {
        IsWindows = Environment.OSVersion.ToString().Contains("windows", StringComparison.CurrentCultureIgnoreCase);
        _debug = Environment.CommandLine.Contains("--debug");
        start:
        Console.Title = "Spicetify Updater";
        Console.WriteLine("\tWelcome to the Spicetify Updater!");
        Console.ForegroundColor = DefaultColor;
        
        if (_showBeginningAsciiArt) 
            AsciiArt.Begin();
        else _showBeginningAsciiArt = true;
        
        Console.WriteLine();
        Console.WriteLine("Choose an option to get started");
        if (IsSpicetifyInstalled())
            Console.ForegroundColor = ConsoleColor.DarkGray;
        Console.WriteLine("1. Install Spicetify");
        Console.ForegroundColor = DefaultColor;
        if (!IsSpicetifyInstalled())
            Console.ForegroundColor = ConsoleColor.DarkGray;
        Console.WriteLine("2. Update Spicetify");
        Console.WriteLine("3. Install Spicetify Marketplace");
        Console.ForegroundColor = ConsoleColor.Cyan;
        Console.WriteLine("4. See a cool cat animation");
        Console.ForegroundColor = ConsoleColor.Red;
        Console.WriteLine("5. Exit");
        Console.ForegroundColor = DefaultColor;
        Console.Write("Enter your choice: ");
        var choice = Console.ReadKey();
        Console.WriteLine();
        try {
            switch (choice.KeyChar) {
                case '1':
                    // if already installed, tell user to not bother
                    if (IsSpicetifyInstalled()) {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine("Spicetify is already installed. Skipping...");
                        Thread.Sleep(1400);
                        Console.Clear();
                        goto start;
                    }

                    // if not installed, install
                    Console.WriteLine("Installing Spicetify...");
                    Console.Title = "Spicetify Updater - Installing Spicetify";
                    RunPowerShellCommand("iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex");
                    RunSpicetifyCommand("backup apply");
                    RunSpicetifyCommand("spicetify restore backup");
                    RunSpicetifyCommand("spicetify backup");
                    goto start;
                case '2':
                    // if not installed, tell user to install it first
                    if (!IsSpicetifyInstalled()) {
                        Console.WriteLine("Spicetify is not installed. Please install it first.");
                        goto start;
                    }
                    
                    // if up to date, ask user if they want to reinstall
                    if (IsSpicetifyUpToDate()) {
                        Console.WriteLine("No update found.");
                        Console.WriteLine("Do you want to re-install the latest version? (y/n)");
                        var _ = Console.ReadKey();
                        if (_.KeyChar == 'y') {
                            Console.Clear();
                            Console.Title = "Spicetify Updater - Reinstalling Spicetify";
                            Console.WriteLine("Reinstalling Spicetify...");
                            RunPowerShellCommand("iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex");
                            RunSpicetifyCommand("restore backup apply");
                            goto start;
                        }
                        
                        Console.Clear();
                        goto start;
                    }

                    // if not up to date, update
                    Console.WriteLine("Updating Spicetify...");
                    Console.Title = "Spicetify Updater - Updating Spicetify";
                    RunPowerShellCommand("upgrade");
                    RunSpicetifyCommand("restore backup apply");
                    break;
                case '3':
                    // Installs Spicetify Marketplace
                    Console.Title = "Spicetify Updater - Installing Spicetify Marketplace";
                    InstallMarketplace();
                    break;
                case '4':
                    // Checks if user is on Windows, in-case this app gets ported for other OSes
                    if (IsWindows) {
                        Player.Load();
                        Player.PlayLooping();
                        IsPlayerRunning = true;
                    }

                    Console.Clear();
                    AsciiArt.CatAnimation();
                    break;
                case 'i':
                    // Just a ton of information
                    Console.Write("Application Version: ");
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine(Assembly.GetExecutingAssembly().GetName().Version!.ToString(3));
                    Console.ForegroundColor = DefaultColor;
                    Console.Write("Application Contributors: ");
                    Console.ForegroundColor = ConsoleColor.Yellow;
                    Console.Write("BaranDev (https://github.com/BaranDev)");
                    Console.ForegroundColor = DefaultColor;
                    Console.Write(" | ");
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine("MintLily (https://github.com/MintLily)");
                    Console.ForegroundColor = DefaultColor;
                    Console.Write("IsWindows: ");
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine(IsWindows);
                    Console.ForegroundColor = DefaultColor;
                    Console.Write("Spicetify Installed? ");
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine(IsSpicetifyInstalled());
                    Console.ForegroundColor = DefaultColor;
                    Console.Write("Spicetify Updated? ");
                    Console.ForegroundColor = ConsoleColor.Cyan;
                    Console.WriteLine(IsSpicetifyUpToDate(false));
                    Console.ForegroundColor = DefaultColor;
                    goto start;
                case 'e':
                case '0':
                case 'c':
                case '5':
                    // Environment.Exit(0);
                    Exit();
                    break;
                default:
                    Console.WriteLine("Invalid choice. Please try again.");
                    Thread.Sleep(1400);
                    Console.Clear();
                    goto start;
            }
        }
        catch (Exception e) {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("An error occurred while running the command. Try running the program as administrator.");
            Console.WriteLine(e.Message);
            Console.WriteLine(e.StackTrace);
            Console.ForegroundColor = DefaultColor;
            goto start;
        }
    }

    private static void RunPowerShellCommand(string command) {
        try {
            if (_debug) {
                Console.WriteLine($"Press any key to continue RunPowerShellCommand with ${command}.\n");
                Console.ReadKey();
            }

            var startInfo = new ProcessStartInfo {
                FileName = "powershell.exe",
                Arguments = $"-Command \"{command}\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = Process.Start(startInfo);

            if (_debug) {
                Console.WriteLine("Press any key to continue RunPowerShellCommand after process.Start.\n");
                Console.ReadKey();
            }

            if (process == null)
                throw new Exception("Unable to start PowerShell process.");

            var output = process.StandardOutput.ReadToEnd();
            var error = process.StandardError.ReadToEnd();

            if (!string.IsNullOrWhiteSpace(output))
                Console.WriteLine(output);
            if (!string.IsNullOrWhiteSpace(error))
                Console.WriteLine(error);

            process.WaitForExit(); // Wait for the process to exit
            process.Close();
        }
        catch (Exception ex) {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("An error occurred while running the PowerShell command. Try running the program as administrator.");
            Console.WriteLine(ex.Message);
            Console.WriteLine(ex.StackTrace);
            Console.ForegroundColor = DefaultColor;
        }
    }

    private static void InstallMarketplace() {
        Console.WriteLine("Installing Spicetify Marketplace...");
        RunPowerShellCommand("Invoke-WebRequest -UseBasicParsing \"https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.ps1\" | Invoke-Expression");
        Console.Clear();
        Console.WriteLine("Spicetify Marketplace installed successfully!");
        AsciiArt.PrintThumbsUp();
        _showBeginningAsciiArt = false;
        Main(null);
    }

    private static void RunSpicetifyCommand(string command, bool showElapsedTime = true, bool showOutput = true) {
        _dateTime = DateTime.Now;
        var startInfo = new ProcessStartInfo {
            FileName = "spicetify",
            Arguments = command,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = false
        };
        
        if (showOutput)
            Console.WriteLine("Running > \"" + startInfo.FileName + " " + startInfo.Arguments + "\" Program Output below:");
        using var process = Process.Start(startInfo);
        process!.WaitForExit();
        var output = process.StandardOutput.ReadToEnd();
        if (showOutput)
            Console.WriteLine(output);

        if (command == "upgrade") {
            Console.Write("Updating Spicetify...");
            // Console.ForegroundColor = ConsoleColor.Green;
            // Console.WriteLine(" (ignore the error below)");
            // Console.ForegroundColor = DefaultColor;
            RunPowerShellCommand("iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex");
        }
        else if (command == "-v") {
            _lastOutput = output.Trim();
        }
        
        if (command != "-v")
            AsciiArt.PrintThumbsUp();

        if (!showElapsedTime) return;
        var elapsed = DateTime.Now - _dateTime;
        Console.WriteLine();
        Console.WriteLine($"Operation completed successfully in {elapsed.TotalSeconds} seconds!");
        Main(null);
    }

    private static void Exit() {
        Console.Title = "Spicetify Updater - Bye!";
        AsciiArt.PrintBye();
        if (IsWindows && IsPlayerRunning) {
            Player.Stop();
            Player.Dispose();
        }

        Console.Write("Press any key to exit.");
        Console.ReadKey();
        Environment.Exit(0);
    }
}