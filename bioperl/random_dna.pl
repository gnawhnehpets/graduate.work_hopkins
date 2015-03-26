#!/usr/bin/env perl
use strict;
use warnings;

#generate random DNA sequence
print "What is length of desired random DNA sequence?\n";
my $length = <STDIN>;
chomp($length);
if($length =~ /^\d+$/){
}else{
    die "Not a #\n";
}
random();

sub random{
    my @nuc = ('A', 'T', 'G', 'C');
    my $dna;
    $dna .= $nuc[rand @nuc] for 1..$length;
    print "Your random DNA sequence of length $length is:\t$dna\n";
}
