namespace SpicetifyUpdater;

public static class AsciiArt {
    public static void Begin() =>
        Console.WriteLine("                   _\r\n               _  / |\r\n              / \\ | | /\\\r\n               \\ \\| |/ /\r\n                \\ Y | /___\r\n              .-.) '. `__/\r\n             (.-.   / /\r\n                 | ' |\r\n                 |___|\r\n                [_____]\r\n                |     |");

    public static void PrintThumbsUp() =>
        Console.WriteLine("            .--------._\r\n           (`--'       `-.\r\n            `.______      `.\r\n         ___________`__     \\\r\n      ,-'           `-.\\     |\r\n     //                \\|    |\\\r\n    (`  .'~~~~~---\\     \\'   | |\r\n     `-'           )     \\   | |\r\n        ,---------' - -.  `  . '\r\n      ,'             ` `\\`     |\r\n     /                      \\  |\r\n    /     \\-----.         \\    `\r\n   /|  ,_/      '-._            |\r\n  (-'  /           /            `     \r\n  ,`--<           |        \\     \\\r\n  \\ |  \\         /               `\\\r\n   |/   \\____---'--`         \\     \\\r\n   |    '           `               \\\r\n   |\r\n    `--.__\r\n          `---._______\r\n                      `.\r\n                        \\  ");

    public static void PrintBye() => Console.WriteLine(" __      __\r\n( _\\    /_ )\r\n \\ _\\  /_ / \r\n  \\ _\\/_ /_ _\r\n  |_____/_/ /|\r\n  (  (_)__)J-)\r\n  (  /`.,   /\r\n   \\/  ;   /\r\n    | === |");

    private static bool _playingAnimation;

    public static void CatAnimation() {
        _playingAnimation = true;
        const string anim1 = "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *\r\n          |\\___/|\r\n          )     (             .              '\r\n         =\\     /=\r\n           )===(       *\r\n          /     \\\r\n          |     |\r\n         /       \\\r\n         \\       /\r\n  _/\\_/\\_/\\__  _/_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_\r\n  |  |  |  |( (  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  | ) ) |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |(_(  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";
        const string anim2 = "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *\r\n          |\\___/|\r\n         =) ^Y^ (=            .              '\r\n          \\  ^  /\r\n           )=*=(       *\r\n          /     \\\r\n          |     |\r\n         /| | | |\\\r\n         \\| | |_|/\\\r\n  /\\__/\\_//_// ___/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_\r\n  |  |  |  | \\_) |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";
        const string anim3 = "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *    _\r\n          |\\___/|                      \\\\\r\n         =) ^Y^ (=   |\\_/|              ||    '\r\n          \\  ^  /    )a a '._.-\"\"\"\"-.  //\r\n           )=*=(    =\\T_= /    ~  ~  \\//\r\n          /     \\     `\"`\\   ~   / ~  /\r\n          |     |         |~   \\ |  ~/\r\n         /| | | |\\         \\  ~/- \\ ~\\\r\n         \\| | |_|/|        || |  // /`\r\n  /\\__/\\_//_// __//\\_/\\_/\\_((_|\\((_//\\_/\\_/\\_\r\n  |  |  |  | \\_) |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";
        const string anim4 = "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *    \r\n          |\\___/|     /\\___/\\\r\n          )     (     )    ~( .              '\r\n         =\\     /=   =\\~    /=\r\n           )===(       ) ~ (\r\n          /     \\     /     \\\r\n          |     |     ) ~   (\r\n         /       \\   /     ~ \\\r\n         \\       /   \\~     ~/\r\n  /\\__/\\_/\\__  _/_/\\_/\\__~__/_/\\_/\\_/\\_/\\_/\\_\r\n  |  |  |  |( (  |  |  | ))  |  |  |  |  |  |\r\n  |  |  |  | ) ) |  |  |//|  |  |  |  |  |  |\r\n  |  |  |  |(_(  |  |  (( |  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |\\)|  |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";
        const string anim5 = "             *     ,MMM8&&&.            *\r\n                  MMMM88&&&&&    .\r\n                 MMMM88&&&&&&&\r\n     *           MMM88&&&&&&&&\r\n                 MMM88&&&&&&&&\r\n                 'MMM88&&&&&&'\r\n                   'MMM8&&&'      *    \r\n           /\\/|_      __/\\\\\r\n          /    -\\    /-   ~\\  .              '\r\n          \\    = Y =T_ =   /\r\n           )==*(`     `) ~ \\\r\n          /     \\     /     \\\r\n          |     |     ) ~   (\r\n         /       \\   /     ~ \\\r\n         \\       /   \\~     ~/\r\n  /\\__/\\_/\\__  _/_/\\_/\\__~__/_/\\_/\\_/\\_/\\_/\\_\r\n  |  |  |  | ) ) |  |  | ((  |  |  |  |  |  |\r\n  |  |  |  |( (  |  |  |  \\\\ |  |  |  |  |  |\r\n  |  |  |  | )_) |  |  |  |))|  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  (/ |  |  |  |  |  |\r\n  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |";

        //start a list with anims
        List<string> anims = [anim1, anim2, anim3, anim4, anim5];

        //set console size and color
        Console.SetWindowSize(50, 25);
        Console.CursorVisible = false;
        while (_playingAnimation) { // loop until running is set to false
            NextFrame(anims);
        }
    }

    private static void NextFrame(IEnumerable<string> anims) {
        Console.Title = "Cat Animation - Press 1 to stop. - Playing \"Littleroot Town.wav\"";
        foreach (var anim in anims.Where(anim => true)) {
            Console.Clear();
            Console.WriteLine(anim);
            Console.WriteLine("Press 1 to stop animation's loop and exit.");
            Thread.Sleep(700);
            CheckKey();
            Thread.Sleep(700);
        }
    }

    private static void CheckKey() {
        if (!Console.KeyAvailable || Console.ReadKey(true).Key != ConsoleKey.D1) return;
        _playingAnimation = false;
        if (Program.IsWindows) {
            Program.Player.Dispose();
            Program.Player.Stop();
        }

        Console.CursorVisible = true;
        Console.Clear();
        Program.Main(null);
    }
}