fp = open('heximage', 'r')
data = fp.readline()
fp.close()

# print(data)

fp = open('out.ppm', 'w')

fp.write('P3\n280 22\n255\n')

i = 0
while i < len(data):
    print(data[i:i+2])
    fp.write(str(int(data[i:i+2], 16)) + ' ')
    i+=2
    fp.write(str(int(data[i:i+2], 16)) + ' ')
    i+=2
    fp.write(str(int(data[i:i+2], 16)) + '\n')
    i+=2
    

print(i)

fp.close()