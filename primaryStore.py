import tkinter as tk
import os
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime as dt
## Code for creating Buttons
########################################################################
class fileData():
    supplierList={}
    itemList={}
    invoiceItemList={}
    invoiceList={}
    transList={}
    transItemList={}
    itemStockList={}
    config={}
    delim=';'
    custom = lambda x : str(x).replace(delim,',')
    FYarray = [['2020 APR - 2021 MAR','2020'],['2021 APR - 2022 MAR','2021'],['2022 APR - 2023 MAR','2022'],['2023 APR - 2024 MAR','2023'],['2024 APR - 2025 MAR','2024'],['2025 APR - 2026 MAR','2025']]
    monthList = [[('April, 2020','202004'),('May, 2020','202005'),('June, 2020','202006'),('July, 2020','202007'),('August, 2020','202008'),('September, 2020','202009'),('October, 2020','202010'),('November, 2020','202011'),('December, 2020','202012'),('January, 2021','202101'),('February, 2021','202102'),('March, 2021','202103')],
                 [('April, 2021','202104'),('May, 2021','202105'),('June, 2021','202106'),('July, 2021','202107'),('August, 2021','202108'),('September, 2021','202109'),('October, 2021','202110'),('November, 2021','202111'),('December, 2021','202112'),('January, 2022','202201'),('February, 2022','202202'),('March, 2022','202203')],
                 [('April, 2022','202204'),('May, 2022','202205'),('June, 2022','202206'),('July, 2022','202207'),('August, 2022','202208'),('September, 2022','202209'),('October, 2022','202210'),('November, 2022','202211'),('December, 2022','202212'),('January, 2023','202301'),('February, 2023','202302'),('March, 2023','202303')],
                 [('April, 2023','202304'),('May, 2023','202305'),('June, 2023','202306'),('July, 2023','202307'),('August, 2023','202308'),('September, 2023','202309'),('October, 2023','202310'),('November, 2023','202311'),('December, 2023','202312'),('January, 2024','202401'),('February, 2024','202402'),('March, 2024','202403')],
                 [('April, 2024','202404'),('May, 2024','202405'),('June, 2024','202406'),('July, 2024','202407'),('August, 2024','202408'),('September, 2024','202409'),('October, 2024','202410'),('November, 2024','202411'),('December, 2024','202412'),('January, 2025','202501'),('February, 2025','202502'),('March, 2025','202503')],
                 [('April, 2025','202504'),('May, 2025','202505'),('June, 2025','202506'),('July, 2025','202507'),('August, 2025','202508'),('September, 2025','202509'),('October, 2025','202510'),('November, 2025','202511'),('December, 2025','202512'),('January, 2026','202601'),('February, 2026','202602'),('March, 2026','202603')]
                ]
    fileSupplier='dataFile\\supplier.csv'
    fileItem='dataFile\\item-master.csv'
    fileItemStock='dataFile\\item-stock.csv'
    fileConfig='dataFile\\config.csv'
    fileInvoice=''
    fileInvoiceItem=''
    gstRate=2.5
    
    @classmethod
    def printLog(cls,dta):
        with open('umaStore.log','a') as filePtr:
            filePtr.write('{:%Y-%m-%d %H:%M:%S}'.format(dt.today())+' : '+str(dta)+'\n')

    @classmethod
    def fConvert(cls,var):
        var = str(var)
        if var.isalpha():
            return 0
        if '.' in var:
            if var.replace('.','').isdigit():
                return float(var)
            else:
                return 0
        if var.strip() == '':
            return 0
        if var.isdigit():
            return float(var)

    '''@classmethod
    def receiptPrint(cls,transID):
        cls.readTransactions()
        vFile = 'receipts\\R_'+str(transID)+'.txt'
        trn = cls.transList[str(transID)]
        with open(vFile,'w') as fp:
            fp.write('UMA MATCHING CENTER'+'\n')
            fp.write('CRP Square'+'\n')
            fp.write('GSTIN:12121212121212'+'\n')
            fp.write('\n' * 2)
            fp.write('Transaction number : '+str(transID)+'\n')
            fp.write('Transaction Date : '+str(trn[0])+'\n')
            fp.write('\n' * 2)
            fp.write('   Item      HSN      Qty     MRP    Discount    Final'+'\n')
            fp.write('-' * 100+'\n')
            for rec in cls.transItemList[str(transID)]:
                fp.write(str(rec[0])+str(rec[1])+str(rec[2])+str(rec[3])+str(rec[4])+str(rec[5])+ '  ' + str(rec[11]) + '  ' + str(rec[6]) + ' ' + str(rec[14]) + ' ' + str(rec[16])+'\n')
            fp.write('-' * 100+'\n')
            fp.write('Total Quantity'+str(trn[1])+'\n')
            fp.write('Total MRP'+str(trn[7])+'\n')
            fp.write('Discount'+str(trn[10])+'\n')
            fp.write('CGST'+str(trn[11])+'\n')
            fp.write('SGST'+str(trn[12])+'\n')
            fp.write('Amount Payable by Customer : '+str(trn[14])+'\n')

        print('Hahahah')'''

    @classmethod
    def receiptPrint(cls,transID):
        dText = { '1' : 'One', '2' : 'Two', '3' : 'Three', '4' : 'Four', '5' : 'Five', '6' : 'Six', '7' : 'Seven', '8' : 'Eight', '9' : 'Nine', '0' : 'Zero'}
        cls.readTransactions()
        vFile = 'receipts\\R_'+str(transID)+'.html'
        trn = cls.transList[str(transID)]
        with open(vFile,'w') as fp:
            fp.write('<html>'+'\n'+'<body>'+'\n')
            fp.write('<h2>'+8*'&nbsp '+'Uma Matching Center</h2>'+'\n')
            fp.write('<address>'+13*'&nbsp '+'Tathastu market Complex, CRP Square<br />'+18*'&nbsp '+'Bhubaneswar-12<br />'+15*'&nbsp '+'GST: 21ASIPP4739P1Z6</address>'+'\n')
            fp.write('<h6>'+ 40 * '-&nbsp; '+'<br />Transaction # :'+ 1 * '&nbsp; '+str(transID) + 6 * '&nbsp; ' +'Date: '+ trn[0].split(' ')[0] + 6 * '&nbsp; ' + 'Time: '+ trn[0].split(' ')[1] +'<br />')
            fp.write(40 * '-&nbsp; ' + '</h6>')

            fp.write('<pre>' + '\n' + 30 * '- '+'\n')
            fp.write('    Item Name'.ljust(20,' ')+'HSN'.ljust(10,' ')+'Qty'.ljust(6,' ')+'MRP'.ljust(6,' ')+'Disc'.ljust(6,' ')+'Final'.ljust(6,' ')+'\n')
            for rec in cls.transItemList[str(transID)]:
                vItm = str(rec[0][:4])+' '+str(rec[1][:4])+' '+str(rec[4][:4])+' '+str(rec[5][:4])
                fp.write(vItm.ljust(20,' ')+str(rec[3]).ljust(10,' ')+str(rec[11]).ljust(6,' ')+str(rec[6]).ljust(6,' ')+str(rec[14]).ljust(6,' ')+str(rec[17]).ljust(6,' ')+'\n')
            fp.write(30 * '- '+'\n')
            fp.write('Total Qty :  <strong>'+str(trn[1])+'</strong>'+'\n')
            fp.write('Total MRP:              <strong>'+str(trn[7])+'</strong>'+'\n')
            fp.write('Discount :              <strong>'+str(trn[10])+'</strong>'+'\n')
            fp.write(30 * '- '+'</pre>'+'\n')
            fp.write('<h3>Total'+ 30 * '&nbsp'+str(trn[14])+'</h3>'+'\n')
            
            [rup,pas] = str(trn[14]).split('.')
            vTxt=''
            for k in rup:
                vTxt += dText[k]+' '
            vTxt+= 'Rupees....'
            fp.write('<h5>'+vTxt+'</h5>'+'\n')

            fp.write('<pre>' + '\n' + 30 * '- '+'\n')
            fp.write('SGST      2.5%      '+str(trn[11])+'\n')
            fp.write('CGST      2.5%      '+str(trn[12])+'\n')
            fp.write(30 * '- '+'\n')
            fp.write('CASH : '+str(trn[14])+'\n')
            fp.write(30 * '- '+'\n')
            fp.write('Tender Amount : '+str(trn[14])+'\n')
            fp.write('Return Amount : 0'+'\n')
            fp.write(30 * '- '+'\n')
            fp.write('*Subject to the Bhubaneswar Jurisdiction only'+'\n')
            fp.write('*Exchange within 16 days against bill and Price Tag'+'\n')
            fp.write('*Exchange time 2.00 PM to 4.00 PM'+'\n')
            fp.write('*No Guarantee on color &amp; durability'+'\n')
            fp.write('*Every Monday Closed on .........Mob:'+'\n')
            fp.write(30 * '- '+'</pre>'+'\n')
        
        response = messagebox.askquestion("Print Receipt","Do you want to print the receipt ?",icon = 'question')
        if response == 'yes':
            #os.startfile('C:\\Python\\'+vFile,'print')
            os.startfile(vFile,'print')
    ########################################################################  Config Methods
    @classmethod
    def returnMonthList(cls):
        vFY=int(cls.getConfigId('FYIDX',0))
        return [rec[0] for rec in cls.monthList[vFY]]

    @classmethod            
    def getMonthYear(cls,val):
        vFY=int(cls.getConfigId('FYIDX',0))
        for rec in cls.monthList[vFY]:
            if rec[0] == val:
                return rec[1]
    
    @classmethod
    def setClassFiles(cls,fyVal=-1):
        if fyVal == -1:
            vStr=cls.FYarray[int(cls.getConfigId('FYIDX',0))][1]
        else:
            vStr=cls.FYarray[fyVal][1]
        cls.fileInvoice='dataFile\\invoice-summary'+vStr+'.csv'
        cls.fileInvoiceItem='dataFile\\invoice-item-List'+vStr+'.csv'
        cls.fileTransaction='dataFile\\trans-summary'+vStr+'.csv'
        cls.fileTransItem='dataFile\\transaction-item-List'+vStr+'.csv'
        cls.printLog(' '*4 + '-PS1- Invoice file selected ' + cls.fileInvoice)
        cls.printLog(' '*4 + '-PS2- Invoice Item file selected ' + cls.fileInvoiceItem)
        cls.printLog(' '*4 + '-PS3- Transaction file selected ' + cls.fileTransaction)
        cls.printLog(' '*4 + '-PS4- Transaction item file selected ' + cls.fileTransItem)

    @classmethod
    def returnFYidx(cls,fyVal):
        idx=-1
        for rec in cls.FYarray:
            idx+=1
            if rec[0] == fyVal:
                break
        return idx    
    
    @classmethod
    def readConfig(cls):
        with open(cls.fileConfig,'r') as fp:
            for rec in fp.readlines():
                if rec != '\n':
                    [k,v]=rec.rstrip('\n').split(':')
                    cls.config[k]=v

    @classmethod
    def getConfigId(cls,vKey,increment=1): #Provide a new generic Id from the config file
        cls.readConfig()
        vReturn=cls.config[vKey]
        if increment:
            cls.config[vKey] = int(cls.config[vKey]) + 1
        cls.updateConfig()
        return vReturn

    @classmethod
    def updateConfig(cls):
        with open(cls.fileConfig,'w') as fp:
            for [k,v] in cls.config.items():
                fp.write(k+':'+str(v)+'\n')
    ########################################################################SUPPIER Methods   
    @classmethod
    def readSupplier(cls):
        cls.printLog(' '*4 + '-PS5- readSupplier() -- Supplier file read')
        with open(cls.fileSupplier,'r') as fp:
            for rec in fp.readlines():
                vTmp=rec.rstrip('\n').split(cls.delim)
                cls.supplierList[vTmp[0]]=vTmp[1:]

    @classmethod
    def returnSupplierList(cls):
        if len(cls.supplierList) < 1:
            cls.readSupplier()
        tmp=[]
        for rec in cls.supplierList.keys():
            tmp.append(rec)
        tmp.sort()
        cls.printLog(' '*4 + '-PS6- returnSupplierList() -- Supplier List returned ' + str(tmp))
        return tmp

    @classmethod
    def returnSupplierInfo(cls,Supl):
        if len(cls.supplierList) < 1:
            cls.readSupplier()
        cls.printLog(' '*4 + '-PS7- returnSupplierInfo() -- Supplier Info returned ' + str(cls.supplierList[Supl][1:]))
        return [Supl]+cls.supplierList[Supl][1:]

    @classmethod
    def getSupplierkey(cls,vSupplier): # supplier name as input and return supplierId as output
        if len(cls.supplierList) < 1:
            cls.readSupplier()
        if vSupplier in cls.supplierList:
            cls.printLog(' '*4 + vSupplier + '-PS8- getSupplierkey() -- Supplier Id returned ' + cls.supplierList[vSupplier][0])
            return cls.supplierList[vSupplier][0]
        else:
            return ''

    @classmethod
    def modifySupplier(cls,item):
        if len(cls.supplierList) < 1:
            cls.readSupplier()
        if item[0] not in cls.supplierList.keys():
            vSuplId = cls.getConfigId('SUPPLIER_ID')
        else:
            vSuplId = cls.supplierList[item[0]][0]
        cls.supplierList[item[0]] = [vSuplId] + item[1:]
        cls.printLog(' '*4 + '-PS9- Values supplied ' + str(cls.supplierList[item[0]]))
        cls.writeSupplier()
    
    @classmethod
    def writeSupplier(cls):
        cls.printLog(' '*4 + '-PS10- getSupplierkey() -- Supplier Info written ')
        with open(cls.fileSupplier,'w') as fp:
            for idx in cls.supplierList.keys():
                fp.write(cls.delim.join(list(map(cls.custom,[idx]+cls.supplierList[idx])))+'\n')
    ########################################################################Trasaction Methods
    @classmethod
    def transSumryInfo(cls,invId):
        with open(cls.fileInvoice,'r') as fp:
            for rec in fp.readlines():
                if rec.startswith(str(invId)+cls.delim):
                    vTmp=rec.rstrip('\n').split(cls.delim)
                    return vTmp[2:]

    @classmethod
    def getTransHead(cls,vTransNum):
        with open(cls.fileTransaction,'r') as fp:
            for rec in fp.readlines():
                if rec.startswith(str(vTransNum)+cls.delim):
                    return rec.rstrip('\n').split(cls.delim)
        return []

    @classmethod
    def getTransItems(cls,vTransNum):
        vList=[]
        with open(cls.fileTransItem,'r') as fp:
            for rec in fp.readlines():
                if rec.startswith(str(vTransNum)+cls.delim):
                    vList.append(rec.rstrip('\n').split(cls.delim)[1:])
        return vList

    @classmethod
    def returnTransList(cls,vDate):
        vList=[]
        with open(cls.fileTransaction,'r') as fp:
            for rec in fp.readlines():
                vTmp=rec.rstrip('\n').split(cls.delim)
                if vTmp[0].startswith(vDate):
                    vTax = round(cls.fConvert(vTmp[12])+cls.fConvert(vTmp[13]),2)
                    vMargin = round(cls.fConvert(vTmp[14])-vTax-cls.fConvert(vTmp[7]),2)
                    vTPay = round(vMargin * 0.05,2)
                    vList.append(vTmp[:3]+[vTmp[7],vTmp[8],cls.fConvert(vTmp[9])+cls.fConvert(vTmp[11]),vTax,vTmp[14],vMargin,vTPay]) 
        return vList

    @classmethod
    def addNewTransaction(cls,vTrans,vTransItem):
        transNumber=vTrans[1]
        cls.printLog(' '*4 + '-PS31- addNewTransaction() -- Transaction info written ' + str(vTrans))
        cls.printLog(' '*4 + '-PS32- addNewTransaction() -- Transaction item info written ' + str(vTransItem))

        if cls.fConvert(vTrans[9]) > 0: # Check if total MRP is zero, since there could be deletion of only item in transaction. This needs to be replaced in file.
            with open(cls.fileTransaction,'r+') as fp:
                vLine=fp.readlines()
                fp.seek(0)
                for rec in vLine:
                    if not rec.startswith(str(transNumber)+cls.delim):
                        fp.write(rec)
                fp.truncate()
                tmp=str(transNumber)
                for itm in vTrans[2:]:
                    tmp+=cls.delim+str(itm)
                fp.write(tmp+'\n')

            with open(cls.fileTransItem,'r+') as fp:
                vLine=fp.readlines()
                fp.seek(0)
                for rec in vLine:
                    if not rec.startswith(str(transNumber)+cls.delim):
                        fp.write(rec)
                fp.truncate()
                for itm1 in vTransItem.values():
                    tmp=str(transNumber)
                    for itm2 in itm1:
                        tmp+=cls.delim+str(itm2)
                    fp.write(tmp+'\n')

    @classmethod
    def readTransactions(cls):
        cls.transList={}
        cls.transItemList={}
        with open(cls.fileTransaction,'r') as fp:
            for rec in fp.readlines():
                vTmp=rec.rstrip('\n').split(cls.delim)
                cls.transList[vTmp[0]]=vTmp[1:]

        with open(cls.fileTransItem,'r') as fp:
            for rec in fp.readlines():
                vTmp=rec.rstrip('\n').split(cls.delim)
                if str(vTmp[0]) not in cls.transItemList.keys():
                    cls.transItemList[str(vTmp[0])] = []
                cls.transItemList[str(vTmp[0])].append(vTmp[1:])
    ########################################################################INVOICE & Invoice Item Methods
    @classmethod
    def invoiceSumryInfo(cls,invId):
        with open(cls.fileInvoice,'r') as fp:
            for rec in fp.readlines():
                if rec.startswith(str(invId)+cls.delim):
                    cls.printLog(' '*4 + '-PS11- invoiceSumryInfo() -- Invoice info returned ')
                    return rec.rstrip('\n').split(cls.delim)[2:]

    @classmethod
    def getInvoice(cls,vInvId): # supplier name as input and return list of invoices as output
        with open(cls.fileInvoice,'r') as fp:
            for rec in fp.readlines():
                if rec.startswith(str(invId)+cls.delim):
                    cls.printLog(' '*4 + '-PS12- getInvoice() -- Invoice returned ' + str(rec))
                    return rec.rstrip('\n').split(cls.delim)[1:]
        return []

    @classmethod
    def getInvoiceList(cls,vSupplier): # supplier name as input and return list of invoices as output
        vSid=cls.getSupplierkey(vSupplier) #fetch supplier id
        vList=[]
        with open(cls.fileInvoice,'r') as fp:
            for rec in fp.readlines():
                vTmp=rec.rstrip('\n').split(cls.delim)
                if vTmp[1] == vSid:
                    vList.append([vTmp[0]]+vTmp[2:5]+[cls.fConvert(vTmp[5])+cls.fConvert(vTmp[9])+cls.fConvert(vTmp[11])]+vTmp[14:17]+[cls.fConvert(vTmp[16])-cls.fConvert(vTmp[18])])
        cls.printLog(' '*4 + '-PS13- getInvoiceList() -- Invoice list returned ')
        for rec in vList:
            cls.printLog(' '*6 + 'InvoiceID:['+str(rec[0])+'] Invoice Number:['+str(rec[1])+'] Invoice Date:['+str(rec[2])+'] Qty:['+str(rec[3])+'] Total Disc:['+str(rec[4])+'] CGST:['+str(rec[5])+'] SGST:['+str(rec[6])+'] Grand Total:['+str(rec[7])+'] Payment Pending:['+str(rec[8])+']')
        return vList

    @classmethod
    def getInvoiceItems(cls,val): # INVOICE_ID as input and list of invoice items as output
        vList=[]
        with open(cls.fileInvoiceItem,'r') as fp:
            for rec in fp.readlines():
                if rec.startswith(str(val)+cls.delim):
                    vList.append(rec.rstrip('\n').split(cls.delim)[1:])
        cls.printLog(' '*4 + '-PS14- getInvoiceItems() -- Invoice item list returned as follows:' )
        for rec in vList:
            cls.printLog(' '*6 + 'ItemId:['+str(rec[0])+'] Size:['+str(rec[1])+'] Box Qty:['+str(rec[2])+'] Color:['+str(rec[3])+'] MRP:['+str(rec[4])+'] Price/Box:['+str(rec[5])+'] Total Price:['+str(rec[6])+'] Discount %:['+str(rec[7])+'] Disc AMount:['+str(rec[8])+'] CGST:['+str(rec[9])+'] SGST:['+str(rec[10])+'] Grand Total:['+str(rec[11])+'] Total Qty:['+str(rec[12])+'] Unit Price:['+str(rec[13])+'] Unit Disc:['+str(rec[14])+'] Unit CGST:['+str(rec[15])+'] Unit SGST:['+str(rec[16])+'] None:['+str(rec[17])+'] Box size:['+str(rec[18])+']')
        return vList

    @classmethod
    def addNewInvoice(cls,vKey,vHead,vDetail):
        cls.printLog(' '*4 + '-PS15- addNewInvoice() -- Invoice info written ' + str( vHead))
        cls.printLog(' '*4 + '-PS16- addNewInvoice() -- Invoice item info written ' + str( vDetail))
        if cls.fConvert(vHead[3]) > 0:
            with open(cls.fileInvoice,'r+') as fp:
                vLine=fp.readlines()
                fp.seek(0)
                for rec in vLine:
                    if not rec.startswith(str(vKey)+cls.delim):
                        fp.write(rec)
                fp.truncate()
                tmp=str(vKey)
                for itm in [cls.getSupplierkey(vHead[0])]+vHead[1:]+[cls.gstRate]:
                    tmp+=cls.delim+str(itm)
                fp.write(tmp+'\n')

            with open(cls.fileInvoiceItem,'r+') as fp:
                vLine=fp.readlines()
                fp.seek(0)
                for rec in vLine:
                    if not rec.startswith(str(vKey)+cls.delim):
                        fp.write(rec)
                fp.truncate()
                for itm1 in vDetail:
                    tmp=str(vKey)
                    for itm2 in itm1[1:]:
                        tmp+=cls.delim+str(itm2)
                    fp.write(tmp+'\n')

    ########################################################################ITEM Methods
    @classmethod
    def readItem(cls):  
        cls.printLog(' '*4 + '-PS17- readItem()')
        with open(cls.fileItem,'r') as fp:
            for rec in fp.readlines():
                vTmp=rec.rstrip('\n').split(cls.delim)
                cls.itemList[str(vTmp[0])]=vTmp[1:]

    @classmethod
    def returnItemList(cls,vBrand): #Provide a list of items as output with Brand name as input
        cls.readItem()
        vTmp=[]
        for rec in cls.itemList.values():
            if rec[0] == vBrand:
                if rec[2] == '':
                    vTmp.append(rec[1])
                else:
                    vTmp.append(rec[1]+':'+str(rec[2]))
        if vTmp is not None:
            vTmp.sort()
        cls.printLog(' '*4 + '-PS18- returnItemList() - Item list returned ' + str(vTmp))
        return vTmp

    @classmethod
    def getItemKey(cls,val):  # brand and item name + model no or item name , model no as input and list key as output #Need Change
        cls.readItem()
        vBrand = val[0]
        cls.printLog(' '*4 + '-PS19- getItemKey() - Item value passed ' + str(val))
        if len(val) == 3:
            [vItem,vModel] = val[1:]
        else:
            if ':' in val[1]:
                [vItem,vModel] = val[1].split(':')
            else:
                vItem = val[1]
                vModel=''
        for k in cls.itemList.keys():
            if cls.itemList[k][:3] == [vBrand,vItem,vModel]:
                cls.printLog(' '*4 + '-PS20- getItemKey() - Item Id returned ' + str(k))
                return k

    @classmethod
    def writeItem(cls):  
        with open(cls.fileItem,'w') as fp:
            for idx in cls.itemList.keys():
                fp.write(cls.delim.join(list(map(cls.custom,[idx]+cls.supplierList[idx])))+'\n')

    @classmethod
    def addNewBrand(cls,vBrand):
        if len(vBrand) != 0:
            if vBrand not in [f[0] for f in list(cls.itemList.values())]:
                cls.itemList[cls.getConfigId('ITEM_ID')]=[vBrand,vBrand,'','']
                cls.writeItem()
                return True
            else:
                messagebox.showinfo('Uma Store','Brand already exists in list')
                return False
        else:
            return False

    @classmethod
    def addNewItem(cls,vList):
        if len(vList[0]) != 0 and len(vList[1]) != 0:
            if vList[:3] not in [[f[:3]] for f in list(cls.itemList.values())]:
                cls.itemList[cls.getConfigId('ITEM_ID')]=vList
                cls.writeItem()
                return True
            else:
                messagebox.showinfo('Uma Store','Item already exists in list')
                return False
        else:
            return False
    ########################################################################ITEM STOCK Methods
    @classmethod
    def readItemStock(cls):
        with open(cls.fileItemStock,'r') as fp:
            for rec in fp.readlines():
                vTmp=rec.rstrip('\n').split(cls.delim)
                cls.itemStockList[vTmp[0]]=vTmp[1:]

    @classmethod
    def itemTreeList(cls,vItemId=0): #input is ITEM_ID key and out put is list of stock entries
        cls.readItem()
        cls.readItemStock()
        vTmp=[];cnt=1
        for k in cls.itemStockList.keys():
            rec=cls.itemStockList[str(k)]
            stockRec = rec[1:8]+[rec[9],rec[8]]
            if vItemId == 0:
                itm=cls.itemList[str(rec[0])]
                vTmp.append([k]+itm[:4]+ stockRec)
                cnt +=1
            if rec[0] == vItemId:
                itm=cls.itemList[str(vItemId)]
                vTmp.append([k]+itm[:4]+stockRec)
            if cnt > 50:
                break
        if len(vTmp) == 0 and vItemId != 0:
            itm=cls.itemList[str(vItemId)]
            vTmp.append([0]+itm[:4]+[]*7)
        return vTmp

    @classmethod
    def itemStockSync(cls):
        cls.readItemStock()
        for k in cls.itemStockList.keys():
            rec = cls.itemStockList[k]
            rec[10] = rec[4]
            rec[11] = rec[7]
        cls.printLog(' '*4 + '-PS21- itemStockSync()')
        cls.writeItemStock()

    @classmethod
    def itemTransSync(cls):
        cls.readItemStock()
        for k in cls.itemStockList.keys():
            rec = cls.itemStockList[k]
            rec[12] = rec[5]
        cls.printLog(' '*4 + '-PS22- itemTransSync()')
        cls.writeItemStock()

    @classmethod
    def adjustStockInvoice(cls,InvoiceId,modList):
        cls.printLog(' '*4 + '-PS25- adjustStockInvoice() for invoiceID - ' + str(InvoiceId))
        cls.printLog(' '*4 + '-PS25A- adjustStockInvoice() Modified item list passed - ' + str(modList))
        cls.readItemStock()
        vInv=cls.getInvoice(str(InvoiceId))
        itemList=cls.getInvoiceItems(str(InvoiceId))

        #Stock Adjustment
        for rec in itemList:
            # Adjust unit price after first inv discount and item discount
            tmp = cls.fConvert(rec[13]) - cls.fConvert(rec[14])  # (Unit Price - Unit Discount)
            tmpDisc1 = round(tmp * cls.fConvert(vInv[7])/100,2)
            # Adjust unit price after second inv discount and item discount
            tmp = cls.fConvert(rec[13]) - cls.fConvert(rec[14]) - tmpDisc1
            tmpDisc2 = round(tmp * cls.fConvert(vInv[9])/100,2)
            
            #tracing item in modified list
            m=cls.changeItemMatchup([rec[0],rec[1],rec[3],rec[4],rec[13]],modList)
            if m != -2:
                if m == -1:
                    deltaDisc = (cls.fConvert(rec[14]) + tmpDisc1 + tmpDisc2) * cls.fConvert(rec[12])
                    deltaQty  = cls.fConvert(rec[12])
                else:
                    deltaDisc = (cls.fConvert(rec[14]) + tmpDisc1 + tmpDisc2) * cls.fConvert(rec[12]) - cls.fConvert(modList[m][9])
                    deltaQty  = cls.fConvert(rec[12]) - cls.fConvert(modList[m][13])

                #Getting stock record
                k = cls.stockMatchup([rec[0],rec[1],rec[3],rec[4],rec[13]]) #Search by - ITEM_ID, Size, Color, MRP, #Unit Price#
                if k == -1:
                    k=cls.getConfigId('STOCK_ID')
                    cls.itemStockList[k] = [rec[0],rec[1],rec[3],rec[4],0,0,rec[13]]+[0]*6 #[item_id,Size,Color,MRP,Inv Qty, Sold Qty, Unit Price...]
                vStock=cls.itemStockList[k]
                cls.printLog(' '*6 + '-PS27- Before Stock Adjustment - itemStockId:['+str(k)+'] ItemId:['+str(vStock[0])+'] Size:['+str(vStock[1])+'] Color:['+str(vStock[2])+'] MRP:['+str(vStock[3])+'] Invoice Qty:['+str(vStock[4])+'] Sold Qty:['+str(vStock[5])+'] Unit Price:['+str(vStock[6])+'] Unit Disc:['+str(vStock[7])+'] Total GST:['+str(vStock[8])+'] Final Price:['+str(vStock[9])+'] Prev Qty:['+str(vStock[10])+'] Prev Disc:['+str(vStock[11])+'] Prev Sold Qty:['+str(vStock[12])+']')

                vStock[4] = cls.fConvert(vStock[10]) + deltaQty #Adding Stock quantity
                varQuant = cls.fConvert(vStock[10])-cls.fConvert(vStock[12]) #What is previous available Quant
                if varQuant < 0:
                    varQuant = 0
                #Avveraging Disocunt - (existing prod of disc,quant + incoming prod of disc,quant) / (existing quant + incoming quant))
                if (varQuant + deltaQty) == 0:
                    vStock[7] = 0
                else:
                    vStock[7] = round((varQuant * cls.fConvert(vStock[11]) + deltaDisc) / (varQuant + deltaQty),2)
                vStock[8] = round((cls.fConvert(vStock[6]) - cls.fConvert(vStock[7])) * 0.05,2) # Calculating GST amount (CGST + SGST)
                vStock[9] = round(cls.fConvert(vStock[6])  - cls.fConvert(vStock[7]),2) #+ cls.fConvert(vStock[8]) # Final price
            
                cls.printLog(' '*6 + '-PS29- After  Stock Adjustment - itemStockId:['+str(k)+'] ItemId:['+str(vStock[0])+'] Size:['+str(vStock[1])+'] Color:['+str(vStock[2])+'] MRP:['+str(vStock[3])+'] Invoice Qty:['+str(vStock[4])+'] Sold Qty:['+str(vStock[5])+'] Unit Price:['+str(vStock[6])+'] Unit Disc:['+str(vStock[7])+'] Total GST:['+str(vStock[8])+'] Final Price:['+str(vStock[9])+'] Prev Qty:['+str(vStock[10])+'] Prev Disc:['+str(vStock[11])+'] Prev Sold Qty:['+str(vStock[12])+']')
                cls.printLog(' '*6 + '-'*25 )

        #Stock Reversal
        cls.printLog(' '*4 + '-PS30- adjustStockInvoice() Looking for any deletion from item stock')
        for rec in [t for t in modList if len(t) > 6]:
            mKey=[rec[1],rec[2],rec[4],rec[5],rec[14]]
            m=cls.changeItemMatchup(mKey,itemList,'ITEM')
            if m == -1:
                cls.printLog(' '*4 + '-PS30A- adjustStockInvoice() Revering the item from stock - ' + str(mKey))

                #Getting stock record
                k = cls.stockMatchup(mKey) #Search by - ITEM_ID, Size, Color, MRP, #Unit Price#
                if k != -1:
                    vStock=cls.itemStockList[k]
                    cls.printLog(' '*6 + '-PS30B- Before Stock Reversal - itemStockId:['+str(k)+'] ItemId:['+str(vStock[0])+'] Size:['+str(vStock[1])+'] Color:['+str(vStock[2])+'] MRP:['+str(vStock[3])+'] Invoice Qty:['+str(vStock[4])+'] Sold Qty:['+str(vStock[5])+'] Unit Price:['+str(vStock[6])+'] Unit Disc:['+str(vStock[7])+'] Total GST:['+str(vStock[8])+'] Final Price:['+str(vStock[9])+'] Prev Qty:['+str(vStock[10])+'] Prev Disc:['+str(vStock[11])+'] Prev Sold Qty:['+str(vStock[12])+']')

                    vStock[4] = cls.fConvert(vStock[10]) - cls.fConvert(rec[13]) #deducting Stock quantity
                    varQuant = cls.fConvert(vStock[10]) - cls.fConvert(vStock[12]) #What is previous available Quant
                    if varQuant < 0:
                        varQuant = 0
                    #Avveraging Disocunt - (existing prod of disc,quant + incoming prod of disc,quant) / (existing quant + incoming quant))
                    if (varQuant - cls.fConvert(rec[13])) == 0:
                        vStock[7] = 0
                    else:
                        vStock[7] = round((varQuant * cls.fConvert(vStock[11]) + cls.fConvert(rec[9])) / (varQuant - cls.fConvert(rec[13])),2)
                    vStock[8] = round((cls.fConvert(vStock[6]) - cls.fConvert(vStock[7])) * 0.05,2) # Calculating GST amount (CGST + SGST)
                    vStock[9] = round(cls.fConvert(vStock[6])  - cls.fConvert(vStock[7]),2) #+ cls.fConvert(vStock[8]) # Final price

                    cls.printLog(' '*6 + '-PS29- After  Stock Reversal - itemStockId:['+str(k)+'] ItemId:['+str(vStock[0])+'] Size:['+str(vStock[1])+'] Color:['+str(vStock[2])+'] MRP:['+str(vStock[3])+'] Invoice Qty:['+str(vStock[4])+'] Sold Qty:['+str(vStock[5])+'] Unit Price:['+str(vStock[6])+'] Unit Disc:['+str(vStock[7])+'] Total GST:['+str(vStock[8])+'] Final Price:['+str(vStock[9])+'] Prev Qty:['+str(vStock[10])+'] Prev Disc:['+str(vStock[11])+'] Prev Sold Qty:['+str(vStock[12])+']')
            cls.printLog(' '*6 + '-'*25 )
        cls.writeItemStock()

    @classmethod
    def adjustStockTrans(cls,transNum,modList):
        cls.readItemStock()
        for rec in cls.getTransItems(str(transNum)):
            #tracing item in modified list
            #m=cls.changeTransMatchup([rec[19]]+rec[4:8],[[t]+modList[t] for t in modList.keys()])
            m=cls.changeTransMatchup([rec[19]]+rec[4:8],modList)
            if m != -2:
                if m == -1:
                    deltaQty  = cls.fConvert(rec[11])
                else:
                    deltaQty  = cls.fConvert(rec[11]) - cls.fConvert(modList[m][5])

                #Getting stock record
                k = cls.stockMatchup([rec[19]]+rec[4:8]) #Search by - ITEM_ID, Size, Color, MRP, #Unit Price#
                if k == -1:
                    k=cls.getConfigId('STOCK_ID')
                    cls.itemStockList[vKey] = [vItemId]+rec[4:7]+[0,0,rec[8]]+[0]*6 #[item_id,Size,Color,MRP,Inv Qty, Sold Qty, Unit Price...]
                vStock=cls.itemStockList[k]
                cls.printLog(' '*6 + '-PS50- Before Stock Adjustment - itemStockId:['+str(k)+'] ItemId:['+str(vStock[0])+'] Size:['+str(vStock[1])+'] Color:['+str(vStock[2])+'] MRP:['+str(vStock[3])+'] Invoice Qty:['+str(vStock[4])+'] Sold Qty:['+str(vStock[5])+'] Unit Price:['+str(vStock[6])+'] Unit Disc:['+str(vStock[7])+'] Total GST:['+str(vStock[8])+'] Final Price:['+str(vStock[9])+'] Prev Qty:['+str(vStock[10])+'] Prev Disc:['+str(vStock[11])+'] Prev Sold Qty:['+str(vStock[12])+']')
                vStock[5] = cls.fConvert(vStock[12]) + deltaQty #Adding Sold quantity                
                cls.printLog(' '*6 + '-PS51- After  Stock Adjustment - itemStockId:['+str(k)+'] ItemId:['+str(vStock[0])+'] Size:['+str(vStock[1])+'] Color:['+str(vStock[2])+'] MRP:['+str(vStock[3])+'] Invoice Qty:['+str(vStock[4])+'] Sold Qty:['+str(vStock[5])+'] Unit Price:['+str(vStock[6])+'] Unit Disc:['+str(vStock[7])+'] Total GST:['+str(vStock[8])+'] Final Price:['+str(vStock[9])+'] Prev Qty:['+str(vStock[10])+'] Prev Disc:['+str(vStock[11])+'] Prev Sold Qty:['+str(vStock[12])+']')
                cls.printLog(' '*6 + '-'*25 )
        cls.writeItemStock()

    @classmethod
    def changeTransMatchup(cls,vList,modList):
        returnKey = -1;k=0
        for r in modList.keys():
            if modList[r][:6] == vList:
                if len(modList[r]) < 6:
                    returnKey = -2
                else:
                    returnKey = r
        return returnKey
            
    @classmethod  
    def changeItemMatchup(cls,vList,modList,vType='MOD',lim=7): # Check is item stock entry exists or not vLIst = [item_id,size,color,MRP,unit_price]
        returnKey = -1;k=0
        cls.printLog(' '*4 + '-PS23A- changeItemMatchup() for ' + str(vList))
        for rec in modList:
            if vType == 'MOD':
                if len(rec) < lim:
                    [itemId,size,color,MRP,uPrice]=rec[1:]
                else:
                    [itemId,size,color,MRP,uPrice]=rec[1:3]+rec[4:6]+[rec[14]]
            else:
                [itemId,size,color,MRP,uPrice]=rec[:2]+rec[3:5]+[rec[13]]
            if str(itemId) == str(vList[0]): #Item_id
                if size == vList[1]:       #size
                    if color == vList[2]:   #color
                        if abs(cls.fConvert(MRP) - cls.fConvert(vList[3])) < 0.5:     #MRP
                            if abs(cls.fConvert(uPrice) - cls.fConvert(vList[4])) < 0.5: #Unit Price
                                if len(modList[k]) < lim:
                                    returnKey = -2
                                else:
                                    returnKey = k
            k+=1

        cls.printLog(' '*4 + '-PS24A- changeItemMatchup() Key returned ' + str(returnKey))
        return returnKey

    @classmethod  
    def stockMatchup(cls,vList): # Check is item stock entry exists or not vLIst = [item_id,size,color,MRP,unit_price]
        returnKey = -1
        cls.printLog(' '*4 + '-PS23- stockMatchup() for ' + str(vList))
        for k in cls.itemStockList.keys():
            rec = cls.itemStockList[k]
            if str(rec[0]) == str(vList[0]): #Item_id
                if rec[1] == vList[1]:       #size
                    if rec[2] == vList[2]:   #color
                        if abs(cls.fConvert(rec[3]) - cls.fConvert(vList[3])) < 0.5:     #MRP
                            if abs(cls.fConvert(rec[6]) - cls.fConvert(vList[4])) < 0.5: #Unit Price
                                returnKey = k
        cls.printLog(' '*4 + '-PS24- stockMatchup() Key returned ' + str(returnKey))
        return returnKey

    @classmethod
    def writeItemStock(cls):
        #print(cls.itemStockList)
        with open(cls.fileItemStock,'w') as fp:
            for idx in cls.itemStockList.keys():
                tmp=str(idx)
                for rec in cls.itemStockList[idx]:
                    tmp+=cls.delim+str(rec)
                fp.write(tmp+'\n')
########################################################################
## Code for creating Child window
########################################################################
class childFrame():
    def __init__(self,arg1,arg2,arg3='1100x650'):
        self.childRoot=tk.Toplevel(arg1)
        self.childRoot.title(arg2)
        self.childRoot.geometry(arg3)

## Code for creating Buttons
########################################################################
class appButtons():
    def __init__(self,arg1,arg2):
        self.window=arg1
        self.butLIst=arg2
        self.returnList=[]
        self.populateButton()

    def populateButton(self):
        for k in self.butLIst:
            tmp=tk.Button(self.window, text=k[0])
            tmp.place(x=k[1][0],y=k[1][1])
            tmp.config(height=k[2][0],width =k[2][1])
            self.returnList.append(tmp)
    
    def destroy(self):
        for wid in self.returnList:
            wid.destroy()
## Code for creating Labels
########################################################################
class appLabel():
    def __init__(self,arg1,arg2):
        self.window=arg1
        self.labelLIst=arg2
        self.returnList=[]
        self.populateLabel()

    def populateLabel(self):
        for k in self.labelLIst:
            tmp=tk.Label(self.window, text=k[0])
            tmp.place(x=k[1],y=k[2])
            self.returnList.append(tmp)

    def destroy(self):
        for wid in self.returnList:
            wid.destroy()
## Code for creating ListBoxes
########################################################################
class appListBox():
    def __init__(self,arg1,arg2,arg3):
        self.window=arg1
        self.cord=arg3
        self.createListbox()
        self.listPopulate(arg2)

    def createListbox(self):
        self.listObject=tk.Listbox(self.window,
                        height = 10,  
                        width  = 20,  
                        activestyle = 'dotbox',  
                        font = "Calibri")
        self.listObject.place(x=self.cord[0],y=self.cord[1])

    def listPopulate(self,vList):
        self.listObject.delete(0,tk.END)
        cnt=1
        for idx in vList:
            self.listObject.insert(cnt,idx)
            cnt+=1
    
    def destroy(self):
        self.listObject.destroy()
    
## Code for creating Entry boxes
########################################################################
class appEntrybox():
    def __init__(self,arg1,arg2):
        self.window=arg1
        self.entryList=arg2
        self.returnList=[]
        self.objList=[]
        self.createEntrybox()

    def createEntrybox(self):
        for k in self.entryList:
            vWidth = k[2] if len(k) > 2 else 20
            vStat= k[3] if len(k) > 3 else 0
            tmp=tk.StringVar()
            vEnt=tk.Entry(self.window,
                     textvariable=tmp,
                     width=vWidth)
            vEnt.place(x=k[0],y=k[1])
            if vStat:
                vEnt['state'] = tk.DISABLED
            self.returnList.append(tmp)
            self.objList.append(vEnt)

    def getValues(self):
        tmpList=[]
        for rec in self.returnList:
            tmpList.append(rec.get())
        return tmpList

    def setValues(self,valList):
        for i in range(len(self.returnList)):
            self.returnList[i].set(valList[i])
    
    def destroy(self):
        for wid in self.objList:
            wid.destroy()
## Code for creating TreeView
########################################################################
class appTreeView():
    def __init__(self,arg1,arg2,arg3):
        self.window=arg1
        self.columnList=arg2
        self.cord=arg3
        #self.returnList=[]
        self.createTree()

    def createTree(self):        
        self.tView = ttk.Treeview(self.window)
        self.tView.place(x=self.cord[0], y=self.cord[1])
        self.tView ["columns"] = [k[0] for k in self.columnList]
        self.tView ['show'] = 'headings'
        for k in self.columnList:
            self.tView.column(k[0], width = k[2],anchor ='c')
            self.tView.heading(k[0], text = k[1])

    def resetValues(self):
        for i in self.tView.get_children():
            self.tView.delete(i)

    def setValues(self,valList,singelVal=[]):
        self.resetValues()
        for rec in valList:
            self.tView.insert("",'end',text='',values=singelVal+rec)
    
    def destroy(self):
        self.tView.destroy()
## Code for creating DropDown
########################################################################
class appDropDown():
    def __init__(self,arg1,arg2,arg3,arg4,arg5=False):
        self.window=arg1
        self.dText=arg2
        self.valueList=arg3
        self.cord=arg4        #[x co-ord, y co-ord, width, default val]
        if arg5:        # If True then arg4[3] is index else value
            self.default = self.cord[3] 
        else:
            self.default = self.getIdx(self.cord[3])
        self.createDropDown()

    def getIdx(self,val):
        i=0
        for rec in self.valueList:
            if rec == val:
                return i
            i += 1

    def createDropDown(self):
        self.dropObject = ttk.Combobox(self.window, width = self.cord[2], textvariable = self.dText)
        self.dropObject['values'] = self.valueList
        self.dropObject.current(self.default)
        self.dropObject.place(x=self.cord[0],y=self.cord[1])        

    def getValue(self):
        return self.dropObject.get()

    def setValue(self,val,flg=False):
        if flg:
            self.dropObject.current(val)
        else:
            self.dropObject.current(self.getIdx(val))
    
    def destroy(self):
        self.dropObject.destroy()