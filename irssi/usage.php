<?php

require_once 'irc_log.inc';

$time = (isset($_GET['b']) && is_numeric($_GET['b'])) ? strtotime('-'.$_GET['b'].' days') : time();

try {

        $log = new Log(array(
			     'channel' => 'irssi',
			     'log_date' => date(DATE_FORMAT, $time)
			     )
		       );

	$doc_title = $log->__get('log_title');
	$log_content = $log->render();

} catch (Exception $e) {

	handle_exception($e);

}

require_once 'irc_log_plain.tpl';

?>
