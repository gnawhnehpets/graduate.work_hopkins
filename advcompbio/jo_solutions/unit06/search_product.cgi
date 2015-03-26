#!/usr/bin/perl -w

use strict;
use CGI;
use HTML::Template;

## create our CGI and TMPL objects
my $cgi  = new CGI;
my $tmpl = HTML::Template->new(filename => 'tmpl/search_product.tmpl');

my $term = $cgi->param('search_term');

open(my $fh, 'e_coli_k12_dh10b.gbk') || die "failed to open GBK file: $!";

## initialize an empty arrayref to store the search matches
my $matches = [];

## this always stores the most recent locus line value found in the file
my $current_locus = '';
my $current_product = '';
my $in_cds = 0;  ## toggles on if we're within a CDS entry

while (my $line = <$fh>) {
    ## if we hit a CDS line, clear our values
    if ( $line =~ /     CDS/ ) {
        
        if ( $current_product =~ /$term/i ) {
            push @$matches, { locus => $current_locus, product => $current_product };
        }
        
        $current_locus = '';
        $current_product = '';
        $in_cds = 1;
    
    ## we want to skip doing anything if we're within entries other than a CDS
    } elsif ( $line =~/^     \S/ ) {
        $in_cds = 0;
    
    ## skip to the next line if we're not within a CDS
    } elsif ( $in_cds == 0 ) {
        next;
        
    ## else store a new locus tag if we found one
    } elsif ( $line =~ m|^\s+/locus_tag="(.+)"| ) {
        $current_locus = $1;
    
    ## match a product line where the entire description is on the single line
    } elsif ( $line =~ m|/product="(.+)"| ) {
        $current_product = $1;
            
    ## else match a discontinuous product line and advance forward until it finishes.
    } elsif ( $line =~ m|/product="(.+)| ) {
        $current_product = $1;
        
        while ( my $sub_line = <$fh> ) {
            ## quit if we match a new attribute
            if ( $sub_line =~ m|^\s+/| ) {
                ## trim off any trailing quote
                $current_product =~ s|(.+)\"$|$1|;
                last;
            
            } elsif ( $sub_line =~ m|^\s+(.+)| ) {
                $current_product .= " $1";
            }
        }
    }
}

## push data to the template
$tmpl->param( MATCHES => $matches );
$tmpl->param( MATCH_COUNT => scalar( @$matches ) );

## print the header and template
print $cgi->header('text/html');
print $tmpl->output;
