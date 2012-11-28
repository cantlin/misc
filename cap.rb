#! /usr/bin/env ruby

require 'trollop'
require 'selenium-webdriver'

CONF = Trollop::options do
	opt :url, "Site to capture", :short => "-u", :default => "cantl.in"
	opt :outfile, "Output file name", :short => "-o"
	opt :protocol, "Protocol to use", :short => "-p", :default => "http"
	opt :width, "Capture width", :short => "-x", :default => 1024
	opt :height, "Capture height", :short => "-y", :default => 760
    opt :force, "Crop output file to width and height (requires ImageMagick)", :short => "-f", :default => true
end

# Start Chrome
driver = Selenium::WebDriver.for :chrome
driver.navigate.to "#{CONF.protocol}://#{CONF.url}"

# Resize the window to the required dimensions. In practise height isn't important,
# since Selenium captures the whole visible page. We do need to account for a scroll
# bar, which will cost us a few pixels if the document height exceeds the window height.
scroll_bar_width = 16
width = (driver.manage.window.size.height > CONF.height) ? CONF.width + scroll_bar_width : CONF.width
driver.manage.window.resize_to(width, CONF.height)

# Save out a screenshot
outfile = CONF.outfile || "#{CONF.url.gsub('.', '_')}_#{Time.now.to_i}.png"
driver.save_screenshot(outfile)

# Optionally crop the file to the required dimensions (the whole page is saved by default)
if(CONF.force)
    %x"convert -crop #{CONF.width}x#{CONF.height}+0+0 #{outfile} #{outfile}"
end

# Highlight the new file in Finder
%x"open -R #{outfile}"

puts outfile
driver.close