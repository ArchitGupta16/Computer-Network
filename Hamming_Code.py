print("\t\tSENDER SIDE")
data = input("Enter the binary string:")
m = len(data)


def find_r(m):
    r = 0
    while 2 ** r < (m + r):
        r += 1
    return r


r = find_r(m)


def represent(word, m, r):
    codeword = ""
    parity_count = 0
    word_count = 0
    for i in range(1, m + r + 1):
        if i == 2 ** parity_count:
            codeword += "P"
            parity_count += 1
        else:
            codeword += word[word_count]
            word_count += 1
    print("Codeword with parities:", codeword, "\nTotal parities to be added:", parity_count)


def code_word(word, m, r):
    codeword = ""
    parity_count = 0
    word_count = 0
    for i in range(1, m + r + 1):
        if i == 2 ** parity_count:
            codeword += "0"
            parity_count += 1
        else:
            codeword += word[word_count]
            word_count += 1
    return codeword


x = code_word(data, m, r)


def generate_binary(m, r):
    binary = []
    for i in range(1, m + r + 1):
        binary.append(bin(i).replace("0b", ""))
    count = 0
    add_zeros = []
    for i in range(len(binary)):
        for j in range(len(binary[i])):
            count += 1
        add_zeros.append(count)
        count = 0
    for i in range(len(binary)):
        binary[i] = "0" * (r - add_zeros[i]) + binary[i]
    return binary


generate_binary(m, r)


def parity(word, m, r):
    codeword = code_word(word, m, r)
    binary_num = generate_binary(m, r)
    parity = []
    temp = []
    for i in range(r):
        temp.append(f"P{2 ** (r - i - 1)}")
        for j in range(len(binary_num)):
            if binary_num[j][i] == '1':
                temp.append(j + 1)
        parity.append(temp)
        temp = []

    res = []
    for i in range(len(parity)):
        xor = 0
        for j in range(2, len(parity[i])):
            xor = xor ^ int(codeword[parity[i][j] - 1])
        res.append(xor)
    return res


parity(data, m, r)


def final_code_word(word, m, r, res):
    codeword = ""
    res = res[::-1]
    parity_count = 0
    word_count = 0
    for i in range(1, m + r + 1):
        if i == 2 ** parity_count:
            codeword += str(res[parity_count])
            parity_count += 1
        else:
            codeword += word[word_count]
            word_count += 1
    return codeword


def receiver(word, m, r):
    codeword = word
    binary_num = generate_binary(m, r)
    parity = []
    temp = []
    for i in range(r):
        temp.append(f"P{2 ** (r - i - 1)}")
        for j in range(len(binary_num)):
            if binary_num[j][i] == '1':
                temp.append(j + 1)
        parity.append(temp)
        temp = []
    res = []
    for i in range(len(parity)):
        xor = 0
        for j in range(1, len(parity[i])):
            xor = xor ^ int(codeword[parity[i][j] - 1])
        res.append(xor)
    return res


def extract_data(word, m, r):
    extracted = ""
    parity_count = 0
    for i in range(1, m + r + 1):
        if i == 2 ** parity_count:
            extracted += ""
            parity_count += 1
        else:
            extracted += word[i - 1]
    return extracted

represent(data, m, r)
sent_data = final_code_word(data, m, r, parity(data, m, r))
print("Sender side data:", sent_data)

print("\n\t\tRECEIVER SIDE")
receive = input("Enter the data to check:")
final_x = receiver(receive, m, r)
s = ""
for i in final_x:
    s += str(i)
dec = int(s, 2)

extracted_data = extract_data(receive, m, r)
error_count = 0
for i in range(m+r):
    if sent_data[i] != receive[i]:
        error_count += 1

if error_count == 0:
    print("No error!")
    print("Extracted data:", extracted_data)
elif error_count == 1:
    print(f"Single Bit Error at position {dec} of {receive}")
    corrected = ""
    for i in range(len(receive)):
        if i == dec-1:
            if receive[i] == "0":
                corrected += "1"
            else:
                corrected += "0"
        else:
            corrected += receive[i]
    print("Corrected data is:", corrected)
    print("Extracted data is:", extract_data(corrected, m, r))
else:
    print("Burst error has occurred!!")
