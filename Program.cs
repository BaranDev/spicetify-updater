using System;
using System.Diagnostics;
using System.Threading;
using System.Media;
using System.Numerics;

class Program
{ 
    static bool running = true;
    public static SoundPlayer player = new SoundPlayer("Littleroot Town.wav");
    public static string elapsedTime = "";

    static void Main(string[] args)
    {
        enteranceMenu();
        Console.SetWindowSize(65,30);
        try
        {
            // Step 1: Upgrade Spicetify using CLI
            Console.WriteLine("Updating Spicetify...");
            //RunSpicetifyCommand("restore backup");
            RunSpicetifyCommand("upgrade");
            RunSpicetifyCommand("apply");

            Console.WriteLine("Spicetify upgrade completed successfully!");
            Console.WriteLine(
                "            .--------._\r\n           (`--'       `-.\r\n            `.______      `.\r\n         ___________`__     \\\r\n      ,-'           `-.\\     |\r\n     //                \\|    |\\\r\n    (`  .'~~~~~---\\     \\'   | |\r\n     `-'           )     \\   | |\r\n        ,---------' - -.  `  . '\r\n      ,'             ` `\\`     |\r\n     /                      \\  |\r\n    /     \\-----.         \\    `\r\n   /|  ,_/      '-._            |\r\n  (-'  /           /            `     \r\n  ,`--<           |        \\     \\\r\n  \\ |  \\         /               `\\\r\n   |/   \\____---'--`         \\     \\\r\n   |    '           `               \\\r\n   |\r\n    `--.__\r\n          `---._______\r\n                      `.\r\n                        \\  ");
            Console.WriteLine("Press any key to exit or click 1 to see a cool cat animation!");
            var a = Console.ReadKey();
            //if a is 1 play animation else exit
            if (a.KeyChar == '1')
            {
                
                player.Load();
                player.PlayLooping();
                ASCIIAnimation();
            }
            else
            {
                Console.Clear();
                Console.WriteLine(); Console.WriteLine(); Console.WriteLine();
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

    static void exit()
    {
        Console.Clear();
        Console.SetWindowSize(30, 15);
        Console.WriteLine(" __      __\r\n( _\\    /_ )\r\n \\ _\\  /_ / \r\n  \\ _\\/_ /_ _\r\n  |_____/_/ /|\r\n  (  (_)__)J-)\r\n  (  /`.,   /\r\n   \\/  ;   /\r\n    | === |");
        Thread.Sleep(500);
        Environment.Exit(0);
    }
    static void enteranceMenu()
    {
        Console.SetWindowSize(45, 15);
        Console.WriteLine("\tWelcome to the Spicetify Updater!");
        Console.WriteLine("                   _\r\n               _  / |\r\n              / \\ | | /\\\r\n               \\ \\| |/ /\r\n                \\ Y | /___\r\n              .-.) '. `__/\r\n             (.-.   / /\r\n                 | ' |\r\n                 |___|\r\n                [_____]\r\n                |     |");
        Console.WriteLine("\tPress any key to start...");
        Console.ReadKey();
        Console.Clear();
    }

    static void RunPowerShellCommand(string command)
    {
        ProcessStartInfo startInfo = new ProcessStartInfo
        {
            FileName = "powershell.exe",
            Arguments = $"-NoProfile -ExecutionPolicy Bypass -Command \"{command}\"",
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true
        };

        using (Process process = Process.Start(startInfo))
        {
            process.WaitForExit();

            string output = process.StandardOutput.ReadToEnd();
            string error = process.StandardError.ReadToEnd();

            if (!string.IsNullOrWhiteSpace(output))
                Console.WriteLine(output);

            if (!string.IsNullOrWhiteSpace(error))
                Console.WriteLine(error);
        }
    }



    static void RunSpicetifyCommand(string arguments)
    {

        try
        {
            //debug throw exception
            //throw new Exception("test");


            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = "spicetify",
                Arguments = arguments,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using (Process process = Process.Start(startInfo))
            {
                Stopwatch stopwatch = new Stopwatch();
                stopwatch.Start();

                process.WaitForExit();

                stopwatch.Stop();

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();

                if (!string.IsNullOrWhiteSpace(output))
                    Console.WriteLine(output);

                if (!string.IsNullOrWhiteSpace(error))
                    Console.WriteLine(error);

                elapsedTime += stopwatch.Elapsed.Seconds + "." + stopwatch.Elapsed.Milliseconds + " seconds";
            }
        }
        catch (Exception ex)
        {
            Console.SetWindowSize(160, 20);
            Console.WriteLine("An error occurred while running the Spicetify command. Make sure the Spicetify is correctly downloaded. Or click 1 to start the process to download Spicetify.");
            //readkey to start download
            var a = Console.ReadKey();
            if (a.KeyChar == '1')
            {
                string command = "Invoke-WebRequest -UseBasicParsing \"https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.ps1\" | Invoke-Expression";
                RunPowerShellCommand(command);
            }
            else
            {
                exit();
            }


        }
    }

    public static string anim1 =
        "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *\r\n          |\\___/|\r\n          )     (             .              '\r\n         =\\     /=\r\n           )===(       *\r\n          /     \\\r\n          |     |\r\n         /       \\\r\n         \\       /\r\n  _/\\_/\\_/\\__  _/_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_\r\n  |  |  |  |( (  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  | ) ) |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |(_(  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";

    public static string anim2 =
        "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *\r\n          |\\___/|\r\n         =) ^Y^ (=            .              '\r\n          \\  ^  /\r\n           )=*=(       *\r\n          /     \\\r\n          |     |\r\n         /| | | |\\\r\n         \\| | |_|/\\\r\n  /\\__/\\_//_// ___/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_\r\n  |  |  |  | \\_) |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";

    public static string anim3 =
        "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *    _\r\n          |\\___/|                      \\\\\r\n         =) ^Y^ (=   |\\_/|              ||    '\r\n          \\  ^  /    )a a '._.-\"\"\"\"-.  //\r\n           )=*=(    =\\T_= /    ~  ~  \\//\r\n          /     \\     `\"`\\   ~   / ~  /\r\n          |     |         |~   \\ |  ~/\r\n         /| | | |\\         \\  ~/- \\ ~\\\r\n         \\| | |_|/|        || |  // /`\r\n  /\\__/\\_//_// __//\\_/\\_/\\_((_|\\((_//\\_/\\_/\\_\r\n  |  |  |  | \\_) |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";

    public static string anim4 =
        "            *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *    \r\n          |\\___/|     /\\___/\\\r\n          )     (     )    ~( .              '\r\n         =\\     /=   =\\~    /=\r\n           )===(       ) ~ (\r\n          /     \\     /     \\\r\n          |     |     ) ~   (\r\n         /       \\   /     ~ \\\r\n         \\       /   \\~     ~/\r\n  /\\__/\\_/\\__  _/_/\\_/\\__~__/_/\\_/\\_/\\_/\\_/\\_\r\n  |  |  |  |( (  |  |  | ))  |  |  |  |  |  |\r\n  |  |  |  | ) ) |  |  |//|  |  |  |  |  |  |\r\n  |  |  |  |(_(  |  |  (( |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |\\)|  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";

    public static string anim5 =
        "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *    \r\n           /\\/|_      __/\\\\\r\n          /    -\\    /-   ~\\  .              '\r\n          \\    = Y =T_ =   /\r\n           )==*(`     `) ~ \\\r\n          /     \\     /     \\\r\n          |     |     ) ~   (\r\n         /       \\   /     ~ \\\r\n         \\       /   \\~     ~/\r\n  /\\__/\\_/\\__  _/_/\\_/\\__~__/_/\\_/\\_/\\_/\\_/\\_\r\n  |  |  |  | ) ) |  |  | ((  |  |  |  |  |  |\r\n  |  |  |  |( (  |  |  |  \\\\ |  |  |  |  |  |\r\n  |  |  |  | )_) |  |  |  |))|  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  (/ |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";


    static void ASCIIAnimation()
    {
        List<string> anims = new List<string>();
        anims.Add(anim1);
        anims.Add(anim2);
        anims.Add(anim3);
        anims.Add(anim4);
        anims.Add(anim5);
        Console.SetWindowSize(50, 25);
        Console.CursorVisible = false;
        Console.BackgroundColor=ConsoleColor.DarkGray;
        Console.ForegroundColor=ConsoleColor.Black;
        while (running)
        {
            nextFrame(anims);
        }
    }

    static void nextFrame(List<string> anims)
    {
        foreach (string a in anims)
        {
            if (running)
            { 
                Console.Clear();
                Console.WriteLine(a);
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
        }
    }

    static void ClearConsoleLines(int numLines)
    {
        // Move the cursor to the top of the current line
        Console.SetCursorPosition(0, Console.CursorTop - numLines);

        // Clear the lines
        for (int i = 0; i < numLines; i++)
        {
            Console.Write(new string(' ', Console.WindowWidth));
            Console.SetCursorPosition(0, Console.CursorTop - 1);
        }

        // Reset the cursor position
        Console.SetCursorPosition(0, 0);
    }
}

