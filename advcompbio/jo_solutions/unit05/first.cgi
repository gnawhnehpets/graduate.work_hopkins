#!/usr/bin/perl -w

use strict;
use CGI;
use HTML::Template;

## create our CGI and TMPL objects
my $cgi  = new CGI;
my $tmpl = HTML::Template->new(filename => 'tmpl/first.tmpl');

## set any variables
my $message = "My first template page";

## push data to the template.
$tmpl->param( PAGE_TITLE  => 'Test title page' );
$tmpl->param( PAGE_HEADER => $message );

## print the header and template
print $cgi->header('text/html');
print $tmpl->output;
