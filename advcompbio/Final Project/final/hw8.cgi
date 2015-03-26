#!/usr/bin/perl
=head1 HW8
In Unit 6, HW #5 you created a web interface and search functionality that read 
the E. coli Genbank file and reported results to the user. For this homework, you 
should make a copy of your unit06 homework into a new directory called unit08 under
your web directory. (If you prefer, you can use the posted solution as your starting 
point instead by copying /var/www/jorvis/unit06 into your directory and renaming it 
to unit08.) If, for any reason, you need your database re-initialized and loaded for
you because you had problems with it send me an e-mail.)

Now, once you have this ready your assignment is to modify the code to read from your 
database instead of the Genbank file to produce its results. You should take care to
do this in a secure way that avoids SQL injection. Also, part of being a perl developer 
is independently reading about a perl module and adding it to your implementation. Read 
the documentation for Config::IniFiles and use that module to store all your database 
connection info in an INI file instead of hard-coding it in your script (this includes 
database, host, user and password.)
=cut

use strict;
use warnings;
use CGI(':standard');
use HTML::Template;
use DBI;
use Config::IniFiles;

my $q = new CGI;
print $q->header( -type => 'text/html' );

#Template
my $tmpl = HTML::Template->new( filename => './hw8.tmpl' );

#data.ini file
=d
[Database]
DB = 'shwang26_chado'
[Host]
loc = 'localhost'
[User]
name = 'shwang26'
[Password]
pw = 'Hopkins1002'
=cut
#Import values from .ini file
my $cfg = Config::IniFiles->new(-file=> "./data.ini");
my $db = $cfg->val('Database','DB');
my $host = $cfg->val('Host','loc');
my $user = $cfg->val('User','name');
my $pass = $cfg->val('Password','pw');

#Remove hyphens from string
$db =~ s/'//gi;
$host =~ s/'//gi;
$user =~ s/'//gi;
$pass =~ s/'//gi;

my $dsn = "DBI:mysql:database=".$db.";host=localhost";
my $dbh = DBI->connect($dsn, $user, $pass, { RaiseError => 1, PrintError => 1 });

my $search= param('search_name');
print p("Your search term was: ",$search);
chomp($search);

my $qry = qq{
SELECT f.uniquename, product.value
FROM feature f
JOIN cvterm polypeptide ON f.type_id=polypeptide.cvterm_id
JOIN featureprop product ON f.feature_id=product.feature_id
JOIN cvterm productprop ON product.type_id=productprop.cvterm_id
WHERE polypeptide.name = 'polypeptide'
AND productprop.name = 'gene_product_name'
AND product.value like ?;
};

my $dsh = $dbh -> prepare($qry);
$dsh -> execute("%".$search."%");
my @locus;
my @product;
my $counter = 0;
while ( my $row = $dsh->fetchrow_hashref ) {
    $locus[$counter]=$$row{uniquename};
    $product[$counter]=$$row{value};
    $counter++;
}

#Print number of matches/search results
print p("You have ", scalar(@product), "results.");

my %gbk_hash;

while (@locus and @product) {
    $gbk_hash{shift @locus} = [shift @product];
}

#The loop data will be put in here
my @loop;

#Fill in the loop, sorted by product name
foreach my $locus_num (sort keys %gbk_hash){
    # get the length and mm from the data hash
    my ($product) = @{$gbk_hash{$locus_num}};
    # make a new row for this seq - the keys are <TMPL_VAR> names
    # and the values are the values to fill in the template.
    my %row = (
        locus_tag => $locus_num,
        product_name => $product
        );
    # put this row into the loop by reference
    push(@loop, \%row);
}

$tmpl->param(gbk_loop => \@loop);
print $tmpl->output;
exit(0);

$dsh -> finish();
$dbh -> disconnect();
