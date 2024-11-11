import pyxel

# ウィンドウサイズ指定
# init(width, height)
pyxel.init(80, 64)

# 画面を色(col)でクリア 
# cls(col) 
pyxel.cls(1)

# 幅w、高さh、色colの矩形を (x, y) に描画
# rect(x, y, w, h, col)
pyxel.rect(5, 5, 16, 16, 2) 

# 画面を表示し、Escキーが押されるまで待機
pyxel.show()