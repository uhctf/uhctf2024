#!/usr/bin/env python

from typing import Optional
from tetris.engine import Engine, Scorer
from tetris.game import BaseGame, MoveDelta
from tetris.impl import gravity, queue, rotation
from tetris.impl.custom import CustomEngine
from tetris.types import PieceType


from twisted.internet import defer, reactor
from twisted.names import dns, server
from twisted.python import failure

from uuid import uuid4, UUID
from os import getenv

from datetime import datetime, timedelta
import re
import logging
logging.getLogger('dnstris')

FLAG = b"uhctf{dnstris_is_a_registered_trademark_of_The_Dnstris_Company_5c5eea40f6}"


#  Info prompts, shown to the user. The first item is the upper limit (written here as a score and then added by one).
trashtalks = list(reversed(sorted([
    (0, b"Looks like you need some practice, better stick to tic-tac-toe for now."),
    (1, b"Oh, you got a point? Let's call it a participation trophy."),
    (2, b"Two points, that's cute. At this rate, it'll take you a month to reach 10."),
    (3, b"Three points? Don't quit your day job."),
    (4, b"Four points, I've seen better play from a toddler."),
    (5, b"Five points, that's just sad."),
    (6, b"Six points? My grandma scores better than that."),
    (7, b"Seven points, it's like watching paint dry, but less exciting."),
    (8, b"Eight points, maybe try a game you're actually good at?"),
    (9, b"Nine points? Better luck next time."),
    (10,
     b"Finally made it to 10 points. Don't break a nail celebrating. " + FLAG),
    (11, b"Oh, so you wanna keep going, huh? Fine, I'll keep trashing you."),
    (15, b"Fifteen points, that's like a drop in the ocean. Time to focus on the CTF and bring home the real prize."),
    (20, b"Twenty points, nice effort, but the real challenge is waiting in the CTF."),
    (25, b"Twenty-five points, not bad, but the CTF needs your full attention if you want to stand a chance."),
    (30, b"Thirty points, impressive, but the clock is ticking and the CTF is calling. Time to put your skills to the test."),
    (40, b"Forty points, still a long way to go if you want to be a CTF champion."),
    (50, b"Fifty points, halfway there, but the CTF will test your coding and debugging skills to the limit."),
    (60, b"Sixty points, impressive, but the CTF is where you'll put your knowledge of cryptography and network security to the test."),
    (70, b"Seventy points, keep pushing, but don't forget the CTF is where you'll showcase your ability to think outside the box."),
    (80, b"Eighty points, almost there, but the CTF is where you'll demonstrate your expertise in digital forensics and exploitation."),
    (90, b"Ninety points, close, but the CTF is where you'll need to combine all your skills to solve real-world security problems."),
    (100, b"A hundred points, well done, but the CTF is where you'll measure yourself against the best in the field."),
    (101, b"Still going, huh? Fine, there's a prize if you can reach the Dragon Ball Z score."),
    (9001, b"It's OVER 9000! I'm sure all those hours spent stacking blocks will come in handy when you're facing real-world security in the future! Please write a message about how you wasted this chance to actually learn something about security to @editicalu."),
], key=lambda item: item[0])))


def score_to_trashtalk(score: int) -> str:
    # Trashtalk by OpenAI :)
    for limit, entry in trashtalks:
        if score >= limit:
            return entry
    return b"ERROR"


class UhctfScorer(Scorer):
    """Our own implementation of a scorer to only count the amount of completed lines."""

    def __init__(self,
                 # Parameters required for library
                 score: Optional[int] = None,
                 level: Optional[int] = None,
                 initial_level: Optional[int] = None):
        _ = score
        _ = level
        _ = initial_level
        self.score = 0
        self.line_clears = 0
        self.level = 0

    def judge(self, delta: MoveDelta) -> None:
        self.score += len(delta.clears)
        self.line_clears += len(delta.clears)


class TetrisGame:
    def __init__(self, **args):
        super(**args)
        self.boardconverter = [b' ', b'I', b'J',
                               b'L', b'O', b'S', b'T', b'Z', b'x']
        # Written pretty extensive, but readeable
        self.piececonverter = {
            None: b'    ' + b'    ' + b'    ' + b'    ',
            PieceType.I: b' I  ' + b' I  ' + b' I  ' + b' I  ',
            PieceType.J: b'  J ' + b'  J ' + b' JJ ' + b'    ',
            PieceType.L: b' L  ' + b' L  ' + b' LL ' + b'    ',
            PieceType.O: b'    ' + b' OO ' + b' OO ' + b'    ',
            PieceType.S: b' S  ' + b' SS ' + b'  S ' + b'    ',
            PieceType.T: b'    ' + b'TTT ' + b' T  ' + b'    ',
            PieceType.Z: b'  Z ' + b' ZZ ' + b' Z  ' + b'    '}
        self.touched = datetime.now()
        # How its done in the official documentation
        engine = CustomEngine
        self.game = BaseGame(engine)
        self.game.engine.parts["scorer"] = UhctfScorer()
        self.game.reset()

    # ----------------------------------
    # Functions for cleanup of old games
    # ----------------------------------
    def touch(self):
        if self.game.playing:
            self.touched = datetime.now()
            self.game.tick()

    def touched(self):
        return self.touched

    # -------------------------------------------------------
    # Functions related to the board and other visualizations
    # -------------------------------------------------------
    def board(self):
        board = self.game.get_playfield()
        output = b""
        for line in board:
            for entry in line:
                output += self.boardconverter[entry]
        return output

    def holded(self) -> bytes:
        holding = self.game.hold
        returning = self.piececonverter[holding]
        return returning

    def next(self):
        next = self.game.queue[0]
        returning = self.piececonverter[next]
        return returning

    # -----
    # State
    # -----
    def score(self):
        return self.game.score

    def gameover(self):
        return not self.game.playing

    # -------
    # Actions
    # -------
    def left(self):
        self.game.left()

    def right(self):
        self.game.right()

    def down(self):
        self.game.soft_drop()

    def rotate(self):
        self.game.rotate()

    def drop(self):
        self.game.hard_drop()

    def hold(self):
        self.game.swap()


class GameController():
    """Handles all the tetris-related stuff. Doesn't know anything about DNS"""

    def __init__(self):
        self.games = dict()

    def new_game(self):
        new_uuid = uuid4()
        self.games[new_uuid] = TetrisGame()
        return new_uuid

    def get_game(self, uuid: UUID) -> TetrisGame | None:
        game_opt = self.games.get(uuid)
        if game_opt is not None:
            game_opt.touch()
        return game_opt

    def clean_games(self, timeout=600):
        """Delete games that aren't touched for over 'timeout' seconds."""


class TetrisAuthorityServer():
    def __init__(self, game_controller: GameController, basedomain='dnstris.ctf'):

        self.gamectl = game_controller
        self.basedomain = basedomain

        self.commands = ['hold', 'left', 'right',
                         'drop', 'down', 'rotate']
        self.cmdregex = re.compile(r'(' + '|'.join(self.commands) + r')\.' +
                                   # UUID
                                   r'([0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15})\.' +
                                   # Basedomain in the regex format
                                   basedomain.replace('.', r'\.'))
        self.txtregex = re.compile(r'([0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15})\.' + basedomain.replace(
            '.', r'\.'))

        # Max length of a valid request. To avoid a DDoS on regex matching
        # Not the most efficient way to calculate it, but it makes the formula clear
        self.maxlength = max(
            map(lambda i: len(i), self.commands)) + len('.') + len(uuid4().hex) + len('.') + len(self.basedomain) + len('.')

    def lookupAllRecords(self, query, timeout=None):
        return defer.fail(failure.Failure(dns.AuthoritativeDomainError()))

    def query(self, query, timeout=None):
        if len(query.name.name) > self.maxlength:
            print(
                f"Skipping query {query} because it is too long to be valid.")
            return defer.fail(failure.Failure(dns.AuthoritativeDomainError()))
        name: bytes = query.name.name.lower()
        name_str = name.decode('utf-8')
        authority = []
        answers = []
        additional = []

        # if query.type == dns.A:
        if name_str == self.basedomain:
            # starting a new game
            uuid = self._new_game()
            cname_name = f'{uuid}.{self.basedomain}'

            answers.append(dns.RRHeader(
                name=name,
                type=dns.CNAME,
                cls=dns.IN,
                ttl=1,
                auth=True,
                # payload=dns.Record_A(address='127.0.0.1'),
                payload=dns.Record_CNAME(name=cname_name),
            ))
            answers.append(dns.RRHeader(
                name=cname_name,
                type=dns.A,
                cls=dns.IN,
                ttl=1,
                payload=dns.Record_A('0.0.0.0')
            ))

            return defer.succeed((answers, authority, additional))

        cmd_regex_match = re.fullmatch(self.cmdregex, name_str)
        if cmd_regex_match is not None:
            # Check if game exists
            uuid = cmd_regex_match[2]
            uuid = UUID(uuid)
            game = self.gamectl.get_game(uuid)
            if game is None:
                return defer.fail(failure.Failure(dns.AuthoritativeDomainError()))

            # perform command
            cmd = cmd_regex_match[1]
            if cmd == self.commands[0]:
                game.hold()
            elif cmd == self.commands[1]:
                game.left()
            elif cmd == self.commands[2]:
                game.right()
            elif cmd == self.commands[3]:
                game.drop()
            elif cmd == self.commands[4]:
                game.down()
            elif cmd == self.commands[5]:
                game.rotate()
            else:
                # Command doesn't exist
                return defer.fail(failure.Failure(dns.AuthoritativeDomainError()))

            return defer.succeed(([], [dns.RRHeader(
                name=name,
                type=dns.TXT,
                cls=dns.IN,
                ttl=1,
                payload=dns.Record_TXT(b'OK'))], []))

        txt_regex_match = re.fullmatch(self.txtregex, name_str)
        if txt_regex_match is not None:
            # Check if game exists.
            uuid = txt_regex_match[1]
            uuid = UUID(uuid)
            game = self.gamectl.get_game(uuid)
            if game is None:
                return defer.fail(failure.Failure(dns.AuthoritativeDomainError()))

            # Add an A-record to ease the challenge
            answers.append(dns.RRHeader(
                name=name,
                type=dns.A,
                cls=dns.IN,
                ttl=1,
                payload=dns.Record_A('0.0.0.0')
            ))

            # Add the board
            board = b'board=' + game.board()
            answers.append(dns.RRHeader(
                name=name,
                type=dns.TXT,
                cls=dns.IN,
                ttl=1,
                # payload=dns.Record_A(address='127.0.0.1'),
                payload=dns.Record_TXT(board)))
            nxt = b'next=' + game.next()
            answers.append(dns.RRHeader(
                name=name,
                type=dns.TXT,
                cls=dns.IN,
                ttl=1,
                payload=dns.Record_TXT(nxt)))
            hold = b'holding=' + game.holded()
            answers.append(dns.RRHeader(
                name=name,
                type=dns.TXT,
                cls=dns.IN,
                ttl=1,
                payload=dns.Record_TXT(hold)))

            # Score record
            score = game.score()
            score_record = b'score=' + bytes(str(score), 'utf-8')
            answers.append(dns.RRHeader(
                name=name,
                type=dns.TXT,
                cls=dns.IN,
                ttl=1,
                payload=dns.Record_TXT(score_record)))

            # Insert trashtalk
            info = b"game over!" if game.gameover() else score_to_trashtalk(score)
            info_record = b'info=' + info
            answers.append(dns.RRHeader(
                name=name,
                type=dns.TXT,
                cls=dns.IN,
                ttl=1,
                payload=dns.Record_TXT(info_record)))

            return defer.succeed((answers, authority, additional))

        return defer.fail(failure.Failure(dns.AuthoritativeDomainError()))

    def _new_game(self) -> str:
        uuid = self.gamectl.new_game()
        return uuid.hex


def main():
    """
    Run the server.
    """
    gc = GameController()
    factory = server.DNSServerFactory(
        clients=[TetrisAuthorityServer(gc)]
    )

    protocol = dns.DNSDatagramProtocol(controller=factory)

    port = int(getenv("PORT_NUMBER") or "5353")
    reactor.listenUDP(port, protocol)
    reactor.listenTCP(port, factory)

    reactor.run()


if __name__ == '__main__':
    main()
