#!/usr/bin/env perl
use strict;
use warnings;

#Print out multiplication table 12x12 using nested loops
my $x=1;
my $y;
for(my $i=0; $i<13; $i++){
    $y=1;
    while($y!=13){
	print $x*$y."\t";
	$y++;
    }
    print "\n";
    $x++;
}
