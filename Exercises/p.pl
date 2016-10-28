use strict;
use warnings;

my @ary = ('a', 'b');
my @ary1 = ('c');
push @ary1, @ary;
print scalar @ary1, "\n";

my @ary2 = ('k', 'l', @ary);
print scalar @ary2, "\n";
print $ary2[2], "\n";
