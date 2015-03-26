#!/usr/bin/perl -w

=head1 DESCRIPTION

When comparing two sets of data a sensible thing to do first is parse the
data into a common, easily comparible format.  If it's reasonable to do 
from a memory/speed standpoint, parsing the input files into perl data
structures can facilitate comparisons.  In our case, the attributes we care
about for each gene are:

    - start coordinate
    - end coordinate
    - orientation (+/-)
    - spans origin

That last part ('spans origin') may be confusing.  For closed prokaryote 
genomes and plasmids, the molecules are usually circular and the choice of any
base position as '0' is completely arbitrary as an origin.  Therefore, it's 
possible to have a gene that spans the origin.  In fact, our example plasmid
used in class has just such a gene, as indicated by the following like in the
GenBank file:

    CDS             join(92527..92721,1..2502)

This needs to be accounted for when doing your comparisons.

Here you'll find two subroutines, 'parse_gbk_genes' and 'parse_gff_genes'
which read an input file and return a simple data structure of the coordinates
of the gene locations stored therein.  Specifically, a data structure like:

    [
        { fmin => 0, fmax => 92721, strand => 1, spans => 1 },
        { fmin => 2589, fmax => 3464, strand => 1, spans => 0 },
        { fmin => 24745, fmax => 25062, strand => -1, spans => 0 }
    ]

The ref genes have additional attributes 'has_overlap', 'match_fmin',
'match_fmax', 'match_type'.  The first is a 0|1 boolean if the gene has an 
overlapping predicted gene and, if it does, the others are coordinate
information for the overlapping predicted gene.

In this example the first gene spans the origin.  Of course, the parsing 
subroutines are dependent on the gene finder you chose.

From the Prodigal documentation, here's how partial genes (such as spanning 
the origin) are specified:

    The "partial=01", etc., field is used to indicate if genes continue off the 
    edges of the contig.  A '0' indicates that the gene is contained within the
    contig, and a '1' indicates the gene runs off that edge.  So '11' runs off both
    edges of the contig, '10' runs off the left edge, '01' runs off the right edge,
    and '00' is fully contained within the contig.

=cut

use strict;
use CGI;
use HTML::Template;

## create our CGI and TMPL objects
my $cgi  = new CGI;
my $tmpl = HTML::Template->new(filename => 'tmpl/index.tmpl');

my $term = $cgi->param('search_term');

my $refgenes = parse_gbk_genes( '../data/AB011549.2.gbk' );
my $sbjgenes = parse_gff_genes( '../data/AB011549.2.prodigal.gff' );

## the stats we're tracking
my $no_ref_overlap_count = 0;
my $exact_ref_match_count = 0;
my $end5_agreement_count = 0;
my $end3_agreement_count = 0;

## the most efficient way would be to sort both arrays and use the coordinates 
##  to walk through them in a pairwise fashion.  If you did that, kudos, but I'm
##  more interested in the comparison and display than choosing the most optimal
##  implementation for now.  Here we do a simple O(n^2) loop where each reference
##  gene is checked against every subject/predicted gene to see if they overlap.
for my $ref ( @$refgenes ) {

    $$ref{has_overlap} = 0;
    $$ref{match_type} = 'none';

    for my $sbj ( @$sbjgenes ) {
        ## don't compare genes that have different span statuses or that don't overlap
        next unless $$ref{spans} == $$sbj{spans};
        next unless genes_overlap($sbj, $ref);
        
        ## if we got here, they at least overlap and are on the same strand
        $$ref{has_overlap}++;
        $$ref{match_fmin} = $$sbj{fmin};
        $$ref{match_fmax} = $$sbj{fmax};

        if ( $$sbj{fmin} == $$ref{fmin} && $$sbj{fmax} == $$ref{fmax} ) {
            ## here we found an exact match.  record it and don't look at any
            #   other predicted genes for this reference
            $$ref{match_type} = 'agrees';
            last;
            
        } else {
            ## here we found an overlapping, non-exact match.  record it
            #   but look for something better.
            $$ref{match_type} = 'disagrees';
            next;
        }
    }
    
    ## what did we ultimately find?
    if ( $$ref{has_overlap} ) {
        if ( $$ref{match_type} eq 'agrees' ) {
            $exact_ref_match_count++;
            
        } else {
            if ( $$ref{strand} eq '+' ) {
                if ( $$ref{fmax} == $$ref{match_fmax} ) {
                    $end5_agreement_count++;
                } else {
                    $end3_agreement_count++;
                }
            } else {
                if ( $$ref{fmax} == $$ref{match_fmax} ) {
                    $end3_agreement_count++;
                } else {
                    $end5_agreement_count++;
                }
            }
            
        }
        
    } else {
        $no_ref_overlap_count++
    }
     
}

## push data to the template
$tmpl->param( REF_GENE_COUNT => scalar @$refgenes );
$tmpl->param( SBJ_GENE_COUNT => scalar @$sbjgenes );
$tmpl->param( NO_REF_OVERLAP_COUNT => $no_ref_overlap_count );
$tmpl->param( EXACT_REF_MATCH_COUNT => $exact_ref_match_count );
$tmpl->param( END5_AGREEMENT_COUNT => $end5_agreement_count );
$tmpl->param( END3_AGREEMENT_COUNT => $end3_agreement_count );
$tmpl->param( REF_GENES => $refgenes );


## print the header and template
print $cgi->header('text/html');
print $tmpl->output;


exit(0);


sub genes_overlap {
    my ($g1, $g2) = @_;
    
    ## if they're on different strands, the answer is no.
    return 0 if ( $$g1{strand} ne $$g2{strand} );

    if ( $$g1{fmin} > $$g2{fmax} || $$g1{fmax} < $$g2{fmin} ) {
        return 0;
    } else {
        return 1;
    }
}



sub parse_gff_genes {
    my $gff_file = shift;
    
    open(my $ifh, $gff_file) || die "failed to read input GFF file: $!";

    my $genes = [];
    
    ## these are in case a gene wraps the origin
    my $gene_wrap_fmin = undef;
    my $gene_wrap_fmax = undef;
    my $gene_wrap_strand = undef;
    
    while (my $line = <$ifh>) {
        my @cols = split("\t", $line);
        next unless scalar @cols == 9;
        next unless $cols[2] eq 'CDS';
        
        my $partial_stat;
        
        ## pull the partial attribute from column 9
        if ( $cols[8] =~ /partial\=(\d\d)/ ) {
            $partial_stat = $1;
        } else {
            die "Expected column 9 to have a 'partial' attribute";
        }
        
        ## check the most common case first, 
        if ( $partial_stat eq '00' ) {
            push @$genes, {
                fmin => $cols[3] - 1, 
                fmax => $cols[4], 
                strand => $cols[6] eq '+' ? 1 : -1, 
                spans => 0
            };
        
        ## record a left partial
        } elsif ( $partial_stat eq '10' ) {
            $gene_wrap_fmin = $cols[4];
            $gene_wrap_strand = $cols[6] eq '+' ? 1 : -1;
        
        ## record a right partial
        } elsif ( $partial_stat eq '01' ) {
            $gene_wrap_fmax = $cols[3] - 1;
            $gene_wrap_strand = $cols[6] eq '+' ? 1 : -1;
        }
        
    }
    
    if ( defined $gene_wrap_fmin ) {
        if ( defined $gene_wrap_fmax ) {
            push @$genes, {
                fmin => $gene_wrap_fmin, 
                fmax => $gene_wrap_fmax, 
                strand => $gene_wrap_strand, 
                spans => 1
            };
            
        } else {
            die "ERROR: found a wrapped fmin coordinate but no fmax coordinate.  this is bad.";
        }
    }
    
    return $genes;
}


sub parse_gbk_genes {
    my $gbk_file = shift;
    
    open(my $ifh, $gbk_file) || die "failed to read input GBK file: $!";

    my $genes = [];

    while (my $line = <$ifh>) {
        ## we only care about CDS lines
        if ( $line =~ /     CDS             (\S+)/ ) {
            my $coordinates = $1;
            
            if ( $coordinates =~ /join\((\d+)\.\.\d+\,\d+\.\.(\d+)\)/ ) {
                push @$genes, { fmin => $2, fmax => $1, strand => 1, spans => 1 };
            
            } elsif ( $coordinates =~ /complement\(\>{0,1}(\d+)\.\.\>{0,1}(\d+)\)/ ) {
                push @$genes, { fmin => $1 - 1, fmax => $2, strand => -1, spans => 0 };
            
            } elsif ( $coordinates =~ /\>{0,1}(\d+)\.\.\>{0,1}(\d+)/ ) {
                push @$genes, { fmin => $1 - 1, fmax => $2, strand => 1, spans => 0 };
            
            } else {
                die "unrecognized CDS line ($line).  this should not have happened.";
            }
        }
    }

    return $genes;
}
















