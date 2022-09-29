set ns [new Simulator]

set f [open out.tr w]
$ns trace-all $f

set nf [open out.nam w]
$ns namtrace-all $nf

set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]

$ns duplex-link $n0 $n1 1Mb 10ms DropTail
$ns duplex-link $n1 $n2 1Mb 10ms DropTail
$ns duplex-link $n2 $n3 1Mb 10ms DropTail
$ns duplex-link $n3 $n0 1Mb 10ms DropTail

set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 500
$cbr0 set interval_ .005
$cbr0 attach-agent $udp0
set null0 [new Agent/Null]
$ns attach-agent $n2 $null0
$ns connect $udp0 $null0

set tcp0 [new Agent/TCP/Reno]
$tcp0 set class_ 0
$tcp0 set window_ 100
$tcp0 set packetSize_ 960
$ns attach-agent $n3 $tcp0
set end0 [new Agent/TCPSink]
$ns attach-agent $n1 $end0
$ns connect $tcp0 $end0

proc finish {} {
global ns nf f
$ns flush-trace
close $f
close $nf
exec nam out.nam &
exit 0
}

$ns at 0.0 "$cbr0 start"
$ns at 10.0 "$cbr0 stop"

set myftp [new Application/FTP]
$myftp attach-agent $tcp0
$ns at 0.0 "$myftp start"
$ns at 10.0 "$myftp stop"
$ns at 10.0 "finish"

$ns run