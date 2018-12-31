# MicroPython XBee3 ZigBee
# coding: utf-8
'''
receive命令を使ってXBee ZigBeeパケットに含まれる文字列の受信を行う
（送信元アドレスとペイロードを表示）
                                                  Copyright (c) 2018-2019 Wataru KUNINO
'''
import xbee
import time
import binascii

while True:
    status = xbee.atcmd('AI')               # ネットワーク参加状態を確認する
    print('.',end='')
    if status == 0x00:                      # 参加状態の時にループを抜ける
        break
    xbee.atcmd('CB',0x01)                   # コミッショニング(ネットワーク参加)
    time.sleep_ms(2000)                     # 2秒間の待ち時間処理
print('\nJoined')

while True:
    packet = xbee.receive()                 # パケットの受信を行う
    if packet:                              # 受信データがある時
        addr = str(binascii.hexlify(packet['sender_eui64']).decode('utf-8'))
        addr = addr[:8] + ' ' + addr[8:]    # 送信元アドレスを表示用(8+8文字)に分離
        payload = str(packet['payload'].decode('utf-8'))    # 受信データを抽出
        print(addr + ', ' + payload)        # アドレスと受信データを表示する
