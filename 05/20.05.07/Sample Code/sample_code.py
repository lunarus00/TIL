import socket
import time
import math

# User and Game Server Information
NICKNAME = 'Python Player'
HOST = '127.0.0.1'
PORT = 1447 # Do not modify

# predefined variables(Do not modify these values)
TABLE_WIDTH = 254
TABLE_HEIGHT = 127
NUMBER_OF_BALLS = 5
HOLES = [ [0, 0], [127, 0], [254, 0], [0, 127], [127, 127], [254, 127] ]

count_play = 0

class Conn:
    def __init__(self):
        self.sock = socket.socket()
        print('Trying to Connect: ' + HOST + ':' + str(PORT))
        self.sock.connect((HOST, PORT))
        print('Connected: ' + HOST + ':' + str(PORT))
        send_data = '9901/' + NICKNAME
        self.sock.send(send_data.encode('utf-8'))
        print('Ready to play.\n--------------------')
    def request(self):
        self.sock.send('9902/9902'.encode())
        print('Received Data has been currupted, Resend Requested.')
    def receive(self):
        recv_data = (self.sock.recv(1024)).decode()
        print('Data Received: ' + recv_data)
        return recv_data
    def send(self, angle, power):
        merged_data = '%f/%f' % (angle, power)
        self.sock.send(merged_data.encode('utf-8'))
        print('Data Sent: ' + merged_data)
    def close(self):
        self.sock.close()

class GameData:
    def __init__(self):
        self.reset()
    def reset(self):
        self.balls = [[0, 0] for i in range(NUMBER_OF_BALLS)]
    def read(self, conn):
        recv_data = conn.receive()
        split_data = recv_data.split('/')
        idx = 0    
        try:
            for i in range(NUMBER_OF_BALLS):
                for j in range(2):
                    self.balls[i][j] = int(split_data[idx])
                    idx += 1
        except:
            self.reset()
            conn.request()
            self.read(conn)
    def show(self):
        print('=== Arrays ===')
        for i in range(NUMBER_OF_BALLS):
            print('Ball%d: %d, %d' % (i, self.balls[i][0], self.balls[i][1]))
        print()

# 자신의 차례가 되어 게임을 진행해야 할 때 호출되는 Method
def play(conn, gameData):
    global count_play
    angle_list = [91.65, 249.4, 356.1, 107.8]
    power_list = [100, 96, 70, 70]
    angle = angle_list[count_play]
    power = power_list[count_play]
    conn.send(angle, power)


def main():
    global count_play
    conn = Conn()
    gameData = GameData()
    while True:
        gameData.read(conn)
        gameData.show()
        if gameData.balls[0][0] == 9909:
            break
        play(conn, gameData)
        count_play += 1
    conn.close()
    print('Connection Closed')

if __name__ == '__main__':
    main()
