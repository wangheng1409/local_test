import os
from flightspider import settings

unk_3716 = [0, 0, 1, 3, 2, 2, 3, 1, 0, 0, 1, 3, 2, 2, 3, 1]


def en_data(p_data, iv=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
    if len(p_data) % 16 != 0:
        padding = 16 - len(p_data) % 16
    else:
        padding = 16
    for i in range(0, padding):
        p_data += chr(padding)

    tmp_p_data = []
    for i in p_data:
        tmp_p_data.append(ord(i))
    p_data = tmp_p_data
    block_size = len(p_data) / 16

    finalroundtable_buffer = ((lambda f: (f.read(), f.close()))(open(os.path.join(settings.FINAL_TABLE_PATH, "mu/keytables/finalRoundTable_auth2.txt"), "rb")))[0]
    finalroundtable_auth2 = []
    for tmp in finalroundtable_buffer:
        finalroundtable_auth2.append(ord(tmp))
    xortables_buffer = ((lambda f: (f.read(), f.close()))(open(os.path.join(settings.FINAL_TABLE_PATH, "mu/keytables/xorTables_auth2.txt"), "rb")))[0]
    xortables_auth2 = []
    for tmp in xortables_buffer:
        xortables_auth2.append(ord(tmp))
    roundtables_buffer = ((lambda f: (f.read(), f.close()))(open(os.path.join(settings.FINAL_TABLE_PATH, "mu/keytables/roundTables_auth2.txt"), "rb")))[0]
    roundtables_auth2 = []
    for tmp in roundtables_buffer:
        roundtables_auth2.append(ord(tmp))

    result = []
    for i in range(0, block_size):
        current_block = p_data[i * 16:i * 16 + 16]
        if i == 0:
            prev_block = iv
        else:
            prev_block = result[(i - 1) * 16:(i - 1) * 16 + 16]
        for j in range(0, 16):
            current_block[j] = current_block[j] ^ prev_block[j]

        current_block_result = en_one_block(current_block, finalroundtable_auth2, xortables_auth2, roundtables_auth2)
        for j in range(0, 16):
            result.append(current_block_result[j])
    return result


def en_one_block(one_block_data, finalroundtable_auth2, xortables_auth2, roundtables_auth2):
    matrix_data = prepare_aes_matrix(one_block_data)
    temp_values1 = [0]*64
    m = 0
    while m <= 8:
        for i in range(0, 4):
            for j in range(0, 4):
                r3 = (unk_3716[i << 1] + j) & 0x80000003
                if r3 < 0:
                    r3 -= 1
                    r3 |= (-4)
                    r3 += 1
                r2 = matrix_data[(i << 3) + r3]
                r1 = ((((m << 2) + r3) << 2) + i) << 8
                r1 = (r2 + r1) << 2
                r2 = ((i << 2) + j) << 2
                for k in range(0, 4):
                    temp_values1[r2+k] = roundtables_auth2[r1 + k]
        for i in range(0, 4):
            for j in range(0, 4):
                r3 = (j << 2) + i
                r2 = temp_values1[r3]
                temp_values2 = [0]*4
                temp_values2[0] = r2
                temp_values2[1] = temp_values1[r3+0x10]
                temp_values2[2] = temp_values1[r3+0x20]
                temp_values2[3] = temp_values1[r3+0x30]
                sp_0x20 = r2 & 0xf
                sp_0x24 = (r2 >> 4) << 4
                for k in range(0, 3):
                    r2 = (3 * i + k) << 1
                    sp_0x34 = r2
                    r1 = sp_0x20 & 0xf
                    r2 = (temp_values2[k + 1] << 4) & 0xff
                    sp_0x2c = r1 | r2
                    r3 = ((0x18 * j + 0x60 * m + sp_0x34) << 8) + sp_0x2c
                    sp_0x20 = (xortables_auth2[r3]) & 0xf
                    sp_0x34 = ((3 * i + k) << 1) + 1
                    r1 = (sp_0x24 >> 4) & 0xf
                    r2 = (temp_values2[k + 1] >> 4) << 4
                    sp_0x2c = r1 | r2
                    r2 = (((0x18 * j + 0x60 * m) + sp_0x34) << 8) + sp_0x2c
                    sp_0x24 = (xortables_auth2[r2] << 4) & 0xff
                r2 = sp_0x20 & 0xf
                r3 = (sp_0x24 >> 4) << 4
                matrix_data[(i << 3) + j] = r2 | r3
        m += 1
    temp_values2 = [0]*32
    for i in range(0, 32):
        temp_values2[i] = matrix_data[i]
    for i in range(0, 4):
        for j in range(0, 4):
            r3 = unk_3716[j << 1]
            r3 = (i+r3) & 0x80000003
            if r3 < 0:
                r3 -= 1
                r3 |= -4
                r3 += 1
            r2 = temp_values2[(j << 3) + r3]
            r3 = ((r3 << 2) + j) << 8
            r3 += r2
            matrix_data[(j << 3) + i] = finalroundtable_auth2[r3]
    result = [0]*16
    for i in range(0, 4):
        for j in range(0, 4):
            result[4 * i + j] = matrix_data[(j << 3) + i]
    return result


def prepare_aes_matrix(data):
    result = [0] * 32
    for i in range(0, 4):
        for j in range(0, 4):
            result[j * 8 + i] = data[i * 4 + j]
    return result


def de_data(p_data, iv=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0]):
    block_size = len(p_data) / 16
    result = []
    for i in range(len(p_data)):
        result.append(0)
    invroundtable_buffer = ((lambda f: (f.read(), f.close()))(open(os.path.join(settings.FINAL_TABLE_PATH, "mu/keytables/invRoundTables_auth2.txt"), "rb")))[0]
    invroundtables_auth2 = []
    for tmp in invroundtable_buffer:
        invroundtables_auth2.append(ord(tmp))
    invxortable_buffer = ((lambda f: (f.read(), f.close()))(open(os.path.join(settings.FINAL_TABLE_PATH, "mu/keytables/invXorTables_auth2.txt"), "rb")))[0]
    invxortables_auth2 = []
    for tmp in invxortable_buffer:
        invxortables_auth2.append(ord(tmp))
    invfirstroundtable_buffer = ((lambda f: (f.read(), f.close()))(open(os.path.join(settings.FINAL_TABLE_PATH, "mu/keytables/invFirstRoundTable_auth2.txt"), "rb")))[0]
    invfirstroundtable_auth2 = []
    for tmp in invfirstroundtable_buffer:
        invfirstroundtable_auth2.append(ord(tmp))
    block_size -= 1
    while block_size >= 0:
        current_block = p_data[block_size * 16:block_size * 16 + 16]
        current_block_result = de_one_block(current_block, invroundtables_auth2,
                                            invxortables_auth2, invfirstroundtable_auth2)
        if block_size == 0:
            prev_block = iv
        else:
            prev_block = p_data[(block_size - 1) * 16:(block_size - 1) * 16 + 16]
        for i in range(0, 16):
            result[block_size*16+i] = current_block_result[i] ^ prev_block[i]
        block_size -= 1
    padding = len(result) - result[len(result) - 1]
    result2 = []
    for i in range(0, padding):
        result2.append(chr(result[i]))
    return "".join(result2).strip()


def de_one_block(one_block, invroundtables_auth2, invxortables_auth2, invfirstroundtable_auth2):
    matrix_data = prepare_aes_matrix(one_block)
    temp_values1 = [0]*64
    count = 10
    while count > 1:
        for i in range(0, 4):
            for j in range(0, 4):
                r3 = (unk_3716[i*2+1]+j) & 0x80000003
                if r3 < 0:
                    r3 -= 1
                    r3 |= -4
                    r3 += 1
                r1 = (i << 3) + r3
                r2 = matrix_data[r1]
                r1 = (((((count - 1) << 2) + r3) << 2) + i) << 8
                r1 = (r1 + r2) << 2
                r2 = ((i << 2) + j) << 2
                for k in range(0, 4):
                    temp_values1[r2+k] = invroundtables_auth2[r1+k]
        for i in range(0, 4):
            for j in range(0, 4):
                r3 = (j << 2) + i
                r2 = temp_values1[r3]
                temp_values2 = [0]*4
                temp_values2[0] = r2
                temp_values2[1] = temp_values1[r3+0x10]
                temp_values2[2] = temp_values1[r3+0x20]
                temp_values2[3] = temp_values1[r3+0x30]

                sp = r2 & 0xf
                sp_0xc = (r2 >> 4) << 4

                for k in range(0, 3):
                    sp_0x14 = (3 * i + k) << 1
                    r2 = sp & 0xf
                    r3 = (temp_values2[k + 1] << 4) & 0xff
                    sp_0x10 = r2 | r3
                    r3 = ((0x18 * j + 0x60 * (count - 1) + sp_0x14) << 8) + sp_0x10
                    sp = invxortables_auth2[r3] & 0xf
                    sp_0x14 = ((3 * i + k) << 1) + 1
                    r2 = (sp_0xc >> 4) & 0xf
                    r3 = ((temp_values2[k + 1] & 0xff) >> 4) << 4
                    sp_0x10 = r2 | r3
                    r3 = ((0x18 * j + 0x60 * (count - 1) + sp_0x14) << 8) + sp_0x10;
                    sp_0xc = (invxortables_auth2[r3] << 4) & 0xff

                r2 = sp & 0xf
                r3 = (sp_0xc >> 4) << 4
                matrix_data[(i << 3) + j] = r2 | r3
        count -= 1
    temp_values2 = [0]* 32
    for i in range(0, 32):
        temp_values2[i] = matrix_data[i]
    for i in range(0, 4):
        for j in range(0, 4):
            r3 = (unk_3716[(j << 1) + 1] + i) & 0x80000003
            if r3 < 0:
                r3 -= 1
                r3 |= -4
                r3 += 1
            r2 = temp_values2[(j << 3) + r3]
            r3 = ((r3 << 2) + j) << 8
            r3 += r2
            matrix_data[(j << 3) + i] = invfirstroundtable_auth2[r3]
    result = [0] * 16
    for i in range(0, 4):
        for j in range(0, 4):
            result[(i << 2)+j] = matrix_data[(j << 3)+i]
    return result



