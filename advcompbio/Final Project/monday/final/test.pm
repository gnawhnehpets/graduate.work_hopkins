#!usr/bin/perl
package test;
use Exporter 'import';
our @EXPORT_OK = ("parse");

=d
BLASTP 2.2.28+
Reference: Stephen F. Altschul, Thomas L. Madden, Alejandro
A. Schaffer, Jinghui Zhang, Zheng Zhang, Webb Miller, and
David J. Lipman (1997), "Gapped BLAST and PSI-BLAST: a new
generation of protein database search programs", Nucleic
Acids Res. 25:3389-3402.


RID: SE9KDKC7014


Database: All non-redundant GenBank CDS
translations+PDB+SwissProt+PIR+PRF excluding environmental samples
from WGS projects
           25,455,905 sequences; 8,764,053,280 total letters
Query= input_fasta

Length=36


                                                                   Score     E
Sequences producing significant alignments:                       (Bits)  Value

ref|WP_001577367.1|  hypothetical protein [Escherichia coli] >...  75.9    4e-15
ref|WP_001533923.1|  cytotoxic necrotizing factor 1 [Escherich...  75.9    7e-15
ref|WP_001682680.1|  cytotoxic necrotizing factor 1 [Escherich...  75.9    7e-15
ref|WP_001566411.1|  cytotoxic necrotizing factor 1 [Escherich...  75.9    7e-15
ref|WP_001537377.1|  cytotoxic necrotizing factor 1 [Escherich...  75.9    7e-15
gb|AAA85196.1|  CNF1 [Escherichia coli]                            75.9    7e-15
ref|WP_000528124.1|  hypothetical protein [Escherichia coli] >...  75.9    7e-15
ref|WP_000528125.1|  hypothetical protein [Escherichia coli] >...  75.9    7e-15
ref|YP_006108791.1|  cytotoxic necrotizing factor 1 [Escherich...  75.9    7e-15
ref|YP_543855.1|  cytotoxic necrotizing factor 1 [Escherichia ...  75.9    7e-15
gb|AAN03785.1|AF483828_1  cytotoxic necrotizing factor 1 [Esch...  75.9    7e-15
gb|AAN03786.1|AF483829_1  cytotoxic necrotizing factor 1 [Esch...  75.9    7e-15
emb|CAA50007.1|  cytotoxic necrotizing factor 1 [Escherichia c...  75.9    7e-15
gb|AAA18229.1|  cytotoxic necrotizing factor type 2 [Escherich...  67.0    9e-12
ref|WP_001102791.1|  hypothetical protein [Escherichia coli] >...  67.0    9e-12
ref|WP_001102790.1|  hypothetical protein [Escherichia coli] >...  67.0    9e-12
ref|YP_003034083.1|  cytotoxic necrotizing factor 2 protein Cn...  67.0    9e-12
emb|CAK19001.1|  cytotoxic necrotizing factor 3 [Escherichia c...  53.1    5e-07
ref|ZP_06157796.1|  cytotoxic necrotizing factor 1 [Photobacte...  48.9    2e-05
ref|ZP_15255136.1|  cytotoxic necrotizing factor 1, partial [Y...  40.0    0.002
ref|ZP_15193172.1|  cytotoxic necrotizing factor 1 domain prot...  40.0    0.002
ref|ZP_15044188.1|  cytotoxic necrotizing factor 1 domain prot...  40.0    0.002
ref|YP_650655.1|  hypothetical protein YPA_0742 [Yersinia pest...  40.0    0.002
ref|YP_001721345.1|  cytotoxic necrotizing factor [Yersinia ps...  42.4    0.003

=cut
sub parse{
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
	    if(/^(\D+)\|(.+?)\|\s(.*?)\s(\d+)(\.\d+)? +(\d+)(\.\d+)? *$/){
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
	    return (\@one, \@acc, \@desc, \@score, \@evalue) ;
	}
    }
    for(my $i=0; $i < scalar(@one); $i++){
#	print "$one[$i] | $acc[$i] | $desc[$i] | $score[$i] | $evalue[$i]\n";
    }
    close FILE;
    return (\@one, \@acc, \@desc, \@score, \@evalue);
}


1;
