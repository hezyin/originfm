#!/usr/bin/env ruby

parameters = [] 

1.upto(6) do |i|
  1.upto(6) do |j|
    parameters << [16, i*0.001, j*0.001, 0.00002, 0.00002]
  end
end

total = parameters.size
start = Time.now

f = open("ptuner_ruby_log", "w+")

parameters.each_with_index do |p, i|
  f.puts "#{i+1}/#{total} k=#{p[0]} e1=#{p[1]} e2=#{p[2]} l1=#{p[3]} l2=#{p[4]} #{(Time.now - start)/60}mins"
  `../fm -k #{p[0]} -t 10 -s 8 -e1 #{p[1]} -e2 #{p[2]} -l1 #{p[3]} -l2 #{p[4]} -g k_#{p[0]}_e1_#{p[1]}_e2_#{p[2]}_l1_#{p[3]}_l2_#{p[4]} train.libfm test.libfm`
end

f.close

