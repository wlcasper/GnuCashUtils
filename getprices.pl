#!/usr/bin/perl -w

# Retrieve stock prices from AlphaVantage and print as CSV format.

# Due to the limit (up to 5 API requests per minute) for free API
# service as mentioned at
# https://www.alphavantage.co/support/#api-key, there are 70 seconds
# pause between each batch.

use Finance::Quote;

my $q = Finance::Quote->new();

my @stocks = ("QCOM", "BABA", "FB", "VT", "BND", "RHT", "VTC", "NVDA", "VEXRX",
	  "VMCPX", "VTSAX", "VGSIX");

my $limits = 5;

for (my $start = 0; $start <= $#stocks; $start += $limits) {
    my $end = $start + $limits - 1;
    $end = $#stocks if $end > $#stocks;
    my @batch = @stocks[$start..$end];
    my %quotes = $q->alphavantage(@batch);
    for my $stock (@batch) {
	print "$stock,", $quotes{$stock, "date"}, ",", $quotes{$stock, "last"}, "\n";
    }
    sleep(70) if $start + $limits <= $#stocks;
}
