class Manipulation():
    @staticmethod
    def parserList(list):
        newList = []
        print(list)
        for li in list:
            if ',' in li:
                li = li.replace(',', '')
            if '+' in li:
                li = li[:-1]
            newList.append(li)
        return newList

    @staticmethod
    def splitAndCheckNum(list_: list):
        newList = []
        for i in list_:
            splt = str(i).split('-')
            if len(splt) == 2:
                newList.append(splt[1])
            if len(splt) == 1:
                newList.append(splt[0])
        return newList

    @staticmethod
    def getAvarage(floatList):
        try:
            avarage = (sum(floatList) / len(floatList)) / 2
            return avarage
        except ZeroDivisionError:
            return 0
    @staticmethod
    def linkParser(linkList):
        newList = []
        for li in linkList:
            li2 = str(li).split('/')
            if 'view' in li2  :
                newList.append(li)
        return newList

    @staticmethod
    def toFloat(list_):
        floatList = []
        for li in list_:
            try:
                li = float(li)
                floatList.append(li)
            except:
                continue
        return floatList

    @staticmethod
    def splitSearchItem(search):
        list = str(search).split()
        result = '+'.join(list).strip()
        return result


