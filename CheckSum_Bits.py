def decimalToBinary(n):
    return bin(n).replace("0b", "")


def binaryToDecimal(n):
    return int(n, 2)


def Ones_Complement(n):
    if n == "0":
        return "1"
    if n == "1":
        return "0"


num = int(input("Enter the total numbers you want to enter: "))
bits = int(input("Enter bits to wrap to:"))
arr = []
for i in range(num):
    elements = int(input(f"Enter number {i + 1}:"))
    arr.append(elements)
print("\nThe numbers are:", arr)
sum_num = 0
for i in range(len(arr)):
    sum_num = sum_num + arr[i]
print("sum:", sum_num)


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


def Bit_sender(sum_num, bits, arr):
    binary_num = decimalToBinary(sum_num)
    print("Binary equivalent: ", binary_num)

    ws = wrapsum(binary_num, bits)
    print("Wrapped Numbers:", ws)

    sum_bin = ws[0]
    for i in range(1, len(ws)):
        sum_bin = bin(int(ws[i], 2) + int(sum_bin, 2)).replace("0b", "")
    print(len(ws[1]),"ypppppo")
    new_sum = ""
    # if sum_bin[0] == "1":
    #     new_sum = "0"
    #     for i in range(len(sum_bin)):
    #         new_sum += sum_bin[i]
    # else:
    #     new_sum = binary_num
    #
    print(sum_bin)

    complement = ""
    for i in range(len(sum_bin)):
        complement += Ones_Complement(sum_bin[i])
    print("Complement checksum:", complement)

    print("Complemented checksum (in decimal):", binaryToDecimal(complement))
    arr.append(binaryToDecimal(complement))
    print("Transmitted data: ", arr)


Bit_sender(sum_num, bits, arr)


def Bit_receiver(arr, bits):
    sum_num = 0
    for i in range(0, len(arr)):
        sum_num += arr[i]
    print("\nReceived numbers:",arr)
    print("Sum:", sum_num)
    binary_num = decimalToBinary(sum_num)
    print("Binary representation:", binary_num)
    wp = wrapsum(binary_num, bits)
    print("Wrapped Sum (receiver):", wp)

    temp = wp[0]
    for i in range(1, len(wp)):
        temp = bin(int(wp[i], 2) + int(temp, 2))
    print(temp)

    complement = ""
    for i in range(2, len(temp)):
        complement += Ones_Complement(temp[i])
    print("Complement:", complement)
    print("Decimal Number:", binaryToDecimal(complement))


Bit_receiver(arr, bits)
