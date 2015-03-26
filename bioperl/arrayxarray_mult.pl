#!/usr/bin/perl
use strict;
use warnings;


#Write a function which takes two arrays as arguments (passed by reference) and returns a reference to an array of arrays, consisting of the products of the elements of the two arrays. Write a script that uses the function and then prints out the resulting matrix.
         # Example:
# input == ( 1 , 2 , 3 ) and ( 2 , 4 , 6 )
# output ==
#          2  4  6
#          4  8 12
#          6 12 18
print "enter in values and enter `done` when done\n";
my $input="";
my @arraya;
my $counter=0;
#first array
while($input ne "done"){
    print "enter value: ";
    $input=<STDIN>;
    chomp($input);
    if($input =~ /\d+/){
#	print $input."\n";
	$arraya[$counter]=$input;
	$counter++;
    }elsif($input eq "done"){
	next;
    }else{
	die "only numbers please!";
    }
}

$input="";
$counter=0;
my @arrayb;
print "enter more values\n";
while($input ne "done"){
    print "enter value: ";
    $input=<STDIN>;
    chomp($input);
    if($input =~ /\d+/){
#	print $input."\n";
	$arrayb[$counter]=$input;
	$counter++;
    }elsif($input eq "done"){
	next;
    }else{
	die "only numbers please!";
    }
}


foreach my $val (@arraya){
    for(my $i=0; $i < scalar(@arrayb); $i++){
	my $matrix = $val*$arrayb[$i];
	print $matrix."\t";
    }
    print "\n";
}

=d
print "first: ";
my $first_a1 = <STDIN>;
chomp($first_a1);
print "second: ";
my $second_a1 = <STDIN>;
chomp($second_a1);
print "third: ";
my $third_a1 = <STDIN>;
chomp($third_a1);

