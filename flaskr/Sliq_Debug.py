from pprint import pprint
import itertools as it
import random


def datasets(dataset, percent):
    f = dataset.replace('\r\n','\n').split('\n')
    attr = {}

# banyak fitur
# id mengindekskan fitur
# length menyimpan banyak id
    attr['id'] = [x.split(':')[0] for x in f[0].split(',')]
    attr['type'] = [x.split(':')[1] for x in f[0].split(',')]
    attr['length'] = len(attr['id']) - 1
# flag mengandung nilai banyak data trainning
    flag = int(percent * (len(f)-1))

# f[1:] equalto *f
    data = [x.split(',') for x in f[1:] if len(x)>0]

#Parsing Data String to Int
    for itemIndex in range(len(data)):
        for attrIndex in range(attr['length']):
            if attr['type'][attrIndex] == 'n':
                data[itemIndex][attrIndex] = int(data[itemIndex][attrIndex])

# Mengacak Array Data
#     random.shuffle(data)
    return attr, data[:flag], data[flag:]

def presort(attr, dataset):
    print("-----------PreSort-----------")
    attrList = []
    attr['value'] = {}

    for attrIndex in range(attr['length']):
# all attribute combinations
        if attr['type'][attrIndex] == 'b':
            attr['value'][attrIndex] = ['yes']
        elif attr['type'][attrIndex] == 'n':
            attr['value'][attrIndex] = sorted(list(set([data[attrIndex] for data in dataset])))
        elif attr['type'][attrIndex] == 'c':
            attr['value'][attrIndex] = subset(list(set([data[attrIndex] for data in dataset])))
# sorted attribute lists

        currAttrList = []
        for dataIndex in range(len(dataset)):
            currAttrList.append([dataset[dataIndex][attrIndex], dataIndex])
        # attrList.append(sorted(currAttrList))

        # print("--",attrIndex,"--")
        # pprint(attr)
        attrList.append((currAttrList))

    return attrList, [[data[attr['length']],1] for data in dataset]

def subset(set):
    # mencari semua kombinasi kemungkinan dari c
    subset = []
    curset = []
    print("-----------SET-----------")
    pprint(set)
    # for i in range (len(set)):

    for value in set:
        curset.append(value)

    for i in range(2,len(set)):
        curset.append(list(it.combinations(set,i)))

    # for curset in range(curset):
        # subset.append(curset)
    # lenght = len(set)
    # for iteration in range(2**lenght):
    #     curset = []
    #     for digit in range(lenght):
            # if(iteration % 2):
            #     curset.append(set[digit])
            # iteration/=2
    # subset.append(curset)
    return curset

def generate_tree(attr, attrList, classList):#, middlestep):
    # print()
    tree = {}
    # INISIASI ROOT
    tree[1] = 'yes'
    # INISIASI QUEUE BFS
    queue = [[1]]
    dataNum = len(classList)
    turn = 1
# breath first search
    while queue:
        print("----------- iterasi:",turn,"-----------")
        turn+=1
        # MENGAMBIL URUTAN PALING AWAL

        tnode = queue.pop(0)

        node = tnode[0]

        used = tnode[1:]

        # if middlestep:
            # print_class(classList, node)
        # leaf terminates the split
        flag = is_leaf(classList, node)

        if flag != "split":
            tree[node] = flag
            continue
        # evaluate split


        minIndex, minValue, deadlock = evaluate_split(attr, attrList, classList, node, used)#middlestep, used)

        print("----------- min Index-----------")
        pprint(minIndex)

        print("----------- min Value-----------")
        pprint(minValue)

        print("----------- deadlock""----------- ")


        # print("evalate split", minIndex, minValue, deadlock)

        if minIndex == -1:
            continue
        # deadlock menghentikan plit
        if deadlock:
            tree[node] = deadlock
            continue

        left = len(tree) + 1
        right = left + 1
        # save to tree
        tree[node] = [tree[node], print_value(attr['id'][minIndex], attr['type'][minIndex], minValue), left, right,
                      minIndex, attr['type'][minIndex], minValue]


        tree[left] = 'yes'
        tree[right] = 'no'

        print("-----------TREE-----------")
        pprint(tree)

        # update node class id
        for item in range(dataNum):
            if classList[attrList[minIndex][item][1]][1] != node:
                continue
            if judge(attrList[minIndex][item][0], attr['type'][minIndex], minValue):
                classList[attrList[minIndex][item][1]][1] = left
            else:
                classList[attrList[minIndex][item][1]][1] = right

        print("-----------Class List-----------")
        pprint(classList)

        # add left and right node to queue
        qleft = [left]
        qright = [right]
        for item in used:
            qleft.append(item)
            qright.append(item)

        if minIndex not in used:
            qleft.append(minIndex)
            qright.append(minIndex)
        queue.append(qleft)
        queue.append(qright)

        print("-----------qleft-----------")
        # kelompok node, root
        pprint(qleft)
        print("-----------qright-----------")
        # kelompok node, root
        print(qright)

    return tree

# def print_class(classList, node):
# # print ('N'+str(node)+':')
#     for index in range(len(classList)):
#         if classList[index][1] == node:
#             1+1
# # print (str(index)+'\t|'+classList[index][0])

def is_leaf(classList, no):
    node = list(set([x[0] for x in classList if x[1]==no]))
    if len(node) != 1:
        return "split"
    else:
        return node[0] # yes/no


def evaluate_split(attr, attrList, classList, node, used): #middlestep, used):
    print("----------- EVALUATE -----------")

    dataNum= len(classList)
    minGini = 1
    minIndex = -1
    minValue = 0
    deadlock = False

    # looping untuk semua atribut
    for attrIndex in range(attr['length']):
        print("----------- Turn Attr",attrIndex,"-----------")

        # print(attrIndex , used)
        # Jika saat Loop bertemu
        minginitemp = 0


        if attrIndex in used:
            continue
        for value in attr['value'][attrIndex]:
            countLy = 0
            countLn = 0
            countRy = 0
            countRn = 0
            print("VALUE:", value)
            for item in range(dataNum):

                print("ITEM:", item, "NODE:", node)

                pprint(classList)

                if classList[attrList[attrIndex][item][1]][1] != node:
                    continue
                if judge(attrList[attrIndex][item][0], attr['type'][attrIndex], value):
                    if classList[attrList[attrIndex][item][1]][0] == 'yes':
                        # print("countLy +1")
                        # mencari banyak yes di sisi kiri
                        countLy += 1
                    else:
                        # print("countLn +1")
                        # mencari banyak nilai no di sisi kiri
                        countLn += 1
                else:
                    if classList[attrList[attrIndex][item][1]][0] == 'yes':
                        # print("countRy +1")
                        # mencari banyak nilai yes di kanan
                        countRy += 1
                    else:
                        # print("countRn +1")
                        # mencari banyak nilai no di kanan
                        countRn += 1
            # if middlestep:
            # print_histogram(node, print_value(attr['id'][attrIndex], attr['type'][attrIndex], value), countLy, countLn, countRy, countRn)

            minginitemp = minGini
            minidextemp = minIndex
            minValuetemp = minValue

            if gini(countLy, countLn, countRy, countRn) < minGini:
                minGini = gini(countLy, countLn, countRy, countRn)
                minValue = value
                minIndex = attrIndex

                print("MinValue:",minValuetemp," menjadi",minValue)
                print("GINI:",minginitemp," menjadi",minGini)
                print("MinIndex:",minidextemp," menjadi",minIndex)


                # deadlock berarti sampel tersebut memiliki nilai atribut yang sama tetapi bertentangan dalam klasifikasi
                deadlock = ((countLy*countLn>0) and (countRy+countRn)==0) or ((countRy*countRn>0) and (countLy+countLn)==0)
                if deadlock:
                    if countLy + countRy > countLn + countRn:
                        deadlock = 'yes'
                    else:
                        deadlock = 'no'
# free attrList

    return minIndex, minValue, deadlock

def print_value(name, attribute, value):
    if attribute == 'n':
        return str(name) + ' < ' + str(value)
    if attribute == 'c':
        return name + ' in {' + (',').join(value) + '}'
    if attribute == 'b':
        return name


def judge(data, attribute, value):
    # print("----------- JUDGE ----------- ")
    print("----------- Data:",data,"VALUE:",value,"-----------")

    if attribute == 'n':
        # true jika data lebih kecil dari nilai
        return data < value
    if attribute == 'c':
        # true jika data dalam value
        return data in value
    if attribute == 'b':
        # true jika data = yes
        return data == 'yes'

def gini(Ly, Ln, Ry, Rn):
    # print()
    L = Ly + Ln
    R = Ry + Rn
    # L dan R tidak nol
    if L:
        GL = (1.0-(float(Ly)/L)**2-(float(Ln)/L)**2)*L/(L+R)
    else:
        GL = 0
    if R:
        GR = (1.0-(float(Ry)/R)**2-(float(Rn)/R)**2)*R/(L+R)
    else:
        GR = 0
    # print("gini:", GL, GR)
    # print()
    return  GL + GR

# def print_histogram(node, value, countLy, countLn, countRy, countRn):
#     print ('N',node,' on ',value)
#     print ('\t|yes\t|no')
#     print ('L\t|'+str(countLy)+'\t|'+str(countLn))
#     print ('R\t|'+str(countRy)+'\t|'+str(countRn))

# def print_tree(tree, no, deep):
#     if tree[no] == 'yes' or tree[no] == 'no':
#         return
# print '-'*deep
    # left = tree[no][2]
    # right = tree[no][3]
    # if tree[left] == 'yes' or tree[left] == 'no':
    #     left = tree[left]
    # if tree[right] == 'yes' or tree[right] == 'no':
    #     right = tree[right]
    # node = '%d %s %s %s %s' %(no, tree[no][0], tree[no][1], str(left), str(right))
    # print (node)
    # print_tree(tree, tree[no][2], deep+1)
    # print_tree(tree, tree[no][3], deep+1)



def test_tree(tree, testData):
    length = len(testData)
    if not length:
        return 'Null'
    count = 0
    for data in testData:
        if test_node(tree, 1, data) == data[-1]:
            count += 1
    return float(count)/length

def test_node(tree, node, data):
    if tree[node] == 'yes':
        return 'yes'
    if tree[node] == 'no':
        return 'no'
    if judge(data[tree[node][4]], tree[node][5], tree[node][6]):
        return test_node(tree, tree[node][2], data)
    else:
        return test_node(tree, tree[node][3], data)





if __name__ == '__main__':
    with open('data_exercise_2.csv') as f:
        file = f.read()
    attr, trainData, testData = datasets(file, 0.7)

    print("-----------attr-----------")
    pprint(attr)

    print("-----------trainData-----------")
    pprint(trainData)

    attrList, classList = presort(attr, trainData)

    # middlestep = 0

    print("-----------Attr-----------")
    pprint(attr)

    print("-----------AttrList-----------")
    pprint(attrList)

    print("-----------ClassList-----------")
    pprint(classList)



    tree = generate_tree(attr, attrList, classList)# middlestep)
    print("-----------Fix Tree-----------")
    pprint(tree)



    testPerTra = test_tree(tree,trainData)
    testPerTes = test_tree(tree,testData)

    print("-----------TEST TRAIN-----------")
    print(testPerTra)

    print("-----------TEST TEST-----------")
    print(testPerTes)


