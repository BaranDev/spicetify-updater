using System;
using System.Diagnostics;
using System.Threading;
using System.Media;
using System.Numerics;
using System.Text.RegularExpressions;

class Program
{
    static bool running = true;
    private static SoundPlayer player = new SoundPlayer("Resources\\Littleroot Town.wav");
    private static Stopwatch _stopwatch = new Stopwatch();
    private static System.Timers.Timer timer = new System.Timers.Timer(1000); // 1 second interval
    private static bool debug = false;
    private static TimeSpan elapsed = new TimeSpan(0, 0, 0);

    static void Main(string[] args)
    {
        enteranceMenu();
        MonitorElapsedTime();
        try
        {
            // Step 1: Upgrade Spicetify using CLI
            Console.WriteLine("Updating Spicetify...");
            RunSpicetifyCommand("upgrade");

            Console.WriteLine("Press any key to exit, click enter to update/install spicetify marketplace or click 1 to see a cool cat animation!");
            var a = Console.ReadKey();
            //if a is 1 play animation else exit
            if (a.KeyChar == '1')
            {
                StartASCIIAnimation();
            }
            else if (a.KeyChar == '\r')
            {
                Console.Clear();

                _stopwatch.Reset(); //timer for marketplace installation
                _stopwatch.Start();
                InstallMarketplace();
                elapsed = _stopwatch.Elapsed;
                _stopwatch.Stop();

                Console.WriteLine($"Elapsed Time: {elapsed.TotalSeconds.ToString("0.00")} seconds");

                Console.WriteLine("Press any key to exit or click 1 to see a cool cat animation!");
                a = Console.ReadKey();
                if (a.KeyChar == '1')
                {
                    StartASCIIAnimation();
                }
                else
                {
                    exit();
                }
            }
            else
            {
                Console.Clear();
                exit();
            }

            running = false; // Stop the animation thread
        }
        catch (Exception ex)
        {
            Console.WriteLine("An error occurred while upgrading Spicetify.");
            Console.WriteLine(ex.Message);
            running = false; // Stop the animation thread
        }

    }
    static public void InstallMarketplace()
    {
        Console.WriteLine("Installing Spicetify Marketplace...");



        RunPowerShellCommand("Invoke-WebRequest -UseBasicParsing \"https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.ps1\" | Invoke-Expression");
        Console.Clear();
        Console.WriteLine("Spicetify Marketplace installed successfully!");
        PrintThumbsUp();
    }

    static public void PrintThumbsUp()
    {
        Console.WriteLine("            .--------._\r\n           (`--'       `-.\r\n            `.______      `.\r\n         ___________`__     \\\r\n      ,-'           `-.\\     |\r\n     //                \\|    |\\\r\n    (`  .'~~~~~---\\     \\'   | |\r\n     `-'           )     \\   | |\r\n        ,---------' - -.  `  . '\r\n      ,'             ` `\\`     |\r\n     /                      \\  |\r\n    /     \\-----.         \\    `\r\n   /|  ,_/      '-._            |\r\n  (-'  /           /            `     \r\n  ,`--<           |        \\     \\\r\n  \\ |  \\         /               `\\\r\n   |/   \\____---'--`         \\     \\\r\n   |    '           `               \\\r\n   |\r\n    `--.__\r\n          `---._______\r\n                      `.\r\n                        \\  ");
    }

    static public void StartASCIIAnimation()
    {
        player.Load();
        player.PlayLooping();
        ASCIIAnimation();
    }

    static async Task MonitorElapsedTime()
    {
        while (running)
        {
            await Task.Delay(1000); // Delay for 1 second

            if (elapsed.TotalMinutes >= 5)
            {
                Console.WriteLine("Can't automatically update. Manual update might be necessary.");
                Console.ReadKey();
                exit();
            }
        }
    }

    static void WriteByeASCII()
    {
        Console.WriteLine(" __      __\r\n( _\\    /_ )\r\n \\ _\\  /_ / \r\n  \\ _\\/_ /_ _\r\n  |_____/_/ /|\r\n  (  (_)__)J-)\r\n  (  /`.,   /\r\n   \\/  ;   /\r\n    | === |");
    }

    static void exit()
    {
        Console.Clear();
        WriteByeASCII();
        Thread.Sleep(500);
        Environment.Exit(0);
    }

    static void enteranceMenu()
    {
        if (debug)
        {
            Console.WriteLine("Press any key to start the enterance menu...\n");
            Console.ReadKey();
        }

        Console.WriteLine("\tWelcome to the Spicetify Updater!");
        Console.WriteLine("                   _\r\n               _  / |\r\n              / \\ | | /\\\r\n               \\ \\| |/ /\r\n                \\ Y | /___\r\n              .-.) '. `__/\r\n             (.-.   / /\r\n                 | ' |\r\n                 |___|\r\n                [_____]\r\n                |     |");
        Console.WriteLine("\tPress any key to start...");
        Console.ReadKey();
        Console.Clear();
    }

    static void RunPowerShellCommand(string command)
    {
        try
        {
            if (debug)
            {
                Console.WriteLine($"Press any key to continue RunPowerShellCommand with ${command}.\n");
                Console.ReadKey();
            }

            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = "powershell.exe",
                Arguments = $"-Command \"{command}\"",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using (Process process = Process.Start(startInfo))
            {
                if (debug)
                {
                    Console.WriteLine("Press any key to continue RunPowerShellCommand after process.Start.\n");
                    Console.ReadKey();
                }
                if (process == null)
                    throw new Exception("Unable to start PowerShell process.");

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();

                if (debug)
                {
                    if (!string.IsNullOrWhiteSpace(output))
                        Console.WriteLine(output);

                    if (!string.IsNullOrWhiteSpace(error))
                        Console.WriteLine(error);
                }

                process.WaitForExit(); // Wait for the process to exit
                process.Close();
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("An error occurred while running the PowerShell command. Try running the program as administrator.");
            Console.WriteLine(ex.Message);
        }
    }


    //parse function to get the version number
    static string GetVersion(string input, string keyword)
    {
        if (debug)
        {
            Console.WriteLine("input: " + input);
            Console.WriteLine("keyword: " + keyword);
            Console.WriteLine("Press any key to continue GetVersion.\n");
            Console.ReadKey();
        }
        // create a regular expression pattern to match the keyword and version number
        string pattern = $@"{keyword}\s*([\d\.]+)";

        // use Regex.Match to find the first match in the input string
        Match match = Regex.Match(input, pattern);

        // if a match is found, return the captured version number; otherwise, return an empty string
        return match.Success ? match.Groups[1].Value : string.Empty;
    }


    //check if the spicetify is on the latest version
    static bool isSpicetifyUpToDate(string consoleoutput)
    {
        if (debug)
        {
            Console.WriteLine("Press any key to continue isSpicetifyUpToDate.\n");
            Console.ReadKey();
        }
        //get the latest version of spicetify
        string latestVersion = GetVersion(consoleoutput, "Latest release:");
        //get the current version of spicetify
        string currentVersion = GetVersion(consoleoutput, "Current version:");
        if (debug)
        {
            Console.WriteLine("latest version: " + latestVersion);
            Console.WriteLine("current version: " + currentVersion + "\n");
        }

        //if latest version or current versionis empty, return null
        if (string.IsNullOrEmpty(latestVersion) || string.IsNullOrEmpty(currentVersion))
        {
            return false;
        }
        //compare the two
        if (latestVersion == currentVersion)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    static void installSpicetify()
    {
        try
        {
            _stopwatch.Reset(); //timer for spicetify installation
            _stopwatch.Start();
            if (debug)
            {
                Console.WriteLine("Press any key to start the installation...\n");
                Console.ReadKey();
            }

            //check if spicetify is installed
            if (!isSpicetifyInstalled())
                Console.WriteLine("Spicetify is not installed. Installing...");

            RunPowerShellCommand("iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex");
        }
        catch (Exception ex)
        {
            Console.WriteLine("An error occurred while installing Spicetify.");
            Console.WriteLine(ex.Message);
            exit();
        }
    }


    //check if spicetify is installed
    static public bool isSpicetifyInstalled()
    {
        if (debug)
        {
            Console.WriteLine("Press any key to continue isSpicetifyInstalled.\n");
            Console.ReadKey();
        }
        // Get the path to the user's AppData\Roaming folder
        string appDataPath = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);

        // Combine the path to Spicetify with the obtained AppData path
        string spicetifyPath = Path.Combine(appDataPath, "Spicetify");

        if (debug)
        {
            Console.WriteLine("spicetifyPath: " + spicetifyPath);
            Console.ReadKey();
        }

        // Check if the Spicetify folder exists
        return Directory.Exists(spicetifyPath);
       
    }

    static void RunSpicetifyCommand(string arguments)
    {
        try
        {
            if (debug)
            {
                //check if the spicetify is installed
                Console.WriteLine("isSpicetifyInstalled: " + isSpicetifyInstalled());
                Console.WriteLine($"Click something to proceed to running the command ${arguments}\n");
                Console.ReadKey();
            }
            if (isSpicetifyInstalled())
            {
                string output = "";
                ProcessStartInfo startInfo = new ProcessStartInfo
                {
                    FileName = "spicetify",
                    Arguments = arguments,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = false
                };
                using (Process process = Process.Start(startInfo))
                {
                    process.WaitForExit();
                    output = process.StandardOutput.ReadToEnd();
                }
                    if (debug)
                    {
                        System.Console.WriteLine("\n\n\nOUTPUT TEST\n\n\n");
                        System.Console.WriteLine(output);
                        System.Console.WriteLine(isSpicetifyUpToDate(output)); //is it up to date?
                        System.Console.WriteLine("\n\n\nOUTPUT TEST\n\n\n");
                    }
                    if (arguments == "upgrade")
                    {
                        if (debug)
                        {
                            Console.WriteLine("Press any key to continue RunSpicetifyCommand with upgrade.\n");
                            Console.ReadKey();
                        }
                        if (!isSpicetifyUpToDate(output))
                        {
                            Console.Clear();
                            Console.WriteLine("Update found. Updating to the latest version!\n");
                            _stopwatch.Reset(); //timer for spicetify upgrade
                            _stopwatch.Start();
                            installSpicetify();
                            RunSpicetifyCommand("restore backup apply");
                            elapsed = _stopwatch.Elapsed;
                            _stopwatch.Stop();
                            Console.WriteLine("Spicetify upgrade completed successfully!");
                            Console.WriteLine($"Elapsed Time: {elapsed.TotalSeconds.ToString("0.00")} seconds");
                            
                            PrintThumbsUp();
                        }
                        else
                        {
                            Console.WriteLine("No updates found. Do you want to re-install the latest version?\n");
                            Console.WriteLine("Press 1 to re-install the latest version, press 2 to see a cool cat animation or press any other key to exit.\n");
                            var a = Console.ReadKey();
                            if (a.KeyChar == '1')
                            {
                                Console.Clear();
                                Console.WriteLine("Reinstalling Spicetify...\n");
                                _stopwatch.Reset(); //timer for spicetify upgrade
                                _stopwatch.Start();
                                installSpicetify();
                                RunSpicetifyCommand("restore backup apply");
                                elapsed = _stopwatch.Elapsed;
                                _stopwatch.Stop();
                                Console.WriteLine("Spicetify upgrade completed successfully!");
                                Console.WriteLine($"Elapsed Time: {elapsed.TotalSeconds.ToString("0.00")} seconds");
                                PrintThumbsUp();
                            }
                            else if (a.KeyChar == '2')
                            {
                                StartASCIIAnimation();
                            }
                            else
                            {
                                exit();
                            }
                            Thread.Sleep(500);
                        }
                    }
                    else
                    {
                        if(debug)
                            Console.WriteLine("Spicetify command completed successfully!");
                    }
                }
                else
                {
                    System.Console.WriteLine("Spicetify is not installed. Click 1 to download Spicetify.\n");
                    var a = Console.ReadKey();
                    if (a.KeyChar == '1')
                    {
                        installSpicetify();
                        RunSpicetifyCommand("backup apply");
                        RunSpicetifyCommand("spicetify restore backup");
                        RunSpicetifyCommand("spicetify backup");
                    }
                    else
                    {
                        exit();
                    }
                }
        }
        catch (Exception)
        {
            Console.WriteLine("An error occurred while running the Spicetify command. Make sure the Spicetify and Spotify is correctly downloaded. Or click 1 to start the process to download Spicetify.");
            //readkey to start download
            var a = Console.ReadKey();
            if (a.KeyChar == '1')
            {
                installSpicetify();
            }
            else
            {
                exit();
            }
        }
    } 



    static void ASCIIAnimation()
    {
        if (debug)
        {
            Console.WriteLine("Press any key to start the animation...");
            Console.ReadKey();
        }
        string anim1 = "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *\r\n          |\\___/|\r\n          )     (             .              '\r\n         =\\     /=\r\n           )===(       *\r\n          /     \\\r\n          |     |\r\n         /       \\\r\n         \\       /\r\n  _/\\_/\\_/\\__  _/_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_\r\n  |  |  |  |( (  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  | ) ) |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |(_(  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";
        string anim2 = "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *\r\n          |\\___/|\r\n         =) ^Y^ (=            .              '\r\n          \\  ^  /\r\n           )=*=(       *\r\n          /     \\\r\n          |     |\r\n         /| | | |\\\r\n         \\| | |_|/\\\r\n  /\\__/\\_//_// ___/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_\r\n  |  |  |  | \\_) |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";
        string anim3 = "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *    _\r\n          |\\___/|                      \\\\\r\n         =) ^Y^ (=   |\\_/|              ||    '\r\n          \\  ^  /    )a a '._.-\"\"\"\"-.  //\r\n           )=*=(    =\\T_= /    ~  ~  \\//\r\n          /     \\     `\"`\\   ~   / ~  /\r\n          |     |         |~   \\ |  ~/\r\n         /| | | |\\         \\  ~/- \\ ~\\\r\n         \\| | |_|/|        || |  // /`\r\n  /\\__/\\_//_// __//\\_/\\_/\\_((_|\\((_//\\_/\\_/\\_\r\n  |  |  |  | \\_) |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";
        string anim4 = "            *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *    \r\n          |\\___/|     /\\___/\\\r\n          )     (     )    ~( .              '\r\n         =\\     /=   =\\~    /=\r\n           )===(       ) ~ (\r\n          /     \\     /     \\\r\n          |     |     ) ~   (\r\n         /       \\   /     ~ \\\r\n         \\       /   \\~     ~/\r\n  /\\__/\\_/\\__  _/_/\\_/\\__~__/_/\\_/\\_/\\_/\\_/\\_\r\n  |  |  |  |( (  |  |  | ))  |  |  |  |  |  |\r\n  |  |  |  | ) ) |  |  |//|  |  |  |  |  |  |\r\n  |  |  |  |(_(  |  |  (( |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |\\)|  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";
        string anim5 = "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *    \r\n           /\\/|_      __/\\\\\r\n          /    -\\    /-   ~\\  .              '\r\n          \\    = Y =T_ =   /\r\n           )==*(`     `) ~ \\\r\n          /     \\     /     \\\r\n          |     |     ) ~   (\r\n         /       \\   /     ~ \\\r\n         \\       /   \\~     ~/\r\n  /\\__/\\_/\\__  _/_/\\_/\\__~__/_/\\_/\\_/\\_/\\_/\\_\r\n  |  |  |  | ) ) |  |  | ((  |  |  |  |  |  |\r\n  |  |  |  |( (  |  |  |  \\\\ |  |  |  |  |  |\r\n  |  |  |  | )_) |  |  |  |))|  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  (/ |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";

        //start a list with anims
        List<string> anims = new List<string>{anim1,anim2,anim3,anim4,anim5};

        //set console size and color
        Console.SetWindowSize(50, 25);
        Console.CursorVisible = false;
        Console.BackgroundColor = ConsoleColor.DarkGray;
        Console.ForegroundColor = ConsoleColor.Black;
        if (debug)
        {
            Console.WriteLine("Animation started.");
            Console.ReadKey();
        }
        else 
        {
            while (running) // loop until running is set to false
            {
                nextFrame(anims);
            }
        }
        
    }

    static void nextFrame(List<string> anims)
    {
        foreach (string anim in anims)
        {
            if (running)
            {
                Console.Clear();
                Console.WriteLine(anim);
                Console.WriteLine("Press 1 to stop animation's loop and exit.");
                Thread.Sleep(1400);
                checkKey();
            }

        }
    }

    static void checkKey()
    {
        if (Console.KeyAvailable && Console.ReadKey(true).Key == ConsoleKey.D1)
        {
            //close program
            player.Stop();
            running = false;
            exit();
        }
    }
}