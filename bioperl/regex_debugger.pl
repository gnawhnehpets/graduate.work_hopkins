#!/usr/bin/env perl
use strict;
use warnings;

#This asks user for regex and then tests inputs against the regex and reports whether they match. It supports 'exit' command to allow quitting
#ex: 5. Enter regexp: oo
#Enter string or 'exit' to exit; foo
#Match!
#Enter string or 'exit' to exit; bar
#No match!
#Enter string or 'exit' to exit; exit
#bye bye!

print "Enter regexp:\n";
my $regex = <STDIN>;
chomp($regex);
my $input = "";

until($input eq "exit"){
    print "Enter string or 'exit' to exit:\n";
    $input = <STDIN>;
    chomp($input);
    if($input =~ /($regex)/){
	print "Match!\n";
    }else{
	print "No match!\n";
    }
}

print "bye bye!\n";
