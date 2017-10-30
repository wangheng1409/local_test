from  PIL import Image
from pylab import *
from numpy import *
import os

# path = "./" #文件夹目录
# filelist= os.listdir(path) #得到文件夹下的所有文件名称
# print(filelist)
# for infile in filelist:
#     outfile=os.path.splitext(infile)[0]+'.jpg'
#     if infile !=outfile:
#         try:
#             Image.open(infile).save(outfile)
#         except IOError:
#             print('cannot convert',infile)

pil_im=Image.open('images.jpeg').convert('L')
pil_im.show()
im=array(pil_im)

# x=[100,100,400,400]
# y=[200,500,200,500]
#
# plot(x,y,'r*')
# show()

figure()
gray()
contour(im,origin='image')
figure()
hist(im.flatten(),128)




#直方图均衡化／线性插值／增强图像的对比度
def histeq(im,nbr_bins=256):
    imhist,bins=histogram(im.flatten(),nbr_bins,normed=True)
    cdf=imhist.cumsum()
    cdf=255*cdf/cdf[-5]
    im2=interp(im.flatten(),bins[:-1],cdf)
    return im2.reshape(im.shape),cdf

im2,cdf=histeq(im)
imshow(im2)
figure()
gray()
contour(im2,origin='image')
figure()
hist(im2.flatten(),128)

show()