#!/opt/perl/bin/perl
=head
Write a CGI to provide web-based search of your database, as in the question last week. 
Allow repeated searches from the single form. Allow queries on gene name, organism, 
tissue type, expression level, or any combination of these attributes. (Assume all input 
is combined with AND; you don't need to support OR .... yet.)
=cut
use strict;
use warnings;
use CGI ':standard';
use q10('search_db');

#Create HTML page
my $title = 'Database search';

print header,
    start_html($title),
    h3($title);

#Handle processing of form if this is a submission
if(param('submit')){ 
    my $gene = param('gene');
    my $organism = param('organism');
    my $tissue = param('tissue');
    my $expression_level = param('expression_level');
    my $level_type = param('level_type');
    my $defined = search_db($gene, $organism, $tissue, $expression_level, $level_type);
    if($defined == 0){
	print h5("* NOT FOUND *");
    }
    print h4("Search again:");
}
# and then print out the base form regardless of whether this is the
# first time or the tenth
my $url = url();
print start_form( -method => 'GET' , action => $url ),
    p( "Gene name: " . textfield( -name => 'gene' )),
    p( "Organism: " . textfield( -name => 'organism' )),
    p( "Tissue type: " . textfield( -name => 'tissue' )),
    p( "Expression level: " . radio_group (-name => 'level_type',
                                           -values => ['less than', 'greater than'])
       . textfield( -name => 'expression_level' )),
    p( submit( -name => 'submit' , value => 'Submit' )),
    end_form(),
    end_html();
