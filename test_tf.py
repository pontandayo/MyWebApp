import tensorflow as tf

# TensorFlowのバージョンを表示
print("TensorFlow version:", tf.__version__)

# 簡単なテスト: 定数の作成と演算
a = tf.constant(5)
b = tf.constant(3)
c = a + b

print("TensorFlow簡単な計算結果:", c.numpy())

