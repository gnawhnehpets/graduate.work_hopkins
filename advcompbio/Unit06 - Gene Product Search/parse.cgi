#!/usr/bin/perl -w

=head1 DESCRIPTION

From Unit 06, homework question #5:

This is the entire annotated genome of E. coli K12. Create an page called 'search.html' in your
web area that contains a valid HTML5 page and a single search box, where users can enter a
gene product name they wish to search for. Make your form submit to a script you create called
'search_product.cgi'. This script should read through that gbk file looking for any ./product.
tags that contain the exact search string, and use a template you create called
'search_product.tmpl' to display the results. The results should show not only the matched
product names but their corresponding locus_tag entries as well. So if I searched for 'glutamate
synthase' I'd expect to get an HTML page that contains a data table that looks like this:
  
=cut

use strict;
use CGI;

my $fasta_file = 'e_coli_k12_dh10b.gbk';

open(INPUT, $fasta_file) || die "ERROR: can't read input FASTA file: $!";
my $counter=0;
my @locus;
my $locus_tag='';
my @product;
my $product_tag='';

print "Print the search\n";

my $search=<STDIN>;
chomp($search);
while ( <INPUT> ) {
    if(/locus_tag="(.+?)"/){
	$locus_tag=$1;
#	print $locus_tag."\n";
    }elsif(/product="(.+?)"/){
	$product_tag=$1;
	if(/($search)/){
	    $product[$counter] = $product_tag;
	    $locus[$counter]=$locus_tag;
	    $counter++;
	    $locus_tag='';
	}
    }
}
for(my $i=0; $i < scalar(@product); $i++){
    print $product[$i]."\t";
    print $locus[$i]."\n";
}
