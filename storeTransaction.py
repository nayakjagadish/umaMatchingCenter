import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime as dt

#custom module imports
import primaryStore  as pStore
import primaryItem   as pItem
import storeSupplier as sSupplier
import storeItem     as sItem
import UmaMatchingCenterApp as umaMain
#####################################################################################
class addTransactions():
    def __init__(self,arg1,arg2=-1,arg3=True):
        self.window  = arg1
        self.transNum=arg2
        self.is_NewTrans = arg3
        self.tempItemList={};self.transCounter=1;self.offSet = 0;self.itemVal = None;self.modifiedList={}
        self.transLabels=[('Customer Name :',50,150),
                            ('Transaction number :',400,150),
                            ('Transaction Date :',750,150),
                            ('Number of Items :',70,460),
                            ('Total Discount :',300,460),
                            ('Total price :',70,500),
                            ('Price after discount :',300,500),
                            ('Total Tax :',600,460),
                            ('Total Buy Price :',600,500),
                            ('Total MRP ',70,560),
                            ('Total Item Discount :',70,600),
                            ('Discount % :',300,560),
                            ('Discount Amount :',300,600),
                            ('CGST Applicable :',600,560),
                            ('SGST Applicable :',600,600),
                            ('Final Price Payable :',200,650), 
                            ('Amount paid by Customer :',430,650)]
        self.transEntry=[(170,150,30,1), (520,150,15,1),(870,150,18,1),
                         (200,460,10,1),(200,500,12,1),
                         (450,460,10,1),(450,500,12,1),
                         (700,460,10,1),(700,500,12,1),
                         (200,560,12,1),(200,600,12,1),
                         (450,560,12),  (450,600,12),
                         (700,560,12,1),(700,600,12,1),
                         (330,650,12),  (600,650,12)]
        self.transTreeConfig = [
                ["0",'Sl#',30],
                ["1",'Brand',100],
                ["2",'Item Name',100],
                ["3",'Model',90],
                ["4",'HSN',80],
                ["5",'Size',60],
                ["6",'Color',80],
                ["7",'Qty',40],
                ["8",'MRP',60],
                ["9",'Unit Price',80],
                ["10",'Discount',80],
                ["11",'Total Tax',80],
                ["12",'Final Price',80],
                ["13",'Customer Paid',100],
                ["14",'Margin',60],
                ["15",'GST payable',80]]
        self.addItemLabels=[('Brand :',600,50),
                            ('Item :' ,800,50),
                            ('Model :',600,100),
                            ('HSN :'  ,800,100),
                            ('Size :' ,600,150),
                            ('Quantity :',600,200),
                            ('Discount Type :' ,600,250),
                            ('Color :' ,900,250)]
        self.addItemEntry=[(650,50,10,1),(850,50,10,1),(650,100,10,1),(850,100,10,1)]
        self.addTransButtons=[['ADD ITEM',[800,450],[4,12]],
                              ['SAVE',[930,450],[4,12]],
                              ['BACK',[1060,450],[4,12]],
                              ['PRINT RECEIPT',[800,550],[4,12]],
                              ['SAVE & CLOSE',[930,550],[4,12]],
                              ['FULL PAYMENT',[680,640],[2,12]]]
        self.vSize=[['Standard'],
                    ['X-Small','Small','Medium','Large','X-Large','DoubleXL'],
                    ['30CM','32CM','34CM','36CM','38CM','40CM','42CM'],
                    ['75CM','80CM','85CM','90CM','95CM','100CM']]
        self.qtyUnit = { 'PIECE' : 1, '5P BOX' : 5,'10P BOX' : 10,'20P BOX' : 20, 'DOZEN' : 12}
        self.discType = ['Disc %','Disc Amount']
        self.colorOpt = ['NO','YES']
        self.customize()

    def transStockTreeSel(self,event):
        curItem = self.itemPage.itemObj.tView.focus()
        self.tItemSelected=self.itemPage.itemObj.tView.item(curItem)['values'][0]

    def backTransPortal(self):
        self.newEntry_destroy()
        umaMain.transPortal(self.window)

    def saveCloseTransaction(self):
        self.finalTransactionEntry()
        self.newEntry_destroy()
        umaMain.transPortal(self.window)

    def writeReceipt(self):
        self.finalTransactionEntry()
        pStore.fileData.receiptPrint(self.transNum)

    def finalTransactionEntry(self):
        transRec=self.transInfo.getValues()
        if pStore.fileData.fConvert(transRec[15]) != 0:
            transRec[16] = transRec[15]
        self.transInfo.setValues(transRec)
        self.refreshTransItemTree()
        pStore.fileData.adjustStockTrans(self.transNum,self.modifiedList)
        pStore.fileData.receiptWrite(self.transNum)

    def refreshTransItemTree(self):
        transRec=self.transInfo.getValues()
        transRec=transRec[0:3] + [0] * 8 + transRec[11:13] + [0] * 3 + [transRec[16]]
        for idx in self.tempItemList:
            rec=self.tempItemList[idx]
            transRec[3] += pStore.fileData.fConvert(rec[11])  #Total Quantity
            transRec[4] += pStore.fileData.fConvert(rec[11]) * pStore.fileData.fConvert(rec[7]) 
            transRec[5] += pStore.fileData.fConvert(rec[11]) * pStore.fileData.fConvert(rec[8])
            transRec[6] = transRec[4] - transRec[5]
            transRec[7] += pStore.fileData.fConvert(rec[11]) * pStore.fileData.fConvert(rec[9])
            transRec[8] += pStore.fileData.fConvert(rec[11]) * pStore.fileData.fConvert(rec[10])

            transRec[9]  += pStore.fileData.fConvert(rec[12])
            transRec[10] += pStore.fileData.fConvert(rec[14])
            transRec[13] += pStore.fileData.fConvert(rec[15])
            transRec[14] += pStore.fileData.fConvert(rec[16])
            transRec[15] += pStore.fileData.fConvert(rec[17])

        transRec[5] = round(transRec[5],2)
        transRec[6] = round(transRec[6],2)
        transRec[7] = round(transRec[7],2)
        transRec[8] = round(transRec[8],2)
        
        if pStore.fileData.fConvert(transRec[16]) != 0:
            if pStore.fileData.fConvert(transRec[16]) >  pStore.fileData.fConvert(transRec[9]):
                messagebox.showinfo('Uma Store','Payment amount cannot be greater than Total MRP amount',parent=self.itemChildObj)
            else:
                transRec[15] = pStore.fileData.fConvert(transRec[16])
                transRec[13] = self.calculateTax(pStore.fileData.fConvert(transRec[16]))
                transRec[14] = self.calculateTax(pStore.fileData.fConvert(transRec[16]))
                transRec[12] = transRec[9] - transRec[10] - transRec[15]
                transRec[11] = round((transRec[12] * 100) / (transRec[9] - transRec[10]),2)
        else:
            if pStore.fileData.fConvert(transRec[11]) != 0:
                transRec[12] = round((transRec[9] - transRec[10]) * pStore.fileData.fConvert(transRec[11]) / 100,2)
                transRec[13] = self.calculateTax(transRec[9] - transRec[10] - transRec[12])
                transRec[14] = self.calculateTax(transRec[9] - transRec[10] - transRec[12])
                transRec[15] = transRec[9] - transRec[10] - transRec[12]
            else:
                if pStore.fileData.fConvert(transRec[12]) != 0:
                    transRec[11] = round((transRec[12] * 100) / (transRec[9] - transRec[10]),2)
                    transRec[13] = self.calculateTax(transRec[9] - transRec[10] - transRec[12])
                    transRec[14] = self.calculateTax(transRec[9] - transRec[10] - transRec[12])
                    transRec[15] = transRec[9] - transRec[10] - transRec[12]

        transRec[15] = round(transRec[15],2)
        self.transInfo.setValues(transRec)
        self.populateItemTree()
        pStore.fileData.addNewTransaction(transRec,self.tempItemList)
        pStore.fileData.adjustStockTrans(self.transNum,self.modifiedList)

    def populateItemTree(self):
        tmp = []
        for idx in self.tempItemList:
            rec=self.tempItemList[idx]
            tmp.append([idx]+ rec[:6] + [rec[11],rec[6],rec[10]] + [rec[14],pStore.fileData.fConvert(rec[15])+pStore.fileData.fConvert(rec[16]),rec[17],rec[18],
                                        round(pStore.fileData.fConvert(rec[17]) - pStore.fileData.fConvert(rec[15]) - pStore.fileData.fConvert(rec[16]) - pStore.fileData.fConvert(rec[11]) * pStore.fileData.fConvert(rec[10]),2),
                                        pStore.fileData.fConvert(rec[15]) + pStore.fileData.fConvert(rec[16]) - pStore.fileData.fConvert(rec[11]) * pStore.fileData.fConvert(rec[9]) ])
        self.transObj.setValues(tmp) # populate tree on transaction item page

    def saveClosetItem(self):
        tmp=self.transCalculate()
        k=0;i=-1
        if len(tmp) > 0:
            for rec in self.tempItemList.keys():
                if self.tempItemList[rec][:7] == tmp[:7]:
                    i = rec
            if i == -1:
                self.tempItemList[self.transCounter] = tmp
                self.transCounter += 1
            else:
                self.tempItemList[i][11] = pStore.fileData.fConvert(self.tempItemList[i][11]) + pStore.fileData.fConvert(tmp[11])
                self.tempItemList[i][12] = pStore.fileData.fConvert(self.tempItemList[i][12]) + pStore.fileData.fConvert(tmp[12])
                self.tempItemList[i][14] = pStore.fileData.fConvert(self.tempItemList[i][14]) + pStore.fileData.fConvert(tmp[14])
                self.tempItemList[i][15] = pStore.fileData.fConvert(self.tempItemList[i][15]) + pStore.fileData.fConvert(tmp[15])
                self.tempItemList[i][16] = pStore.fileData.fConvert(self.tempItemList[i][16]) + pStore.fileData.fConvert(tmp[16])
                self.tempItemList[i][17] = pStore.fileData.fConvert(self.tempItemList[i][17]) + pStore.fileData.fConvert(tmp[17])
                self.tempItemList[i][18] = pStore.fileData.fConvert(self.tempItemList[i][18]) + pStore.fileData.fConvert(tmp[18])
                self.tempItemList[i][13] = round(pStore.fileData.fConvert(self.tempItemList[i][14]) * 100 / pStore.fileData.fConvert(self.tempItemList[i][18]),2)
        self.refreshTransItemTree()
        self.newWin.withdraw()

    def calculateTax(self,vAmount):
        vCost = round(vAmount / 1.05,2)
        return round(vCost * 0.025,2)

    def transCalculate(self):    #Save Transaction Item
        tmp=[]
        transRec = self.tItemInfo.getValues()
        if self.tItemSelected == 0:
            messagebox.showinfo('Uma Store','Please Select an Item from the stock list !!',parent=self.itemChildObj)
        else:
            if pStore.fileData.fConvert(transRec[0]) == 0:
                messagebox.showinfo('Uma Store','Please input Buy Quantity !!',parent=self.itemChildObj)
            else:
                stockRec = pStore.fileData.itemStockList[str(self.tItemSelected)]
                vItem = pStore.fileData.itemList[stockRec[0]]
                #stockRec = pStore.fileData.getItemStock(str(self.tItemSelected))
                transRec[1] = pStore.fileData.fConvert(transRec[0]) * pStore.fileData.fConvert(stockRec[3]) #Total MRP
                if pStore.fileData.fConvert(transRec[7]) != 0:
                    if pStore.fileData.fConvert(transRec[7]) > transRec[1] :
                        messagebox.showinfo('Uma Store','Amount cannot be greater than Total MRP amount',parent=self.itemChildObj)
                    else:
                        transRec[6]=transRec[7] #Final Price
                        transRec[5] = self.calculateTax(pStore.fileData.fConvert(transRec[7]))
                        transRec[4] = self.calculateTax(pStore.fileData.fConvert(transRec[7]))
                        transRec[3] = transRec[1] - pStore.fileData.fConvert(transRec[7]) #Discount amount
                        transRec[2] = round(transRec[3] * 100 / transRec[1],2) #Discount %
                else:
                    if pStore.fileData.fConvert(transRec[2]) != 0:
                        if pStore.fileData.fConvert(transRec[2]) > 90:
                            messagebox.showinfo('Uma Store','Enter a valid Discount percentage !!',parent=self.itemChildObj)
                        else:
                            transRec[3] = round(pStore.fileData.fConvert(transRec[2]) * transRec[1] / 100,2)
                            transRec[4] = self.calculateTax(transRec[1] - transRec[3])
                            transRec[5] = self.calculateTax(transRec[1] - transRec[3])
                            transRec[6] = transRec[1] - transRec[3]
                    else:
                        if pStore.fileData.fConvert(transRec[3]) != 0:
                            transRec[2] = round(pStore.fileData.fConvert(transRec[3]) * 100 / transRec[1],2)
                            transRec[4] = self.calculateTax(transRec[1] - pStore.fileData.fConvert(transRec[3]))
                            transRec[5] = self.calculateTax(transRec[1] - pStore.fileData.fConvert(transRec[3]))
                            transRec[6] = transRec[1] - pStore.fileData.fConvert(transRec[3])
                        else:
                            transRec[2] =0
                            transRec[3] =0
                            transRec[4] = self.calculateTax(transRec[1])
                            transRec[5] = self.calculateTax(transRec[1])
                            transRec[6] = transRec[1]
                tmp = vItem + stockRec[1:4] + stockRec[6:10] + transRec + [stockRec[0]]
        #transRec[6] = round(transRec[6],2)
        self.tItemInfo.setValues(transRec)
        return tmp

    def addItemInfo(self):
        pStore.fileData.readItem()
        pStore.fileData.readItemStock()
        self.tItemSelected=0
        self.itmLabels=[('Buy Quantity :',50,550),
                        ('Total MRP :',250,550),
                        ('Disc % :',450,550),
                        ('Disc Amount :',650,550),
                        ('SGST (2.5%) :',50,600),
                        ('CGST (2.5%) :',250,600),
                        ('Final Price :',450,600),
                        ('Paid by Customer :',650,600)]

        self.addTItemButtons=[['SAVE',[880,550],[4,8]],
                              ['SAVE & CLOSE',[980,550],[4,12]]]

        self.tItemEntry=[(140,550,8),(320,550,10,1),(500,550,10),(740,550,10),
                         (140,600,10,1),(340,600,10,1),(530,600,12,1),(760,600,10)]
        
        self.newWin=pStore.fileData.createChild(self.window,'Add purchased Item')
        self.itemPage = pItem.itemSearchPanel(self.newWin,50)
        
        pStore.appLabel(self.newWin,self.itmLabels)
        obj=pStore.appButtons(self.newWin,self.addTItemButtons)
        self.itemPage.itemObj.tView.bind('<ButtonRelease-1>',self.transStockTreeSel)
        self.tItemInfo = pStore.appEntrybox(self.newWin,self.tItemEntry)

        obj.returnList[0]['command']=self.transCalculate
        obj.returnList[1]['command']=self.saveClosetItem
        pStore.fileData.adjustStockTrans(self.transNum,self.modifiedList)
        #pStore.appLabel(self.newWin,self.addItemLabels)
        #self.addItemEntryList=pStore.appEntrybox(self.newWin,self.addItemEntry)

        #self.itemPage.itemsList.listObject.bind('<<ListboxSelect>>',self.actionItemList)
        #self.addRadioButtons()
        #self.addLineButton=pStore.appButtons(self.newWin,[['ADD LINES',[450,270],[1,10]]])
        #self.addLineButton.returnList[0]['command'] = self.createLineItems

    def itemViewPopulate(self):
        rec=self.tempItemList[self.itemVal]
        #tmp=[rec[0]]+pStore.fileData.itemList[rec[1]]+[rec[2],rec[4],rec[3],rec[19],rec[5],rec[6],rec[8],rec[9],rec[14],rec[15],rec[16],rec[17],float(rec[10])+float(rec[11]),rec[7]] 
        self.viewItemEntryList.setValues([self.itemVal]+rec[:18]+[''])
        #pStore.fileData.printLog(' '*4 + ' -INV25- Values populate on single item screen now - '+str(tmp) )

    def saveTransItem(self):
        #pStore.fileData.printLog(' '*4 + ' -INV23- Single Item line opened for view or edit')
        vList = self.viewItemEntryList.getValues()
        #pStore.fileData.printLog(' '*4 + ' -INV24- Values read from single item screen - '+str(vList) + ' Disc % ? - ' + vDisc )

        #self.addChanges(self.itemVal)
        if pStore.fileData.fConvert(vList[12]) != 0:
            self.tempItemList[self.itemVal][11] = pStore.fileData.fConvert(vList[12])  #Quantity Bought
            self.tempItemList[self.itemVal][12] = self.tempItemList[self.itemVal][11] * pStore.fileData.fConvert(self.tempItemList[self.itemVal][6])

            if pStore.fileData.fConvert(vList[19]) != 0:
                if pStore.fileData.fConvert(vList[19]) > self.tempItemList[self.itemVal][12] :
                    messagebox.showinfo('Uma Store','Amount cannot be greater than Total MRP amount',parent=self.itemChildObj)
                else:
                    self.tempItemList[self.itemVal][18] = pStore.fileData.fConvert(vList[19])
                    self.tempItemList[self.itemVal][17] = self.tempItemList[self.itemVal][18]
            else:
                self.tempItemList[self.itemVal][17] = self.tempItemList[self.itemVal][12]

            self.tempItemList[self.itemVal][14] = pStore.fileData.fConvert(self.tempItemList[self.itemVal][12]) - pStore.fileData.fConvert(self.tempItemList[self.itemVal][17])
            self.tempItemList[self.itemVal][13] = round(self.tempItemList[self.itemVal][14] * 100 / self.tempItemList[self.itemVal][12],2)
            self.tempItemList[self.itemVal][15] = self.calculateTax(self.tempItemList[self.itemVal][14])
            self.tempItemList[self.itemVal][16] = self.calculateTax(self.tempItemList[self.itemVal][14])

            if not self.is_NewTrans and len(self.modifiedList[self.itemVal]) < 6:
                self.modifiedList[self.itemVal].append(self.tempItemList[self.itemVal][11])
        else:
            messagebox.showinfo('Uma Store','Please input Buy Quantity or delete the item',parent=self.itemChildObj)
        self.itemViewPopulate()
        self.refreshTransItemTree()

    def copyPayment(self):
        self.transInfo.returnList[16].set(self.transInfo.getValues()[15])

    def saveCloseTransItem(self):
        self.saveTransItem()
        self.itemChildObj.withdraw()

    def deleteItemTransItem(self):
        if self.is_NewTrans: # If new trans, delete the entry
            del self.tempItemList[self.itemVal]
        else: 
            if len(self.modifiedList[self.itemVal]) < 6: # If not modified yet, log the change
                self.modifiedList[self.itemVal].append(self.tempItemList[self.itemVal][11])
            self.tempItemList[self.itemVal][11] = 0 # Make quantity as zero indicating deletion.
        self.refreshTransItemTree()
        self.itemChildObj.withdraw()

    def transItemTreeSel(self,evt):
        try:
            curItem = self.transObj.tView.focus()
            self.itemVal=self.transObj.tView.item(curItem)['values'][0]
            self.itemChildObj=pStore.fileData.createChild(self.window,'view/modify Item','600x550')
            xPos=40;off=310
            itemLabels=[('Sl # :', xPos,50),
                        ('Brand :',xPos,90),
                        ('Item Name :',xPos + off,90),
                        ('Model :',    xPos,130),
                        ('HSN code :',xPos + off,130),
                        ('Size :',    xPos,170),
                        ('Color :',xPos+off,170),
                        ('MRP :',       xPos,210),
                        ('Price/unit :',xPos + off,210),
                        ('Discount/unit :',  xPos,250),
                        ('Total GST :',xPos+off,250),
                        ('Final Price :',  xPos,290),
                        ('Quantity Bought :',xPos+off,290),
                        ('Total MRP :',xPos,330),
                        ('Disc % :',xPos+off,330),
                        ('Disc Amount :',xPos,370),
                        ('SGST/Unit :',xPos+off,370),
                        ('CGST/Unit :',xPos,410),
                        ('Final Amount :',xPos+off,410),
                        ('Customer Payment :',xPos,450)]

            xPos=130;off=330
            itemEntry=[(xPos,50,10,1),(xPos,90,20,1),(xPos+off,90,20,1),(xPos,130,20,1),
                   (xPos+off,130,20,1),(xPos,170,10,1),(xPos+off,170,12,1),(xPos,210,12,1),
                   (xPos+off,210,5,1),(xPos,250,12,1),(xPos+off,250,10,1),(xPos,290,12,1),
                   (xPos+off,290,12),(xPos,330,12,1),(xPos+off,330,12,1),(xPos,370,12,1),
                   (xPos+off,370,12,1),(xPos,410,12,1),(xPos+off,410,12,1),(xPos+30,450,12)]
            pStore.appLabel(self.itemChildObj,itemLabels)
            self.viewItemEntryList=pStore.appEntrybox(self.itemChildObj,itemEntry)
            self.itemViewPopulate()
            if not self.is_NewTrans:
                self.viewItemEntryList.objList[12]['state'] = tk.DISABLED
                self.viewItemEntryList.objList[19]['state'] = tk.DISABLED
            obj=pStore.appButtons(self.itemChildObj,[['SAVE',[40,480],[1,10]],
                                                      ['SAVE & CLOSE',[240,480],[1,12]],
                                                      ['DELETE ITEM',[440,480],[1,10]]])
            obj.returnList[0]['command']=self.saveTransItem       #SAVE Button Click
            obj.returnList[1]['command']=self.saveCloseTransItem  #SAVE & CLOSE Button Click
            obj.returnList[2]['command']=self.deleteItemTransItem #DELETE ITEM Button Click
        except:
            pass

    def newEntry_destroy(self):
        pStore.fileData.adjustStockTrans(self.transNum,self.modifiedList)
        self.newLabel.destroy()
        self.transInfo.destroy()
        self.transObj.destroy()
        self.newButton.destroy()

    def customize(self):
        self.newLabel=pStore.appLabel(self.window,self.transLabels)
        self.transInfo = pStore.appEntrybox(self.window,self.transEntry)

        self.transObj  = pStore.appTreeView(self.window,self.transTreeConfig,[10,200])
        self.transObj.tView.bind('<Double-1>',self.transItemTreeSel)
        #self.refreshTransItemTree()

        self.newButton=pStore.appButtons(self.window,self.addTransButtons)
        self.newButton.returnList[0]['command']=self.addItemInfo   #ADD ITEM Button Click
        self.newButton.returnList[1]['command']=self.refreshTransItemTree #SAVE Button Click
        self.newButton.returnList[2]['command']=self.backTransPortal #SAVE Button Click
        self.newButton.returnList[3]['command']=self.writeReceipt
        self.newButton.returnList[4]['command']=self.saveCloseTransaction
        self.newButton.returnList[5]['command']=self.copyPayment

        if self.is_NewTrans:
            self.transNum = '{:%Y%m%d%H%M%S}'.format(dt.today())
            self.transInfo.returnList[1].set(self.transNum)
            self.transInfo.returnList[2].set('{:%Y-%m-%d %H:%M:%S}'.format(dt.today()))
        else:
            rec=pStore.fileData.getTransHead(str(self.transNum))
            rec[15]=0 #Reseting the customer paid field
            self.transInfo.setValues(['']+rec)

            for rec in pStore.fileData.getTransItems(str(self.transNum)):
                self.tempItemList[self.transCounter] = rec
                self.modifiedList[self.transCounter] = [rec[19]] + rec[4:8]
                self.transCounter += 1
            self.populateItemTree()
            #pStore.fileData.adjustStockTrans(self.transNum,)
