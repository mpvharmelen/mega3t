# Mega3T
**Harder, better, faster, stronger tic-tac-toe**

> So what is this Mega3T thing?

Mega3T (Mega Tic-Tac-Toe), more commonly known as Ultimate Tic Tac Toe or
Extreme Tic Tac Toe, is a game based on the well-known timekiller tic-tac-toe
(3t). It's a bit bigger though...

> How do you play it then?

The game is played on a classic 3t board, with a smaller 3t board in each tile
tile. The players fill the small tiles, but can only play in the small board
that was played in the previous turn.

> Huh?

So I wrote a description below, but you can also just read
[this excellent explanation](http://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/).

Okay, picture a Mega3T board:

     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
          |       |
    ------+-------+------
          |       |
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
          |       |
    ------+-------+------
          |       |
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |

The first player gets to play where-ever she wants. The other player has to
play in the small board in the location where the first player played in her
chosen small board. So, let's say the first player starts out here (2, 1):

     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |X |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
          |       |
    ------+-------+------
          |       |
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
          |       |
    ------+-------+------
          |       |
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |

She played in the middle right tile of that particular small board, so her
opponent now has to play in the small board in the middle right of the larger
board. Say she chooses the middle left tile (6, 4):

     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |X |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
          |       |
    ------+-------+------
          |       |
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  | O| |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
          |       |
    ------+-------+------
          |       |
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |

Now the player who started, X, has to play in the middle left board.

     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |X |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
          |       |
    ------+-------+------
          |       |
    X| |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  | O| |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
          |       |
    ------+-------+------
          |       |
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |
    -+-+- | -+-+- | -+-+-
     | |  |  | |  |  | |

And now the O player has to play in the top left. See where this is going?
That was basically the entire overview of rules in Mega3T. The winner is either
whoever wins three small boards in a row, or, if neither player does, whoever
wins more small boards.

> Sounds boring and weird...

Well, it's complicated and it has some interesting new tactics. Because the
gameplay is almost entirely different from classic 3t, almost all the tricks
you might've learned for that are useless here. A lot of new ways to play
arise and it becomes more chess-like.

### Features

* Shows a Mega3T board.
* Allows for entering O's and X's.
* Keeps track of whose turn it is.
* [planned] Enforce gameplay rules.
* [planned] Show winner.
* [planned] Online multiplayer mode.
* [planned] AI.
* [who knows] Android app?
