#!/usr/bin/perl -w
#wilson_keys_dump.pl
# 09-30-2009 ejf
#reads table 'wilson' "in order"
#writes out the 'key' field to stdout
#writes a 2nd field as the SLP transliteration of key
#writes a 3rd field as the number of records having the given key.
use DBI;
use lib "../../../../../../cgi/libutilcgi";
use SLPtransliterate;
$| = 1;
my  $dbh = DBI->connect (<missing>)
             || die "Could not connect to database: "
             . DBI-> errstr;
my $table = "wilson";
my $line;
my $more= 1;
my ($nmax,$n);
my ( $key, $lnum, $data);
my $dbg=0; #0 for no dbg, 1 for dbg
my %keyhash;
my @keyarr;
my $numrec=0;
$nmax=0;
$lnum = 0;
my $nfound;

my $nkey=0;
$nfound=do_process1();
print STDERR "$nfound keys found in table $table\n";
$dbh->disconnect;
$n=0;

for($n=0;$n<$nkey;$n++) {
    $key=$keyarr[$n];
    $val = $keyhash{$key};
    my $slp = HK2SLP($key);
    print "$key\t$slp\t$val\n";
}
print STDERR "$n distinct keys\n";
exit 0;
sub do_process1 {
    my $nfound1=0;
    my $sql1 = "select `key`,`lnum` from `$table` ORDER BY `lnum`";
    my $dbhout = $dbh->prepare($sql1);
    $dbhout->execute;
    $nfound1=0;
    while(my($key1,$lnum1)=$dbhout->fetchrow_array) {
#	chomp($key1);
	$val = $keyhash{$key1};
	$lnum1 =~ s/[.]00$//;
	if (! $val) {
	    $val = $lnum1;
	    $keyarr[$nkey] = $key1;
	    $nkey++;
	}else {
	    $val = $val . ",$lnum1";
	}
	$keyhash{$key1} = $val;
	$nfound1++;
    }
    $nfound1;
}

