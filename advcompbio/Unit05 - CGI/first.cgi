#!/usr/bin/perl
use warnings;
use strict;
use CGI (':standard');

#Ask user for length of random sequence
my $length = 50;

#Title of HTML page
my $title = 'Random sequence generator';
#Create HTML page
print header,
  start_html( $title ),
  h4( $title );

# handle processing of form if this is a submission
if( param( 'submit' )) {
    my $sequence_type = param('sequence');

    if($sequence_type eq 'DNA'){
        print p("Your random DNA sequence is:");
        print my $DNA_sequence = random_DNA_sequence($length);
    }

    if($sequence_type eq 'Protein'){
        print p("Your random protein sequence is:");
        print my $protein_sequence = random_protein_sequence($length);
}

  '<ul>';

  print '</ul>',
   hr();
}

# and then print out the base form regardless of whether this is the
# first time or the tenth
my $url = url();
print start_form( -method => 'GET' , action => $url ),
    p( "What type of sequence do you want:" . popup_menu(-name => 'sequence',
                                                         -values => ['DNA', 'Protein'],
                                                         -default => 'DNA')),
    p( submit( -name => 'submit' , value => 'Submit' )),
    end_form(),
    end_html();

#Subroutine generates random sequence of given length
sub random_DNA_sequence{
    #length of random sequence
    my ($length,$option)= (@_);

    #nucleotides
    my @nt=('A','G','C','T');

    my $random_string;
    foreach (1..$length){
        $random_string.=$nt[rand @nt];
    }
    return $random_string;
}

sub random_protein_sequence{
    #length of random sequence
    my ($length,$option)= (@_);

    #nucleotides
    my @nt=('A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'D', 'T', 'W', 'Y', 'V');

    my $random_string;
    foreach (1..$length){
        $random_string.=$nt[rand @nt];
    }
    return $random_string;
}

