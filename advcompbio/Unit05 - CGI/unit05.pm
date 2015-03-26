#!usr/bin/perl
use strict;
use warnings;
#use SeqStats;
#use Bio::Seq;
#use Bio::Tools::Seqstats;
use Exporter 'import';
our @EXPORT_OK=("table");
our @EXPORT_OK=("summary");

sub table{
#   my $seq_stats=SeqStats->new($seqobj);
    my $printable = 0;
    my $count = 0;
    my $seq_num=0;
    my @seq_id;
    my $sequence='';
    my $string_length=0;
    my @len;
    my $len_num=0;
    my $string_counter=0;
    my @aa_seq;
    my $amino_seq='';
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
	    $amino_seq='';
	}else{
            #Otherwise (aka sequence), store length of line/sequence...
	    $string_length+=length();
	    $amino_seq.=$_;
#	    my $seqobj = Bio::Seq->new(-seq => $amino_seq);
#	    my $seq_stats=SeqStats->new($seqobj);
#	    $weight=$seq_stats->get_mol_wt();
#	    print $amino_seq."\n";
	    $len[$len_num]=$string_length;
	    $aa_seq[$len_num]=$amino_seq;
#	    $aa_seq[$len_num]=$weight;

            #If same sequence (!0), then store updated string_length to prior array position
	    if($string_counter!=0){
		$len_num--;
		$len[$len_num]=$string_length;
		$aa_seq[$len_num]=$amino_seq;
#		$seq_stats=SeqStats->new($seqobj);
#		$seqobj = Bio::Seq->new(-seq => $amino_seq);
#		$weight=$seq_stats->get_mol_wt();
#		$aa_seq[$len_num]=$weight;

	    }
            #Progress along array position...
	    $len_num++;
            #Add to sequence counter...
	    $string_counter++;
	}
    }
    return (\@seq_id, \@len, \@aa_seq);
}

sub summary{

    my $min_protein_length = undef;
    my $max_protein_length = 0;
    my $hypothetical_count = 0;

    ## variables needed to get an average protein length
    my $protein_count = 0;
    my $sum_protein_size = 0;

    ## temporary variables to use while iterating through the file
    my $current_seq = undef;

    ## iterate through the file line-by-line
    while ( my $line = <INPUT> ) {
	## look for new entry lines and match the annotation portion
	if ( $line =~ /^\>\S+(.+)/ ) {
	    my $product = $1;
	    $protein_count++;
	    
	    $hypothetical_count++ if $product =~ /hypothetical/i;
	    
	    ## do we have a sequence to process?  this would only be false at the beginning of the file
	    if ( defined $current_seq ) {
		## make sure there's no whitespace in our sequence that could throw off the length
		$current_seq =~ s/\s//g;
		
		$sum_protein_size += length($current_seq);
		$max_protein_length = length($current_seq) if length($current_seq) > $max_protein_length;
		
		if ( ! defined $min_protein_length || length($current_seq) < $min_protein_length ) {
		    $min_protein_length = length($current_seq);
		}
	    }
	    
	    ## we're finished processing, so now reset to build this sequence
	    $current_seq = '';

	} else {
	    ## if this isn't a header line, add it to the current sequence
	    $current_seq .= $line;
	}
    }
    
    ## since we were processing the building sequence when we encountered a new > symbol, the last
    #   sequence in the file would go unprocessed unless we handle it now
    #   NOTE: this should normally be a subroutine called both here and within the loop, but we're
    #   assuming you don't know that yet.
    $current_seq =~ s/\s//g;
    
    $sum_protein_size += length($current_seq);
    $max_protein_length = length($current_seq) if length($current_seq) > $max_protein_length;
    
    if ( ! defined $min_protein_length || length($current_seq) < $min_protein_length ) {
	$min_protein_length = length($current_seq);
    }


    ## now print the results.
    my $avg_protein_length = sprintf("%.1f", $sum_protein_size / $protein_count );
    my $a = "gene count: $protein_count\n";
    my $b = "min protein length: $min_protein_length\n";
    my $c = "max protein length: $max_protein_length\n";
    my $d = "average protein_length: $avg_protein_length\n";
    my $e = "hypothetical genes: $hypothetical_count\n";
    return ($a, $b, $c, $d, $e);
}	
1;
