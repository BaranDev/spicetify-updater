# styling.py

# ASCII Art for the cool cat animation frames
CAT_FRAMES = [
    """
             *     ,MMM8&&&.            *
                  MMMM88&&&&&    .
                 MMMM88&&&&&&&
     *           MMM88&&&&&&&&
                 MMM88&&&&&&&&
                 'MMM88&&&&&&'
                   'MMM8&&&'      *
          |\\___/|
          )     (             .              '
         =\\     /=
           )===(       *
          /     \\
          |     |
         /       \\
         \\       /
  _/\\_/\\_/\\__  _/_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_
  |  |  |  |( (  |  |  |  |  |  |  |  |  |  |
  |  |  |  | ) ) |  |  |  |  |  |  |  |  |  |
  |  |  |  |(_(  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    """,
    """
             *     ,MMM8&&&.            *
                  MMMM88&&&&&    .
                 MMMM88&&&&&&&
     *           MMM88&&&&&&&&
                 MMM88&&&&&&&&
                 'MMM88&&&&&&'
                   'MMM8&&&'      *
          |\\___/|
         =) ^Y^ (=            .              '
          \\  ^  /
           )=*=(       *
          /     \\
          |     |
         /| | | |\\
         \\| | |_|/\\
  /\\__/\\_//_// ___/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_
  |  |  |  | \\_) |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    """,
    """
             *     ,MMM8&&&.            *
                  MMMM88&&&&&    .
                 MMMM88&&&&&&&
     *           MMM88&&&&&&&&
                 MMM88&&&&&&&&
                 'MMM88&&&&&&'
                   'MMM8&&&'      *    _
          |\\___/|                      \\
         =) ^Y^ (=   |\\_/|              ||    '
          \\  ^  /    )a a '._.-\"\"\"\"-.  //
           )=*=(    =\\T_= /    ~  ~  \\//
          /     \\     `\"`\\   ~   / ~  /
          |     |         |~   \\ |  ~/
         /| | | |\\         \\  ~/- \\ ~\\
         \\| | |_|/|        || |  // /`
  /\\__/\\_//_// __//\\_/\\_/\\_((_|\\((_//\\_/\\_/\\_
  |  |  |  | \\_) |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    """,
    """
            *     ,MMM8&&&.            *
                  MMMM88&&&&&    .
                 MMMM88&&&&&&&
     *           MMM88&&&&&&&&
                 MMM88&&&&&&&&
                 'MMM88&&&&&&'
                   'MMM8&&&'      *    
          |\\___/|     /\\___/\\
          )     (     )    ~( .              '
         =\\     /=   =\\~    /=
           )===(       ) ~ (
          /     \\     /     \\
          |     |     ) ~   (
         /       \\   /     ~ \\
         \\       /   \\~     ~/
  /\\__/\\_/\\__  _/_/\\_/\\__~__/_/\\_/\\_/\\_/\\_/\\_
  |  |  |  |( (  |  |  | ))  |  |  |  |  |  |
  |  |  |  | ) ) |  |  |//|  |  |  |  |  |  |
  |  |  |  |(_(  |  |  (( |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |\\)|  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    """,
    """
             *     ,MMM8&&&.            *
                  MMMM88&&&&&    .
                 MMMM88&&&&&&&
     *           MMM88&&&&&&&&
                 MMM88&&&&&&&&
                 'MMM88&&&&&&'
                   'MMM8&&&'      *    
           /\\/|_      __/\\\\
          /    -\\    /-   ~\\  .              '
          \\    = Y =T_ =   /
           )==*(`     `) ~ \\
          /     \\     /     \\
          |     |     ) ~   (
         /       \\   /     ~ \\
         \\       /   \\~     ~/
  /\\__/\\_/\\__  _/_/\\_/\\__~__/_/\\_/\\_/\\_/\\_/\\_
  |  |  |  | \\_) |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
    """,
    # Add other frames here
]

# ASCII Art for thumbs up
THUMBS_UP = """
            .--------._
           (`--'       `-.
            `.______      `.
         ___________`__     \\
      ,-'           `-.\\     |
     //                \\|    |\\
    (`  .'~~~~~---\\     \\'   | |
     `-'           )     \\   | |
        ,---------' - -.  `  . '
      ,'             ` `\\`     |
     /                      \\  |
    /     \\-----.         \\    `
   /|  ,_/      '-._            |
  (-'  /           /            `
  ,`--<           |        \\     \\
  \\ |  \\         /               `\\
   |/   \\____---'--`         \\     \\
   |    '           `               \\
   |
    `--.__
          `---._______
                      `.
                        \\
"""

# ASCII Art for BARANDEV banner
BANNER = """
    ██████╗  █████╗ ██████╗  █████╗ ███╗   ██╗██████╗ ███████╗██╗   ██╗
    ██╔══██╗██╔══██╗██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔════╝██║   ██║
    ██████╔╝███████║██████╔╝███████║██╔██╗ ██║██║  ██║█████╗  ██║   ██║
    ██╔══██╗██╔══██║██╔══██╗██╔══██║██║╚██╗██║██║  ██║██╔══╝  ╚██╗ ██╔╝
    ██████╔╝██║  ██║██║  ██║██║  ██║██║ ╚████║██████╔╝███████╗ ╚████╔╝ 
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝  ╚═══╝  
██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██████╗     ██╗   ██╗██████╗ 
██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗    ██║   ██║╚════██╗
██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██████╔╝    ██║   ██║ █████╔╝
██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ██╔══██╗    ╚██╗ ██╔╝██╔═══╝ 
╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██║  ██║     ╚████╔╝ ███████╗
 ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝      ╚═══╝  ╚══════╝                                                                                              
"""
