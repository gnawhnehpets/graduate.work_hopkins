#!/usr/bin/env perl
use strict;
use warnings;
use CGI ':standard';

my $cgi = new CGI;
my $database = $cgi->param('myDatabase');
my $accession = $cgi->param('myAccession');
my $description = $cgi->param('myDescription');
my $score = $cgi->param('myScore');
my $evalue = $cgi->param('myEvalue');

open (REFINED, ">>", "/var/www/shwang26/final/refine.txt") || die "Could not open: $!";
print REFINED "$database|$accession|$description|$score|$evalue\n";
close REFINED;

