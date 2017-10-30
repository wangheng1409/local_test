#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image
from pylab import *
from numpy import *
import os
def process_image(imagename,resultname,params="--edge-thresh 10 --peak-thresh 5"):
    """ 处理一幅图像，然后将结果保存在文件中"""
    if imagename[-3:] != 'pgm':
        print (imagename,1)
    # 创建一个pgm 文件
        im = Image.open(imagename).convert('L')
        im.save('tmp.pgm')
        imagename = 'tmp.pgm'
    cmmd = str("sift "+imagename+" --output="+resultname+
    " "+params)
    os.system(cmmd)
    print ('processed', imagename, 'to', resultname)

def write_features_to_file(filename,locs,desc):
    """ 将特征位置和描述子保存到文件中"""
    savetxt(filename,hstack((locs,desc)))

def plot_features(im,locs,circle=False):
    """ 显示带有特征的图像
    输入：im（数组图像），locs（每个特征的行、列、尺度和朝向）"""
    def draw_circle(c,r):
        t = arange(0,1.01,.01)*2*pi
        x = r*cos(t) + c[0]
        y = r*sin(t) + c[1]
        plot(x,y,'b',linewidth=2)
        imshow(im)
    if circle:
        for p in locs:
            draw_circle(p[:2],p[2])
    else:
        plot(locs[:,0],locs[:,1],'ob')
    axis('off')

def read_features_from_file(filename):
    """ 读取特征属性值，然后将其以矩阵的形式返回"""
    f = loadtxt(filename)
    return f[:,:4],f[:,4:] # 特征位置，描述子

def match(desc1,desc2):
    """ 对于第一幅图像中的每个描述子，选取其在第二幅图像中的匹配
    输入：desc1（第一幅图像中的描述子），desc2（第二幅图像中的描述子）"""
    desc1 = array([d / linalg.norm(d) for d in desc1])
    desc2 = array([d / linalg.norm(d) for d in desc2])
    dist_ratio = 0.6
    desc1_size = desc1.shape
    matchscores = zeros((desc1_size[0], 1), 'int')
    desc2t = desc2.T  # 预先计算矩阵转置
    for i in range(desc1_size[0]):
        dotprods = dot(desc1[i, :], desc2t)  # 向量点乘
        dotprods = 0.9999 * dotprods
        # 反余弦和反排序，返回第二幅图像中特征的索引
        indx = argsort(arccos(dotprods))
        # 检查最近邻的角度是否小于dist_ratio 乘以第二近邻的角度
        if arccos(dotprods)[indx[0]] < dist_ratio * arccos(dotprods)[indx[1]]:
            matchscores[i] = int(indx[0])
    return matchscores

def match_twosided(desc1,desc2):
    """ 双向对称版本的match()"""
    matches_12 = match(desc1,desc2)
    matches_21 = match(desc2,desc1)
    ndx_12 = matches_12.nonzero()[0]
    # 去除不对称的匹配
    for n in ndx_12:
        if matches_21[int(matches_12[n])] != n:
            matches_12[n] = 0
    return matches_12


def appendimages(im1,im2):
    """ 返回将两幅图像并排拼接成的一幅新图像"""
    # 选取具有最少行数的图像，然后填充足够的空行
    rows1 = im1.shape[0]
    rows2 = im2.shape[0]
    if rows1 < rows2:
        im1 = concatenate((im1,zeros((rows2-rows1,im1.shape[1]))),axis=0)
    elif rows1 > rows2:
        im2 = concatenate((im2,zeros((rows1-rows2,im2.shape[1]))),axis=0)
    # 如果这些情况都没有，那么它们的行数相同，不需要进行填充
    return concatenate((im1,im2), axis=1)

def plot_matches(im1,im2,locs1,locs2,matchscores,show_below=True):
    """ 显示一幅带有连接匹配之间连线的图片
    输入：im1，im2（数组图像），locs1，locs2（特征位置），matchscores（match() 的输出），
    show_below（如果图像应该显示在匹配的下方）"""
    im3 = appendimages(im1,im2)
    if show_below:
        im3 = vstack((im3,im3))
    imshow(im3)
    cols1 = im1.shape[1]
    for i,m in enumerate(matchscores):
        if m>0:
            plot([locs1[i][1],locs2[m][1]+cols1],[locs1[i][0],locs2[m][0]],'c')
    axis('off')
