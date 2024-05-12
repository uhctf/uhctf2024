# dnstris

Run Tetris over DNS.

Challenge (and solution) for UHCTF 2024.

# Introduction

All these vulnerabilities, pff. Wouldn't you rather play a game? I've made this Tetris™ game. Why not give it a shot? I'll give you a flag if you can clear 10 lines. One problem: it's made using DNS.

# Howto

- To start a new game, query to dnstris.ctf. This will give you a CNAME, which is the UUID (domain) for the game.

Now, to perform actions, you can perform the following queries (as subdomain of your game's domain).

- 'left' and 'right' to move the tetromino to the left and right resp.
- 'rotate' to rotate the block.
- 'down' to move the block down by one.
- 'drop' to immediately drop the tetromino.
- '@' gives you board, next block, holded block, an info line and your score. Board, next and hold are encoded as a string. ` ` indicates an empty square, an uppercase letter means a filled square (from the tetromino with that name, so the J-block has letter `J`) and a lowercase letter `x` means a ghost.
- 'score' to view the score
- 'next' shows the following tetromino, visualized as the holding block.
- 'hold' to put the tetromino in holding
- 'holding' 4x4 display of any holding block. Visualisation is similar to the board.

# Solution

Write an application that queries the server and puts out commands when needed.

# Hint (60%)

Gives you Python code that handles all DNS specifics, reducing this to a simple coding assignment.
