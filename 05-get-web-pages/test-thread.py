import threading

def print_numbers():
    for i in range(1, 6):
        print(f'线程1：{i}')

def print_letters():
    for i in range(ord('A'), ord('F')):
        print(f'线程2：{chr(i)}')

# 创建线程对象
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# 启动线程
thread1.start()
thread2.start()

# 等待线程执行完毕
thread1.join()
thread2.join()

print('主线程结束')