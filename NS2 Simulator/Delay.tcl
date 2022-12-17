set ns [new Simulator]
$ns rtproto DV

set f [open Lab11.tr w]
$ns trace-all $f

set nf [open Lab11.nam w]
$ns namtrace-all $nf

# Color Setup
$ns color 1 Blue
$ns color 2 Red
$ns color 3 Yellow

# Node Creation
for {set i 0} {$i < 6} {incr i} {
set n($i) [$ns node]
}

# Node Connections
for {set i 0} {$i < 6} {incr i} {
$ns duplex-link $n($i) $n([expr ($i+1)%6]) 1Mb 10ms DropTail
}
$ns duplex-link $n(1) $n(3) 1Mb 10ms DropTail
$ns duplex-link $n(4) $n(0) 1Mb 10ms DropTail


# TCP Connection 1
set tcp0 [new Agent/TCP/Reno]
$tcp0 set class_ 2
$tcp0 set packetSize_ 500
$tcp0 set interval_ .005
$ns attach-agent $n(0) $tcp0
set end0 [new Agent/TCPSink]
$ns attach-agent $n(4) $end0
$ns connect $tcp0 $end0
set ftp0 [new Application/FTP]
$ftp0 attach-agent $tcp0

# TCP Connection 2
set tcp1 [new Agent/TCP/Reno]
$tcp1 set class_ 2
$tcp1 set packetSize_ 500
$tcp1 set interval_ .005
$ns attach-agent $n(1) $tcp1
set end1 [new Agent/TCPSink]
$ns attach-agent $n(5) $end1
$ns connect $tcp1 $end1
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1

# UDP Connection 1
set udp0 [new Agent/UDP]
$udp0 set class_ 1
$ns attach-agent $n(4) $udp0
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 500
$cbr0 set interval_ .005
$cbr0 attach-agent $udp0
set null0 [new Agent/Null]
$ns attach-agent $n(0) $null0
$ns connect $udp0 $null0

# UDP Connection 2
set udp1 [new Agent/UDP]
$udp1 set class_ 1
$ns attach-agent $n(5) $udp1
set cbr1 [new Application/Traffic/CBR]
$cbr1 set packetSize_ 500
$cbr1 set interval_ .005
$cbr1 attach-agent $udp1
set null1 [new Agent/Null]
$ns attach-agent $n(1) $null1
$ns connect $udp1 $null1


# TCP Connection 3
set tcp2 [new Agent/TCP/Reno]
$tcp2 set class_ 0
$tcp2 set packetSize_ 500
$tcp2 set interval_ .005
$ns attach-agent $n(2) $tcp2
set end2 [new Agent/TCPSink]
$ns attach-agent $n(5) $end2
$ns connect $tcp2 $end2
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2

# UDP Connection 3
set udp2 [new Agent/UDP]
$udp2 set class_ 1
$ns attach-agent $n(5) $udp2
set cbr2 [new Application/Traffic/CBR]
$cbr2 set packetSize_ 500
$cbr2 set interval_ .005
$cbr2 attach-agent $udp2
set null2 [new Agent/Null]
$ns attach-agent $n(2) $null2
$ns connect $udp2 $null2

# Execution
proc finish {} {
global ns nf f
$ns flush-trace
close $f
close $nf
exec nam Lab11.nam &
exit 0
}

# Start and stop
$ns at 1.0 "$cbr1 start"
$ns at 1.0 "$ftp0 start"
$ns at 1.0 "$ftp1 start"
$ns at 1.0 "$cbr0 start"
$ns at 1.0 "$ftp2 start"
$ns at 1.0 "$cbr2 start"

$ns at 5.0 "$cbr0 stop"
$ns at 5.0 "$cbr1 stop"
$ns at 5.0 "$ftp0 stop"
$ns at 5.0 "$ftp1 stop"
$ns at 5.0 "$cbr2 stop"
$ns at 5.0 "$ftp2 stop"



$ns at 6.0 "finish"

$ns run
