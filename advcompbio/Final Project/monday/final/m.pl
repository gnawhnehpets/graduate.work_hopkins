#!usr/bin/perl
use strict;
use warnings;
=d
                                                                   Score     E
Sequences producing significant alignments:                       (Bits)  Value

ref|WP_001577367.1|  hypothetical protein [Escherichia coli] >...  75.9    4e-15
ref|WP_001533923.1|  cytotoxic necrotizing factor 1 [Escherich...  75.9    7e-15
ref|WP_001682680.1|  cytotoxic necrotizing factor 1 [Escherich...  75.9    7e-15
ref|WP_001566411.1|  cytotoxic necrotizing factor 1 [Escherich...  75.9    7e-15
ref|WP_001537377.1|  cytotoxic necrotizing factor 1 [Escherich...  75.9    7e-15
gb|AAA85196.1|  CNF1 [Escherichia coli]                            75.9    7e-15
ref|WP_000528124.1|  hypothetical protein [Escherichia coli] >...  75.9    7e-15
ref|ZP_15193172.1|  cytotoxic necrotizing factor 1 domain prot...  40.0    0.002
ref|ZP_15044188.1|  cytotoxic necrotizing factor 1 domain prot...  40.0    0.002
ref|YP_650655.1|  hypothetical protein YPA_0742 [Yersinia pest...  40.0    0.002
ref|YP_001721345.1|  cytotoxic necrotizing factor [Yersinia ps...  42.4    0.003

=cut
    open (FILE, '/var/www/shwang26/final/input_fasta.blastoutput');
    my $marker = 0;
    my @one;
    my @acc;
    my @desc;
    my @score;
    my @evalue;
    my $counter = 0;
    while(<FILE>){
	chomp;
	if($marker == 1){
#	    if(/^(\D+)\|(.+?)\|\s(.*?)\s(\d+)(\.\d+)? +(\d+)(\.\d+)? *$/){
	    if(/^(\D+)\|(.+?)\|\s(.*?)\s(\d+)(\.\d+)? +((\d+)((\.\d+)?(e.*?)?)) *$/) {
		$one[$counter] = $1;
		$acc[$counter] = $2;
		$desc[$counter] = $3;
		$score[$counter] = $4+$5;
		if(! $7){
		    $evalue[$counter] = $6;
		}else{
		    $evalue[$counter] = $6+$7;
		}
		$counter++;
	    }
	}
	if(/Sequences producing significant alignments/){
	    $marker = 1;
	}elsif(/ALIGNMENTS/){
	    $marker = 0;
	}elsif(/No significant similarity found/){
	    last; 
	}
    }
    for(my $i=0; $i < scalar(@one); $i++){
	print "$one[$i] | $acc[$i] | $desc[$i] | $score[$i] | $evalue[$i]\n";
    }
    close FILE;
#    return (\@one, \@acc, \@desc, \@score, \@evalue);



