import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import primaryStore as pStore

class supplierGrid():
    def __init__(self,arg1,arg2=0):
        self.offset=arg2
        self.window=arg1

        self.supplDetail=[('Supplier Name :',50+self.offset,50),('Address :',350+self.offset,50),('Contact :',50+self.offset,100),
                          ('GSTN :',350+self.offset,100),('PAN # :',50+self.offset,150),('Bank Name :',350+self.offset,150),
                          ('Account No :',50+self.offset,200),('Branch Name :',350+self.offset,200),('IFSC Code :',50+self.offset,250)]
        self.supplyEntry=[(150+self.offset,50),(450+self.offset,50),(150+self.offset,100),(450+self.offset,100),(150+self.offset,150),
                          (450+self.offset,150),(150+self.offset,200),(450+self.offset,200),(150+self.offset,250)]
        self.populateGrid()

    def populateGrid(self):
        pStore.appLabel(self.window,self.supplDetail)
        self.supEntryList=pStore.appEntrybox(self.window,self.supplyEntry)
        #self.supplyValues=self.supEntryList.createEntrybox()    ##May be redundant

class childWindow():
    def __init__(self,arg1,arg2,arg3):
        self.popMessage = arg3
        self.childWin = pStore.childFrame(arg1,arg2,'600x400')
        self.addGrid=supplierGrid(self.childWin.childRoot)
        self.subButton=pStore.appButtons(self.childWin.childRoot,{'SUBMIT' : ([150,300],[2,15])})
        self.subButton.returnList[0]['command']=self.submitAction

    def submitAction(self):
        pStore.fileData.modifySupplier(self.addGrid.supEntryList.getValues())
        messagebox.showinfo('Uma Store',self.popMessage)
        self.childWin.childRoot.withdraw()

class supplierWindow():
    def __init__(self):
        self.supplierRoot = tk.Tk()
        pStore.fileData.readSupplier()
        pStore.fileData.readInvoice()
        pStore.fileData.readInvoiceItem()
        pStore.fileData.readItem()

        self.treeConfig=[["0",'Id',80],["1",'Supplier',200],["2",'Invoice NO',150],["3",'Date',100],["4",'Total Qty',100],
                ["5",'Discount',100],["6",'CGST',100],["7",'SGST',100],["8",'Grand Total',100]]
        self.buttonConfig=[ ['REFRESH LIST',[60,300], [2,15]],
                            ['ADD SUPPLIER',[260,300],[2,15]],
                            ['CHANGE SUPPLIER',[460,300],[2,15]],
                            ['DELETE SUPPLIER',[660,300],[2,15]],
                            ['ADD INVOICE',[860,300],[2,15]]]
        self.suplSelection=None

    def refreshList(self):
        self.supplierListbox.listPopulate(list(pStore.fileData.supplierList.keys()))

    def addTransaction(self):
        #obj=childWindow(self.supplierRoot,'ADD Transaction','Supplier Added Successfully')
        self.newWin=pStore.childFrame(self.supplierRoot,'Add Transaction')
        obj = sTrans.addTransactions(self.newWin.childRoot,1111)
    '''
    def changeSupplier(self):
        if self.suplSelection is not None:
            obj=childWindow(self.supplierRoot,'CHANGE SUPPLIER','Supplier information modified Successfully')
            obj.addGrid.supEntryList.setValues(self.mainGrid.supEntryList.getValues())
        else:
            messagebox.showinfo('Uma Store','Please Select a Supplier First !!')

    def deleteSupplier(self):
        #obj=childWindow(self.supplierRoot,'DELETE SUPPLIER')
        pass

    def selectSupplierList(self,evt):
        w=evt.widget
        try:
            idx=int(w.curselection()[0])
            self.suplSelection = w.get(idx)
            self.mainGrid.supEntryList.setValues([self.suplSelection]+pStore.fileData.supplierList[self.suplSelection][1:])
            self.invoiceObj.setValues(pStore.fileData.getInvoices(self.suplSelection))
        except:
            self.suplSelection=None

    def addInvoice(self):
        if self.suplSelection is not None:
            winObj=pStore.childFrame(self.supplierRoot,'Add Invoice')
            obj = sInvoice.addInvoicePanel(winObj.childRoot,self.suplSelection,pStore.fileData.getConfigId('INVOICE_ID'))
        else:
            messagebox.showinfo('Uma Store','Please Select a Supplier First !!')

    def treeSelection(self,event):
        curItem = self.invoiceObj.tView.focus()
        tmp=self.invoiceObj.tView.item(curItem)['values'][:2]
        childObj=pStore.childFrame(self.supplierRoot,'View/Modify Invoice')
        obj = sInvoice.addInvoicePanel(childObj.childRoot,tmp[1],tmp[0])
    '''
    def customize(self):
        self.supplierRoot.title("Uma Store Supplier and Invoice Frame")
        self.supplierRoot.geometry('1100x650')
        self.mainGrid=supplierGrid(self.supplierRoot,250)

        self.supplierListbox=pStore.appListBox(self.supplierRoot,list(pStore.fileData.supplierList.keys()),[50,50])
        #self.supplierListbox.listObject.bind('<<ListboxSelect>>',self.selectSupplierList)

        obj=pStore.appButtons(self.supplierRoot,self.buttonConfig)
        #obj.returnList[0]['command']=self.refreshList             #REFRESH BUTTON
        obj.returnList[1]['command']=self.addTransaction             #ADD SUPPLIER BUTTON
        
        #self.invoiceObj=pStore.appTreeView(self.supplierRoot,self.treeConfig,[50,390])
        #self.invoiceObj.tView.bind('<Double-1>',self.treeSelection)
        #self.invoiceTree=self.invoiceObj.createTree()

    def __main__(self):
        self.customize()
        self.supplierRoot.mainloop()
