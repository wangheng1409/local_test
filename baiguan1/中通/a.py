def first_num():
    import random
    ran_list = [10, 193, 228, 2227, 5605, 1834]
    for i in range(len(ran_list), 1, -1):
        ran_list[i - 1] = sum(ran_list[:i])

    a = random.randrange(0, 10097)
    for i in range(len(ran_list)):
        if a < ran_list[i]:
            break

    return i+1

s=[first_num() for i in range(100000)]

print(len([ x for x in s if x ==5])/100000)