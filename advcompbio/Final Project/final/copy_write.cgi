#!/usr/bin/env perl
use strict;
use warnings;
use CGI ':standard';

my $cgi = new CGI;
my $accession = $cgi->param('myAccession');
open (REFINED, ">>", "/var/www/shwang26/final/refine.txt") || die "Could not open: $!";
print REFINED $accession."\n";
close REFINED;

=d
#use CGI::Ajax;
#create our CGI and TMPL objects
#my $cgi = new CGI;
#my $ajax = new CGI::Ajax('exported_func'=>\&perl_func);

sub perl_func{
    my $input = shift;
    open (REFINED, ">", "/var/www/shwang26/final/refine.txt") || die "Could not open: $!";
    print REFINED $shift."\n";
    close REFINED;
}
