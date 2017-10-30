#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fly'

import os
from flightspider import settings

def print_data(input_data):
    print "\ndata:"
    for i in range(0, len(input_data)):
        if input_data[i] < 0x10:
            print "0x0" + hex(input_data[i])[2:].upper() + ",",
        else:
            print "0x" + hex(input_data[i])[2:].upper() + ",",
        if (i + 1) % 8 == 0:
            print " ",
        if (i + 1) % 16 == 0:
            print ""
    print ""

def en_data(p_data, iv=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]):
    if len(p_data) % 16 != 0:
        for i in range(16 - len(p_data) % 16):
            p_data += chr(0x3)

    tmp_p_data = []
    for i in p_data:
        tmp_p_data.append(ord(i))
    p_data = tmp_p_data
    block_size = len(p_data) / 16
    finalRoundTable_buffer = ((lambda f: (f.read(), f.close()))(open(os.path.join(settings.FINAL_TABLE_PATH, "cs/keytables1/finalRoundTable_auth2.txt"), "rb")))[0]
    finalRoundTable = []
    for tmp in finalRoundTable_buffer:
        finalRoundTable.append(ord(tmp))
    invXorTable_buffer = ((lambda f: (f.read(), f.close()))(open(os.path.join(settings.FINAL_TABLE_PATH, "cs/keytables1/invXorTables_auth2.txt"), "rb")))[0]
    invXorTable = []
    for tmp in invXorTable_buffer:
        invXorTable.append(ord(tmp))
    invFirstRoundTable_buffer = \
    ((lambda f: (f.read(), f.close()))(open(os.path.join(settings.FINAL_TABLE_PATH, "cs/keytables1/invFirstRoundTable_auth2.txt"), "rb")))[0]
    invFirstRoundTable = []
    for tmp in invFirstRoundTable_buffer:
        invFirstRoundTable.append(ord(tmp))

    result = []
    for loop_i in range(0, block_size):
        current_de_block = p_data[loop_i * 16:loop_i * 16 + 16]
        if loop_i == 0:
            prev_de_block = iv
        else:
            prev_de_block = result[(loop_i - 1) * 16:(loop_i - 1) * 16 + 16]

        for i in range(0, 16):
            current_de_block[i] = current_de_block[i] ^ prev_de_block[i]

        current_de_block_result = en_one_block(current_de_block, invFirstRoundTable, invXorTable, finalRoundTable)
        for i in range(0, 16):
            result.append(current_de_block_result[i])
        loop_i -= 1

    return result


def en_one_block(one_block_data, invFirstRoundTable, invXorTable, finalRoundTable):
    byte_782604AD = [
        0x00, 0x00, 0x01, 0x03, 0x02, 0x02, 0x03, 0x01,
        0x00, 0x00, 0x01, 0x03, 0x02, 0x02, 0x03, 0x01,
        0x00, 0x00, 0x01, 0x03, 0x02, 0x02, 0x03, 0x01,
        0x00, 0x00, 0x01, 0x05, 0x02, 0x04, 0x03, 0x03,
        0x00, 0x00, 0x01, 0x07, 0x03, 0x05, 0x04, 0x04
    ]
    input_data = [0]*32
    for i in range(0, 4):
        for j in range(0, 4):
            input_data[j * 8 + i] = one_block_data[4 * i + j]

    for loop_i in range(0, 9):

        #loop 1
        tmp_values2 = []
        for loop_j in range(0, 4):
            v6 = 2 * loop_j
            for loop_z in range(0, 4):
                v12 = loop_z + byte_782604AD[v6]
                v13 = v12 & 3;
                v14 = input_data[8 * loop_j + v13]
                v15 = (4 * (v13 + 4 * loop_i) + loop_j) << 8
                v10 = 4 * (v14 + v15)
                tmp_values2.append(invFirstRoundTable[v10])
                tmp_values2.append(invFirstRoundTable[v10 + 1])
                tmp_values2.append(invFirstRoundTable[v10 + 2])
                tmp_values2.append(invFirstRoundTable[v10 + 3])

        # loop 2
        salt_val = 96 * loop_i
        for loop_j in range(0, 4):
            v17_start_idx = loop_j
            v47 = 0
            for z in range(0, 4):
                tmp_bytes = []
                tmp_bytes.append(tmp_values2[v17_start_idx])
                tmp_bytes.append(tmp_values2[v17_start_idx + 16])
                tmp_bytes.append(tmp_values2[v17_start_idx + 32])
                tmp_bytes.append(tmp_values2[v17_start_idx + 48])
                v18 = tmp_values2[v17_start_idx]
                v40 = v18 & 0xF
                v19 = 6 * loop_j
                v20 = 16 * (v18 >> 4)
                for x in range(1, 4):
                    v21 = tmp_bytes[x]
                    v24 = v19 + 1
                    offset1 = (((24 * v47 + salt_val + v19) << 8) + (v40 | 16 * v21 & 0xFF))
                    v40 = int((invXorTable[offset1] & 0xF))
                    v25 = (v20 >> 4) | 16 * (v21 >> 4)
                    v19 += 2
                    offset2 = ((v24 + 24 * v47 + salt_val) << 8) + v25
                    v20 = 16 * (invXorTable[offset2] & 0xFF)

                v17_start_idx += 4
                input_data[8 * loop_j + v47] = v20 | v40
                v47 += 1
    tmp_input_data = []
    for t_input_data in input_data:
        tmp_input_data.append(t_input_data)
    for loop_j in range(0, 4):
        input_data_idx = loop_j
        for loop_z in range(0, 4):
            byte_7815B4AD_idx = 2 * loop_z
            loop1_xa = (loop_j + byte_782604AD[byte_7815B4AD_idx]) & 3
            v34 = tmp_input_data[8 * loop_z + loop1_xa]
            v36 = ((4 * loop1_xa + loop_z) << 8) + v34
            input_data[input_data_idx] = finalRoundTable[v36]
            input_data_idx += 8
    result = []
    for i in range(0, 4):
        for j in range(0, 4):
            result.append(input_data[8 * j + i])
    return result


if __name__ == "__main__":
    pass