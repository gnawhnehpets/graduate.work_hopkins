#!/usr/bin/perl

##################################
# Script for parsing a GenBank   #
# file containing sequences from #
# multiple genes.                #
# S. Hedtke Sept 2011            #
# v.1.1 26Feb2013 SMH			 #
##################################

# https://sites.google.com/site/shannonhedtke/Scripts
# This script was developed for Hedtke SM, Patiny S, Danforth BN. The Bee Tree of Life: a supermatrix approach to apoid phylogeny and biogeography.
#  Copyright (C) 2011  Shannon M Hedtke
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#   See <http://www.gnu.org/licenses/>.

## To use this program, type: perl parseGB.pl filename [y/n]
## where filename is a GenBank file and y = include introns, n = remove introns from DNA sequence data.
## For example, if you go to the NCBI website <http://www.ncbi.nlm.nih.gov/> and search
##  the nucleotide database for Apidae[organism]; click "Send to:"; select "File"; 
##  Format "GenBank(Full)"; click "Create File"
## This script outputs :
#	a file with information on each accession number, including classification and publication reference
#	an error file detailing problems with particular accession numbers
#	separate fasta files for each gene, as that gene is annotated in the GenBank accession.
#		This means you may have separate files for the same gene. For example, two files could
#		be created for "cytochrome oxidase I" and "COI" if they differ in annotation.
#		The identifier for each sequence is in the format >Species name_accession#

my $stripintrons=$ARGV[1];
if ($stripintrons=~/y/i) {print "\nIntrons will be included in sequence output.";} elsif ($stripintrons=~/n/i) {print "\nAnnotated introns will not be included in sequences (note if record annotation is poor, introns may be present in the data).";} 
## If you want the files to go to a separate folder, create the folder and change this name. 
my $directory='';		# e.g., my $directory='Apidae_genes/';
my $infile=$ARGV[0];
## You can change the name of the information and error files here.
my $infofile=$directory.$infile.'.AccessionInfo.xls';
my $errorfile=$directory.$infile.'.Errors.txt';

use Bio::SeqIO;
use Bio::DB::GenBank;
use Bio::AnnotationI;

open(ERROR,">>$errorfile");
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
$year += 1900;
$mon++;
print ERROR "\n$mon/$mday/$year $hour:$min\n";

my $inseq = Bio::SeqIO->new(-file=>$infile, -format => 'genbank',);

print "\nInformation loaded from $infile.\n";

### Retrieve each GenBank record (as objects) and parse them.

while (my $seq=$inseq->next_seq) { 
    my $accession='';
    my $dna='';
    my $yes=0;
    my $species='';
    $accession = $seq->accession;
print "\nParsing info from $infile, accession $accession...";

### Get information from Features : gene, CDS, and species
    for my $features ($seq->get_SeqFeatures) {
      if ($features->has_tag('gene')) {
	for my $val ($features->get_tag_values('gene')) {$gene=$val;}
      } elsif ($features->has_tag('product')) {
	for my $val ($features->get_tag_values('product')) {$gene=$val;}
      } else {$gene='Unknown';}
print "  gene $gene";
      if ($features->primary_tag eq 'CDS' && $stripintrons eq 'Y') { $dna=$features->spliced_seq->seq; $yes++; }
      if ($features->has_tag('organism')) {
	for my $val ($features->get_tag_values('organism')) { $species = $val; }
    } elsif ($species eq '') { $species='Unknown'; }}

if ($yes==0) { $dna=$seq->seq(); if ($stripintrons=~/n/i) {print ERROR "\n Accession no. $accession, gene $gene, was not stripped of introns.";} }
if ($dna eq '') { print ERROR "\n Accession no. $accession didn't seem to have a sequence."; next; } 

### Get information from Annotation : authors and reference citation

    my $anno_collection = $seq->annotation;
    my @reference=$anno_collection->get_Annotations('reference');
    my $ref=$reference[0];
	my $authors='';
	my $journalref='';
	my $hash_ref='';
    unless ($ref eq undef) {
    $hash_ref=$ref->hash_tree;
    $authors=$hash_ref->{'authors'};
    $journalref=$hash_ref->{'location'};
}

### Get information about classification of the organism.
    my @classification = $seq->species->classification;

### Print the information to file.
my $genefilename=$directory.$gene.".txt";
    unless (-e $genefilename) { open (GENE,">$genefilename"); } else { open (GENE,">>$genefilename");}   # If the file exists, then append the info, otherwise create a new file.
my $id=$species."_".$accession;
print GENE ">$id\n$dna\n";
close GENE;

# To the .info file:
    if (-e $infofile) { open (INFO,">>$infofile"); } else { open (INFO,">$infofile"); }
print INFO "$species\t$gene\t$accession\t$classification[5] / $classification[4] / $classification[3] / $classification[2]\t$authors\t$journalref\n";
close INFO;
  }
close ERROR;

print "\nCOMPLETED!!\n";

exit;
