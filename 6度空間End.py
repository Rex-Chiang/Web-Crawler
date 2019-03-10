import pymysql

conn=pymysql.connect(host='127.0.0.1',port=3306,user='Rex',passwd='Rex3893090',db='mysql',charset='utf8')
cur=conn.cursor()#建立游標物件
cur.execute('USE wikipedia')#'.execute'等同在MySQL中鍵入

class SolutionFound(RuntimeError):#RuntimeError關聯的值是一個字符串，指示出錯的地方。
    def __init__(self,message):
#        super(RuntimeError, self).__init__(message)#原本沒有這行
        self.message=message

def getLinks(fromPageId):
    cur.execute('SELECT toPageId FROM links WHERE fromPageId = %s',int(fromPageId))
    if cur.rowcount==0:
        return None
    else:
        return [x[0] for x in cur.fetchall()]#回傳一串列內容為toPageId，也就是傳入之fromPageId可連到的每個頁面id
    
def constructDict(currentPageId):
    links=getLinks(currentPageId)
    if links:#非空串列則回傳True
        return dict(zip(links,[{}]*len(links)))#zip參數為可迭代的資料型態，並回傳一串列將參數中的元素打包成一個個組
    return {}

def searchDepth(targetPageId,currentPageId,linkTree,depth):
    if depth==0:
        return linkTree
    if not linkTree:
        linkTree=constructDict(currentPageId)
    if not linkTree:#確認是否為空字典
        return{}
    if targetPageId in linkTree.keys():
        print('TARGET',str(targetPageId),'FOUND!!')
        raise SolutionFound('PAGE:'+str(currentPageId))#這裡拋出例外會跳回42行except
    #print('遞迴前',linkTree)
    for branchKey,branchValue in linkTree.items():
        #print(111)
        try:
            linkTree[branchKey]=searchDepth(targetPageId,branchKey,branchValue,depth-1)#由此遞迴下去
             
        except SolutionFound as e:
            #print(222)
            print(e.message)
            raise SolutionFound('PAGE:'+str(currentPageId))#這裡拋出例外若是在第3層遞迴會跳回第2層的42行except，
                                                           #若在第1層遞迴則會跳回53行except
    return linkTree
    

try:
    searchDepth(9,3,{},4)
    print('No solution found')
except SolutionFound as e:
    #print(333)
    print(e.message)