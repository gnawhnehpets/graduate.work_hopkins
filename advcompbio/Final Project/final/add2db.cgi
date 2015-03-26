#!/usr/bin/env perl
use strict;
use warnings;
#use CGI(':standard');
#use HTML::Template;
use Bio::Perl;
use Bio::DB::GenBank;
use Bio::SeqIO;
use DBI;
use Config::IniFiles;

my @acc;
open (REFINED, "/var/www/shwang26/final/refine.txt") || die "Could not open: $!";

while(<REFINED>){
    if(/^(\D+)\|(.*?)\|/){
#       print $2."\n";
        push(@acc, $2);
    }
}
close REFINED;

my $db  = 'genbank';

foreach my $accession(@acc){
    my $seq = get_sequence( $db , $accession );    

    my $name      = $seq->display_id;
    my $accession = $seq->accession_number;
    my $sequence  = $seq->seq;
    my $first_ten = $seq->subseq( 1 , 10 );
    
    print "
NAME: $name
 ACC: $accession
 TEN: $first_ten

";
}
=d
#Import values from .ini file
my @accession;
open (REFINED, "/var/www/shwang26/final/refine.txt") || die "Could not open: $!";

while(<REFINED>){
    if(/^(\D+)\|(.*?)\|/){
#	print $2."\n";
	push(@accession, $2);
    }
}
close REFINED;


foreach my $number(@accession){
#    print $_."\n";
    
    my $seq = get_sequence($number);
}

my $cfg = Config::IniFiles->new(-file=> "./data.ini");
my $db = $cfg->val('Database','DB');
my $host = $cfg->val('Host','loc');
my $user = $cfg->val('User','name');
my $pass = $cfg->val('Password','pw');

