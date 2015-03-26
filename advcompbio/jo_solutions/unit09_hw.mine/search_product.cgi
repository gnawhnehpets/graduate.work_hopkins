#!/usr/bin/perl -w

use strict;
use CGI;
use Config::IniFiles;
use DBI;
use JSON;

## create our CGI and TMPL objects
my $cgi  = new CGI;

my $cfg = Config::IniFiles->new( -file => "settings.ini" ) || die "failed to read INI file: $!";

my $dsn = "DBI:mysql:database=" . $cfg->val('database', 'name') . 
                       ";host=" . $cfg->val('database', 'server') . ";";

my $dbh = DBI->connect($dsn, $cfg->val('database', 'user'), $cfg->val('database', 'pass'),
                       {RaiseError => 1, PrintError => 0});

my $json = JSON->new->allow_nonref;

my $term = $cgi->param('term');

## initialize an empty arrayref to store the search matches
my $matches = [];

my $qry = qq{
    SELECT f.uniquename AS locus, product.value AS product
    FROM feature f
    JOIN featureprop product ON f.feature_id=product.feature_id
    JOIN cvterm productprop ON product.type_id=productprop.cvterm_id
    WHERE productprop.name = ?
    AND product.value like ?
    LIMIT 5
};

my $dsh = $dbh->prepare($qry);

$dsh->execute('gene_product_name', "\%$term\%");

while (my $row = $dsh->fetchrow_hashref) {
    ## push the row to the match array
    push @$matches, { label => "$$row{locus} - $$row{product}", value => $$row{locus} };
}

$dsh->finish;
$dbh->disconnect;

## print the header and JSON data
print $cgi->header('application/json');

print $json->encode( $matches );
