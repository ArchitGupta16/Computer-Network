def decimal_to_hex(n):
    return '{0:x}'.format(n)


def decimalToBinary(n):
    return bin(n).replace("0b", "")


def ascii(word):
    ascii_arr = []
    for i in range(len(word)):
        ascii_arr.append(ord(word[i]))
    return ascii_arr


def binary(word, ascii):
    binary = []
    for i in range(len(word)):
        binary.append(decimalToBinary(ascii[i]))
    return binary


def Ones_Complement(arr):
    com = []
    for i in range(len(arr)):
        if arr[i] == "0":
            com.append("1")
        if arr[i] == "1":
            com.append("0")
    return com


def hexadecimal(ascii):
    hexa = []
    for i in range(len(ascii)):
        hexa.append(hex(ascii[i]).replace("0x", ""))
    return hexa


def hex_sum(a, b):
    return hex(int(a, 16) + int(b, 16))


def hex_complement(val):
    comp = ""
    comple = []
    for i in range(len(val)):
        con = int(val[i], 16)
        comp = 15 - con
        comple.append(decimal_to_hex(comp))
        comp = ""
    return comple


def wrapsum(binary_num, bits):
    binary_split = []
    if len(binary_num) > bits:
        count = bits
        n = len(binary_num) - bits
        while count != len(binary_num):
            count += n
            binary_split.append(binary_num[:n])
            binary_split.append(binary_num[n:])
            n = len(binary_split[0])
    else:
        binary_split.append(binary_num)
    return binary_split


def sender_hex(word, group_size):
    ascii_nums = ascii(word)
    print("ASCII values:", ascii_nums)
    hexa_val = hexadecimal(ascii_nums)
    print("Hexadecimal Values:", hexa_val)

    sum_array = []
    st = ""

    for i in range(0, len(hexa_val), group_size):
        for j in range(i, i + group_size):
            st += hexa_val[j]
        sum_array.append(st)
        st = ""

    sum_hex = sum_array[0]
    for i in range(1, len(sum_array)):
        sum_hex = hex(int(sum_array[i], 16) + int(sum_hex, 16))
    print("Sum:", sum_hex.replace("0x", ""))

    # Wrap sum
    wp = []
    if len(sum_hex) > 4:
        wp = wrapsum(sum_hex.replace("0x", ""), 4)

    # final sum of wrap sum
    wrap_sum = wp[0]
    for i in range(1, len(wp)):
        wrap_sum = hex(int(wp[i], 16) + int(wrap_sum, 16))

    if len(wrap_sum.replace("0x", "")) != 4:
        new_wp = wrapsum(wrap_sum.replace("0x", ""), 4)
        new_wrap_sum = new_wp[0]
        for i in range(1, len(new_wp)):
            new_wrap_sum = hex(int(new_wp[i], 16) + int(new_wrap_sum, 16))
    else:
        new_wrap_sum = wrap_sum
    print("WrapSum:", new_wrap_sum.replace("0x", ""))

    # complement of the wrap sum
    complement = hex_complement(new_wrap_sum.replace("0x", ""))
    c = ""
    for i in range(len(complement)):
        c += complement[i]
    print("Checksum:", c)

    # addition of extra complemented characters to the original word
    st = ""
    for i in range(0, len(c)):
        st += c[i]
    z = bytearray.fromhex(st).decode()
    print("Added:", z)
    word += z

    print("Codeword:", word)

    return word


def receiver_hex(word, group_size):
    print("Received word:", word)
    ascii_nums = ascii(word)
    print("ASCII values:", ascii_nums)
    hexa_val = hexadecimal(ascii_nums)
    print("Hexadecimal Values:", hexa_val)

    while len(hexa_val) % group_size != 0:
        hexa_val.append('00')
    print(hexa_val)

    # break according to group size
    sum_array = []
    st = ""
    for i in range(0, len(hexa_val), group_size):
        for j in range(i, i + group_size):
            st += hexa_val[j]
        sum_array.append(st)
        st = ""

    sum_hex = sum_array[0]
    for i in range(1, len(sum_array)):
        sum_hex = hex(int(sum_array[i], 16) + int(sum_hex, 16))
    print("Sum:", sum_hex.replace("0x", ""))

    # Wrap sum
    wp = []
    if len(sum_hex) > 4:
        wp = wrapsum(sum_hex.replace("0x", ""), 4)

    # final sum of wrap sum
    wrap_sum = wp[0]
    for i in range(1, len(wp)):
        wrap_sum = hex(int(wp[i], 16) + int(wrap_sum, 16))
    print("WrapSum:", wrap_sum.replace("0x", ""))

    if len(wrap_sum.replace("0x", "")) != 4:
        new_wp = wrapsum(wrap_sum.replace("0x", ""), 4)
        new_wrap_sum = new_wp[0]
        for i in range(1, len(new_wp)):
            new_wrap_sum = hex(int(new_wp[i], 16) + int(new_wrap_sum, 16))
    else:
        new_wrap_sum = wrap_sum
    print("WrapSum:", new_wrap_sum.replace("0x", ""))

    # complement of the wrap sum
    complement = hex_complement(new_wrap_sum.replace("0x", ""))
    c = ""
    for i in range(len(complement)):
        c += complement[i]
    print("Checksum:", c)
    if int(c) == 0:
        print("No error")
    else:
        print("Error!")


def binary_sender(word, group_size):
    ascii_nums = ascii(word)
    print("ASCII values:", ascii_nums)
    binary_nums = binary(word, ascii_nums)
    print("Binary values:", binary_nums)

    count = 0
    add_zeros = []
    for i in range(len(binary_nums)):
        for j in range(len(binary_nums[i])):
            count += 1
        add_zeros.append(count)
        count = 0

    # adding zero till length of string is 8
    for i in range(len(binary_nums)):
        binary_nums[i] = "0" * (8 - add_zeros[i]) + binary_nums[i]

    # adding zeros
    while len(binary_nums) % group_size != 0:
        binary_nums.append('00000000')
    print(binary_nums)

    # Merging numbers according to group size
    sum_array = []
    st = ""
    for i in range(0, len(binary_nums), group_size):
        for j in range(i, i + group_size):
            st += binary_nums[j]
        sum_array.append(st)
        st = ""

    # Binary addition of all numbers
    sum_bin = sum_array[0]
    for i in range(1, len(sum_array)):
        sum_bin = bin(int(sum_array[i], 2) + int(sum_bin, 2))
    print("Sum:", sum_bin.replace("0b", ""))

    # wrapping of sum
    wp = []
    if len(sum_bin) > 16:
        wp = wrapsum(sum_bin.replace("0b", ""), 16)

    # final sum of wrap sum
    wrap_sum = wp[0]
    for i in range(1, len(wp)):
        wrap_sum = bin(int(wp[i], 2) + int(wrap_sum, 2))

    if len(wrap_sum.replace("0b", "")) != 16:
        new_wp = wrapsum(wrap_sum.replace("0b", ""), 16)
        new_wrap_sum = new_wp[0]
        for i in range(1, len(new_wp)):
            new_wrap_sum = bin(int(new_wp[i], 2) + int(new_wrap_sum, 2))

    else:
        new_wrap_sum = wrap_sum
    print("WrapSum:", new_wrap_sum.replace("0b", ""))

    # complement of sum
    complement = Ones_Complement(new_wrap_sum.replace("0b", ""))
    c = ""
    for i in range(len(complement)):
        c += complement[i]
    print("Checksum:", c)

    # addition of checksum bits for codeword
    c = int(c, 2)
    c = c.to_bytes((c.bit_length() + 7) // 8, 'big').decode()
    print("Added:", c)
    for i in range(0, len(c), group_size):
        x = c[i] + c[i + 1]
        word += x
    print("Codeword:", word)


def binary_reciever(word, group_size):
    ascii_nums = ascii(word)
    print("ASCII values:", ascii_nums)
    binary_nums = binary(word, ascii_nums)
    print("Binary values:", binary_nums)

    count = 0
    add_zeros = []
    for i in range(len(binary_nums)):
        for j in range(len(binary_nums[i])):
            count += 1
        add_zeros.append(count)
        count = 0

    # adding zero till length of string is 8
    for i in range(len(binary_nums)):
        binary_nums[i] = "0" * (8 - add_zeros[i]) + binary_nums[i]
    print("After adding zeroes:", binary_nums)

    while len(binary_nums) % group_size != 0:
        binary_nums.append('00000000')
    print(binary_nums)

    # Merging numbers according to group size
    sum_array = []
    st = ""
    for i in range(0, len(binary_nums), group_size):
        for j in range(i, i + group_size):
            st += binary_nums[j]
        sum_array.append(st)
        st = ""

    sum_bin = sum_array[0]
    for i in range(1, len(sum_array)):
        sum_bin = bin(int(sum_array[i], 2) + int(sum_bin, 2))
    print("Sum:", sum_bin.replace("0b", ""))

    # wrapping of sum
    wp = []
    if len(sum_bin) > 16:
        wp = wrapsum(sum_bin.replace("0b", ""), 16)

    # final sum of wrap sum
    wrap_sum = wp[0]
    for i in range(1, len(wp)):
        wrap_sum = bin(int(wp[i], 2) + int(wrap_sum, 2))

    if len(wrap_sum.replace("0b", "")) != 16:
        new_wp = wrapsum(wrap_sum.replace("0b", ""), 16)
        new_wrap_sum = new_wp[0]
        for i in range(1, len(new_wp)):
            new_wrap_sum = bin(int(new_wp[i], 2) + int(new_wrap_sum, 2))
    else:
        new_wrap_sum = wrap_sum
    print("WrapSum:", new_wrap_sum.replace("0b", ""))

    # complement of sum
    complement = Ones_Complement(new_wrap_sum.replace("0b", ""))
    c = ""
    for i in range(len(complement)):
        c += complement[i]

    print("Checksum:", c)
    if int(c) == 0:
        print("No error")
    else:
        print("Error!")


cont = "y"
while cont.lower() == "y":
    choice = int(input("\n\t\tMENU\n1.Hex\n2.Binary:"))
    word = input("Enter word to transmit:")
    group_size = int(input("Enter group size:"))
    if choice == 1:
        sent_word = sender_hex(word, group_size)
        print("\n")
        received = input("Enter codeword to check:")
        receiver_hex(received, group_size)

    if choice == 2:
        binary_sender(word, group_size)
        print("\n")
        received = input("Enter codeword to check:")
        binary_reciever(received, group_size)
    cont = input("Do you want to continue?(y/n):")
