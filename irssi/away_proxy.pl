use Irssi;
use Irssi::Irc;

$VERSION =  '0.1';

%IRSSI = (
  authors     => "cantlin",
  name        => "away_proxy",
  description => "/away when irssi-proxy has 0 or >0 clients connected.",
  license     => "GPLv2"
);

$away_message = 'away';
$connected_client_count = 0;

sub client_connect {
  $connected_client_count++;

  foreach my $server (Irssi::servers) {
    $server->send_raw('AWAY :') unless $server->{usermode_away} == '0'
  }
}

sub client_disconnect {
  $connected_client_count--;

  if($connected_client_count == 0) {
    foreach my $server (Irssi::servers) {
      $server->send_raw('AWAY :' . $away_message) if $server->{usermode_away} == '0'
    }
  }
}

Irssi::signal_add_last('proxy client connected', 'client_connect');
Irssi::signal_add_last('proxy client disconnected', 'client_disconnect');
