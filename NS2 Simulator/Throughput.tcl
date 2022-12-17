set ns [new Simulator]
$ns rtproto DV

set f [open Lab12.tr w]
$ns trace-all $f

set nf [open Lab12.nam w]
$ns namtrace-all $nf

# Color Setup
$ns color 1 Blue
$ns color 2 Red

# Node Creation
for {set i 0} {$i < 10} {incr i} {
set n($i) [$ns node]
}

# Node Connections
for {set i 0} {$i < 10} {incr i} {
$ns duplex-link $n($i) $n([expr ($i+1)%10]) 1Mb 10ms DropTail
}
$ns duplex-link $n(1) $n(3) 1Mb 10ms DropTail
$ns duplex-link $n(4) $n(0) 1Mb 10ms DropTail
$ns duplex-link $n(5) $n(8) 1Mb 10ms DropTail
$ns duplex-link $n(6) $n(8) 1Mb 10ms DropTail


# TCP Connection 1
set tcp0 [new Agent/TCP/Reno]
$tcp0 set class_ 1
$tcp0 set packetSize_ 500
$tcp0 set interval_ .005
$ns attach-agent $n(2) $tcp0
set end0 [new Agent/TCPSink]
$ns attach-agent $n(6) $end0
$ns connect $tcp0 $end0
set ftp0 [new Application/FTP]
$ftp0 attach-agent $tcp0

# UDP Connection 1
set udp0 [new Agent/UDP]
$udp0 set class_ 2
$ns attach-agent $n(4) $udp0
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 500
$cbr0 set interval_ .005
$cbr0 attach-agent $udp0
set null0 [new Agent/Null]
$ns attach-agent $n(8) $null0
$ns connect $udp0 $null0

# Execution
proc finish {} {
global ns nf f
$ns flush-trace
close $f
close $nf
exec nam Lab12.nam &
exit 0
}

# Start and stop
$ns at 1.0 "$ftp0 start"
$ns at 1.0 "$cbr0 start"

# Link Breaks
$ns rtmodel-at 2.0 down $n(6) $n(5)
$ns rtmodel-at 2.0 down $n(8) $n(5)
$ns rtmodel-at 2.0 down $n(0) $n(4)
$ns rtmodel-at 4 up $n(0) $n(4)
$ns rtmodel-at 4 up $n(8) $n(5)
$ns rtmodel-at 4 up $n(6) $n(5)

$ns at 5.0 "$cbr0 stop"
$ns at 5.0 "$ftp0 stop"

$ns at 6.0 "finish"

$ns run