#!/usr/bin/perl -w
#mwtab_dump.pl
# 05-04-2007 ejf
#reads table 'monier' "in order"
#writes out file like MONIERhBU.txt 
#output written to STDOUT, so a redirect normally needed.
use DBI;
$| = 1;
my  $dbh = DBI->connect (<MISSING>)
             || die "Could not connect to database: "
             . DBI-> errstr;

my $line;
my $more= 1;
my ($nmax,$n);
my (@keydat, $key, $lnum, $data);
my $dbg=0; #0 for no dbg, 1 for dbg
my $numrec=0;
$nmax=0;
$lnum = 0;
my $nfound;

$nfound=do_process1();
print STDERR $nfound;
$dbh->disconnect;
exit 0;
sub do_process1 {
    my $sql;
    my $sql1;
    my $lnum1;
    my $nfound=0;
    my $nfound1=0;
    $sql1 = "select `data` from `monier` ORDER BY `lnum`";
    my $dbhout;
    $dbhout = $dbh->prepare($sql1);
    $dbhout->execute;
    $nfound1=0;
    while(my($data1)=$dbhout->fetchrow_array) {
	chomp($data1);
	print "$data1\n";
	$nfound1++;
	if ($data1 =~ /<MW>.*?<\/MW>/) {
	    print "\n"; # for conformity with original file.
	}
    }
    $nfound1;
}

