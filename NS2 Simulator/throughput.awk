BEGIN {

   recvdSize = 0

   recvdSize2=0

   startTime = 1

   stopTime = 5

}

{

         event = $1

         time = $2

         to = $4

         pkt_size = $6

         pkt_type = $5
         


if (event == "r" && to == 6 && pkt_type=="tcp") {

   recvdSize += pkt_size

   }

if (event == "r" && to == 8 && pkt_type=="cbr") {

   recvdSize2 += pkt_size

   }
}

END { 

   printf("\t\tThroughput[kbps] TCP : %.2f\n",(recvdSize/(stopTime-startTime))*(8/1000))
   printf("\t\tThroughput[kbps] UDP : %.2f\n",(recvdSize2/(stopTime-startTime))*(8/1000))


}
