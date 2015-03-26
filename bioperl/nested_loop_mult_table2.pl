#!/usr/bin/env perl
use strict;
use warnings;

#Print out multiplication table based on user input

print "Please enter size of mult table:\n";
my $size = <STDIN>;
chomp($size);

my $x=1;
my $y;
for(my $i=0; $i<$size; $i++){
    $y=1;
    while($y!=$size+1){
	print $x*$y."\t";
	$y++;
    }
    print "\n";
    $x++;
}
