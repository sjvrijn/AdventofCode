# coding: utf-8
import numpy as np
shape = (25, 6)
with open('input8.txt') as f:
    img = np.array(list(map(int, next(f).strip()))).reshape((-1, 6, 25))
    
final_img = img[0]
for layer in img[1:]:
    indices = final_img == 2
    final_img[indices] = layer[indices]
    
import matplotlib.pyplot as plt
plt.imshow(final_img)
plt.savefig('8b.png')
plt.show()
