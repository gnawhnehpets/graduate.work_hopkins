#!/usr/bin/perl
use strict;
use warnings;
use HTML::Template;

# the fruit data - the keys are the fruit names and the values are
# pairs of color and shape contained in anonymous arrays
my $apple_color = 'test color';
my %sequence_data = (
    pple => [$apple_color, 'Round'],
    Orange => ['Orange', 'Round'],
    Pear => ['Green or Red', 'Pear-Shaped'],
    Banana => ['Yellow', 'Curved'],
    );

my $template = HTML::Template->new(filename => 'f.tmpl');

my @loop;  # the loop data will be put in here

# fill in the loop, sorted by fruit name
foreach my $seq_id (sort keys %sequence_data) {
    # get the color and shape from the data hash
    my ($seq_length, $mm) = @{$sequence_data{$seq_id}};
    
    # make a new row for this fruit - the keys are <TMPL_VAR> names
    # and the values are the values to fill in the template.
    my %row = ( 
	id => $seq_id,
	sequence_length => $seq_length,
	mm => $mm
	);
    
    # put this row into the loop by reference             
    push(@loop, \%row);
}

  # call param to fill in the loop with the loop data by reference.
$template->param(sequence_loop => \@loop);

# send the obligatory Content-Type
print "Content-Type: text/html\n\n";

# print the template
print $template->output;
