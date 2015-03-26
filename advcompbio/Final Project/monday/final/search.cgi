#!/usr/bin/env perl
use strict;
use warnings;
use CGI ':standard';
use DBI;
use Config::IniFiles;
use JSON;
my $json = JSON->new->allow_nonref;

my $cgi = new CGI;
my $term = $cgi->param('db_search');
#my $term = "WP_001533923";
my $cfg = Config::IniFiles->new(-file=> "/var/www/shwang26/final/data.ini");
my $db = $cfg->val('Database','DB');
my $host = $cfg->val('Host','loc');
my $user = $cfg->val('User','name');
my $pass = $cfg->val('Password','pw');

my $dsn = "DBI:mysql:database=".$db.";host=localhost";
my $dbh = DBI->connect($dsn, $user, $pass, { RaiseError => 1, PrintError => 1 });

my $sth = $dbh->prepare("select h.description, h.accession, s.sequence
from hits h, structural s
where h.id=s.id
and h.accession like ?");
$sth->execute("%".$term."%");
my @data;
=d
while (@data = $sth->fetchrow_array()) {
    my $id = $data[0];
    my $first = $data[1];
    my $second = $data[2];
    print "\n$first \t$second\n";
}
=cut
my @id;
my @accession;
my @description;
my @structural;
my $counter=0;
while ( my $row = $sth->fetchrow_hashref ) {
    $id[$counter]=$$row{id};
    $accession[$counter]=$$row{accession};
    $description[$counter]=$$row{description};
    $structural[$counter]=$$row{sequence};
    $counter++;
}
my $counter=0;
foreach(@accession){
    $counter++;
#    print $_."\n\n";
}
#print $counter."\n";

$sth->finish();
$dbh->disconnect;
my $count = scalar(@structural);
my $dbmatches=[];
#Store parsed results as hashref in arrayref
for(my $i=0; $i < scalar(@accession); $i++){
    #hash ref:  $href->{ $key } = $value;
    my $href = {};
    $href->{'accession'}=$accession[$i];
    $href->{'description'}=$description[$i];
    $href->{'structural'}=$structural[$i];
#    while( my ($k, $v) = each %$href ) {
#        print "key: $k, value: $v.\n";
#    }
    push(@$dbmatches, $href);
}

#STDERR->autoflush(1);

print $cgi->header('application/json');
print $json->encode(
    { db_count => $count, dbmatches => $dbmatches }
    );