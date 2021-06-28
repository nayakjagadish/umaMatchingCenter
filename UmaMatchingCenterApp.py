import tkinter as tk
from tkinter import ttk
import primaryStore as pStore
import storeSupplier as sSupplier
import storeItem as sItem
import storeTransaction as sTrans
from datetime import datetime as dt
########################################################################
## Uma Store Primary Class creation
########################################################################
class transPortal():
    def __init__(self,arg1=None):
        self.appRoot=arg1
        self.treeConfig = [
               [ "0",'transId',100],
               [ "1",'Date',130],
               [ "2",'Item Count',70],
               [ "3",'Buy Price',90],
               #[ "4",'Tax Paid',90],
               [ "4",'Total MRP',90],
               [ "5",'Customer Discount',110],
               [ "6",'Customer Tax',110],
               [ "7",'Customer Price',110],
               [ "8",'Margin',90],
               [ "9",'Tax Payable',90]]

        self.trLabel=[('First Name',650,180),('Last Name',650,230),('Phone',650,280),('Month List',50,125),('Date List',350,125)]
        self.trEntry=[(750,180),(750,230),(750,280)]
        self.trButton=[ ['SEARCH',[600,330],[1,10]],
                        ['SEARCH ALL',[700,330],[1,10]],
                        ['CLEAR',[800,330],[1,10]],
                        ['ADD TRANSACTION',[400,380],[1,15]],
                        ['REFRESH',[200,380],[1,15]]]
        self.genericButtons=[
                        ['Supplier & Invoice MANAGEMENT',[50,30],[4,40]],
                        ['ITEM & STOCK MANAGEMENT',[370,30],[4,40]],
                        ['REPORT MANAGEMENT',[690,30],[4,40]],
                        ['SET FINANCIAL YEAR',[1000,30],[2,20]]]

        self.monthSelected=None
        self.dateSelected=None
        self.customize()

    def selectMonthList(self,evt):
        w=evt.widget
        try:
            idx=int(w.curselection()[0])
            self.monthSelected = w.get(idx)
            monthYear=pStore.fileData.getMonthYear(self.monthSelected)
            self.transObj.setValues(pStore.fileData.returnTransList(monthYear))
        except:
            pass

    def selectDateList(self,evt):
        w=evt.widget
        try:
            idx=int(w.curselection()[0])
            self.dateSelected = w.get(idx)
            if self.monthSelected is None:
                messagebox.showinfo('Uma Store','Select a Month/Year to Search transaction')
            else:
                varDate = pStore.fileData.getMonthYear(self.monthSelected) + str(self.dateSelected).rjust(2,'0')
                self.transObj.setValues(pStore.fileData.returnTransList(varDate))
        except:
            pass

    def searchAll(self):
        pass
        #self.transObj.setValues(pStore.fileData.getTop50()) #Populate Item List Tree

    def resetValues(self):
        self.trSearchList.setValues([''] * 3)

    def searchTrans(self):
        pass
        '''
        vList=self.trSearchList.getValues()
        firstSearch = True;cnt=1;tmp=[]
        for var in vList:
            if len(var) > 0:
                if firstSearch:
                    for k in [f for f in pStore.fileData.itemList.keys() if var in pStore.fileData.itemList[f][cnt]]:
                        tmp += pStore.fileData.itemTreeList(k)
                    firstSearch=False
                else:
                    for rec in tmp:
                        if rec[cnt+1] != var:
                            tmp.remove(rec)
            cnt += 1
            self.itemObj.setValues(tmp) #Populate Item List Tree
        '''
    def addTransactionRec(self):
        self.transaction_destroy()
        pStore.fileData.itemTransSync()
        obj=sTrans.addTransactions(self.appRoot)

    def refreshTree(self):
        self.transObj.setValues(pStore.fileData.returnTransList('{:%Y%m%d}'.format(dt.today())))

    def transactionTreeSel(self,event):
        curItem = self.transObj.tView.focus()
        self.transSelected=self.transObj.tView.item(curItem)['values'][0]
        self.transaction_destroy()
        pStore.fileData.itemTransSync()
        obj=sTrans.addTransactions(self.appRoot,self.transSelected,False)

    def openItemStockPage(self):
        sWindow = pStore.childFrame(self.appRoot,'Uma Store Brand and Item Frame')
        obj=sItem.brandItemWindow(sWindow.childRoot)
        pStore.fileData.printLog('Item and Stock management page is opened')

    def openSupplierPage(self):
        sWindow = pStore.childFrame(self.appRoot,'Uma Store Supplier and Invoice Frame')
        obj=sSupplier.supplierWindow(sWindow.childRoot)
        pStore.fileData.printLog('Supplier & Invoice page is opened')

    def setFinanceYear(self):
        idx=pStore.fileData.returnFYidx(self.FYselected.getValue())
        if idx != -1:
            pStore.fileData.readConfig()
            pStore.fileData.config['FYIDX'] = int(idx)
            pStore.fileData.updateConfig()
        pStore.fileData.setClassFiles()
        self.FYselected.dropObject['state'] = tk.DISABLED
        pStore.fileData.printLog('Financial Year modified to - ')

    def transaction_destroy(self):
        self.monthList.destroy()
        self.dateList.destroy()
        self.transLbl.destroy()
        self.trSearchList.destroy()
        self.transObj.destroy()
        self.transBtn.destroy()

    def customize(self):
        if __name__ == '__main__':
            self.appRoot = tk.Tk()
            self.appRoot.title("Uma Store Billing App")
            self.appRoot.geometry('1100x650')

            self.FYval=tk.StringVar()
            self.FYselected = pStore.appDropDown(self.appRoot,self.FYval,[t[0] for t in pStore.fileData.FYarray],[1000,80,20,pStore.fileData.getConfigId('FYIDX',0)],True)
            pStore.fileData.setClassFiles()
            pStore.fileData.printLog('Financial Year for this session is - ')
            
            obj=pStore.appButtons(self.appRoot,self.genericButtons)
            obj.returnList[0]['command']=self.openSupplierPage   #OPEN ITEM & STOCK MANAGEMENT PAGE
            obj.returnList[1]['command']=self.openItemStockPage #OPEN TRANSACTION & CUSTOMER MANAGEMENT PAGE
            #obj.returnList[2]['command']=self.openReportPage     #ADD REPORT MANAGEMENT PAGE
            obj.returnList[3]['command']=self.setFinanceYear      #SET FINANCIAL YEAR

        pStore.fileData.readTransactions()
        self.monthList=pStore.appListBox(self.appRoot,pStore.fileData.returnMonthList(),[50,150])
        self.dateList=pStore.appListBox(self.appRoot,range(1,31),[350,150])
        self.monthList.listObject.bind('<<ListboxSelect>>',self.selectMonthList)
        self.dateList.listObject.bind('<<ListboxSelect>>',self.selectDateList)
        self.transObj=pStore.appTreeView(self.appRoot,self.treeConfig,[50,450])
        self.refreshTree()
        self.transObj.tView.bind('<Double-1>',self.transactionTreeSel)
        
        self.transLbl = pStore.appLabel(self.appRoot,self.trLabel)
        self.trSearchList = pStore.appEntrybox(self.appRoot,self.trEntry)
        self.transBtn = pStore.appButtons(self.appRoot,self.trButton)
        self.transBtn.returnList[0]['command']=self.searchTrans
        self.transBtn.returnList[1]['command']=self.searchAll
        self.transBtn.returnList[2]['command']=self.resetValues
        self.transBtn.returnList[3]['command']=self.addTransactionRec
        self.transBtn.returnList[4]['command']=self.refreshTree
        self.appRoot.mainloop()

if __name__ == '__main__':
    transPortal()
