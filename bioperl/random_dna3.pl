#!/usr/bin/env perl
use strict;
use warnings;

#generate 10 random DNA sequences, print each sequence to a file, return files that contain sequences with at least one run of four identical bases in them.

my $length=100;
my $file = "dna3_";
for(my $i=1; $i<11; $i++){
    $length=int(rand($length))+50;
    $file = "dna3_";
    $file .= $i.".txt";
    random();
}
    
sub random{
    my @nuc = ('A', 'T', 'G', 'C');
    my $dna;
    $dna .= $nuc[rand @nuc] for 1..$length;
    open FILE, ">", $file or die "Unable to open $file.\n";
    print FILE "$dna\n";
    close FILE;
    if($dna =~ /A{4,}/){
	print "A run found in ./$file.\n";
    }elsif($dna =~ /T{4,}/){
	print "T run found in ./$file.\n";
    }elsif($dna =~ /G{4,}/){
	print "G run found in ./$file.\n";
    }elsif($dna =~ /C{4,}/){
	print "C run found in ./$file.\n";
    }
}

