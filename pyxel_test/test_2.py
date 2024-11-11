import pyxel

# ウィンドウサイズ指定
# init(width, height)
pyxel.init(80, 64)
# リソース読み込み
# load(filename)
pyxel.load("my_resource.pyxres")

# 画面を色(col)でクリア 
# cls(col) 
pyxel.cls(1)

# イメージバンクimg(0-2) の (u, v) からサイズ (w, h) の領域を (x, y) にコピー
# colkeyに色を指定すると透明色として扱われれる
# blt(x, y, img, u, v, w, h, [colkey], [rotate], [scale])
pyxel.blt( 5, 5, 0, 0, 0, 8, 8, 0) 
pyxel.blt(20, 5, 0, 8, 0, 8, 8, 0)
pyxel.blt(35, 5, 0, 0, 8, 8, 8, 0)

# 画面を表示し、Escキーが押されるまで待機
pyxel.show()