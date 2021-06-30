import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import primaryStore     as pStore
import supplierInvoice  as sInvoice
import storeItem        as sItem
import storeTransaction as sTrans
######################################################New Class
class supplierGrid():
    def __init__(self,arg1,arg2=0):
        offset=arg2;window=arg1
        supplDetail=[('Supplier Name :',50+offset,50),('Address :',400+offset,50),('Contact :',50+offset,100),
                          ('GSTN :',400+offset,100),('PAN # :',50+offset,150),('Bank Name :',400+offset,150),
                          ('Account No :',50+offset,200),('Branch Name :',400+offset,200),('IFSC Code :',50+offset,250)]
        supplyEntry=[(150+offset,50,30),(500+offset,50,30),(150+offset,100,30),(500+offset,100,30),(150+offset,150,30),
                          (500+offset,150,30),(150+offset,200,30),(500+offset,200,30),(150+offset,250,30)]
        self.lbl=pStore.appLabel(window,supplDetail)
        self.supEntryList=pStore.appEntrybox(window,supplyEntry)

    def destroy(self):
        self.lbl.destroy()
        self.supEntryList.destroy()
######################################################New Class
class childWindow():
    def __init__(self,arg1,arg2,arg3):
        self.popMessage = arg3
        self.childWin = pStore.fileData.createChild(arg1,arg2,'700x400')
        self.addGrid=supplierGrid(self.childWin)
        self.subButton=pStore.appButtons(self.childWin,[['SAVE',[150,300],[4,15]]])
        self.subButton.returnList[0]['command']=self.submitAction
        pStore.fileData.printLog(' '*2 + '-SV6- Add or Modify Supplier window was opened')

    def submitAction(self):
        pStore.fileData.modifySupplier(self.addGrid.supEntryList.getValues())
        messagebox.showinfo('Uma Store',self.popMessage,parent=self.childWin)
        self.childWin.withdraw()

######################################################New Class
class supplierWindow():
    def __init__(self,arg,arg1=None):
        self.supplierRoot=arg
        self.supplierName=arg1
        self.listLabel = [('List of Suppliers :',50,30),('Total Invoice Amount :',300,300),('Payment pending :',650,300)]
        self.invAmtText=[(430,300,20,1),(780,300,20,1)]
        self.treeConfig=[["0",'Id',80],["1",'Invoice NO',150],["2",'Date',120],["3",'Total Items',100],
                ["4",'Discount',100],["5",'CGST',100],["6",'SGST',100],["7",'Grand Total',100],["8",'Payment Pending',120]]
        self.buttonConfig=[ ['ADD SUPPLIER',[60,350],[4,15]],
                            ['CHANGE SUPPLIER',[260,350],[4,15]],
                            ['DELETE SUPPLIER',[460,350],[4,15]],
                            ['ADD INVOICE',[1060,450],[4,15]],
                            ['CLOSE PAGE',[1060,550],[4,15]]]
        self.suplSelection=None
        self.customize()

    def addSupplier(self):
        obj=childWindow(self.supplierRoot,'ADD SUPPLIER','Supplier Added Successfully')
        pStore.fileData.printLog(' '*2 + '-SV4- Add Supplier option')
    
    def changeSupplier(self):
        pStore.fileData.printLog(' '*2 + '-SV5- Modify Supplier option')
        if self.suplSelection is not None:
            obj=childWindow(self.supplierRoot,'CHANGE SUPPLIER','Supplier information modified Successfully')
            obj.addGrid.supEntryList.setValues(self.mainGrid.supEntryList.getValues())
        else:
            messagebox.showinfo('Uma Store','Please Select a Supplier First !!',parent=self.supplierRoot)

    def deleteSupplier(self):
        #obj=childWindow(self.supplierRoot,'DELETE SUPPLIER')
        pass

    def popSupplierPage(self,supplierName):
        self.mainGrid.supEntryList.setValues(pStore.fileData.returnSupplierInfo(supplierName)) #Populate supplier data
        vInvList = pStore.fileData.getInvoiceList(supplierName)
        self.invoiceObj.setValues(vInvList) # Populate invoice tree
        vAmount = 0;vPending=0
        for rec in vInvList:
            vAmount += pStore.fileData.fConvert(rec[7])
            vPending += pStore.fileData.fConvert(rec[8])
        self.invAmtEntry.setValues([round(vAmount,2),round(vPending,2)])
        pStore.fileData.printLog(' '*2 + '-SV2-'+supplierName+' - Invoice Tree is populated')

    def selectSupplierList(self,evt): #Click on any supplier
        w=evt.widget
        try:
            idx=int(w.curselection()[0])
            supClick = w.get(idx)
            self.suplSelection=supClick
            pStore.fileData.printLog(' '*2 + '-SV1-'+self.suplSelection+' Supplier Selected')
            self.popSupplierPage(self.suplSelection)
        except:
            supClick=None
            pStore.fileData.printLog(' '*2 + '-SV3-**Error in Supplier selection')

    def addInvoice(self):
        if self.suplSelection is not None:
            self.supplier_destroy()
            pStore.fileData.printLog(' '*2 + '-SV11- Add Invoice option clicked')
            obj = sInvoice.addInvoicePanel(self.supplierRoot, self.suplSelection, pStore.fileData.getConfigId('INVOICE_ID'),True) #Open invoice window for adding new invoice
        else:
            pStore.fileData.printLog(' '*2 + '-SV12- **Error, No Supplier selected for Add Invoice option')
            messagebox.showinfo('Uma Store','Please Select a Supplier First !!',parent=self.supplierRoot)

    def treeSelection(self,event):  # Double click on any invoice in Invoice tree
        curItem = self.invoiceObj.tView.focus()
        pStore.fileData.printLog(' '*2 + '-SV9- Double click on Invoice tree')
        try:
            tmp=self.invoiceObj.tView.item(curItem)['values'][0] #[Invoice ID] returned
            pStore.fileData.printLog(' '*2 + str(tmp) + '-SV10- Invoice ID seleted')
            self.supplier_destroy()
            obj = sInvoice.addInvoicePanel(self.supplierRoot,self.suplSelection,tmp) #Open invoice window to view one existing invoice
        except:
            pass

    def supplier_destroy(self):
        self.mainGrid.destroy()
        self.supLbl.destroy()
        self.invAmtEntry.destroy()
        self.supBut.destroy()
        self.supplierListbox.destroy()
        self.invoiceObj.destroy()

    def closePage(self):
        self.supplierRoot.withdraw()

    def customize(self):
        self.mainGrid=supplierGrid(self.supplierRoot,250)   # Populate Supplier info on primary page
        self.supLbl = pStore.appLabel(self.supplierRoot,self.listLabel)
        self.invAmtEntry=pStore.appEntrybox(self.supplierRoot,self.invAmtText)

        #Supplier list box
        self.supplierListbox=pStore.appListBox(self.supplierRoot,pStore.fileData.returnSupplierList(),[50,60],[15,30])
        self.supplierListbox.listObject.bind('<<ListboxSelect>>',self.selectSupplierList)

        #Populate buttons on primary page
        self.supBut=pStore.appButtons(self.supplierRoot,self.buttonConfig)
        self.supBut.returnList[0]['command']=self.addSupplier         #ADD SUPPLIER BUTTON
        self.supBut.returnList[1]['command']=self.changeSupplier      #MODIFY SUPPLIER BUTTON
        #butList[3]['command']=self.deleteSupplier          #DELETE SUPPLIER BUTTON
        self.supBut.returnList[3]['command']=self.addInvoice          #ADD INVOICE BUTTON
        self.supBut.returnList[4]['command']=self.closePage          #Close page

        #List all invoices that belong to a supplier
        self.invoiceObj=pStore.appTreeView(self.supplierRoot,self.treeConfig,[50,440])
        self.invoiceObj.tView.bind('<Double-1>',self.treeSelection) # Double click on any invoice in Invoice tree
        if self.supplierName is not None:
            self.popSupplierPage(self.supplierName)
            self.suplSelection = self.supplierName
