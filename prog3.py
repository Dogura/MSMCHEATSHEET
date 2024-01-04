import math

import pandas
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

classes = ['granite', 'diorite', 'marble', 'slate', 'limestone', 'breccia']
colums = ['RMCS', 'RMFX', 'AAPN']
p_val_barier = 0.05

#RMCS RMFX
#RMCS RMFX

#RMFX AAPN
#RMFX AAPN

#AAPN RMCS
#AAPN RMCS


# irq = q3- q1
# tmp = irq *1.5
# q1-tmp < hodnota < q3+tmp
def testoutlaier(val, q1, q3):
    irq = q3-q1
    tmp = irq*1.5
    if q1-tmp < val < q3+tmp:
        return False
    else:
        return True

def t_testCompare(k1, k2, param):
    t_val, p_val=st.ttest_ind(k1[param], k2[param])
    key1=0
    key2=0
    if p_val<p_val_barier:
        return False
    else:
        return True

    pass


def t_testCompare2D(k1, k2, param, param1,key1,key2):
    tmp11 = []
    for i in k1[param]:
        tmp11.append(i)
    tmp12 = []
    for i in k1[param1]:
        tmp12.append(i)

    tmpK1 = []
    for i in range(len(tmp11)):
        tmpK1.append([tmp11[i],tmp12[i]])

    tmp21 = []
    for i in k2[param]:
        tmp21.append(i)
    tmp22 = []
    for i in k2[param1]:
        tmp22.append(i)

    tmpK2 = []
    for i in  range(len(tmp21)):
        tmpK2.append([tmp21[i], tmp22[i]])


    plt.scatter(tmp11, tmp12, color='Blue')
    plt.scatter(tmp21, tmp22, color='Red')
    plt.xlabel(param)
    plt.ylabel(param1)
    t_val, p_val = st.ttest_ind(tmpK1, tmpK2)

    if (p_val[0] > p_val_barier) and (p_val[1] > p_val_barier):
        plt.legend(["Modré: " + str(key1), "Červené: " + str(key2)])
        plt.show()
        return True
    else:
        plt.cla()
        return False
    pass


def t_testCompare3d(k1, k2, param, param1, param2):
    tmp1 = []
    for i in k1[param]:
        tmp1.append(i)
    tmp2 = []
    for i in k1[param1]:
        tmp2.append(i)

    tmp3 = []
    for i in k1[param2]:
        tmp3.append(i)

    tmpK1 = []
    for i in range(len(tmp1)):
        tmpK1.append([tmp1[i], tmp2[i],tmp3[i]])

    tmp1 = []
    for i in k2[param]:
        tmp1.append(i)
    tmp2 = []
    for i in k2[param1]:
        tmp2.append(i)
    tmp3 = []
    for i in k2[param2]:
        tmp3.append(i)

    tmpK2 = []
    for i in range(len(tmp1)):
        tmpK2.append([tmp1[i], tmp2[i], tmp3[i]])

    t_val, p_val = st.ttest_ind(tmpK1, tmpK2)
    key1 = 0
    key2 = 0

    if (p_val[0] > p_val_barier) and (p_val[1] > p_val_barier) and (p_val[2] > p_val_barier):
        return True
    else:
        return False
    pass


def All_T_tests(graph):
    for i in range(len(graph)):
        k1 = graph[i]
        for j in range(i + 1, len(graph), 1):
            k2 = graph[j]
            for key in k1['Class']:
                key1 = key
                break
            for key in k2['Class']:
                key2 = key
                break
            if(key2 == key1):
                break
            if((t_testCompare(k1,k2,'RMCS'))):
                print("podle 1d testu atributu atributu RMCS jsou " + str(key1) + " a " + str(key2) + " stejné")

            if (t_testCompare(k1, k2, 'RMFX')):
                print("podle 1d testu atributu atributu RMFX jsou " + str(key1) + " a " + str(key2) + " stejné")

                pass
            if  (t_testCompare(k1, k2, 'AAPN')):
                print("podle 1d testu atributu atributu AAPN jsou " + str(key1) + " a " + str(key2) + " stejné")


            if (t_testCompare2D(k1,k2,'RMCS','RMFX',key1,key2)):
                print("podle 2d testu atributů RMCS a RMFX jsou " + str(key1) + " a " + str(key2) + " stejné")

            if (t_testCompare2D(k1, k2, 'RMFX','AAPN',key1,key2)):
                print("podle 2d testu atributů AAPN a RMFX jsou " + str(key1) + " a " + str(key2) + " stejné")

            if (t_testCompare2D(k1, k2, 'AAPN', 'RMCS',key1,key2)):
                print("podle 2d testu atributů AAPN a RMCS jsou " + str(key1) + " a " + str(key2) + " stejné")


            if((t_testCompare3d(k1,k2,'RMCS','RMFX','AAPN'))):
                print("podle 3d testu atributu všech atributů jsou " + str(key1) + " a " + str(key2) + " stejné")



def remove_outlaiers(graph, datas):
    outlaiers = {}
    for index, row in graph.iterrows():
        outlaiers[row['Code']] = []
        rmcs = float(row['RMCS'])
        rmfx = float(row['RMFX'])
        aapn = float(row['AAPN'])
        for data in datas:
            if (data['class'] == row['Class']) and (data['column'] =='RMCS'):
                rmcs_q1 = float(data['Q1'])
                rmcs_q3 = float(data['Q3'])
            elif (data['class'] == row['Class']) and (data['column'] =='RMFX'):
                rmfx_q1 = float(data['Q1'])
                rmfx_q3 = float(data['Q3'])
            elif (data['class'] == row['Class']) and (data['column'] =='AAPN'):
                aapn_q1 = float(data['Q1'])
                aapn_q3 = float(data['Q3'])

        outlaiers[row['Code']].append(testoutlaier(rmcs,rmcs_q1,rmcs_q3))
        outlaiers[row['Code']].append(testoutlaier(rmfx, rmfx_q1, rmfx_q3))
        outlaiers[row['Code']].append(testoutlaier(aapn, aapn_q1, aapn_q3))

    return outlaiers

    pass


def draw_boxPlots(graph,key):


    data_1 = graph[0][key]
    data_2 = graph[1][key]
    data_3 = graph[2][key]
    data_4 = graph[3][key]
    data_5 = graph[4][key]
    data_6 = graph[5][key]
    data = [data_1, data_2, data_3, data_4,data_5,data_6]

    plt.figure(figsize=(10, 7))
    plt.title(key)


    # Creating plot
    plt.boxplot(data, labels=classes)

    # show plot
    plt.show()


def print_hi():
    datas = list()
    graph = list()
    excel_data_df = pandas.read_excel('Rocks.xlsx', sheet_name='Data',
                                      usecols=['Code', 'Class', 'RMCS', 'RMFX', 'AAPN'])
    tmp = excel_data_df.copy()
    tmp = tmp.reset_index()

    for b in classes:
        data = excel_data_df[excel_data_df['Class'] == b]
        graph.append(data)
        for a in colums:
            class_dict = {
                'class': b,
                'column': a,
                'count': len(data),
                'mean': np.mean(data[a]),
                'stand': np.std(data[a]),
                'stand_error': (np.std(data[a] / np.sqrt(np.size(data[a])))),
                'Q1': np.percentile(data[a], 25),
                'Q3': np.percentile(data[a], 75),
                'normality': True if st.kstest(data[a], 'norm')[1] < 0.05 else False
            }
            datas.append(class_dict)

    #print(remove_outlaiers(tmp, datas))
    #colums = ['RMCS', 'RMFX', 'AAPN']
    draw_boxPlots(graph,'RMCS')
    draw_boxPlots(graph, 'RMFX')
    draw_boxPlots(graph, 'AAPN')
    All_T_tests(graph)









# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
