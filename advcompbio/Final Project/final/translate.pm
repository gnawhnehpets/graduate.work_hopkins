package translate;

use strict;
use warnings;

use Exporter 'import';
our @EXPORT_OK = ("translate_dna");
sub get_aa{
    my ($codon) = (@_);
    my (%aminoacids) = ('TCA'=>'S', 'TCC'=>'S', 'TCG'=>'S',
                        'TCT'=>'S', 'TTC'=>'F', 'TTT'=>'F',
                        'TTA'=>'L', 'TTG'=>'L', 'TAC'=>'Y',
                        'TAT'=>'Y', 'TAA'=>'_', 'TAG'=>'_',
                        'TGC'=>'C', 'TGT'=>'C', 'TGA'=>'_',
                        'TGG'=>'W', 'CTA'=>'L', 'CTC'=>'L',
                        'CTG'=>'L', 'CTT'=>'L', 'CCA'=>'P',
                        'CCC'=>'P', 'CCG'=>'P', 'CCT'=>'P',
                        'CAC'=>'H', 'CAT'=>'H', 'CAA'=>'Q',
                        'CAG'=>'Q', 'CGA'=>'R', 'CGC'=>'R',
                        'CGG'=>'R', 'CGT'=>'R', 'ATA'=>'I',
                        'ATC'=>'I', 'ATT'=>'I', 'ATG'=>'M',
                        'ACA'=>'T', 'ACC'=>'T', 'ACG'=>'T',
                        'ACT'=>'T', 'AAC'=>'N', 'AAT'=>'N',
                        'AAA'=>'K', 'AAG'=>'K', 'AGC'=>'S',
                        'AGT'=>'S', 'AGA'=>'R', 'AGG'=>'R',
                        'GTA'=>'V', 'GTC'=>'V', 'GTG'=>'V',
                        'GTT'=>'V', 'GCA'=>'A', 'GCC'=>'A',
                        'GCG'=>'A', 'GCT'=>'A', 'GAC'=>'D',
                        'GAT'=>'D', 'GAA'=>'E', 'GAG'=>'E',
                        'GGA'=>'G', 'GGC'=>'G', 'GGG'=>'G',
                        'GGT'=>'G');
 if($codon =~ /[ATGC]{3}/){
     return $aminoacids{$codon};
 }else{
     return "Sequence can only contain ATGC\n";
 }
}
sub translate_dna{
    my($sequence)=(@_);
    $sequence = uc($sequence);
    print "The sequence is: $sequence\n";
    my $length = length($sequence);
    #Is there a start codon?
    my $start_codon=0;
    my $position = 0;
    my $codon = '';
    my $aa = '';
    my $protein = '';
    #If sequence contains non-ATGC, return error
    if($sequence =~ /^[ATGC]+$/){
    }else{
        return "Sequence can only contain ATGC\n";
    }
    #For every ORF...
    for(my $i=0; $i<$length-2; $i++){
        $position=$i;
        $codon=substr($sequence,$position,3);
        #Get amino acid.
        $aa = get_aa($codon);
        #If codon is ATG (start codon)...
        if($codon =~ /ATG/){
            #Increase counter i.e. start codon exists...
            $start_codon++;
            #and add amino acid to protein sequence
            $protein .= $aa;
            #and advance to next codon (e.g. move forward three positions)
            $position += 3;
            last;
        }
    }
 #If no start codon present, then exit
    if($start_codon == 0){
        return "No start codon present. Will not translate sequence.\n";
    }
    #If start codon is present...
    else{
        #Start translating from codon right after start codon
        for($position; $position<$length-2; $position+=3){
            $codon=substr($sequence,$position,3);
            #Get amino acid.
            $aa = get_aa($codon);
            #If codon is not stop codon...
            if($aa !~ /\_/){
                #Add amino acid to protein sequence
                $protein .= $aa;
            }
            #If stop codon...
            else{
#               $protein .= '_';
                #Return protein sequence
                return $protein;
            }
        }
        return $protein;
    }
}

1;
