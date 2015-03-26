#!/usr/bin/perl
use strict;
use warnings;

my $string = "THISISASTRINGINUPPERCAPS";

my $start = 4;
my $end = 10;
my $length = $end-$start;
my $substring = substr($string, $start, $length);
my $lowercase = lc($substring);
$string =~ s/$substring/$lowercase/g;
print $string."\n";
