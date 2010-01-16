#!/usr/bin/env ruby

require 'fileutils'

if ARGV.length == 0
  puts "usage: gm project_name"
  exit
end

gmdir = File.join(File.dirname(__FILE__), '..', 'skelton')
FileUtils.cp_r(gmdir, ARGV[0])
puts "+ ./#{ARGV[0]}"
puts "==================="
puts "cd #{ARGV[0]}"
puts "dev_appserver.py ./"
