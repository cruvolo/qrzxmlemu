#!/usr/bin/perl

# xmldata.qrz.com XML callsign lookup emulation.  2-clause BSD license.

# Copyright 2020 Chris Ruvolo. All rights reserved.

use strict;
use warnings;
use utf8;
use Cwd 'realpath';
use File::Basename;
use CGI qw(-utf8);
use POSIX qw(strftime);

# Configure this if not using the recommended checkout procedure:
my $qrzpath = dirname(realpath(__FILE__)) . "/../qrmbot/lib/qrz";

# end configuration

my $cgi = CGI->new;
my %param = map { $_ => scalar $cgi->param($_) } $cgi->param() ;

if (exists $param{'html'} or exists $param{'dxcc'}) {
  print $cgi->header(
    -type => 'text/plain;charset=UTF-8',
    -status => '501 Not Implemented'
  );
  print "501 Not Implemented\n";
  exit 0;
}

print $cgi->header( -type => 'text/xml;charset=UTF-8' );

print('<?xml version="1.0" ?>',"\n");
print('<QRZDatabase version="1.34">',"\n");

if (exists $param{'callsign'}) {
  my $c = uc $param{'callsign'};
  $c =~ s/[^A-ZØ0-9]//g;

  system "$qrzpath --xml $c";
}

printSession();

print "</QRZDatabase>\n";
exit 0;


sub printSession {
  my $key = "";

  if (exists $param{'s'}) {
    $key = $param{'s'};
    $key =~ s/[^A-Z0-9]//ig;
  }

  if ($key eq "") {
    for (1 .. 4) {
      $key .= sprintf("%08x", rand(0xffffffff));
    }
  }
  my $fmt = "%a %b %d %H:%M:%S %Y";
  my $ts = strftime($fmt, gmtime());
  my $exp = strftime($fmt, gmtime(time() + (60*60*24*30*3))); # 3 months

  print("  <Session>\n");
  print("    <Key>$key</Key>\n");
  print("    <Count>0</Count>\n");
  print("    <SubExp>$exp</SubExp>\n");
  print("    <GMTime>$ts</GMTime>\n");
  print("  </Session>\n");
}
