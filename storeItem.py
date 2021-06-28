import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import primaryStore as pStore
import primaryItem as pItem

class brandItemWindow():

    def __init__(self,arg1):
        self.itemRoot = arg1
        pStore.fileData.readConfig()
        self.addButton=[['ADD BRAND',[100,280],[1,10]],
                        ['CHANGE ITEM',[300,280],[1,11]],
                        ['ADD ITEM',[500,280],[1,10]]]
        pStore.fileData.printLog('-'*10 +'ITM1- Item object initialized'+'-'*10)
        self.customize()

    def newBrandSubmit(self):
        if pStore.fileData.addNewBrand(self.brandEntry.getValues()[0]): #do following only when brand add is a success
            self.itemObject.brandListRefresh()
            self.newBrand.withdraw()

    def newItemSubmit(self):
        if pStore.fileData.addNewItem(self.itemEntry.getValues()): #do following only when item add is a success
            self.itemObject.brandItemListRefresh()
            self.newItem.withdraw()

    def changedItemSubmit(self):
        pStore.fileData.itemList[self.vKeyItem]=self.itemChange.getValues()
        pStore.fileData.writeItem()
        self.itemObject.brandItemListRefresh()
        self.oldItem.withdraw()

    def addBrand(self):
        self.newBrand=pStore.fileData.createChild(self.itemRoot,'ADD BRAND','300x200')
        pStore.appLabel(self.newBrand,[('New Brand :',20,50)])
        self.brandEntry=pStore.appEntrybox(self.newBrand,[(100,50)])
        oBrand=pStore.appButtons(self.newBrand,[['SUBMIT',[50,100],[2,15]]])
        oBrand.returnList[0]['command']=self.newBrandSubmit

    def addItem(self):
        if self.itemObject.brandVal == None:
            messagebox.showinfo('Uma Store','Select a Brand to add Item')
        else:
            self.newItem=pStore.fileData.createChild(self.itemRoot,'ADD ITEM','400x300')
            pStore.appLabel(self.newItem,[('Brand :',50,50),('Item name :',50,100),('Model No :',50,150),('HSN Code :',50,200)])
            self.itemEntry=pStore.appEntrybox(self.newItem,[(150,50,20,1),(150,100),(150,150),(150,200)])
            self.itemEntry.setValues([self.itemObject.brandVal,'','',''])
            obj=pStore.appButtons(self.newItem,[['SUBMIT',[150,250],[2,15]]])
            obj.returnList[0]['command']=self.newItemSubmit

    def changeItem(self):
        if self.itemObject.itemVal == None:
            messagebox.showinfo('Uma Store','Select an Item to change')
        else:
            self.oldItem=pStore.fileData.createChild(self.itemRoot,'CHANGE ITEM','400x300')
            pStore.appLabel(self.oldItem,[('Brand :',50,50),('Item name :',50,100),('Model No :',50,150),('HSN Code :',50,200)])
            self.itemChange=pStore.appEntrybox(self.oldItem,[(150,50,20,1),(150,100),(150,150),(150,200)])
            self.vKeyItem=pStore.fileData.getItemKey([self.itemObject.brandVal,self.itemObject.itemVal])
            self.itemChange.setValues(pStore.fileData.itemList[self.vKeyItem])
            obj=pStore.appButtons(self.oldItem,[['SUBMIT',[150,250],[2,15]]])
            obj.returnList[0]['command']=self.changedItemSubmit
                
    def customize(self):
        #self.itemRoot.title("Uma Store Brand and Item Frame")
        #self.itemRoot.geometry('1100x650')
        self.itemObject=pItem.itemSearchPanel(self.itemRoot)
        obj=pStore.appButtons(self.itemRoot,self.addButton)
        
        obj.returnList[0]['command']=self.addBrand
        obj.returnList[1]['command']=self.changeItem
        obj.returnList[2]['command']=self.addItem
        self.itemRoot.mainloop()

