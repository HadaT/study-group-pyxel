import pyxel

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

class App:
    # 初期化
    def __init__(self):
        # ウィンドウサイズ指定
        # init(width, height)
        pyxel.init(160, 120)
        # リソース読み込み
        # load(filename)
        pyxel.load("my_resource.pyxres")

        self.player_w = 8
        self.player_h = 8
        self.player_x = 5
        self.player_y = 5
        self.player_dx = 0
        self.player_dy = 0

        # Pyxelアプリケーションを開始 フレーム更新時にupdate関数、描画時にdraw関数を呼ぶ
        # run(update, draw)
        pyxel.run(self.update, self.draw)

    # フレームの更新処理
    def update(self):
        self.update_player()

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player_dx = -2
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player_dx = 2
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.player_dy = -2
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.player_dy = 2
        
        self.player_x, self.player_y = push_back(self.player_x, self.player_y, self.player_dx, self.player_dy)
        if self.player_x > pyxel.width-self.player_w:
            self.player_x = pyxel.width-self.player_w
        if self.player_x < 0:
            self.player_x = 0
        if self.player_y > pyxel.height-self.player_h:
            self.player_y = pyxel.height-self.player_h
        if self.player_y < 0:
            self.player_y = 0
        self.player_dx = int(self.player_dx * 0.5)
        self.player_dy = int(self.player_dy * 0.5)

    # 描画処理
    def draw(self):
        # 画面を色(col)でクリア 
        # cls(col) 
        pyxel.cls(1)

        # イメージバンクimg(0-2) の (u, v) からサイズ (w, h) の領域を (x, y) にコピー
        # colkeyに色を指定すると透明色として扱われれる
        # blt(x, y, img, u, v, w, h, [colkey], [rotate], [scale])
        pyxel.blt( self.player_x, self.player_y, 0, 0, 0, self.player_w, self.player_h, 0) 

App()