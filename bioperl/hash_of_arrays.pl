#!/usr/bin/env perl
use strict;
use warnings;

#Hard-coded hash of arrays; prints out hash of arrays when run
my %hash = (
    alphabet => ["a", "b", "c", "d", "e"],
    numbers => [1, 2, 3, 4, 5],
    names => ["maddie", "amy", "sabrina"]
    );

foreach my $group (keys %hash){
    print "The members of group $group are:\n";
    foreach (@{$hash{$group}}){
	print "\t$_\n";
    }
}
