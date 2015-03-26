#!usr/bin/perl
use strict;
use warnings;

#my $file = "test.faa";
my $file = "e_coli_k12_dh10b.faa";

if($file =~ m/.gz/){
    open(INPUT, "gunzip -c $file |") or die "Can't open pipe to file";
}else{
    open(INPUT, $file) or die "Can't open file.\n";
}
gene_count();

sub gene_count{
    my $num_sequences = 0;
    my $string_length;
    my $min_length = 10000000000000000000000000000000000000000000;
    my $max_length = 0;
    my $average_length;
    my $total_length;
    my $hypothetical =0;
    while(<INPUT>){
	if(/>*hypothetical/){
	    $hypothetical++;
	}
	if(/>/){
	    $num_sequences++;
	    $string_length = 0;
	}else{
	    $string_length+=length();

	    if($string_length > $max_length){
		$max_length = $string_length;
	    }elsif($string_length < $min_length){
		$min_length = $string_length;
	    }else{
		next;
	    }
	    #Add string(line) length to total
            $total_length += $string_length;
#	    print $string."\n";
#	    print $total_length."\n";
	}
#	print "max $max_length\n";
#	print "min $min_length\n";
    }

    $average_length = int($total_length/$num_sequences);
    print "Number of genes: $num_sequences\n";
    print "Minimum protein length: $min_length\n";
    print "Maximum protein length: $max_length\n";
    print "Average protein length: $average_length\n";
    print "Number of 'hypothetical' genes: $hypothetical\n";
}
=cut
