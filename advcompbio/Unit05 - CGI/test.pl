#!usr/bin/perl
use strict;
use warnings;
=d
    print "Please enter in accession number: \n";
my $accession = <STDIN>;
chomp($accession);
if($accession !~ /.*.._/){
    print "Not an accession number!\n";
exit;
}
=cut
    my $file = "test.faa";
#my $file = "e_coli_k12_dh10b.faa";
if($file =~ m/.gz/){
    open(INPUT, "gunzip -c $file |") or die "Can't open pipe to file";
}else{
    open(INPUT, $file) or die "Can't open file.\n";
}
#lookup($accession);
lookup();

sub lookup {
    #    my ($x) = (@_);
    my $printable = 0;
    my $count = 0;
    my $seq_num=0;
    my @seq_id;
    my $sequence='';
    my $string_length=0;
    my @len;
    my $len_num=0;
    my $string_counter=0;
    #If $printable = 1, print line; otherwise, don't print
    while (<INPUT>) {
	#If line matches the sequence ID (aka if line is header)...
	if ($_ =~ /^>gi\|(\d+)\|ref/){
	    $count++;
	    #Place sequence ID into array...
	    $seq_id[$seq_num]=$1;
	    $seq_num++;
	    #Reset sequence length...
	    $string_length=0;
	    #Reset sequence counter (0 = new sequence; !0 = same sequence)
	    $string_counter=0;
	}else{
	    #Otherwise (aka sequence), store length of line/sequence...
	    $string_length+=length();
	    $len[$len_num]=$string_length;
	    #If same sequence (!0), then store updated string_length to prior array position
	    if($string_counter!=0){
		$len_num--;
		$len[$len_num]=$string_length;
	    }
	    #Progress along array position...
	    $len_num++;
	    #Add to sequence counter...
	    $string_counter++;
	}
    }

    #Display sequence ID; going to be put into hash
    foreach(@seq_id){
	print $_."\n";
    }

    #Display sequence length; going to be put into hash
    foreach(@len){
	print $_."\n";
    }

    if($count==0){
	#print "Sorry, no matches to that accession number!\n";
	print "Sorry, no sequences detected in file!\n";
    }
}
