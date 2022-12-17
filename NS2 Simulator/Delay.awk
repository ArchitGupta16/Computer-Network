BEGIN {

   time1 = 0

   time2 = 0
   
   time3 = 0

   time4 = 0
   
   time5 = 0
    
   time6 = 0

   time7 = 0

   time8 = 0

   time9 = 0

   time10 = 0

   time11 = 0 

   time12 = 0

   max = 0
   
   max1 = 0
   max3 = 0
   max2 = 0
   max4 = 0
   max5 = 0
   max6 = 0
}

{

         action = $1

         time = $2

         from = $3

         to = $4

         pkt_size = $6

         pkt_type = $5
         
         seq = $11

# TCP connection 1--------------------------------------------

if (action == "+" && seq==0 && pkt_type=="tcp" && from==0 && to==4) {

   time1 = time

   }


if (action == "r" && seq>max && pkt_type=="tcp" && to==4) {

    max = seq
    time2 = time

   }
# UDP connection 1
if (action == "+" && seq==0 && pkt_type=="cbr" && from==4 && to==0) {

   time3 = time

   }


if (action == "r" && seq>max1 && pkt_type=="cbr" && to==0) {

    max1 = seq
    time4 = time

   }


# TCP connection 2------------------------------------------
if (action == "+" && seq==0 && pkt_type=="tcp" && from==1) {

  time5 = time

   }

if (action == "r"  && seq>max3 && pkt_type=="tcp" && to==5) {

   max3 = seq
   time6 = time

   }

# UDP connection 2
if (action == "+" && seq==0 && pkt_type=="cbr" && from==5) {

  time7 = time

   }

if (action == "r"  && seq>max4 && pkt_type=="cbr" && to==1) {

   max4 = seq
   time8 = time

   }

# TCP connection 3----------------------------------------
if (action == "+" && seq==0 && pkt_type=="tcp" && from==2) {

   time9 = time

   }

if (action == "r"  && seq>max5 && pkt_type=="tcp" && to==5) {

    max5 = seq
    time10 = time

   }

# # UDP connection 3
if (action == "+" && seq==0 && pkt_type=="cbr" && from==5) {

   time11 = time

   }

if (action == "r"  && seq>max6 && pkt_type=="cbr" && to==2) {

    max6= seq
    time12 = time

   }
}

END { 

   printf("\t\tDelay from 0 to 4 TCP : %.4f\n",time2-time1)
   printf("\t\tDelay from 4 to 0 UDP : %.4f\n",time4-time3)
   printf("\t\tDelay from 1 to 5 TCP : %.4f\n",time6-time5)
   printf("\t\tDelay from 5 to 1 UDP : %.4f\n",time8-time7)
   printf("\t\tDelay from 2 to 5 TCP : %.4f\n",time10-time9)
   printf("\t\tDelay from 5 to 2 UDP : %.4f\n",time12-time11)

#    printf("\t\tTotal Delay UDP %.4f \n",((time4-time1)+(time2-time1)+(time6-time5))/3)
   #printf("\t\tTotal Delay %.4f \n",((time4-time3)+(time2-time1))/2)
 
}
