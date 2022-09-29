set ns [new Simulator]
$ns rtproto DV

set f [open out.tr w]
$ns trace-all $f

set nf [open out.nam w]
$ns namtrace-all $nf

# Color Setup
$ns color 1 Blue
$ns color 2 Red

# Node Creation
for {set i 0} {$i < 5} {incr i} {
set n($i) [$ns node]
}

# Node Connections
for {set i 0} {$i < 5} {incr i} {
	for {set j 0} {$j < 5} {incr j} {
		if {$i != $j && $j>$i} {
		$ns duplex-link $n($i) $n($j) 1Mb 10ms DropTail	
	}
}
}

# UDP Connection
set udp0 [new Agent/UDP]
$ns attach-agent $n(0) $udp0
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 500
$cbr0 set interval_ .005
$cbr0 attach-agent $udp0
set null0 [new Agent/Null]
$ns attach-agent $n(2) $null0
$ns connect $udp0 $null0

# TCP Connection
set tcp0 [new Agent/TCP/Reno]
$tcp0 set class_ 0
$tcp0 set window_ 100
$tcp0 set packetSize_ 500
$ns attach-agent $n(3) $tcp0
set end0 [new Agent/TCPSink]
$ns attach-agent $n(1) $end0
$ns connect $tcp0 $end0
set myftp [new Application/FTP]
$myftp attach-agent $tcp0

# Giving Colors
$udp0 set class_ 1
$tcp0 set class_ 2

proc finish {} {
global ns nf f
$ns flush-trace
close $f
close $nf
exec nam out.nam &
exit 0
}

# Start and stop
$ns at 0.0 "$cbr0 start"
$ns rtmodel-at 0.5 down $n(0) $n(2)
$ns rtmodel-at 3.0 up $n(0) $n(2)
$ns at 3.0 "$cbr0 stop"
$ns at 3.0 "$myftp start"
$ns rtmodel-at 3.5 down $n(1) $n(3)
$ns rtmodel-at 5.0 up $n(1) $n(3)
$ns at 5.0 "$myftp stop"
$ns at 6.0 "finish"

$ns run