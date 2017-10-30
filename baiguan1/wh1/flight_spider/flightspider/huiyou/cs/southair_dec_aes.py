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


def de_data(p_data, iv=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
    block_size = len(p_data) / 16
    loop_i = block_size - 1
    result = []
    for i in range(len(p_data)):
        result.append(0)
    finalRoundTable_buffer = ((lambda f: (f.read(), f.close()))(
        open(os.path.join(settings.FINAL_TABLE_PATH, "cs/keytables1/finalRoundTable_auth1.txt"), "rb")))[0]
    finalRoundTable = []
    for tmp in finalRoundTable_buffer:
        finalRoundTable.append(ord(tmp))
    invXorTable_buffer = \
    ((lambda f: (f.read(), f.close()))(open(os.path.join(settings.FINAL_TABLE_PATH, "cs/keytables1/invXorTables_auth1.txt"), "rb")))[
        0]
    invXorTable = []
    for tmp in invXorTable_buffer:
        invXorTable.append(ord(tmp))
    invFirstRoundTable_buffer = ((lambda f: (f.read(), f.close()))(
        open(os.path.join(settings.FINAL_TABLE_PATH, "cs/keytables1/invFirstRoundTable_auth1.txt"), "rb")))[0]
    invFirstRoundTable = []
    for tmp in invFirstRoundTable_buffer:
        invFirstRoundTable.append(ord(tmp))
    while loop_i >= 0:
        current_de_block = p_data[loop_i * 16:loop_i * 16 + 16]
        if loop_i == 0:
            next_de_block = iv
        else:
            next_de_block = p_data[(loop_i - 1) * 16:(loop_i - 1) * 16 + 16]
        current_de_block_result = de_one_block(current_de_block, invFirstRoundTable, invXorTable, finalRoundTable)
        for i in range(0, 16):
            result[loop_i * 16 + i] = current_de_block_result[i] ^ next_de_block[i]
        loop_i -= 1
    result2 = []
    for i in range(0, len(result)):
        result2.append(chr(result[i]))

    return "".join(result2).strip()


def de_one_block(one_block_data, invFirstRoundTable, invXorTable, finalRoundTable):
    byte_7815B4AD = [
        0x00, 0x00, 0x01, 0x03, 0x02, 0x02, 0x03, 0x01,
        0x00, 0x00, 0x01, 0x05, 0x02, 0x04, 0x03, 0x03,
        0x00, 0x00, 0x01, 0x07, 0x03, 0x05, 0x04, 0x04
    ]

    input_data = [0] * 32
    tmp_values2 = [0] * 64
    for i in range(0, 4):
        for j in range(0, 4):
            input_data[j * 8 + i] = one_block_data[4 * i + j]
    loop_i = 10
    v50 = 1
    while True:
        v5 = loop_i
        if loop_i < v50:
            break
        loop_i -= 1
        if v5 == 1:
            if v50 == 1:
                tmp_input_data = []
                for t_input_data in input_data:
                    tmp_input_data.append(t_input_data)
                for loop_j in range(0, 4):
                    byte_7815B4AD_idx = 1
                    input_data_idx = loop_j
                    for loop_z in range(0, 4):
                        v33 = (loop_j + byte_7815B4AD[byte_7815B4AD_idx]) & 3
                        loop1_xa = (loop_j + byte_7815B4AD[byte_7815B4AD_idx]) & 3
                        byte_7815B4AD_idx += 2
                        v34 = tmp_input_data[(loop_z << 3) + v33]
                        v36 = (((loop1_xa << 2) + loop_z) << 8) + v34

                        input_data[input_data_idx] = invFirstRoundTable[v36]
                        input_data_idx += 8
            break
        tmp_values2_i = 0
        for loop_j in range(1, 5):
            for_array_index = loop_j - 1
            for loop_z in range(0, 4):
                v12 = (loop_z + byte_7815B4AD[(loop_j << 1) - 1]) & 3
                v13 = input_data[(for_array_index << 3) + v12]
                v14 = ((v12 + (loop_i << 2) << 2) + loop_j - 1) << 8
                v10 = (v13 + v14) << 2
                tmp_values2[tmp_values2_i] = finalRoundTable[v10]
                tmp_values2_i += 1
                tmp_values2[tmp_values2_i] = finalRoundTable[v10 + 1]
                tmp_values2_i += 1
                tmp_values2[tmp_values2_i] = finalRoundTable[v10 + 2]
                tmp_values2_i += 1
                tmp_values2[tmp_values2_i] = finalRoundTable[v10 + 3]
                tmp_values2_i += 1

        salt_val = 96 * loop_i
        for loop_j in range(0, 4):
            v17_start_idx = loop_j
            for loop_z in range(0, 4):
                v40 = tmp_values2[v17_start_idx] & 0xF
                v19 = 6 * loop_j
                v20 = (tmp_values2[v17_start_idx] >> 4) << 4
                for x in range(1, 4):
                    v21 = tmp_values2[v17_start_idx + (x << 4)]
                    v24 = v19 + 1
                    offset1 = (((24 * loop_z + salt_val + v19) << 8) + (v40 | (v21 << 4) & 0xFF))
                    v40 = (invXorTable[offset1] & 0xF) | (v40 & 0xFFFFFF00)
                    v25 = (v20 >> 4) | (v21 >> 4) << 4
                    v19 += 2
                    offset2 = ((v24 + 24 * loop_z + salt_val) << 8) + v25
                    v20 = (invXorTable[offset2] & 0xFF) << 4
                v17_start_idx += 4
                input_data[(loop_j << 3) + loop_z] = v20 | v40

    result = []
    for i in range(0, 4):
        for j in range(0, 4):
            result.append(input_data[(j << 3) + i])
    return result


if __name__ == "__main__":
    pass
