#!/usr/bin/env ruby

require 'erb'

if ARGV[0] == 'controller' && ARGV[1]
  unless File.exist?('app/controllers') && File.exist?('app/templates')
    puts "please execute root dir."
    exit
  end

  dir = File.join(File.dirname(__FILE__), 'erb')
  controller = File.join(dir, 'controller.erb')
  template = File.join(dir, 'template.erb')
  name = ARGV[1].capitalize

  controller_body = ERB.new(File.read(controller)).result
  template_body = ERB.new(File.read(template)).result

  open("app/controllers/#{name.downcase()}.py", "w") do |f|
    f.write controller_body
  end
  Dir.mkdir("app/templates/#{name.downcase()}") unless File.exist?("app/templates/#{name.downcase()}")
  open("app/templates/#{name.downcase()}/index.html", "w") do |f|
    f.write template_body
  end

  puts "+ app/controllers/#{name.downcase()}.py"
  puts "+ app/templates/#{name.downcase()}/index.html"
else
  puts "usage: gmgen.rb controller helloworld"
end
