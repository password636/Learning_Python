use strict;
use warnings;

my @array = qw/a b c/;
my @array1 = ('d', @array);	#
printf "array has %d elements\n", scalar @array;
printf "array1 has %d elements\n", scalar @array1;

my @array2 = qw/e f/;
push @array2, @array1;		#
printf "array2 has %d elements\n", scalar @array2;
