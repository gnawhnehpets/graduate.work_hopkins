#!/usr/bin/env perl

use warnings;
use strict;

#Prompt user for file name
print "Enter in name of input file:\n";
chomp(my $input_file = <STDIN>) || die "Error: pass the path of a sequence file";

my $fasta_seq_count = 0;
my $fastq_seq_count = 0;
my $total_residues = 0;

# Open the file, allowing for gzip compression
my $seq_fh;
if ($input_file =~ /\.gz$/){
    open($seq_fh, "<:gzip", $input_file) || die "failed to read input file: $!";
} else {
    open($seq_fh, $input_file) || die "failed to read input file: $!";
}

while (my $line = <$seq_fh>){
    chomp $line;

    # Skip comments and blank lines and optional repeat of title line
    next if $line =~ /^\#/ || $line =~ /^\s*$/ || $line =~ /^\+/;

    # Count FASTQ sequence
    if ($line =~ /^\@/){
	$fastq_seq_count++;
    # Count FASTA sequence
    } elsif ($line =~ /^\>/){
	$line =~s/\s//g;
	$fasta_seq_count++;
    # Skip "quality line"
    } elsif ($line !~ /\D[a-z]/i){
	next;
    # Count residues
    } else {
	$line =~ s/\s//g;
	$total_residues += length($line);
    }
}

# If no FASTQ sequences found, then report the number of FASTA sequences (and vice versa)
if($fasta_seq_count == 0){
    print "Total FASTA sequences found: $fasta_seq_count\n";
} else {
    print "Total FASTQ sequences found: $fastq_seq_count\n";
}

# Report number of residues found.
print "Total residues found: $total_residues\n";
