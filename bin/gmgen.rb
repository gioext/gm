#!/usr/bin/env ruby

require 'erb'

if ARGV[0] == 'controller' && ARGV[1]
  unless File.exist?('app/controllers') && File.exist?('app/templates')
    puts "please execute root dir."
    exit
  end

  name = ARGV[1].capitalize

  if File.exist?("app/controllers/#{name.downcase}.py") || File.exist?("app/templates/#{name.downcase()}")
    puts "already exist #{name}"
    exit
  end

  dir = File.join(File.dirname(__FILE__), 'erb')
  controller = File.join(dir, 'controller.erb')
  template = File.join(dir, 'template.erb')
  controller_body = ERB.new(File.read(controller)).result
  template_body = ERB.new(File.read(template)).result

  Dir.mkdir("app/templates/#{name.downcase()}")
  open("app/controllers/#{name.downcase()}.py", "w") do |f|
    f.write controller_body
  end
  open("app/templates/#{name.downcase()}/index.html", "w") do |f|
    f.write template_body
  end

  puts "+ app/controllers/#{name.downcase()}.py"
  puts "+ app/templates/#{name.downcase()}/index.html"
elsif ARGV[0] == 'template' && ARGV[1]
  unless File.exist?('app/templates')
    puts "please execute root dir."
    exit
  end
  controller = ARGV[1].downcase
  action = ARGV[2].downcase
  if !File.exist?("app/templates/#{controller}")
    puts "no controller #{controller}"
    exit
  end
  if File.exist?("app/templates/#{controller}/#{action}.html")
    puts "already exist #{controller}/#{action}.html"
    exit
  end

  name = action
  dir = File.join(File.dirname(__FILE__), 'erb')
  template = File.join(dir, 'template.erb')
  template_body = ERB.new(File.read(template)).result

  open("app/templates/#{controller}/#{action}.html", "w") do |f|
    f.write template_body
  end

  puts "+ app/templates/#{controller}/#{action}.html"
else
  puts "usage: gmgen.rb controller helloworld"
end
