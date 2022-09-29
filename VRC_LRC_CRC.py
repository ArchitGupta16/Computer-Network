cont = "y"

while cont == "y":
    choice = int(input("MENU\n1.VRC \n2.LRC \n3.CRC:"))

    if choice == 1:
        def VRC_sender(data, parity_type):
            parity = ""
            count = 0
            for i in range(len(data)):
                parity += data[i]
                if data[i] == "1":
                    count += 1

            if parity_type == "even":
                if count % 2 == 0:
                    parity += "0"
                else:
                    parity += "1"
            if parity_type == "odd":
                if count % 2 == 0:
                    parity += "1"
                else:
                    parity += "0"

            return parity


        def VRC_reciever(data, parity_type):
            checkbit = ""
            count = 0
            for i in range(len(data)):
                checkbit += data[i]
                if data[i] == "1":
                    count += 1

            if parity_type == "even":
                if count % 2 == 0:
                    checkbit += "0"
                    print("No error")
                else:
                    checkbit += "1"
                    print("Error")

            if parity_type == "odd":
                if count % 2 == 0:
                    checkbit += "1"
                    print("Error")
                else:
                    checkbit += "0"
                    print("No Error")

            return checkbit


        data = input("Enter the bits to be transmitted:")
        parity_type = input("Enter odd or even for parity type:")
        sender_vrc = VRC_sender(data, parity_type)
        print("Transmitted data:", sender_vrc)
        receiver = input("Enter data to check on receiver side:")
        receiver_vrc = VRC_reciever(receiver, parity_type)
        final = ""
        for i in range(0, len(receiver_vrc) - 2):
            final += receiver_vrc[i]
        print("Extracted data:", final)

    if choice == 2:
        def LRC_sender(data, parity_type, length):
            count = 0
            split = []
            string = ""

            for i in range(len(data)):
                string += data[i]
                count += 1
                if count == length:
                    split.append(string)
                    string = ""
                    count = 0

            parity = ""
            count = 0
            final = []
            for i in range(len(split)):
                for j in range(len(split[i])):
                    parity += split[i][j]
                    if split[i][j] == "1":
                        count += 1

                if parity_type == "even":
                    if count % 2 == 0:
                        parity += "0"
                        final.append(parity)
                    else:
                        parity += "1"
                        final.append(parity)

                if parity_type == "odd":
                    if count % 2 == 0:
                        parity += "1"
                        final.append(parity)
                    else:
                        parity += "0"
                        final.append(parity)
                parity = ""
                count = 0

            count = 0
            st = ""
            parity = ""
            for i in range(0, length + 1):
                for j in range(len(final)):
                    st += final[j][i]
                for i in range(len(st)):
                    if st[i] == "1":
                        count += 1
                if count % 2 == 0:
                    st += "0"
                    parity += "0"
                    count = 0
                else:
                    st += "1"
                    parity += "1"
                    count = 0
                st = " "
            final.append(parity)

            return final


        def LRC_receiver(data, parity_type):
            checkbit = ""
            final = []
            count = 0
            for i in range(len(data)):
                for j in range(len(data[i])):
                    checkbit += data[i][j]
                    if data[i][j] == "1":
                        count += 1

                if parity_type == "even":
                    if count % 2 == 0:
                        checkbit += "0"
                        print("No Error!")
                    else:
                        checkbit += "1"
                        print("Error!")
                    final.append(checkbit)
                    checkbit = ""

                if parity_type == "odd":
                    if count % 2 == 0:
                        checkbit += "1"
                        print("Error!")
                    else:
                        checkbit += "0"
                        print("No Error!")
                    final.append(checkbit)
                    checkbit = ""
            return final


        data = input("Enter the bits to be transmitted:")
        parity_type = input("Enter odd or even for parity type:")
        length = int(input("Enter length to split data into:"))
        lrc_sender = LRC_sender(data, parity_type, length)
        print("Sender data:", lrc_sender)
        blocks = int(input(f"Enter how many blocks of {length+1} bit data you want to enter"))
        new_data = []
        for i in range(blocks):
            inp = input("Enter data bits:")
            new_data.append(inp)
        lrc_receiver = LRC_receiver(new_data, parity_type)
        print(lrc_receiver)

    if choice == 3:
        def XOR(b1, b2):
            if b1 == "0" and b2 == "0":
                return "0"
            elif b1 == "1" and b2 == "1":
                return "0"
            elif b1 == "0" and b2 == "1":
                return "1"
            else:
                return "1"


        def CRC_sender(message, divisor):
            rem = ""
            for i in range(len(divisor) - 1):
                message += "0"

            temp = ""

            for i in range(len(divisor)):
                temp += message[i]

            for i in range(len(divisor), len(message)):
                if temp[0] == "0":
                    temp = temp[1:]
                    temp += message[i]
                else:
                    for j in range(len(divisor)):
                        rem += XOR(divisor[j], temp[j])
                    rem = rem[1:]
                    rem += message[i]
                    temp = rem
                    rem = ""

            return temp[1:]


        data = input("Enter the data bits:")
        divisor = input("Enter the divisor:")
        rem = CRC_sender(data, divisor)
        print("Remainder:", rem)


        def CRC_receiver(message, remainder, divisor):
            rem = ""
            for i in range(len(remainder)):
                message += remainder[i]

            temp = ""

            for i in range(len(divisor)):
                temp += message[i]

            for i in range(len(divisor), len(message)):
                if temp[0] == "0":
                    temp = temp[1:]
                    temp += message[i]
                else:
                    for j in range(len(divisor)):
                        rem += XOR(divisor[j], temp[j])
                    rem = rem[1:]
                    rem += message[i]
                    temp = rem
                    rem = ""

            return temp[1:]


        receiver_data = input("Enter the data received:")
        rem = CRC_receiver(receiver_data, rem, divisor)
        if int(rem) /2 == 0:
            print("No Error! \nReceiver end:",rem )
        else:
            print("Error and remainder:",rem)

    cont = input("Do you want to continue(y/n)")
