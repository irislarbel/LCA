# -*- coding: utf-8 -*-
import hashlib
import random


TARGET_FILE_NAME = r"YOUR LOCATE"
OUTPUT_FILE_NAME = r"YOUR LOCATE"
IV_LEN = 16

MAGIC_NUM = 0x45d9f3b
DATA_LEN = 10
BLOCK_SIZE = 512

WARMUP = 200
RUN = 1000

TABLE = bytearray(16)

def main_run():
    
    def xor_seed(data: bytes, oldkey: int) -> int:
        oldkbyte = oldkey.to_bytes(32, 'big')
        hashdat = hashlib.sha256(oldkbyte + data).digest()
        seed = (int.from_bytes(hashdat, 'big') ^ MAGIC_NUM) & 0xFFFFFFFF
        return seed, (seed % 7) + 1

    def make_table(seed, rotval):
        random.seed(seed << rotval | rotval)
        
        pool = list(range(16))
        for i in range(16):
            j = random.getrandbits(4) % (16 - i)
            TABLE[i] = pool.pop(j)
        
        return TABLE

    def convert(chunk, mapping_table, rot):
        prev = 0
        for i in range(len(chunk)):
            up4 = (chunk[i] >> 4) & 0x0F
            lo4 = chunk[i] & 0x0F
            chunk[i] = ((mapping_table.index(up4) << 4) | mapping_table.index(lo4))
            
            
            rotate = ((prev << rot) | (prev >> (8 - rot))) & 0xFF
            chunk[i] = (chunk[i] - rotate) % 256
            prev = chunk[i]
            
            
        return chunk

    def dec_file():
        with open(TARGET_FILE_NAME, 'rb') as infile, open(OUTPUT_FILE_NAME, 'wb') as outfile:
            IV = infile.read(IV_LEN)
            next_key = FIR_KEY ^ int.from_bytes(IV, 'big')
            next_rot = 1
            while chunk := infile.read(BLOCK_SIZE):
                outfile.write(convert(bytearray(chunk), make_table(next_key, next_rot), next_rot))
                next_key, next_rot = xor_seed(chunk[:DATA_LEN], next_key)
                
    FIR_KEY = '1'
    key_hash = hashlib.sha256(FIR_KEY.encode()).digest()
    FIR_KEY = int.from_bytes(key_hash, 'big')
    dec_file()




main_run()