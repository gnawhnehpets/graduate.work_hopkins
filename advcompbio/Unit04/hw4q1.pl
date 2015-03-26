#!usr/bin/perl
use strict;
use warnings;

my $file = "test.txt";

if($file =~ m/.gz/){
    open(INPUT, "gunzip -c $file |") or die "Can't open pipe to file";
}else{
    open(INPUT, $file) or die "Can't open file.\n";
}
capture_id();

sub capture_id{
#If regex match to gi accession number, print ID number.
    while (<INPUT>) {
	if(/>gi_(\w+)/){
	    print $1."\n";
	}else{
	    print "No ID captured.\n";
	}
    }
}
