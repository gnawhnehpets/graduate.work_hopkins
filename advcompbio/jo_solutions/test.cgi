#!/usr/bin/perl -w

use strict;
use CGI;
my $q = new CGI;
print $q->header('text/plain');
print "Hello world!\n";
