#!/usr/bin/env perl
use strict;
use warnings;

open (REFINED, ">>", "/var/www/shwang26/final/refine.txt") || die "Could not open: $!";
print REFINED "database.pl\n";
close REFINED;
