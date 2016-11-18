numLines = Dir["**/*.py"].map{|n|open(n).read.count("\n")+1}.inject(&:+)
numLines += Dir["**/*.js"].map{|n|open(n).read.count("\n")+1}.inject(&:+)
numLines += Dir["**/*.css"].map{|n|open(n).read.count("\n")+1}.inject(&:+)
numLines += Dir["**/*.html"].map{|n|open(n).read.count("\n")+1}.inject(&:+)
numLines += Dir["**/*.json"].map{|n|open(n).read.count("\n")+1}.inject(&:+)
numLines += Dir["**/*.java"].map{|n|open(n).read.count("\n")+1}.inject(&:+)

numImages = Dir["**/*.png"].length

puts "#{numLines} line#{numLines == 1 ? '' : 's'} of code"
puts "#{numImages} image#{numImages == 1 ? '' : 's'}"