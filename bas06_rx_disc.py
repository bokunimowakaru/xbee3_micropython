# MicroPython XBee3 ZigBee
# coding: utf-8
'''
discover命令を使ってネットワーク上のデバイスを発見したときに表示する
                                                  Copyright (c) 2018-2019 Wataru KUNINO
'''
import xbee
import time
import binascii

DEV_TYPES = ['COORDINATOR', 'ROUTER', 'END DEVICE']
next_ms = 0                                 # 次回、discover関数を実行する時刻
devs=[]                                     # デバイスのアドレスを登録する配列変数

def discover(next_ms):                      # discover関数の定義
    if time.ticks_ms() < next_ms:           # 現在時刻が次回の実行時刻に満たない時
        return next_ms                      # 処理を中止
    disc_devs = xbee.discover()             # デバイスを検索し、結果をdisc_devsへ代入
    for dev in disc_devs:                   # 個々のデバイスの処理
        addr = str(binascii.hexlify(dev['sender_eui64']).decode('utf-8'))
        type = DEV_TYPES[ dev['node_type'] ]
        if addr not in devs:                # 過去に発見されていないデバイス発見時
            devs.append(addr)               # 配列に送信元アドレスを追加
            addr=addr[:8] + ' ' + addr[8:]  # 送信元アドレスを表示用(8+8文字)に分離
            print('found',addr,type)        # 発見したデバイスを表示する
    next_ms = time.ticks_ms() + 6000        # 次回の実行は6秒後
    return next_ms

while True:
    status = xbee.atcmd('AI')               # ネットワーク参加状態を確認する
    print('.',end='')
    if status == 0x00:                      # 参加状態の時にループを抜ける
        break
    xbee.atcmd('CB',0x01)                   # コミッショニング(ネットワーク参加)
    time.sleep_ms(2000)                     # 2秒間の待ち時間処理
print('\nJoined')

xbee.atcmd('CB',0x01)                       # コミッショニング(ネットワーク参加通知)
time.sleep_ms(2000)                         # 2秒間の待ち時間処理

while True:
    next_ms = discover(next_ms)             # discover関数の呼び出し
    packet = xbee.receive()                 # パケットの受信を行う
    if packet:                              # 受信データがある時
        addr = str(binascii.hexlify(packet['sender_eui64']).decode('utf-8'))
        addr = addr[:8] + ' ' + addr[8:]    # 送信元アドレスを表示用(8+8文字)に分離
        payload = str(packet['payload'].decode('utf-8'))    # 受信データを抽出
        print(addr + ', ' + payload)        # アドレスと受信データを表示する
