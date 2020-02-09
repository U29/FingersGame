""" Fingers game called "Yubisuma" """

import sys
import os
import random
import time
import pygame
from pygame.locals import *


# pygameを初期化
pygame.init()

# ウィンドウサイズ
(WIDTH, HEIGHT) = (1800, 1080)
# スクリーンサイズ
SCREEN_SIZE = (WIDTH, HEIGHT)
# SCREEN_SIZEの画面を作成
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
# タイトルバーの文字列をセット
pygame.display.set_caption("FingersGame")
SCREEN.fill((0, 0, 0))

# フォルダへのパスを変数に格納
GAME_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(GAME_DIR, "images")

# Player画像の読み込み
PLAYER_LEFT_DOWN_IMG = pygame.image.load(os.path.join(IMG_DIR, "left_down.png")).convert_alpha()
PLAYER_LEFT_UP_IMG = pygame.image.load(os.path.join(IMG_DIR, "left_up.png")).convert_alpha()
PLAYER_RIGHT_DOWN_IMG = pygame.image.load(os.path.join(IMG_DIR, "right_down.png")).convert_alpha()
PLAYER_RIGHT_UP_IMG = pygame.image.load(os.path.join(IMG_DIR, "right_up.png")).convert_alpha()


# フォントの読み込み
FONT = pygame.font.SysFont(None, 30)

class pycolor():
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

class LeftUpImg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(PLAYER_LEFT_UP_IMG, (100, 100))
        self.rect = self.image.get_rect()

    def set_position(self, offset_x, offset_y):
        """ プレイヤーごとに画像に隙間を開ける """
        self.rect.move_ip(offset_x, offset_y)

class LeftDownImg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(PLAYER_LEFT_DOWN_IMG, (100, 100))
        self.rect = self.image.get_rect()

    def set_position(self, offset_x, offset_y):
        """ プレイヤーごとに画像に隙間を開ける """
        self.rect.move_ip(offset_x, offset_y)

class RightUpImg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(PLAYER_RIGHT_UP_IMG, (100, 100))
        self.rect = self.image.get_rect()

    def set_position(self, offset_x, offset_y):
        """ プレイヤーごとに画像に隙間を開ける """
        self.rect.move_ip(offset_x, offset_y)

class RightDownImg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(PLAYER_RIGHT_DOWN_IMG, (100, 100))
        self.rect = self.image.get_rect()

    def set_position(self, offset_x, offset_y):
        """ プレイヤーごとに画像に隙間を開ける """
        self.rect.move_ip(offset_x, offset_y)

class Player():
    """ Player class """
    def __init__(self, num):
        self.num = num
        self.name = 'Player' + str(self.num)
        self.current_hands_num = 2
        self.saying_num = 0
        self.is_finished = False
        self.left_up_img = LeftUpImg()
        self.left_down_img = LeftDownImg()
        self.right_up_img = RightUpImg()
        self.right_down_img = RightDownImg()
        self.hand_sprites = pygame.sprite.Group()
        self.name_text = FONT.render(self.name, True, (255, 255, 255))

        # プレイヤー番号に従って画像を右へずらす
        if num < 16:
            self.left_up_img.set_position(num*110, 0)
            self.left_down_img.set_position(num*110, 0)
            self.right_up_img.set_position(num*110+30, 0)
            self.right_down_img.set_position(num*110+30, 0)
        else:
            self.left_up_img.set_position((num-16)*110, 140)
            self.left_down_img.set_position((num-16)*110, 140)
            self.right_up_img.set_position((num-16)*110+30, 140)
            self.right_down_img.set_position((num-16)*110+30, 140)


    def draw_hand(self, mode):
        # 画像の描画
        self.hand_sprites.empty()   # グループを空にする
        if mode == 0:
            if self.current_hands_num == 2:
                # 2機残ってるとき
                self.hand_sprites.add(self.left_down_img)
            self.hand_sprites.add(self.right_down_img)
        elif mode == 1:
            if self.current_hands_num == 2:
                # 2機残ってるとき
                self.hand_sprites.add(self.left_down_img)
            self.hand_sprites.add(self.right_up_img)
        elif mode == 2:
            self.hand_sprites.add(self.left_up_img)
            self.hand_sprites.add(self.right_up_img)
        
        # グループの画像を描画
        self.hand_sprites.draw(SCREEN)
        self.draw_player_name()

    def say_num(self, finger_max):
        """ saying fingers num in one's turn """
        self.saying_num = random.randint(0, finger_max)
        print('|' + self.name +'|' + " said " + str(self.saying_num))
        text = FONT.render('said ' + str(self.saying_num), True, (0, 255, 0))
        if self.num < 16:
            SCREEN.blit(text, (self.num * 110 + 40, 100))
        else:
            SCREEN.blit(text, ((self.num-16) * 110 + 40, 240))
        text = FONT.render('|' + self.name + '|'' said ' + str(self.saying_num), True, (0, 255, 0))
        SCREEN.blit(text, (600, 340))


    def up_finger(self, all_fingers_num):
        """ 指をあげる時の処理(毎ターン) """
        if self.saying_num == all_fingers_num:
            up_finger_num = self.current_hands_num
        else:
            up_finger_num = random.randint(0, self.current_hands_num)

        # print('|' + self.name +'|' + " up " + str(up_finger_num))
        self.draw_hand(up_finger_num)
        #　上げた指の数を返す
        return up_finger_num

    def draw_player_name(self):
        if self.current_hands_num == 1:
            self.name_text = FONT.render(self.name, True, (255, 255, 0))
        if self.num < 16:
            SCREEN.blit(self.name_text, (self.num*110+30, 0))
        else:
            SCREEN.blit(self.name_text, ((self.num-16)*110+30, 140))

def draw_ui(ranking, last_one, turn_num, all_fingers_num=-1):
    ranking_title_text = FONT.render('--- RANKING ---', True, (0, 255, 255))
    last_one_title_text = FONT.render('--- LAST ONE ---', True, (255, 255, 0))
    turn_num_text = FONT.render('Turn: ' + str(turn_num), True, (0, 0, 255))
    
    for j in range(len(ranking)):
        ranking_name = str(j + 1).rjust(len(str(ranking.index(ranking[-1]))) + 1) + ': ' + ranking[j]
        ranking_name_text = FONT.render(ranking_name, True, (0, 255, 255))
        SCREEN.blit(ranking_name_text, (0, 400 + 20 * j))
    
    for j in range(len(last_one)):
        last_one_name = str(j + 1).rjust(len(str(last_one.index(last_one[-1]))) + 1) + ': ' + last_one[j]
        last_one_name_text = FONT.render(last_one_name, True, (255, 255, 0))
        SCREEN.blit(last_one_name_text, (300, 400 + 20 * j))

    SCREEN.blit(ranking_title_text, (0, 360))
    SCREEN.blit(last_one_title_text, (300, 360))
    SCREEN.blit(turn_num_text, (600, 400))
    # 全ての指の数を表示する
    if all_fingers_num == -1:
        # 指の宣言前
        all_fingers_num_text = FONT.render('Raised finger(s): ', True, (255, 0, 0))
        SCREEN.blit(all_fingers_num_text, (600, 360))
    else:
        # 指の数が宣言されている(ゲーム中)
        all_fingers_num_text = FONT.render('Raised finger(s): ' + str(all_fingers_num), True, (255, 0, 0))
        SCREEN.blit(all_fingers_num_text, (600, 360))
        
    

def main():
    """ ゲーム本体 """
    pygame.display.update()  # 画面を更新

    # プレイヤー人数を入力
    # players_num = \
    #     int(input(pycolor.PURPLE + 'How many people in the game?: ' + pycolor.END).rstrip())
    players_num = 1000

    # プレイヤー1人1人を格納するからのリストを作成
    players = []

    # inputで受け取った数のプレイヤーを作成、リストに格納
    for i in range(players_num):
        players.append(Player(i))

    # Game Start #
    start_time = time.time()
    turns = 1 # turn coutner
    game_speed = 0
    finish_num = 0
    ranking = []
    one_left_ranking = []
    game_finished = False

    # メインゲームループ
    while True:
        for i in range(len(players)):
            # ゲームが終了していたらループを抜ける
            if game_finished:
                continue
            
            # 上がったプレイヤーはスキップ
            if players[i].is_finished:
                continue

            # イベント処理
            for event in pygame.event.get():
                if event.type == QUIT:  # 終了イベント
                    sys.exit()
            # 全ての指の数の初期化
            all_fingers_num = 0
            # 指の数の最大値を求める
            all_hands_num = 0
            for j in range(len(players)):
                all_hands_num += players[j].current_hands_num
            finger_max = all_hands_num

            # 上がったプレイヤーはスキップ
            if players[i].is_finished:
                continue

            # ターン開始
            print('\n[Turn ' + str(turns) + ']')

            # 全員指を下げた状態を描画
            for j in range(len(players)):
                # 上がったプレイヤーはスキップ
                if players[j].is_finished:
                    players[j].finish_turn = turns
                    continue
                players[j].draw_hand(0)
            draw_ui(ranking, one_left_ranking, turns)
            pygame.display.update()  # 画面を更新
            pygame.time.delay(game_speed)
            # 真っ黒に塗りつぶす
            SCREEN.fill((0, 0, 0))

            # 指の数を宣言
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
                    # リーチになったとき
                    one_left_ranking.append(players[i].name + ' (Turn: ' + str(turns) +')')
                    print(pycolor.RED + '|' + players[i].name +'|' + ' one left!' + pycolor.END)
                if players[i].current_hands_num < 1:
                    # プレイヤー抜け
                    players[i].is_finished = True
                    finish_num += 1
                    ranking.append(players[i].name + ' (Turn: ' + str(turns) +')')
                    print(pycolor.BLUE + '|' + players[i].name +'|' + ' finished!' + pycolor.END)

            # 残りのプレイヤーが1人かどうかを調べる
            if finish_num >= (players_num - 1):
                # 最下位プレイヤーをランキングへ追加
                for j in range(len(players)):
                    if not players[j].is_finished:
                        ranking.append(players[j].name +' (Turn: ' + str(turns) + ' [lose])')
                        draw_ui(ranking, one_left_ranking, turns, all_fingers_num)
                        pygame.display.update()  # 画面を更新
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
                game_finished = True


            draw_ui(ranking, one_left_ranking, turns, all_fingers_num)
            pygame.display.update()  # 画面を更新
            pygame.time.delay(game_speed)
            # 真っ黒に塗りつぶす
            SCREEN.fill((0, 0, 0))
            
            turns += 1

if __name__ == "__main__":
    main()
