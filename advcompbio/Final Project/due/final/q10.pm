#!/usr/bin/perl
package q10;
use DBI;
use Exporter 'import';
our @EXPORT_OK = ("search_db");
sub search_db{
    my $gene = "";
    my $organism = "";
    my $tissue = "";
    my $expression_level = "";
    my $level_type = "";
    ($gene, $organism, $tissue, $expression_level, $level_type)=(@_);
    #Base query i.e. no input for gene, organism, tissue or expression
    my $query = "SELECT g.name, o.name, t.name, e.expression_level
FROM gene g, organism o, gene_organism go, gene_organism_expression e, tissue t
WHERE g.id == go.gene_id
AND t.id == e.tissue_id
AND e.id == go.id
AND o.id == go.organism_id";    
    if($gene ne ''){
	$query .= " AND g.name == '$gene'";
    }
    if($organism ne ''){
	$query .= " AND o.name == '$organism'";
    }
    if($tissue ne ''){
	$query .= " AND t.name == '$tissue'";
    }
    if($expression_level ne ''){
	if($level_type eq 'greater than'){
	    $query .= " AND e.expression_level > $expression_level";
	}else{
	    $query .= " AND e.expression_level < $expression_level";
	}
    }
    #DBI
    my $db_file = './example.db';
    my $dbh = DBI->connect( "DBI:SQLite:dbname=$db_file" , "" , "" ,
			    { PrintError => 0 , RaiseError => 1 } )
	or die DBI->errstr;
    my $sth;
    $sth = $dbh -> prepare("$query");
    #Run DBI query
    $sth -> execute();
    #HTML table
    print '<table border="2" bordercolor="111111" width="600">';
    #HTML table header
    print "<tr><td><b>Gene</b></td><td><b>Organism</b></td><td><b>Organism</b></td><td><b>Expression</b></td></tr>\n";
    my $found =0;
    while ((my($gene, $organism, $tissue, $expression)) = $sth->fetchrow_array()){
	$found++;
	print "<tr>";
	print "<td>$gene</td>";
	print "<td>$organism</td>";
	print "<td>$tissue</td>";
	print "<td>$expression</td>";
	print "</tr>";
    }
    print "</table>";
    $sth->finish();
    $dbh->disconnect();
    return $found;
}

1;
