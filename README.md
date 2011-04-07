## ggu

Basically a glorified shell script that chains some commands: `[gphoto2](http://www.gphoto.org/]` to get all the pictures from your digital camera, `[ImageMagick](http://www.imagemagick.org/script/)` to normalize, resize and optionally rotate the images, and `ftp` to upload them some place. Do `./ggu.py -h` for options.

## hon_talk

Class for sending Private Messages on a remote vBulletin forum that you don't control with cURL, implemented as a Drupal 6 module that overrides the default activation email behaviour.

## irssi

Hacky Perl script to log topics to a database, if you don't mind bloat you could make it log everything easily enough. Basic class for reading log files that doesn't really do anything yet, log like `/var/log/irc/channel_%Y-%m-%d.log: #channel ALL` if you want it to work out of the box.