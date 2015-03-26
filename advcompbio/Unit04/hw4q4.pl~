#!usr/bin/perl
use strict;
use warnings;

my $foo = 'this is foo';
my @data = qw(this is an array of data);
my $woo = 'this is woo';
do_stuff( $foo, \@data, \$woo);

sub do_stuff {
    my ($var1, $arr1, $var2) = @_;
    print $var1."\n";
    foreach(@$arr1){print $_."\t";
    }
    print "\n".$$var2."\n";
}
