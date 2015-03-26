#!/usr/bin/perl -w

=head1 DESCRIPTION

From Unit 05, homework question #1:

In the homework from Unit 3 you wrote scripts to parse a FASTA file and gather
some size statistics on the sequences found within it. For this assignment, make a copy of that
script and modify it to present the same summary as a CGI page instead. This will mean that
you'll need to create a template file your script will populate using HTML::Template. You
should store your code in your user directory under /var/www and follow the directory
conventions from the lecture.

Your template should have the summary information at the top of the page, and then underneath
it I want you to add a table that contains three columns. In the first put the ID of each sequence
from the file, put the length in the second, and molar mass in the third.

NOTE: I've modified the core of the script some since lesson 3, since you know subroutine now.
  
=cut

use strict;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use HTML::Template;

my $q = new CGI;
print $q->header( -type => 'text/html' );

my $tmpl = HTML::Template->new( filename => './summarize_fasta.tmpl' );

my $fasta_file = 'e_coli_k12_dh10b.faa';

open(my $ifh, $fasta_file) || die "ERROR: can't read input FASTA file: $!";

## variables to hold requested stats
my $min_protein_length = undef;
my $max_protein_length = 0;
my $hypothetical_count = 0;

## variables needed to get an average protein length
my $protein_count = 0;
my $sum_protein_size = 0;

## temporary variables to use while iterating through the file
my $current_seq = undef;
my $current_seq_id = undef;

## holds data on ALL of the sequences in the FASTA file
#   each element is a hash with keys: seq_id, seq_len, molar_mass
my @seqs = ();

## source: https://www.neb.com/tools-and-resources/usage-guidelines/amino-acid-structures
my %mol_weight = (
    G =>  57.05, A =>  71.09, S =>  87.08, T => 101.11, C => 103.15,
    V =>  99.14, L => 113.16, I => 113.16, M => 131.19, P =>  97.12,
    F => 147.18, Y => 163.18, W => 186.21, D => 115.09, E => 129.12,
    N => 114.11, Q => 128.14, H => 137.14, K => 128.17, R => 156.19,
);

## iterate through the file line-by-line
while ( my $line = <$ifh> ) {

    ## look for new entry lines and match ID and annotation portions
    if ( $line =~ /^\>(\S+)(.+)/ ) {
        my ($seq_id, $product) = ($1, $2);
        $protein_count++;
        $hypothetical_count++ if $product =~ /hypothetical/i;
        
        ## do we have a sequence to process?  this would only be false at the beginning of the file
        if ( defined $current_seq ) {
            process_sequence($current_seq_id, $current_seq);
        }
        
        ## we're finished processing, so now reset to build this sequence
        $current_seq = '';
        $current_seq_id = $seq_id;
        
    } else {
        ## if this isn't a header line, add it to the current sequence
        $current_seq .= $line;
    }
}

## since we were processing the building sequence when we encountered a new > symbol, the last
#   sequence in the file would go unprocessed unless we handle it now
process_sequence($current_seq_id, $current_seq);

## now print the results to the template
my $avg_protein_length = sprintf("%.1f", $sum_protein_size / $protein_count );

$tmpl->param( PROTEIN_COUNT => $protein_count );
$tmpl->param( MIN_PROTEIN_LENGTH => $min_protein_length );
$tmpl->param( MAX_PROTEIN_LENGTH => $max_protein_length );
$tmpl->param( AVG_PROTEIN_LENGTH => $avg_protein_length );
$tmpl->param( HYPOTHETICAL_GENES => $hypothetical_count );
$tmpl->param( SEQS => \@seqs );

print $tmpl->output;

exit(0);

sub process_sequence {
    my ($id, $seq) = @_;

    ## make sure there's no whitespace in our sequence that could throw off the length
    $seq =~ s/\s//g;
    
    my $seq_len = length($seq);
    $sum_protein_size += $seq_len;
    $max_protein_length = $seq_len if $seq_len > $max_protein_length;

    if ( ! defined $min_protein_length || $seq_len < $min_protein_length ) {
        $min_protein_length = $seq_len;
    }

    push @seqs, { seq_id => $id, seq_len => $seq_len, molar_mass => calculate_mol_weight($seq) };
}

## returns the molecular weight of a passed amino acid sequence
#   or the value 'Unknown' if a residue is encountered that isn't in the
#   molecular weight lookup.
sub calculate_mol_weight {
    my $seq = shift @_;
    my $weight = 0;

    for my $aa ( split('', $seq) ) {
        if ( exists $mol_weight{$aa} ) {
            $weight += $mol_weight{$aa};
        } else {
            return "Unknown";
        }
    }

    return sprintf("%.2f", $weight);
}












