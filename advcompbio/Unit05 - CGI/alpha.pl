#!/usr/bin/perl
use strict;
use warnings;

my @num = qw(one two three);
my @alpha = qw(A B C);
my @place = qw(first second third);
my %hash;

while(@num and @alpha and @place){
    $hash{shift @num}=[shift @alpha, shift @place];
}
print \%hash;
