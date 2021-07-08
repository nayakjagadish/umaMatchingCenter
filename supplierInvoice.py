import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import primaryStore as pStore
import primaryItem as pItem
import storeSupplier as sSupplier
######################################################New Class
class addInvoicePanel():
    def __init__(self,arg1,arg2,arg3,arg4=False):
        pStore.fileData.readItem()
        self.is_newInvoice=arg4
        self.window = arg1
        self.passedSupplier=arg2
        self.passInvoiceId=arg3
        self.finalItemList=[];self.modifiedList=[];self.itemCounter=1;self.offSet = 0;self.itemVal = None
        self.invoiceLabels=[('Supplier Name :',50,50),
                            ('Invoice number :',400,50),
                            ('Invoice Date :',750,50),
                            ('Total number of Items :',150,350),
                            ('Total Item Discount :',150,380),
                            ('Total Price before Discount and Tax :',450,350),
                            ('Total Price After Item Discount and before Tax :',450,380),
                            ('Add Invoice Discount - 1 :    Percentage(%)',200,450),
                            ('OR Amount ',510,450),
                            ('Add Invoice Discount - 2 :    Percentage(%)',200,480),
                            ('OR Amount ',510,480),
                            ('Total Invoice Discount :',150,530),
                            ('Price after Invoice Discount and Before Tax :',450,530),
                            ('Total SGST Amount :',150,560),
                            ('Total CGST Amount :',400,560),
                            ('Grand Total :',670,560),
                            ('Mode of Payment :',150,610),
                            ('Payment reference :',390,610),
                            ('Payment Amount :',660,610)]
        self.invoiceEntry=[(170,50,30,1),(520,50),(870,50),
                           (300,350,10,1,1),(300,380,10,1,1),(710,350,12,1,1),(710,380,12,1,1),
                           (435,450,10,0,1),(600,450,12,0,1),(435,480,10,0,1),(600,480,12,0,1),
                           (300,530,12,1,1),(700,530,12,1,1),
                           (300,560,12,1,1),(540,560,12,1,1),(780,560,12,1,1),
                           (510,610,20,0,1),(780,610,12,0,1)]
        self.invoiceTreeConfig = [
                ["0",'Sl#',30],
                ["1",'Brand',100],
                ["2",'Item Name',100],
                ["3",'Model',90],
                ["4",'HSN',80],
                ["5",'Size',80],
                ["6",'Color',80],
                ["7",'Quantity',50],
                ["8",'MRP',80],
                ["9",'Unit Price',80],
                ["10",'Discount',80],
                ["11",'SGST+CGST',80],
                ["12",'Total',100],
                ["13",'Total+Tax',100]]
        self.addItemLabels=[('Brand :',600,50),
                            ('Item :' ,800,50),
                            ('Model :',600,100),
                            ('HSN :'  ,800,100),
                            ('Size :' ,600,150),
                            ('Quantity :',760,150),
                            ('Piece Box',880,150),
                            ('Color :' ,600,200),
                            ('Discount % ? :' ,740,200)]
        self.addItemEntry=[(650,50,20,1),(850,50,25,1),(650,100,15,1),(850,100,15,1)]
        self.addItemButtons=[ ['ADD ITEM',[840,350],[4,12]],
                              ['BACK',[960,350],[4,12]],
                              ['SAVE',[840,450],[4,12]],
                              ['SAVE & CLOSE',[960,450],[4,12]],
                              ['FULL PAYMENT',[780,640],[2,14]]]
        self.vSize={'Standard' : ['Standard'],
                    'S to XXL' : ['X-Small','Small','Medium','Large','X-Large','DoubleXL'],
                    '4-7CM'    : ['4CM','5CM','6CM','7CM'],
                    '32-42CM'  : ['30CM','32CM','34CM','36CM','38CM','40CM','42CM'],
                    '45-75CM'  : ['45CM','50CM','55CM','60CM','65CM','70CM','75CM'],
                    '80-110CM' : ['80CM','85CM','90CM','95CM','100CM','105CM','110CM']}
        self.qtyUnit =[1,2,3,4,5,10,12,20]
        self.pmtMethods=['CASH','BANK NEFT','CHECK PAYMENT','PHONE PAY']
        pStore.fileData.printLog('-'*10 + 'INVOICE page section initialized' + '-'*10)
        pStore.fileData.itemStockSync()
        self.customize()

    def __del__(self):
        pStore.fileData.printLog('-'*10 + 'INVOICE page is now closed' + '-'*10)

    def actionItemList(self,evt): #Click on item in the list.
        w=evt.widget
        pStore.fileData.printLog(' '*4 + ' -INV35 - Add Item line is clicked')
        try:
            idx=int(w.curselection()[0])
            clickVal = w.get(idx)
            self.itemVal = clickVal
            pStore.fileData.printLog(' '*4 + ' -INV36- Item that is clicked - Brand & item :' + str([self.itemPage.brandVal,self.itemVal]))
            self.addItemEntryList.setValues(pStore.fileData.itemList[pStore.fileData.getItemKey([self.itemPage.brandVal,self.itemVal])])
        except:
            clickVal=None

    def addRadioButtons(self):   # Add radio buttons in item page
        self.varSize = tk.StringVar()
        self.sizeDrop = pStore.appDropDown(self.newWin,
                                           self.varSize,
                                           ['Standard','S to XXL','4-7CM','32-42CM','45-75CM','80-110CM'],
                                           [650,150,10,0],
                                           True)
        self.varQty = tk.StringVar()
        self.quantDrop = pStore.appDropDown(self.newWin,
                                           self.varQty,
                                           self.qtyUnit,
                                           [830,150,3,0],
                                           True)
        self.varColor = tk.StringVar()
        self.colorDrop = pStore.appDropDown(self.newWin,
                                           self.varColor,
                                           ['NO','YES'],
                                           [650,200,3,0],
                                           True)

        self.varDisc = tk.StringVar()
        self.discDrop = pStore.appDropDown(self.newWin,
                                           self.varDisc,
                                           ['YES','NO',],
                                           [830,200,3,0],
                                           True)

    def populateScreen(self,iPage):
        vList=iPage.getValues() #Get values from screen
        pStore.fileData.printLog(' '*4 + ' -INV10- Item values from screen - Size:[' + str(vList[0]) +'] Quantity:['+ str(vList[1]) +'] Color:['+ str(vList[2]) +'] MRP:['+ str(vList[3]) +'] Box Price:['+ str(vList[4]) +'] Total Price:['+ str(vList[5]) +'] Disc %:['+ str(vList[6]) +'] Disc Amt:['+ str(vList[7]) +'] CGST:['+ str(vList[8]) +'] SGST:['+ str(vList[9])+'] Grand Total:['+ str(vList[10]) +']')
        vTemp=[]
        vList[1] = pStore.fileData.fConvert(vList[1])
        if vList[1] != 0:
            vList[3] = pStore.fileData.fConvert(vList[3])
            vList[4] = pStore.fileData.fConvert(vList[4])
            vList[6] = pStore.fileData.fConvert(vList[6])
            vList[7] = pStore.fileData.fConvert(vList[7])
            vList[5] = round(vList[1] * float(vList[4]),2)    #Total Price
            if self.discVal == 'YES':
                vList[7] = round(float(vList[6]) * vList[5] * 0.01,2)  #Discount Price
            else:
                vList[6] = 0 if vList[5] == 0 else round(float(vList[7]) * 100 / vList[5],2)
            vList[8] = round((vList[5] - float(vList[7])) * 2.5 / 100,2)  #CGST
            vList[9] = round((vList[5] - float(vList[7])) * 2.5 / 100,2)  #SGST
            vList[10] = round(vList[5] - float(vList[7]) + vList[8] + vList[9],2) #Grand Total

            totQuant = vList[1]*int(self.qtyVal)
            vTemp.append(totQuant) #total Quantity
            vTemp.append(round(vList[5]/totQuant,2)) #unit price
            vTemp.append(round(float(vList[7])/totQuant,2)) #unit discount
            vTemp.append(round(vList[8]/totQuant,2)) #unit CGST
            vTemp.append(round(vList[9]/totQuant,2)) #unit SGST
            vTemp.append(self.discVal) #Invoice discount on unit
            vTemp.append(self.qtyVal) #Quantity Unit
            iPage.setValues(vList)#populate values in screen
            pStore.fileData.printLog(' '*4 + ' -INV11- Item values after calculation -  Size:[' + str(vList[0]) +'] Quantity:['+ str(vList[1]) +'] Color:['+ str(vList[2]) +'] MRP:['+ str(vList[3]) +'] Box Price:['+ str(vList[4]) +'] Total Price:['+ str(vList[5]) +'] Disc %:['+ str(vList[6]) +'] Disc Amt:['+ str(vList[7]) +'] CGST:['+ str(vList[8]) +'] SGST:['+ str(vList[9])+'] Grand Total:['+ str(vList[10]) +'] Total Qty:[' + str(vTemp[0])+'] Unit Price:['+ str(vTemp[1])+'] Unit Disc:['+ str(vTemp[2])+'] Unit CGST:['+ str(vTemp[3])+'] Unit SGST:['+ str(vTemp[4])+'] Disc % ?:['+ str(vTemp[5])+'] Box Unit:['+ str(vTemp[6])+']')
            return vList+vTemp
      
    def updateInvoicePage(self):
        pStore.fileData.printLog(' '*4 + ' -INV15 - Update invoice page clicked')
        vList = self.invoiceInfo.getValues()
        pStore.fileData.printLog(' '*4 + ' -INV16- Invoice summary values from screen - ' + str(vList))
        pStore.fileData.printLog(' '*4 + ' -INV17- Final Item list - ' + str(self.finalItemList))
        [vList[3],vList[4],vList[5],vList[6],vList[11],vList[12],vList[13],vList[14],vList[15]] = [0,0,0,0,0,0,0,0,0]
        tmp=[]
             
        for rec in self.finalItemList:
            vList[3] += float(rec[3]) #Total no of items
            vList[4] += float(rec[9]) #Total Discount
            vList[5] += float(rec[7]) #Price before Discount & Tax
            
        vList[6] = vList[5] - vList[4] #Price after Item Discount and before tax
        if pStore.fileData.fConvert(vList[7]) > 0:
            vList[8] = round(float(vList[6]) * pStore.fileData.fConvert(vList[7]) / 100,2)
        else:
            if pStore.fileData.fConvert(vList[8]) > 0:
                vList[7] = round(pStore.fileData.fConvert(vList[8]) * 100 / float(vList[6]),2)
        if pStore.fileData.fConvert(vList[9]) > 0:
            vList[10] = round(float(vList[6]) * pStore.fileData.fConvert(vList[9]) / 100,2)
        else:
            if pStore.fileData.fConvert(vList[10]) > 0:
                vList[9] = round(pStore.fileData.fConvert(vList[10]) * 100 / float(vList[6]),2)

        vList[11] = pStore.fileData.fConvert(vList[8]) + pStore.fileData.fConvert(vList[10]) # Total Invoice discount
        vList[12] = vList[6] - vList[11] # Total price after Invoice discount & before tax
        vList[13] += round(vList[12]*2.5/100,2) #Total SGST
        vList[14] += round(vList[12]*2.5/100,2) #Total CGST
        vList[15]  = round(vList[12] + vList[13] + vList[14],2) # Grand Total

        self.invoiceInfo.setValues(vList)
        vList.append(self.pymtDrop.getValue())
        pStore.fileData.printLog(' '*4 + ' -INV18- Invoice summary values after calculation - ' + str(vList))
        pStore.fileData.addNewInvoice(self.passInvoiceId,vList,self.finalItemList) # Add both invoice head and detail to file & Dictionary
        pStore.fileData.adjustStockInvoice(self.passInvoiceId,self.modifiedList) # Add item stock entries

    def calculateTotal(self):
        self.singleItemInfo=[]
        for rec in self.itemEntryObject:
            tmp=self.addItemEntryList.getValues()
            pStore.fileData.printLog(' '*4 + ' -INV9- Calculation for item ' + str(tmp))
            vVal= self.populateScreen(rec)
            if vVal is not None:
                self.singleItemInfo.append([pStore.fileData.getItemKey(tmp[:3])]+vVal)
        pStore.fileData.printLog(' '*4 + ' -INV12- Items from item page as follows -')
        for rec in self.singleItemInfo:
            pStore.fileData.printLog(' '*6 + ' -INV12A- itemId:['+str(rec[0])+'] Size:['+str(rec[1])+'] Box qty:['+str(rec[2])+'] Color:['+str(rec[3])+'] MRP:['+str(rec[4])+'] Box Price:['+str(rec[5])+'] Total Price:['+str(rec[6])+'] Disc %:['+str(rec[7])+'] Disc Amt:['+str(rec[8])+'] Total CGST:['+str(rec[9])+'] Total SGST:['+str(rec[10])+'] Grand Total:['+str(rec[11])+'] Tot Qty:['+str(rec[12])+'] Unit Price:['+str(rec[13])+'] Unit Disc:['+str(rec[14])+'] Unit CGST:['+str(rec[15])+'] Unit SGST:['+str(rec[16])+'] Disc %?:['+str(rec[17])+'] Box unit:['+str(rec[17])+']')

    def checkItem(self,rec):
        returnKey = -1
        cnt = 0
        pStore.fileData.printLog(' '*4 + '-INV37- checkItem() for ' + str(rec))
        for itm in self.finalItemList:
            if str(rec[0]) == str(itm[1]): #Item_id
                if rec[1] == itm[2]:       #size
                    if rec[3] == itm[4]:   #color
                        if abs(pStore.fileData.fConvert(rec[4]) - pStore.fileData.fConvert(itm[5])) < 0.5:     #MRP
                            if abs(pStore.fileData.fConvert(rec[13]) - pStore.fileData.fConvert(itm[14])) < 0.5: #Unit Price
                                returnKey = cnt
            cnt += 1
        pStore.fileData.printLog(' '*4 + '-INV38- checkItem() Key returned ' + str(returnKey))
        return returnKey    
    
    def saveClose(self): #Save & close of Item page
        pStore.fileData.printLog(' '*4 + ' -INV13- Item save & close clicked')
        self.calculateTotal()
        for rec in self.singleItemInfo:
            k = self.checkItem(rec)
            if k == -1:
                self.finalItemList.append([self.itemCounter] + rec) # Appending elements in temp master array
                pStore.fileData.printLog(' '*6 + ' -INV13A- New item Added - ' + str(rec))
            else:
                self.addChanges(k)
                pStore.fileData.printLog(' '*6 + ' -INV13B- Exisitng Item found for item line - ' + str(rec))
                self.finalItemList[k][13] = pStore.fileData.fConvert(self.finalItemList[k][13]) + pStore.fileData.fConvert(rec[12])
                self.finalItemList[k][12] = pStore.fileData.fConvert(self.finalItemList[k][12]) + pStore.fileData.fConvert(rec[11])
                self.finalItemList[k][11] = pStore.fileData.fConvert(self.finalItemList[k][11]) + pStore.fileData.fConvert(rec[10])
                self.finalItemList[k][10] = pStore.fileData.fConvert(self.finalItemList[k][10]) + pStore.fileData.fConvert(rec[9])
                self.finalItemList[k][9]  = pStore.fileData.fConvert(self.finalItemList[k][9]) + pStore.fileData.fConvert(rec[8])
                self.finalItemList[k][7]  = pStore.fileData.fConvert(self.finalItemList[k][7]) + pStore.fileData.fConvert(rec[6])
                self.finalItemList[k][8]  = round(pStore.fileData.fConvert(self.finalItemList[k][9]) / self.finalItemList[k][7],2)
                if str(self.finalItemList[k][19]) == str(rec[18]):
                    self.finalItemList[k][3] = pStore.fileData.fConvert(self.finalItemList[k][3]) + pStore.fileData.fConvert(rec[2])
                else:
                    self.finalItemList[k][3] = pStore.fileData.fConvert(self.finalItemList[k][3]) + round(pStore.fileData.fConvert(rec[2]) * pStore.fileData.fConvert(rec[18]) / pStore.fileData.fConvert(self.finalItemList[k][19]), 2)
                self.finalItemList[k][15] = round((pStore.fileData.fConvert(self.finalItemList[k][15]) * self.finalItemList[k][13] + pStore.fileData.fConvert(rec[14]) * pStore.fileData.fConvert(rec[12])) / (self.finalItemList[k][13] + pStore.fileData.fConvert(rec[12])),2)
                pStore.fileData.printLog(' '*6 + ' -INV13C- Item line after avveraging calculation - ' + str(self.finalItemList[k]))
            self.itemCounter += 1
        self.updateInvoicePage()
        self.refreshInvoiceItemTree()
        pStore.fileData.printLog(' '*4 + ' -INV14- Closing Item page')
        self.newWin.withdraw()
        
    def createLineItems(self): #Add Item window - everything
        tmp=self.addItemEntryList.getValues()
        pStore.fileData.printLog(' '*4 + ' -INV4A- Item details from screen - ' + str(tmp))
        if len(tmp[1]) == 0:
            messagebox.showinfo('Uma Store','Please Select an Item from Item List Box !!',parent=self.newWin)
        else:
            self.itemEntryObject=[];offSet=0;yPos=320
            labelList = [('Size',30,yPos),
                         ('Quantity' ,100,yPos),
                         ('Color',210,yPos),
                         ('MRP'  ,300,yPos),
                         ('Piece/Box price' ,395,yPos),
                         ('Total price' ,500,yPos),
                         ('Discount %',600,yPos),
                         ('Discount Amount',690,yPos),
                         ('CGST (2.5%)' ,800,yPos),
                         ('SGST (2.5%)' ,900,yPos),
                         ('Grand Total',1000,yPos)]
            pStore.appLabel(self.newWin,labelList)
            yPos1=yPos+40
            itemInfoEntry = [[20,yPos1,8,1],[100,yPos1,6,0,1],[210,yPos1,7,0],[300,yPos1,8,0,1],[400,yPos1,8,0,1],[500,yPos1,8,1,1],
                             [600,yPos1,6,0,1],[700,yPos1,8,0,1],[800,yPos1,8,1,1],[900,yPos1,8,1,1],[1000,yPos1,8,1,1]]
            buttons=[[ 'SAVE',[1100,400],[4,12]],['SAVE & CLOSE',[1100,500],[4,12]]]

            sizeVal     = self.sizeDrop.getValue()
            self.qtyVal = self.quantDrop.getValue()
            colorVal    = self.colorDrop.getValue()
            self.discVal= self.discDrop.getValue()

            pStore.fileData.printLog(' '*4 + ' -INV5- Size selected -' + sizeVal)
            pStore.fileData.printLog(' '*4 + ' -INV6- Box qty selected -' + self.qtyVal)
            pStore.fileData.printLog(' '*4 + ' -INV7- Color selected -' + colorVal)
            pStore.fileData.printLog(' '*4 + ' -INV7A- Disocunt % selected -' + self.discVal)

            qtyLabel = 'PIECE' if int(self.qtyVal) == 1 else str(self.qtyVal) +'P Box'
            itemInfoEntry[2][3] = 1 if colorVal == 'NO' else 0
            if self.discVal == 'YES':
                itemInfoEntry[7][3] = 1
            else:
                itemInfoEntry[6][3] = 1
            for rec in self.vSize[sizeVal]:           
                tmp = pStore.appEntrybox(self.newWin,itemInfoEntry)
                tmp.returnList[0].set(rec)
                pStore.appLabel(self.newWin,[(qtyLabel,140,360+offSet)])
                self.itemEntryObject.append(tmp)
                for i in range(len(itemInfoEntry)):
                    itemInfoEntry[i][1] += 40
                offSet+= 40
                pStore.fileData.printLog(' '*4 + ' -INV8- Item line added for size -' + rec)

            buttObject=pStore.appButtons(self.newWin,buttons)
            buttObject.returnList[0]['command']=self.calculateTotal    # Action #2 SAVE button
            buttObject.returnList[1]['command']=self.saveClose         # Action #3 SAVE & CLOSE button
            self.addLineButton.returnList[0]['state'] = tk.DISABLED

    def addItemInfo(self): # Click on Add item button in Invoice page.
        ### Total 3 Actions
        # 1. ADD LINES 
        # 2. Click on Save button (self.updateInvoicePage)
        # 3. Click on Save & Close button (self.saveCloseInvoice)
        pStore.fileData.printLog(' '*4 + ' -INV4- New Item page selected')
        self.newWin=pStore.fileData.createChild(self.window,'Add Item')
        self.itemPage = pItem.primaryItem(self.newWin)
        pStore.appLabel(self.newWin,self.addItemLabels)
        self.addItemEntryList=pStore.appEntrybox(self.newWin,self.addItemEntry)

        self.itemPage.itemsList.listObject.bind('<<ListboxSelect>>',self.actionItemList)
        self.addRadioButtons()
        self.addLineButton=pStore.appButtons(self.newWin,[['ADD LINES',[450,240],[4,10]]])
        self.addLineButton.returnList[0]['command'] = self.createLineItems #Action #1
        pStore.fileData.adjustStockInvoice(self.passInvoiceId,self.modifiedList)

    def saveCloseInvoice(self):  #Save & close of invoice page
        pStore.fileData.printLog(' '*4 + ' -INV19- Invoice Save & Close clicked')
        self.updateInvoicePage()
        pStore.fileData.printLog(' '*4 + ' -INV20 - Closing invoice page')
        self.invoice_destroy()
        obj=sSupplier.supplierWindow(self.window,self.passedSupplier)

    def copyBackPayment(self):
        self.invoiceInfo.returnList[17].set(self.invoiceInfo.getValues()[15])

    def refreshInvoiceItemTree(self):
        tmp = []
        for rec in self.finalItemList:
            tmp.append([rec[0]]+pStore.fileData.itemList[rec[1]]+
                           [rec[2],rec[4],rec[13],rec[5],rec[14],rec[9],float(rec[10])+float(rec[11]),float(rec[7])-float(rec[9]),rec[12]])
        pStore.fileData.printLog(' '*4 + ' -INV21- Refreshing invoice item tree with list - '+str(tmp))
        self.invoiceItemObj.setValues(tmp) # populate tree on invoice page

    def getItemIndex(self,val,vLIst):
        cnt=0
        for rec in vLIst:
            if rec[0] == val:
                return cnt
            cnt += 1
        return -1
    
    def addChanges(self,vIdx):
        pStore.fileData.printLog(' '*4 + ' -INV30- Attempt of modifying item values')
        if self.is_newInvoice:
            pStore.fileData.printLog(' '*4 + ' -INV31- item change not logged since new invoice')
        else:
            k = self.getItemIndex(self.finalItemList[vIdx][0],self.modifiedList)
            if k == -1:
                pStore.fileData.printLog(' '*4 + ' -INV31D- Error in selecting key from self.modifiedList')
            elif len(self.modifiedList[k]) < 7:
                pStore.fileData.printLog(' '*4 + ' -INV31A- Deleting dummy entry and logging the item change')
                pStore.fileData.printLog(' '*6 + ' -INV31B- addChanges() Dummey entry Deleted - ' + str(self.modifiedList[k]))
                del self.modifiedList[k] #deleting existing dummy entry
                self.modifiedList.append(self.finalItemList[vIdx][:])  # Preserve previous value for stock adjustment
                pStore.fileData.printLog(' '*6 + ' -INV31C- addChanges() Added - ' + str(self.finalItemList[vIdx]))
            else:
                pStore.fileData.printLog(' '*4 + ' -INV32- item change is not logged as already logged')

    def itemViewPopulate(self):
        rec=self.finalItemList[self.selectedItem]
        tmp=[rec[0]]+pStore.fileData.itemList[rec[1]]+[rec[2],rec[4],rec[3],rec[19],rec[5],rec[6],rec[8],rec[9],rec[14],rec[15],rec[16],rec[17],float(rec[10])+float(rec[11]),rec[7]] 
        self.viewItemEntryList.setValues(tmp)
        self.itemDiscDrop.setValue(rec[18])
        pStore.fileData.printLog(' '*4 + ' -INV25- Values populate on single item screen now - '+str(tmp) )

    def saveInvoiceItem(self):
        pStore.fileData.printLog(' '*4 + ' -INV23- Single Item line opened for view or edit')
        vList = self.viewItemEntryList.getValues()
        vDisc=self.itemDiscDrop.getValue()
        pStore.fileData.printLog(' '*4 + ' -INV24- Values read from single item screen - '+str(vList) + ' Disc % ? - ' + vDisc )

        self.addChanges(self.selectedItem)
        self.finalItemList[self.selectedItem][4] = vList[6]  #Color
        self.finalItemList[self.selectedItem][3] = pStore.fileData.fConvert(vList[7])   #Box Quant
        self.finalItemList[self.selectedItem][19] = vList[8]  # Box size
        self.finalItemList[self.selectedItem][5] = pStore.fileData.fConvert(vList[9])   #MRP
        self.finalItemList[self.selectedItem][6] = pStore.fileData.fConvert(vList[10])  #Box price
            
        self.finalItemList[self.selectedItem][7]  = pStore.fileData.fConvert(vList[7]) * pStore.fileData.fConvert(vList[10]) #Total Price
        self.finalItemList[self.selectedItem][14] = round(pStore.fileData.fConvert(vList[10]) / pStore.fileData.fConvert(vList[8]),2) #price per unit

        if vDisc == 'YES':
            self.finalItemList[self.selectedItem][8] = pStore.fileData.fConvert(vList[11])
            self.finalItemList[self.selectedItem][9] = round(pStore.fileData.fConvert(vList[11]) * self.finalItemList[self.selectedItem][7] * 0.01,2)
        else:
            self.finalItemList[self.selectedItem][9] = pStore.fileData.fConvert(vList[12])
            self.finalItemList[self.selectedItem][8] = round(100 * pStore.fileData.fConvert(vList[12]) / self.finalItemList[self.selectedItem][7],2)

        self.finalItemList[self.selectedItem][13] = pStore.fileData.fConvert(vList[7]) * pStore.fileData.fConvert(vList[8])
        self.finalItemList[self.selectedItem][15] = round(pStore.fileData.fConvert(self.finalItemList[self.selectedItem][9]) / self.finalItemList[self.selectedItem][13],2) if self.finalItemList[self.selectedItem][13] > 0 else 0
        self.finalItemList[self.selectedItem][10] = round((pStore.fileData.fConvert(vList[7]) * pStore.fileData.fConvert(vList[10]) - pStore.fileData.fConvert(vList[15])) * 0.025,2)
        self.finalItemList[self.selectedItem][11] = round((pStore.fileData.fConvert(vList[7]) * pStore.fileData.fConvert(vList[10]) - pStore.fileData.fConvert(vList[15])) * 0.025,2)
            
        self.finalItemList[self.selectedItem][16] = round(self.finalItemList[self.selectedItem][10] / self.finalItemList[self.selectedItem][13],2) if self.finalItemList[self.selectedItem][13] > 0 else 0
        self.finalItemList[self.selectedItem][17] = round(self.finalItemList[self.selectedItem][11] / self.finalItemList[self.selectedItem][13],2) if self.finalItemList[self.selectedItem][13] > 0 else 0
        self.finalItemList[self.selectedItem][12] = pStore.fileData.fConvert(vList[7]) * pStore.fileData.fConvert(vList[10]) - pStore.fileData.fConvert(vList[15])
            
        self.itemViewPopulate()
        self.updateInvoicePage()

    def saveCloseInvoiceItem(self):
        pStore.fileData.printLog(' '*4 + ' -INV26- Save Close on single item page clicked')
        self.saveInvoiceItem()
        self.refreshInvoiceItemTree()
        pStore.fileData.printLog(' '*4 + ' -INV27- Closing single item page')
        self.itemChildObj.withdraw()

    def deleteItemInvoiceItem(self):
        pStore.fileData.printLog(' '*4 + ' -INV28- Delete item clicked')
        self.addChanges(self.selectedItem)
        del self.finalItemList[int(self.selectedItem)]
        self.updateInvoicePage()
        self.refreshInvoiceItemTree()
        pStore.fileData.printLog(' '*4 + ' -INV29- Closing single item page')
        self.itemChildObj.withdraw()

    def itemTreeSelection(self,event):
        curItem = self.invoiceItemObj.tView.focus()
        itemSeq=self.invoiceItemObj.tView.item(curItem)['values'][0]
        self.selectedItem = self.getItemIndex(itemSeq,self.finalItemList)
        pStore.fileData.printLog(' '*4 + ' -INV21A- Item in item tree double clicked - item Sl# : '+str(itemSeq))
        self.itemChildObj=pStore.fileData.createChild(self.window,'view/modify Item','600x550')
        xPos=40;off=310
        itemLabels=[('Sl # :',xPos,50),
                    ('Brand :',xPos,90),
                    ('Item Name :',xPos + off,90),
                    ('Model :',xPos,130),
                    ('HSN code :',xPos + off,130),
                    ('Size :',xPos,170),
                    ('Color :',xPos+off,170),
                    ('Quantity :',xPos,210),
                    ('Unit of Quantity :',xPos + off,210),
                    ('PIECE',xPos + off + 145,210),
                    ('MRP :',xPos,250),
                    ('Piece/Box price :',xPos+off,250),
                    ('Discount % :',xPos,290),
                    ('Disc % ? :',xPos+180,290),
                    ('Discount Amount :',xPos+off,290),
                    ('Price/unit ',xPos,330),
                    ('Discount/unit :',xPos+off,330),
                    ('CGST/unit :',xPos,370),
                    ('SGST/Unit :',xPos+off,370),
                    ('Total Tax :',xPos,410),
                    ('Before Disocunt Total:', xPos+off-25,410)]
        self.itemDisc = tk.StringVar()
        self.itemDiscDrop = pStore.appDropDown(self.itemChildObj,
                                           self.itemDisc,
                                           ['YES','NO',],
                                           [xPos+240,290,3,0],
                                           True)
        xPos=130;off=330
        itemEntry=[(xPos,50,10,1),(xPos,90,20,1),(xPos+off,90,20,1),(xPos,130,20,1),
                   (xPos+off,130,20,1),(xPos,170,10,1),(xPos+off,170,12),(xPos,210,12),
                   (xPos+off,210,5),(xPos,250,12),(xPos+off,250,10),(xPos,290,12),
                   (xPos+off,290,12),(xPos,330,12,1),(xPos+off,330,12,1),(xPos,370,12,1),
                   (xPos+off,370,12,1),(xPos,410,12,1),(xPos+off,410,12,1)]
        pStore.appLabel(self.itemChildObj,itemLabels)
        self.viewItemEntryList=pStore.appEntrybox(self.itemChildObj,itemEntry)
        self.itemViewPopulate()
        obj=pStore.appButtons(self.itemChildObj,[['SAVE',[40,480],[1,10]],
                                                      ['SAVE & CLOSE',[240,480],[1,12]],
                                                      ['DELETE ITEM',[440,480],[1,10]]])
        obj.returnList[0]['command']=self.saveInvoiceItem       #SAVE Button Click
        obj.returnList[1]['command']=self.saveCloseInvoiceItem  #SAVE & CLOSE Button Click
        obj.returnList[2]['command']=self.deleteItemInvoiceItem #DELETE ITEM Button Click

    def Supplier(self):
        pStore.fileData.adjustStockInvoice(self.passInvoiceId,self.modifiedList)
        self.invoice_destroy()
        obj=sSupplier.supplierWindow(self.window,self.passedSupplier)

    def invoice_destroy(self):
        self.invLbl.destroy()
        self.invoiceInfo.destroy()
        self.pymtDrop.destroy()
        self.invoiceItemObj.destroy()
        self.invBut.destroy()

    def customize(self):
        ### Total 4 Actions
        # 1. Double Click on one of the items (self.itemTreeSelection)
        # 2. Click on Add Item button (self.addItemInfo)
        # 3. Click on Save button (self.updateInvoicePage)
        # 4. Click on Save & Close button (self.saveCloseInvoice)
        self.invLbl=pStore.appLabel(self.window,self.invoiceLabels) #Print labels
        self.invoiceInfo = pStore.appEntrybox(self.window,self.invoiceEntry) #Create Invoice related text boxes

        #Payment methof DropDown#######
        self.dropVal=tk.StringVar()
        self.pymtDrop = pStore.appDropDown(self.window,self.dropVal,self.pmtMethods,[270,610,15,0],True)
        ###############################
        if self.is_newInvoice:
            self.invoiceInfo.returnList[0].set(self.passedSupplier)
            pStore.fileData.printLog(' '*2 + '-INV1- New Invoice to be added')
        else:
            pStore.fileData.printLog(' '*2 + str(self.passInvoiceId) + ' -INV2- Exisitng Invoice to be viewed/modified')
            tmp=pStore.fileData.getInvoice(self.passInvoiceId)
            self.invoiceInfo.setValues([self.passedSupplier]+tmp[1:]) # Populate invoice info in text boxes
            pStore.fileData.printLog(' '*2 + str(self.passInvoiceId) + ' -INV2A- Loading temp Item list with invoice items and item keys in modified list.')
            for rec in pStore.fileData.getInvoiceItems(str(self.passInvoiceId)):
                self.finalItemList.append([self.itemCounter] + rec)
                self.modifiedList.append([self.itemCounter] + [rec[0],rec[1],rec[3],rec[4],rec[13]]) #Adding item keys in modified list
                self.itemCounter += 1
            pStore.fileData.printLog(' '*2 + ' -INV3- Following Items loaded')
            for rec in self.finalItemList:
                pStore.fileData.printLog(' '*4 + str(rec))
            pStore.fileData.printLog(' '*2 + ' -INV3A- Following Item keys loaded in Modified List :')
            for rec in self.modifiedList:
                pStore.fileData.printLog(' '*4 + str(rec))
            pStore.fileData.printLog(' '*2 + '-'*10)
            #pStore.fileData.deductStockInvoice(self.passInvoiceId)
            self.pymtDrop.setValue(tmp[18])

        self.invoiceItemObj = pStore.appTreeView(self.window,self.invoiceTreeConfig,[50,100])
        self.invoiceItemObj.tView.bind('<Double-1>',self.itemTreeSelection) #Action #1
        self.refreshInvoiceItemTree()

        self.invBut=pStore.appButtons(self.window,self.addItemButtons) 
        self.invBut.returnList[0]['command']=self.addItemInfo   #ADD ITEM Button Click   #Action #2
        self.invBut.returnList[1]['command']=self.Supplier   #ADD ITEM Button Click   #Action #2
        self.invBut.returnList[2]['command']=self.updateInvoicePage #SAVE button         #Action #3
        self.invBut.returnList[3]['command']=self.saveCloseInvoice  #SAVE & CLOSE button #Action #4
        self.invBut.returnList[4]['command']=self.copyBackPayment  #SAVE & CLOSE button #Action #4
