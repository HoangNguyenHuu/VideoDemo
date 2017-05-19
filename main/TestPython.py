a = "/home/hoangnh/Downloads/Bitcoin.mp4"

start = a.rfind('/')
end = a.find('.')
print start
print end

s = a[start+1:end]
print s