<?php

// Default directory for IRC log files

define('LOG_DIR', '/var/log/irc/');

// Default date format

define('DATE_FORMAT', 'Y-m-d');

class Log {

	private $log_dir = LOG_DIR;
	private $log_ext = '.log';
	private $delim = '_';

	private $channel, $log_date, $log_title, $log_content = '';

	public function __construct($params = array(), $wait = NULL) {

	        $this->log_date = date(DATE_FORMAT);

		if(!empty($params))
                        self::__set($params);

		if(is_null($wait))
                        self::read_log();

	}
	
	public function __set($key, $val= NULL) {

                (is_array($key)) ? self::__arr_set($key) : $this->$key = $val;

	}
	
	public function __arr_set($arr) {

		foreach($arr as $key => $val)
		        self::__set($key, $val);

	}

	public function __get($key) {

	        switch($key) {

	                case 'log_title':
		                $val = $this->log_title = '#'.$this->channel.' logfile for '.date('F jS Y', strtotime($this->log_date));

		        case 'log_title_raw':
			        $val = $this->log_title; 

            	        default:
		                $val = $this->$key;

            	}

		return $val;

	}

	public function read_log() {

		if(empty($this->channel))
			throw new Exception('No channel set to get log for');

		$file = $this->channel.$this->delim.$this->log_date.$this->log_ext;
		$filepath = $this->log_dir.$file;

		if(!is_readable($filepath)) {
			if(DEBUG_LEVEL == 1)
				$file = $filepath;
			if(is_file($filepath))
				throw new Exception($file.' cannot be read by the web service');
			else
				throw new Exception($file.' does not exist');
		}

		if(!$log_content = file_get_contents($filepath))
			throw new Exception('Could not get contents of '.$file);

		$this->log_content = $log_content;

	}

	private function parse_links() {
		
		$this->log_content = links_to_html_a($this->log_content);

	}

	public function render() {

		if(empty($this->log_content))
			throw new Exception('No content to render');

		self::parse_links();

		return $this->log_content;

	}

}

// Simple exception handler

function handle_exception($e, $continue = NULL) {

        $out = $e->getMessage().'.';

	switch(DEBUG_LEVEL) {
		case 1:
			$out .= ' File: '.$e->getFile().'. Line: '.$e->getLine().'.';
			break;
	        default:
                        break;
	}

        if(is_null($continue))
                exit($out);

	return $out;

}

// Helper to make http://example.com into <a href="http://example.com">http://example.com</a>

function links_to_html_a($str) {

	$output =
	eregi_replace(
		'(((f|ht){1}tp://)[-a-zA-Z0-9@:%_\+.~#?&//=]+)',
		'<a target="_blank" href="\\1">\\1</a>', $str);
        $output = 
	eregi_replace(
		'([[:space:]()[{}])(www.[-a-zA-Z0-9@:%_\+.~#?&//=]+)',
		'\\1<a target="_blank" href="http://\\2">\\2</a>', $output);
	
	return $output;

}

?>