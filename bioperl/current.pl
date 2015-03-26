#!/usr/bin/perl
use strict;
use warnings;


#Write a script that generates an array of 10 random DNA 50mers and uses Storable to write them out to disk. Write a second script that uses Storable to read the stored sequences back into memory and then loops over them printing out details about which sequences contain 4mer runs of identical bases (i.e., 4 As, 4 Cs, etc.) (Yes, this is the same as the problem from week 3, only using Storable instead of files.)

my $length = 50;
my @array;
for(my $i=0; $i!=10; $i++){
    print $i."\n";
    random($i);
    
}

sub random{
    my $counter=$_;
    my @nuc = ('A', 'T', 'G', 'C');
    my $dna;
    $dna .= $nuc[rand @nuc] for 1..$length;
#    print "Your random DNA sequence of length $length is:\t$dna\n";
    print $dna."\n";
#    $array[$counter]=$dna;
    print $counter;
#    print $array[$counter]."\n";
}
=d
foreach my $x (@array){
    print $x."\n";
}
