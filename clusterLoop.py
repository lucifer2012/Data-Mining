import csv
import numpy as np
from sklearn import datasets, linear_model
import math

# regs返回模型的斜率以及截距
def regs(datagroup):
    charge = []
    poverty = []
    for i in range(1, len(whole)):
        if whole[i][7] != 'what' and whole[i][4] in datagroup:
            charge.append([float(whole[i][6])])
            poverty.append(float(whole[i][8]))
    regr = linear_model.LinearRegression()
    regr.fit(charge, poverty)
    return regr.coef_[0], regr.predict(0)[0]

def kmeans():
    #这一部分是读入数据
    #     whole = []
    #     with open('hospitalLevels.csv', 'rb') as csvfile:
    #         reader = csv.reader(csvfile)
    #         for row in reader:
    #             whole.append(row)
    
    #初步定义五个地区
    west = ['AK', 'CA', 'CO', 'HI', 'ID', 'MT', 'NV', 'OR', 'UT', 'WA', 'WY']
    midwest = ['ND', 'SD', 'NE', 'KS', 'MN', 'IA', 'MO', 'WI', 'IL', 'IN', 'MI', 'OH']
    southwest = ['NM', 'AZ', 'OK', 'TX']
    southeast = ['AR', 'LA', 'MS', 'AL', 'TN', 'KY', 'GA', 'FL', 'WV', 'VA']
    northeast = ['CT', 'DE', 'ME', 'MD', 'MA', 'NH', 'NH', 'NY', 'PA', 'RI', 'VT']
    
    #sort一下
    west.sort()
    midwest.sort()
    southwest.sort()
    southeast.sort()
    northeast.sort()
    
    #初步定义斜率和截距
    west_coef, west_incept = 0, 0
    midwest_coef, midwest_incept = 0, 0
    southeast_coef, southeast_incept = 0, 0
    northeast_coef, northeast_incept = 0, 0
    southwest_coef, southwest_incept = 0, 0
    
    #loop 开始条件
    flag = 1
    
    while(flag):
        #初始化模型中所有州到该regression的距离价格 初始值设置为0
        westdata = dict()
        midwestdata = dict()
        southeastdata = dict()
        northeastdata = dict()
        southwestdata = dict()
        allstates = west + midwest + southwest + southeast + northeast
        for state in allstates:
            westdata[state] = 0
            midwestdata[state] = 0
            southeastdata[state] = 0
            northeastdata[state] = 0
            southwestdata[state] = 0
        
        # 如果在新产生的数据中某个地区的州数为0 则保留原有的模型 并用原有的模型去做计算
        if len(west) != 0:
            west_coef, west_incept = regs(west)
        if len(midwest) != 0:
            midwest_coef, midwest_incept = regs(midwest)
        if len(southeast) != 0:
            southeast_coef, southeast_incept = regs(southeast)
        if len(northeast) != 0:
            northeast_coef, northeast_incept = regs(northeast)
        if len(southwest) != 0:
            southwest_coef, southwest_incept = regs(southwest)
        
        # row[4] 为州的缩写 这里计算同一个州的医院到所有模型的距离
        for row in whole:
            if row[4] in westdata.keys():
                westdata[row[4]] += abs(float(row[6]) * west_coef - float(row[8]) + west_incept) / math.sqrt(float(west_coef) ** 2 + 1)
                midwestdata[row[4]] += abs(float(row[6]) * midwest_coef - float(row[8]) + midwest_incept) / math.sqrt(float(midwest_coef) ** 2 + 1)
                southeastdata[row[4]] += abs(float(row[6]) * southeast_coef - float(row[8]) + southeast_incept) / math.sqrt(float(southeast_coef) ** 2 + 1)
                northeastdata[row[4]] += abs(float(row[6]) * northeast_coef - float(row[8]) + northeast_incept) / math.sqrt(float(northeast_coef) ** 2 + 1)
                southwestdata[row[4]] += abs(float(row[6]) * southwest_coef - float(row[8]) + northeast_incept) / math.sqrt(float(southwest_coef) ** 2 + 1)
        # 新的clusters
        new_west = []
        new_midwest = []
        new_southwest = []
        new_northwest = []
        new_southeast = []
        # 根据总距离最小值分配州到模型
        for key in westdata.keys():
            tmp = [westdata[key], midwestdata[key], southeastdata[key], northeastdata[key], southwestdata[key]]
            idx = tmp.index(min(tmp))
            if idx == 0:
                new_west.append(key)
            elif idx == 1:
                new_midwest.append(key)
            elif idx == 2:
                new_southeast.append(key)
            elif idx == 3:
                new_northwest.append(key)
            else:
                new_southwest.append(key)
        new_west.sort()
        new_midwest.sort()
        new_southwest.sort()
        new_northwest.sort()
        new_southeast.sort()
        # 如果新的cluster与旧的cluster一样 则终止loop；否则用新的cluster覆盖原始cluster
        if (west == new_west and midwest == new_midwest and southeast == new_southeast and southwest == new_southwest and northeast == new_northwest):
            flag = 0
        else:
            west = new_west
            midwest = new_midwest
            southeast = new_southeast
            southwest = new_southwest
            northeast = new_northwest
    #输出结果
    print "west includes:", west
    print "midwest includes:", midwest
    print "southeast includes:", southeast
    print "northeast includes:", northeast
    print "southwest includes:", southwest
