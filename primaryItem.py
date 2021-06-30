import tkinter as tk
from tkinter import ttk
import primaryStore as pStore
#####################################################################################
class primaryItem():
    def __init__(self,arg1):
        self.brandVal=None
        self.itemVal=None
        self.brandClick=None
        self.itemClick=None
        pStore.fileData.readItem()
        pStore.fileData.readItemStock()
        self.window=arg1
        self.listLabel = [('BRAND LIST :',80,30),('ITEM LIST :',330,30)]
        self.customize()

    def brandItemListRefresh(self):
        self.itemsList.listPopulate(pStore.fileData.returnItemList(self.brandVal)) #Populate Item Name List box

    def brandListRefresh(self):
        tmp=list(set([f[0] for f in list(pStore.fileData.itemList.values())]))
        if tmp is not None:
            tmp.sort()
        self.brandList.listPopulate(tmp) #Populate Item Name List box

    def selectBrandList(self,evt):
        w=evt.widget
        try:
            idx=int(w.curselection()[0])
            self.brandClick = w.get(idx)
            self.brandVal = self.brandClick
            pStore.fileData.printLog(' '*2 +'ITM3- Brand selected - ' + self.brandVal)
            self.brandItemListRefresh() #Function call does not work for some reason
        except:
            self.brandClick=None

    def customize(self):
        pStore.appLabel(self.window,self.listLabel)
        self.brandList=pStore.appListBox(self.window,[],[50,50])
        self.itemsList=pStore.appListBox(self.window,[],[300,50],[10,30])
        self.brandListRefresh()
        self.brandList.listObject.bind('<<ListboxSelect>>',self.selectBrandList)
#####################################################################################
class itemSearchPanel(primaryItem):
    def __init__(self,arg1,arg2=0):
        primaryItem.__init__(self,arg1)
        self.offset = arg2
        self.treeConfig = [
               [ "0",'stockId',50],
               [ "1",'Brand',100],
               [ "2",'Item Name',150],
               [ "3",'Model No',150],
               [ "4",'HSN Code',80],
               [ "5",'Size',80],
               [ "6",'Color',60],
               [ "7",'MRP',70],
               [ "8",'Stock Qty',60],
               [ "9",'Sold Qty',60],
               [ "10",'Buy Price',90],
               [ "11",'Piece Disc',90],
               [ "12",'Final Price',90],
               [ "13",'Total GST',90]]
        self.itemLabel=[('ITEM SEARCH PANEL',750,50),('ITEM NAME',650,80),('MDOEL NO',650,130),('HSN CODE',650,180)]
        self.itemEntry=[(750,80),(750,130),(750,180)]
        self.itemButton=[['SEARCH',[600,230],[1,10]],
                         ['SEARCH ALL',[700,230],[1,10]],
                         ['CLEAR',[800,230],[1,10]]]
        pStore.fileData.printLog('-'*10 +'ITM2- Item Search panel initiated'+'-'*10)
        self.customize()
        self.customize1()

    def customize1(self):
        self.itemsList.listObject.bind('<<ListboxSelect>>',self.selectItemList)

        self.itemObj=pStore.appTreeView(self.window,self.treeConfig,[50,350-self.offset])
        pStore.appLabel(self.window,self.itemLabel)
        self.itemSearchList=pStore.appEntrybox(self.window,self.itemEntry)
        obj=pStore.appButtons(self.window,self.itemButton)
        obj.returnList[0]['command']=self.searchItem
        obj.returnList[1]['command']=self.searchAll
        obj.returnList[2]['command']=self.resetValues

    def selectItemList(self,evt):
        w=evt.widget
        try:
            idx=int(w.curselection()[0])
            self.itemClick = w.get(idx)
            self.itemVal = self.itemClick
            pStore.fileData.printLog(' '*2 +'ITM4- Item selected' + self.itemVal)
            k=pStore.fileData.getItemKey([self.brandVal,self.itemVal])
            self.itemObj.setValues(pStore.fileData.itemTreeList(k))#Populate Item List Tree
        except:
            self.itemClick=None

    def searchAll(self):
        self.itemObj.setValues(pStore.fileData.itemTreeList())#Populate Item List Tree

    def resetValues(self):
        self.itemSearchList.setValues([''] * 3)

    def searchItem(self):
        vList=self.itemSearchList.getValues()
        firstSearch = True;cnt=1;tmp=[]
        for var in vList:
            if len(var) > 0:
                if firstSearch:
                    for k in [f for f in pStore.fileData.itemList.keys() if var.upper() in pStore.fileData.itemList[f][cnt]]:
                        tmp += pStore.fileData.itemTreeList(k)
                    firstSearch=False
                else:
                    for rec in tmp:
                        if rec[cnt+1] != var:
                            tmp.remove(rec)
            cnt += 1
            self.itemObj.setValues(tmp) #Populate Item List Tree
