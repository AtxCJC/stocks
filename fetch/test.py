score = -3.44
past = 1.7

if score > past:
    dif = score - past
    dif = abs((round(dif, 2)))
    print("UP", dif)
elif score < past:
    dif = past - score
    dif = abs((round(dif, 2)))
    print("DOWN", dif)