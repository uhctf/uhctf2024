import cv2

img = cv2.imread('alfasmall.png', cv2.IMREAD_COLOR)

print(img.shape)
rows, cols, depth = img.shape

# cv2.imshow('', img)
# cv2.waitKey(0)

fp = open('data.h', 'w')

fp.write('static const unsigned char ImageData[] = {\n')

for i in range(rows):
    for j in range(cols):
        for k in range(depth):
            k = img[i,j,k]
            fp.write(str(hex(k)) + ',')
        fp.write('\n')

fp.write('\n};')

fp.close()

cv2.destroyAllWindows()