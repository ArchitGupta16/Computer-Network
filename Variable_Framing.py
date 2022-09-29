choice = "y"
while choice.lower() == "y":
    mode = int(input("\tMENU \n1.Bit Framing\n2.Byte Framing:"))
    if mode == 1:
        def bit_stuffing(input):
            flag = "01111110"
            count = 0
            destuff = ""
            for i in range(len(input)):
                if input[i] == "1":
                    count += 1
                else:
                    count = 0

                if count < 5:
                    destuff = destuff + input[i]

                if count == 5:
                    destuff = destuff + input[i] + "0"
                    count = 0
            destuff = flag + destuff
            destuff = destuff + flag

            return destuff


        string = input("\nEnter the string to transmit in binary:")
        stuffed_data = bit_stuffing(string)
        print("Transmitter Data:", stuffed_data)



        def destuffing(stuffed):
            count = 0
            unstuff = ""
            bool = False
            for i in range(8, len(stuffed) - 8):
                if stuffed[i] == "1":
                    count += 1
                else:
                    count = 0

                if count == 5:
                    bool = True
                    count = 0

                if bool == True and stuffed[i] == "0":
                    unstuff = unstuff + ""
                    bool = False

                else:
                    unstuff = unstuff + stuffed[i]

            return unstuff


        final_data = destuffing(stuffed_data)
        print("receiver data:", final_data)

    elif mode == 2:
        string = input("\nEnter the string to transmit:")
        flag = input("Enter the flag character:")
        escape = input("Enter the escape character:")


        def bytestuffing(string, escape, flag):
            stuff = ""
            for i in range(len(string)):
                if string[i] == flag:
                    stuff = stuff + escape + string[i]
                elif string[i] == escape:
                    stuff = stuff + escape + string[i]
                else:
                    stuff += string[i]

            stuff = flag + stuff + flag

            return stuff


        byte_stuff = bytestuffing(string, escape, flag)
        print("Transmitter data:", byte_stuff)


        def bytedestuffing(string, escape, flag):
            destuff = ""
            count = 0
            for i in range(1, len(string) - 1):
                # if i < len(string):
                #     break
                if string[i] == escape and string[i + 1] == flag:
                    destuff += ""
                elif string[i] == escape and string[i + 1] == escape:
                    count += 1
                    if count % 2 == 0:
                        destuff += string[i + 1]
                        count = 0
                else:
                    destuff += string[i]

            return destuff


        byte_destuff = bytedestuffing(byte_stuff, escape, flag)
        print("Receiver data:", byte_destuff)

    else:
        print("Wrong choice entered")

    choice = input("\nDo you want to continue (y/n):")
