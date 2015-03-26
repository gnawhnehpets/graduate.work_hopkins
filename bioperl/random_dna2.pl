#!/usr/bin/env perl
use strict;
use warnings;

#generate random DNA sequence
#ask user length of string
print "What is length of desired random DNA sequence?\n";
my $length = <STDIN>;
chomp($length);
if($length =~ /^\d+$/){
}else{
    die "Not a #\n";
}

print "Variable or fixed length? Enter in 'v' or 'f', default is fixed:\n";
my $string;
$string = <STDIN>;
chomp($string);

if($string eq 'v'){
    $length=int(rand($length))+1;
    random();
}elsif($string eq 'f'){
    random();
}elsif($string eq ''){
    random();
}else{
    die "Not a valid option\n";
}

sub random{
    my @nuc = ('A', 'T', 'G', 'C');
    my $dna;
    $dna .= $nuc[rand @nuc] for 1..$length;
    print "Your random DNA sequence of length $length is:\t$dna\n";
}
