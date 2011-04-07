#
# Logs topics.
# 
# table format;
# +---------+-----------------------+------+-----+-------------------+----------------+
# | Field   | Type                  | Null | Key | Default           | Extra          |
# +---------+-----------------------+------+-----+-------------------+----------------+
# | id      | int(10) unsigned      | NO   | PRI | NULL              | auto_increment | 
# | stamp   | timestamp             | NO   |     | CURRENT_TIMESTAMP |                | 
# | nick    | varchar(32)           | NO   |     |                   |                | 
# | channel | varchar(32)           | NO   |     |                   |                | 
# | value   | text                  | NO   |     |                   |                | 
# | action  | enum('TOPIC','OTHER') | NO   |     |                   |                | 
# +---------+-----------------------+------+-----+-------------------+----------------+

use DBI;
use Irssi;
use Irssi::Irc;
# use Data::Dumper;

use vars qw($VERSION %IRSSI);

$VERSION = "0.2";
%IRSSI = (
        authors     => "Riku Voipio, lite, Dae",
        name        => "log_topic",
        description => "logs topics to a mysql database",
        license     => "GPLv2",
    );

$db_name = 'dbname';
$db_host = 'localhost';

$dsn = 'DBI:mysql:' . $db_name . ':' . $db_host;

$db_user_name = 'dbuser';
$db_password = 'dbpass';

sub cmd_logurl {
	my ($channel) = @_;

	$name = $channel->{visible_name};
	@topic_by = split('!', $channel->{topic_by});
	$nick = $topic_by[0];
	$text = $channel->{topic};

	save($nick, $name, $text);
	
	return 1;
}

sub save {
	my ($nick, $channel, $text)=@_;

	my $dbh = DBI->connect($dsn, $db_user_name, $db_password);
	my $sql="INSERT INTO irclog (action, nick, channel, value) VALUES ('TOPIC', ". $dbh->quote($nick) ."," . $dbh->quote($channel) ."," . $dbh->quote($text) .")";
	my $sth = $dbh->do($sql);

	$dbh->disconnect();
}

# Init

Irssi::print('Now logging topics to ' . $db_name);
Irssi::signal_add_last('channel topic changed', 'cmd_logurl');
