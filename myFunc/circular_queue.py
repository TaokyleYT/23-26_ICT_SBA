lst = [0 for _ in range(10)]
head = 0
tail = 0
layer = 0
length = 10

while True:
    temp = input()
    if temp == "d":
        lst[head] = 0
        head += 1
        if head >= 10:
            head = 0
            layer -= 1
    else:
        try:
            int_temp = int(temp)
        except ValueError:
            continue
        else:
            if int_temp == 0:
                continue
        lst[tail] = int_temp
        tail += 1
        if tail >= 10:
            if layer == 0:
                tail = 0
                layer += 1
            else:
                print("full")
                tail -= 1
                continue
        if tail == head and layer == 1:
            print("full")
            continue
    print(f"lst = {lst}", f"head = {head}", f"tail = {tail}", f"layer = {layer}")
        