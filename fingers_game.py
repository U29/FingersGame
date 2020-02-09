""" Fingers game called "Yubisuma" """

import sys
import random
import time

class pycolor:
    """ print color """
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RETURN = '\033[07m' #反転
    ACCENT = '\033[01m' #強調
    FLASH = '\033[05m' #点滅
    RED_FLASH = '\033[05;41m' #赤背景+点滅
    END = '\033[0m'

class Player():
    """ Player class """
    def __init__(self, num):
        self.name = 'Player' + str(num)
        self.current_hands_num = 2
        self.saying_num = 0
        self.is_finished = False

    def say_num(self, finger_max):
        """ saying fingers num in one's turn """
        self.saying_num = random.randint(0, finger_max)
        print('|' + self.name +'|' + " said " + str(self.saying_num))

    def up_finger(self, all_fingers_num):
        """ up one's finger(s) in every turn """
        if self.saying_num == all_fingers_num:
            up_finger_num = self.current_hands_num
        else:
            up_finger_num = random.randint(0, self.current_hands_num)
        # print('|' + self.name +'|' + " up " + str(up_finger_num))
        return up_finger_num

def main():
    """ main game loop """
    players_num = int(input(pycolor.PURPLE + 'How many people in the game?: ' + pycolor.END).rstrip())

    players = []

    for i in range(players_num):
        players.append(Player(i))


    # print('Joined Player List')
    # for i in range(len(players)):
    #     print(players[i].name)
    #     print(players[i].current_finger_num)

    # Game Start #
    start_time = time.time()
    turns = 1 # turn coutner
    finish_num = 0
    ranking = []
    one_left_ranking = []

    while True:
        for i in range(len(players)):
            all_fingers_num = 0
            # 指の数の最大値を求める
            all_hands_num = 0
            for j in range(len(players)):
                all_hands_num += players[j].current_hands_num
            finger_max = all_hands_num

            # 上がったプレイヤーはスキップ
            if players[i].is_finished:
                continue
            print('\n[Turn ' + str(turns) + ']')
            players[i].say_num(finger_max)

            for j in range(len(players)):
                # 上がったプレイヤーはスキップ
                if players[j].is_finished:
                    continue
                all_fingers_num += players[j].up_finger(all_fingers_num)
            
            print('all fingers: ' + str(all_fingers_num)) 
            if players[i].saying_num == all_fingers_num:
                players[i].current_hands_num -= 1
                if players[i].current_hands_num == 1:
                    one_left_ranking.append(players[i].name)
                    print(pycolor.RED + '|' + players[i].name +'|' + ' one left!' + pycolor.END)
                if players[i].current_hands_num < 1:
                    players[i].is_finished = True
                    finish_num += 1
                    ranking.append(players[i].name)
                    print(pycolor.BLUE + '|' + players[i].name +'|' + ' finished!' + pycolor.END)

            # 残りのプレイヤーが1人かどうかを調べる
            if finish_num >= (players_num - 1):
                # 最下位プレイヤーをランキングへ追加
                for j in range(len(players)):
                    if not players[j].is_finished:
                        ranking.append(players[j].name)
                        break
                print('\n\n')
                # ゲームにかかった時間を取得
                elapsed_time = time.time() - start_time
                print(pycolor.GREEN + 'Game Finished!' + pycolor.END)
                print('Total turns: ' + str(turns))
                print('Total time: {0}' .format(elapsed_time) + '[sec]')
                print('\n')
                print(pycolor.RED + '--- one left ranking ---')
                for j in range(len(one_left_ranking)):
                    print(str(j + 1).rjust(len(str(one_left_ranking.index(one_left_ranking[-1]))) + 1) + ': ' + one_left_ranking[j])
                print(pycolor.END)

                print(pycolor.YELLOW + '--- RANKING ---')
                for j in range(len(ranking)):
                    print(str(j + 1).rjust(len(str(ranking.index(ranking[-1]))) + 1) + ': ' + ranking[j])
                print(pycolor.END + '\n')
                sys.exit(0)

            turns += 1

if __name__ == "__main__":
    main()
