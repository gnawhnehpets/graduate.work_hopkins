use Bio::SeqIO;
use Bio::DB::GenBank;
use Bio::AnnotationI;

my $inseq = Bio::SeqIO->new(-file=>$infile, -format => 'genbank',);

### Retrieve each GenBank record (as objects) and parse them.

while (my $seq=$inseq->next_seq) { 
    my $accession='';
    my $dna='';
    my $species='';
    $accession = $seq->accession;

### Get information from Features : gene, CDS, and species
    for my $features ($seq->get_SeqFeatures) {
      if ($features->has_tag('gene')) {
	for my $val ($features->get_tag_values('gene')) {$gene=$val;}
      } elsif ($features->has_tag('product')) {
	for my $val ($features->get_tag_values('product')) {$gene=$val;}
      } else {$gene='Unknown';}
print "  gene $gene";
      if ($features->primary_tag eq 'CDS' && $stripintrons eq 'Y') { $dna=$features->spliced_seq->seq; $yes++; }
      if ($features->has_tag('organism')) {
	for my $val ($features->get_tag_values('organism')) { $species = $val; }
    } elsif ($species eq '') { $species='Unknown'; }}

### Get information from Annotation : authors and reference citation
    my $anno_collection = $seq->annotation;
    my @reference=$anno_collection->get_Annotations('reference');
    my $ref=$reference[0];
	my $authors='';
	my $journalref='';
	my $hash_ref='';
    unless ($ref eq undef) {
    $hash_ref=$ref->hash_tree;
    $authors=$hash_ref->{'authors'};
    $journalref=$hash_ref->{'location'};
}

### Get information about classification of the organism.
    my @classification = $seq->species->classification;

### Print the information to file.
my $genefilename=$directory.$gene.".txt";
    unless (-e $genefilename) { open (GENE,">$genefilename"); } else { open (GENE,">>$genefilename");}   # If the file exists, then append the info, otherwise create a new file.
my $id=$species."_".$accession;
print GENE ">$id\n$dna\n";
close GENE;
exit;
