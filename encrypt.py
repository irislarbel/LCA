# -*- coding: utf-8 -*-
import os
import hashlib
import random


TARGET_FILE_NAME = r"YOUR LOCATE"
OUTPUT_FILE_NAME = r"YOUR LOCATE"
IV_LEN = 16

MAGIC_NUM = 0x45d9f3b
DATA_LEN = 10
BLOCK_SIZE = 512



TABLE = bytearray(16)

def main_run():
    
        
    def seedset(data, oldkey):
        oldkbyte = oldkey.to_bytes(32, 'big')
        hashdat = hashlib.sha256(oldkbyte + data).digest()
        seed = (int.from_bytes(hashdat, 'big') ^ MAGIC_NUM) & 0xFFFFFFFF
        return seed, (seed % 7) + 1
        
        
    
    def maindo(key, rotval, chunk, outfile):
        mapping_table = make_table(key, rotval)
        prevdata = convert(bytearray(chunk), mapping_table, outfile, rotval)
        return seedset(prevdata, key)
    


    def convert(isdatain, mapping_table, file, rot):

        prev = 0
        for i in range(len(isdatain)):
            rotate = ((prev << rot) | (prev >> (8 - rot))) & 0xFF
            prev = isdatain[i]
            isdatain[i] = (isdatain[i] + rotate) % 256
            
            isdatain[i] = (mapping_table[((isdatain[i] >> 4) & 0x0F)] << 4) | mapping_table[(isdatain[i] & 0x0F)]
        file.write(isdatain)
        
        return isdatain[:DATA_LEN]
            

    def enc_file():
        
        with open(TARGET_FILE_NAME, 'rb') as targetfile, open(OUTPUT_FILE_NAME, 'wb') as outfile:
            isfirst = True
            IV = os.urandom(IV_LEN)
            
            outfile.write(IV)
            next_rotval = 1
            while chunk := targetfile.read(BLOCK_SIZE):
                
                if chunk:
                    if isfirst:
                        
                        next_key = FIR_KEY ^ int.from_bytes(IV, 'big')
                        isfirst = False
                    next_key, next_rotval = maindo(next_key, next_rotval, chunk, outfile)
                
            
    def make_table(seed, rotval):
        random.seed(seed << rotval | rotval)
        pool = list(range(16))
        for i in range(16):
            j = random.getrandbits(4) % (16 - i)
            
            TABLE[i] = pool.pop(j)
        
        return TABLE
    

    
    
    FIR_KEY = '1'
    key_hash = hashlib.sha256(FIR_KEY.encode()).digest()
    FIR_KEY = int.from_bytes(key_hash, 'big')
    enc_file()





main_run()
