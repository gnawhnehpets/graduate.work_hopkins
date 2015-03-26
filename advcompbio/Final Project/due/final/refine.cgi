#!/usr/bin/env perl
use strict;
use warnings;
use Bio::Root::Exception;
use Error qw(:try);
use CGI ':standard';
use JSON;
use IO::Handle;
STDOUT->autoflush(1);
STDERR->autoflush(1);

my $cgi = new CGI;
my $json = JSON->new->allow_nonref;

my $count = $_POST["items"];

open (FASTA, ">>", "/var/www/shwang26/final/refine.txt") || die "Could not open: $!";
print FASTA ">success:$count\n";
close FASTA;

=d
print $cgi->header('application/json');
print $json->encode(
    { saved_count => $count, saved_matches => $matches }
    );
