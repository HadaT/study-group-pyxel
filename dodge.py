import pyxel
import random

SCENE_TITLE = 0 # タイトル画面
SCENE_PLAY = 1  # ゲーム画面
SCENE_GAMEOVER = 2  # ゲームオーバー画面

player = None
enemies = []

def push_back(x, y, dx, dy):
    for _ in range(pyxel.ceil(abs(dy))):
        step = max(-1, min(1, dy))
        y += step
        dy -= step
    for _ in range(pyxel.ceil(abs(dx))):
        step = max(-1, min(1, dx))
        x += step
        dx -= step
    return x, y

def spwan_enemy():
    global enemies
    match random.randint(0, 3):
        case 0:
            enemies.append(Enemy(0, random.randint(0, pyxel.height)))
        case 1:
            enemies.append(Enemy(pyxel.width, random.randint(0, pyxel.height)))
        case 2:
            enemies.append(Enemy(random.randint(0, pyxel.width), 0))
        case 3:
            enemies.append(Enemy(random.randint(0, pyxel.width), pyxel.height))

class Player:
    def __init__(self, x, y):
        self.w = 8
        self.h = 8
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        
    def update(self):
        # キー入力
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.dx = -2
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.dx = 2
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.dy = -2
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.dy = 2
        
        # 移動量分移動
        self.x, self.y = push_back(self.x, self.y, self.dx, self.dy)

        # 画面外に行かないように
        if self.x > pyxel.width-self.w:
            self.x = pyxel.width-self.w
        if self.x < 0:
            self.x = 0
        if self.y > pyxel.height-self.h:
            self.y = pyxel.height-self.h
        if self.y < 0:
            self.y = 0

        # 移動量を徐々に減らす
        self.dx = int(self.dx * 0.8)
        self.dy = int(self.dy * 0.8)

    def draw(self):
        # 動いていない時は静止、動いている時は歩行アニメーション
        v =  (0 if self.dx == 0 and self.dy == 0 else 1) * (pyxel.frame_count % 2 + 1) * 8
        pyxel.blt(self.x, self.y, 0, 0, v, self.w, self.h, 0) 

class Enemy:
    def __init__(self, x, y):
        self.w = 8
        self.h = 8
        self.x = x
        self.y = y
        self.random_direction()
        self.rotate = 0

    def update(self):
        # 移動
        self.x += self.dx
        self.y += self.dy

        # 壁に当たった場合はランダムで方向転換
        if self.x > pyxel.width-self.w:
            self.x = pyxel.width-self.w
            self.random_direction()
        if self.x < 0:
            self.x = 0
            self.random_direction()
        if self.y > pyxel.height-self.h:
            self.y = pyxel.height-self.h
            self.random_direction()
        if self.y < 0:
            self.y = 0
            self.random_direction()

        # 回転
        self.rotate += 0.5

    def random_direction(self):
        self.dx = random.uniform(2, -2)
        self.dy = random.uniform(2, -2)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, self.w, self.h, 0, self.rotate) 

class App:
    def __init__(self):
        # 画面サイズ設定
        pyxel.init(160, 120, "Dodge")

        # リソース読み込み
        pyxel.load("my_resource.pyxres")

        self.score = 0
        self.scene = SCENE_TITLE

        # プレイヤーの初期配置
        global player
        player = Player(pyxel.width/2 - 4 , pyxel.height/2 - 4)

        # 敵のポップ
        spwan_enemy()
        
        # 実行
        pyxel.run(self.update, self.draw)

    def update(self):
        # 画面分岐
        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        
        player.update()
        
        # スコア計算
        self.score = len(enemies)
        
        for enemy in enemies:
            # 当たり判定
            if abs(player.x - enemy.x) < enemy.w - 2 and abs(player.y - enemy.y) < enemy.h - 2:
                # 当たっていたらゲームオーバー
                self.gameover()
                return
            
            # 敵の移動処理
            enemy.update()
        
        # 時間経過で敵のポップ
        if pyxel.frame_count != 0 and pyxel.frame_count % 60 == 0:
            spwan_enemy()

    def update_gameover_scene(self):
        global player
        
        # リトライ
        if pyxel.btn(pyxel.KEY_R) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
            self.score = 0
            self.scene = SCENE_PLAY
            player = Player(pyxel.width/2 - 4 , pyxel.height/2 - 4)

        # 終了
        if pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_START):
            pyxel.quit()

    def draw(self):
        # 画面のクリア
        pyxel.cls(0)

        # 画面分岐
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

    def draw_title_scene(self):
        pyxel.text(pyxel.width/2 - 10 , pyxel.height/2-10, "DODGE", 7)
        pyxel.text(pyxel.width/2 - 30 , pyxel.height/2+10, "- PRESS SPACE -", 7)

    def draw_play_scene(self):
        # プレイヤー表示
        player.draw()

        # 敵表示
        for enemy in enemies:
            enemy.draw()
        
        # スコア表示
        pyxel.text(0, 0, f"SCORE {self.score}", 7)

    def draw_gameover_scene(self):
        pyxel.text(pyxel.width/2 - 17 , pyxel.height/2-20, "GAME OVER", 7)
        pyxel.text(pyxel.width/2 - 17 , pyxel.height/2-10, f"SCORE {self.score}", 7)
        pyxel.text(pyxel.width/2 - 17 , pyxel.height/2+10, "[R] RETRY", 7)
        pyxel.text(pyxel.width/2 - 17 , pyxel.height/2+20, "[Q] QUIT", 7)

    def gameover(self):
        # 各種リセット
        global player, enemies
        player = None
        enemies = []
        self.scene = SCENE_GAMEOVER

App()