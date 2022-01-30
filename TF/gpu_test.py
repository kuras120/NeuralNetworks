import tensorflow as tf


if __name__ == '__main__':
    print(tf.python.client.device_lib.list_local_devices())
    tf.debugging.set_log_device_placement(True)
    # Place tensors on the CPU
    with tf.device('/device:CPU:0'):
        a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    # Run on the GPU
    c = tf.matmul(a, b)
    print(c)
