#!/usr/bin/env perl
use strict;
use warnings;
#use CGI(':standard');
#use HTML::Template;
use Bio::Perl;
use Bio::DB::GenBank;
use Bio::SeqIO;
use Bio::Tools::OddCodes;
use DBI;
use Config::IniFiles;

my @acc;
my @start;
my @stop;
open (REFINED, "/var/www/shwang26/final/refine.txt") || die "Could not open: $!";

while(<REFINED>){
#gb|AAA85196.1|CNF1 [Escherichia coli]                           |75.9|7e-15|157|192
    if(/^(\D+)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(\d+)\|(\d+) *$/){
	push(@acc, $2);
	push(@start, $6);
	push(@stop, $7);
    }
}
close REFINED;

foreach(@start){
#    print $_."\n";
}

#print "\n";
foreach(@stop){
#    print $_."\n";
}
my $dbe  = 'genbank';
my $i=0;

foreach my $accession(@acc){
    my $seq = get_sequence( $dbe , $accession );    
    my $feature_count = $seq -> feature_count;
    my $accession = $seq->accession_number;
    my $sequence  = $seq->seq;
    my $length = $seq->length;
    my $description = $seq-> desc;
    my $keywords = $seq -> keywords;
#    my $species = $seq->species->binomial();
    my $species = $seq->species->binomial();
    my $alpha = $seq->alphabet;             # 'dna', 'rna', 'protein'
    my $version = $seq->seq_version;
    my $primary = $seq->primary_id;
    my $start ='';
    my $end = '';

#Oddcode object
    my $oddcode = Bio::Tools::OddCodes->new(-seq => $seq);

#Determine length of alignment for substr method
    my $start_pos = $start[$i];
    my $stop_pos = $stop[$i];
#    print "#########################################";
#    print $start_pos."\t".$stop_pos."\n";
    $i++;
    my $align_length = $stop_pos-$start_pos;

#Oddcode: Structural
    my $structural = ${$oddcode->structural};
    $structural = lowercase($structural, $start_pos, $align_length);
#    print $accession."\n";
#    print substr($structural, 1, 100)."\n";;

#Oddcode: Chemical 
    my $chemical = ${$oddcode->chemical};
    $chemical = lowercase($chemical, $start_pos, $align_length);

#Oddcode: Functional
    my $functional = ${$oddcode->functional};
    $functional = lowercase($functional, $start_pos, $align_length);

#Oddcode: Charge
    my $charge = ${$oddcode->charge};
    $charge = lowercase($charge, $start_pos, $align_length);

#Oddcode: Hydrophobic
    my $hydrophobic = ${$oddcode->hydrophobic};
    $hydrophobic = lowercase($hydrophobic, $start_pos, $align_length);

#Oddcode: Dayhoff
    my $dayhoff = ${$oddcode->Dayhoff};
    $dayhoff = lowercase($dayhoff, $start_pos, $align_length);

#Oddcode: Sneath
    my $sneath = ${$oddcode->Sneath};
    $sneath = lowercase($sneath, $start_pos, $align_length);

    foreach my $feat ($seq->top_SeqFeatures()){
	if($feat->primary_tag eq 'exon'){
	    $start = $seq->start;
	    $end = $seq->end;
	}
    }
}
=d
FEAT: 3
NAME: WP_001566411
ACC: WP_001566411
LENGTH: 1014
DESC: cytotoxic necrotizing factor 1 [Escherichia coli].
KEY:
SPEC: Escherichia coli
ALPHA: protein
VERS: 1
PRIM: 486261610
STRUCTURAL: $structural
CHEMICAL: $chemical
FUNCTIONAL: $functional
CHARGE: $charge
HYDROPHOBIC: $hydrophobic
DAYHOFF: $dayhoff
SNEATH: $sneath
";
=cut

#Import values from .ini file
#open (REFINED, "/var/www/shwang26/final/refine.txt") || die "Could not open: $!";

my $cfg = Config::IniFiles->new(-file=> "./data.ini");
my $db = $cfg->val('Database','DB');
my $host = $cfg->val('Host','loc');
my $user = $cfg->val('User','name');
my $pass = $cfg->val('Password','pw');

my $dsn = "DBI:mysql:database=".$db.";host=localhost";
my $dbh = DBI->connect($dsn, $user, $pass, { RaiseError => 1, PrintError => 1 });


my $sth = $dbh->prepare( "" );
$sth->execute();
$sth->finish();
$dbh->disconnect();


sub lowercase{
    my ($string, $start, $length) = (@_);
    my $substring = substr($string, $start, $length);
    my $lower = lc($substring);
    $string =~ s/$substring/$lower/g;
    return $string;
}
