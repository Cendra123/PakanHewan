from pprint import pprint

if __name__ == '__main__':
    Array ={1: ['yes', 'pos_det in {r,i,g,h,t,_,u,p}', 2, 3, 7, 'c', 'right_up'], 2: 'yes', 3: 'no'}
    # pprint(Array)

    tree = []
    mappedArr = [[]]

    for i in Array:
        # i merupakan index of array
        # pprint(Array[i])
        arrayElem = Array[i]
        mappedArr[i][0] = arrayElem
        mappedArr[i][1] = []

    pprint(mappedArr)
    # for id in mappedArr:
    #     if(mappedArr.hasattr(id)):
    #         mappedElem = mappedArr[id]
    #
    #         pprint(mappedElem)
            # if(mappedElem):