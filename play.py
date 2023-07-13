# -*- coding: utf-8 -*-
"""
human VS AI models
Input your move in the format: 2,3

@original author: Junxiao Song || https://github.com/junxiaosong/AlphaZero_Gomoku

Dimodifikasi untuk kepentingan seleksi Asisten'21 Laboratorium IRK STEI ITB
"""
from __future__ import print_function
from game import Board, Game
from human import Human
from bots.Bot13521089 import Bot13521089
def run():
    n = 5
    width, height = 8, 8
    try:
        board = Board(width=width, height=height, n_in_row=n)
        game = Game(board)

        """
            TODO: Ganti isi variabel player menjadi bot mu
        """
        player1 = Bot13521089()
        player2 = Human()

        winner = game.start_play(player1, player2, start_player=1, is_shown=1)
        print("SELAMAT KEPADA: ", winner)
    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
