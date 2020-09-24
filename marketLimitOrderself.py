from datetime import datetime


askSize={}
bidSize={}

class sellPrice:
    def __init__(self):
        self.data=set()
        self.size=0
    def push(self,e,shares):
        e=float(e)
        if self.size==0:
            self.data.add(e)
            self.size+=1
            askSize[e]=shares
        else:
            if e in self.data:
                askSize[e]+=shares
            else:
                self.data.add(e)
                self.size+=1
                askSize[e]=shares
    def pop(self,e,shares):
        e=float(e)
        if e in self.data:
            if shares>=askSize[e]:
                askSize[e]=0
                self.data.discard(e)
                self.size-=1
            else:
                askSize[e]-=shares

class buyPrice:
    def __init__(self):
        self.data=set()
        self.size=0
    def push(self,e,shares):
        e=float(e)
        if self.size==0:
            self.data.add(e)
            self.size+=1
            bidSize[e]=shares
        else:
            if e in self.data:
                bidSize[e]+=shares
            else:
                self.data.add(e)
                self.size+=1
                bidSize[e]=shares
    def pop(self,e,shares):
        e=float(e)
        if e in self.data:
            if shares>=bidSize[e]:
                bidSize[e]=0
                self.data.discard(e)
                self.size-=1
            else:
                bidSize[e]-=shares



def createMarketOrder(bORs,shares):
    if bORs == 'b':
        if sp.size>0:
            if askSize[min(sp.data)]>=shares:
                f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from ASK listing priced at '+str(min(sp.data))+'\n')
                sp.pop(min(sp.data),shares)
                shares=0
                
            else:
                while sp.size>0 and shares>0:
                    if askSize[min(sp.data)]>=shares:
                        f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from ASK listing priced at '+str(min(sp.data))+'\n')
                        sp.pop(min(sp.data),shares)
                        shares=0
                    else:
                        f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(askSize[min(sp.data)])+' removed from ASK listing priced at '+str(min(sp.data))+'\n')
                        shares-=askSize[min(sp.data)]
                        sp.pop(min(sp.data),askSize[min(sp.data)])
    if bORs=='s':
        if bp.size>0:
            if bidSize[max(bp.data)]>=shares:
                f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from BID listing priced at '+str(max(bp.data))+'\n')
                bp.pop(max(bp.data),shares)
                shares=0
            else:
                while bp.size>0 and shares>0:
                    if bidSize[max(bp.data)]>=shares:
                        f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from BID listing priced at '+str(max(bp.data))+'\n')
                        bp.pop(max(bp.data),shares)
                        shares=0
                    else:
                        f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(bidSize[max(bp.data)])+' removed from BID listing priced at '+str(max(bp.data))+'\n')
                        shares-=bidSize[max(bp.data)]
                        bp.pop(max(bp.data),bidSize[max(bp.data)])

def createLimitOrder(bORs,shares,price):
    if bORs == 'b':
        if sp.size>0:
            if askSize[min(sp.data)]>=shares and min(sp.data)<=price:
                f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from ASK listing priced at '+str(min(sp.data))+'\n')
                sp.pop(min(sp.data),shares)
                shares=0
        flag=True
        while sp.size>0 and shares>0 and flag:
            if askSize[min(sp.data)]>=shares and min(sp.data)<=price:
                f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from ASK listing priced at '+str(min(sp.data))+'\n')
                sp.pop(min(sp.data),shares)
                shares=0
                break
            if askSize[min(sp.data)]<shares and min(sp.data)<=price:
                temp=shares
                f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(askSize[min(sp.data)])+' removed from ASK listing priced at '+str(min(sp.data))+'\n')
                shares-=askSize[min(sp.data)]
                sp.pop(min(sp.data),temp)
                #print(sp.data,shares,min(sp.data))
            elif min(sp.data)>price:
                flag=False
                #print(sp.data)
            
        else:
            if shares>0:
                f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' added to BID listing priced at '+str(price)+'\n')
                bp.push(price,shares)

    elif bORs == 's':
        if bp.size>0:
            if bidSize[max(bp.data)]>=shares and max(bp.data)>=price:
                f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from BID listing priced at '+str(max(bp.data))+'\n')
                bp.pop(max(bp.data),shares)
                shares=0
        flag=True
        while bp.size>0 and shares>0 and flag:
            if bidSize[max(bp.data)]>=shares and max(bp.data)>=price:
                f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from BID listing priced at '+str(max(bp.data))+'\n')
                bp.pop(max(bp.data),shares)
                shares=0
                break
            if bidSize[max(bp.data)]<shares and max(bp.data)>=price:
                temp=shares
                f.write(str(time.time())+' : '+str(bidSize[max(bp.data)])+' removed from BID listing priced at '+str(max(bp.data))+'\n')
                shares-=bidSize[max(bp.data)]
                bp.pop(max(bp.data),temp)
            elif max(bp.data)<price:
                flag=False
        else:
            if shares>0:
                f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' added to ASK listing priced at '+str(price)+'\n')
                sp.push(price,shares)

def cancelOrder(bORs,shares,price):
    if bORs == 'b':
        if price in bp.data:
            if bidSize[price] >= shares:
                print('Cancled '+str(shares)+' shares priced at '+str(price))
                bp.pop(price,shares)
            elif bidSize[price] < shares:
                print('Cancled '+str(bidSize[price])+' shares priced at '+str(price))
                bp.pop(price,bidSize[price])
        else:
            print("No order found")
    if bORs == 's':
        if price in sp.data:
            if askSize[price] >= shares:
                print('Cancled '+str(shares)+' shares priced at '+str(price))
                sp.pop(price,shares)
            elif askSize[price] < shares:
                print('Cancled '+str(askSize[price])+' shares priced at '+str(price))
                sp.pop(price,askSize[price])
        else:
            print("No order found")

def showDetails():
    print('Price\tAsk Size')
    for i in sorted(sp.data,reverse=True)[-5:]:
        print(str(i)+'\t'+str(askSize[i]))
    print('-'*25)
    print('Price\tBid Size')
    for i in sorted(bp.data,reverse=True)[:5]:
        print(str(i)+'\t'+str(bidSize[i]))
    print('-'*25)

                    
sp=sellPrice()
bp=buyPrice()

while True:
    f=open('log.txt','a')
    print('Price\tAsk Size')
    for i in sorted(sp.data,reverse=True)[-5:]:
        print(str(i)+'\t'+str(askSize[i]))
    print('-'*25)
    print('Price\tBid Size')
    for i in sorted(bp.data,reverse=True)[:5]:
        print(str(i)+'\t'+str(bidSize[i]))
    print('-'*25)
    e=input('type "m" for market order and "l" for limit order and "c" to cancle existing order')

    
    if e=='c':
        bORs = input('what is the type of order? enter "b" for buy order and "s" for sell order')
        if bORs not in 'bs':
            print()
            print('#'*20+'\nselect "b" or "s"\n'+'#'*20)
            print()
            continue
        try:
            shares=int(input("enter no. of shares"))
            price=float(input("enter price"))
        except:
            print()
            print('#'*20+'\nINVALID DATATYPE\n'+'#'*20)
            print()
            continue
        print('\n'+'#'*35)
        
        if bORs == 'b':
            if price in bp.data:
                if bidSize[price] >= shares:
                    print('Cancled '+str(shares)+' shares priced at '+str(price))
                    bp.pop(price,shares)
                elif bidSize[price] < shares:
                    print('Cancled '+str(bidSize[price])+' shares priced at '+str(price))
                    bp.pop(price,bidSize[price])
        if bORs == 's':
            if price in sp.data:
                if askSize[price] >= shares:
                    print('Cancled '+str(shares)+' shares priced at '+str(price))
                    sp.pop(price,shares)
                elif askSize[price] < shares:
                    print('Cancled '+str(askSize[price])+' shares priced at '+str(price))
                    sp.pop(price,askSize[price])
            else:
                print("No order found")
        print('#'*35+'\n')
            
        
        
    if e=='m':
        bORs = input('enter "b" to buy and "s" to sell')
        if bORs not in 'bs':
            print()
            print('#'*20+'\nselect "b" or "s"\n'+'#'*20)
            print()
            continue
        try:
            shares=int(input("enter no. of shares"))
        except:
            print()
            print('#'*20+'\nINVALID DATATYPE\n'+'#'*20)
            print()
            continue
        if bORs == 'b':
            if sp.size>0:
                if askSize[min(sp.data)]>=shares:
                    f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from ASK listing priced at '+str(min(sp.data))+'\n')
                    sp.pop(min(sp.data),shares)
                    shares=0
                    
                else:
                    while sp.size>0 and shares>0:
                        if askSize[min(sp.data)]>=shares:
                            f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from ASK listing priced at '+str(min(sp.data))+'\n')
                            sp.pop(min(sp.data),shares)
                            shares=0
                        else:
                            f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(askSize[min(sp.data)])+' removed from ASK listing priced at '+str(min(sp.data))+'\n')
                            shares-=askSize[min(sp.data)]
                            sp.pop(min(sp.data),askSize[min(sp.data)])
        if bORs=='s':
            if bp.size>0:
                if bidSize[max(bp.data)]>=shares:
                    f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from BID listing priced at '+str(max(bp.data))+'\n')
                    bp.pop(max(bp.data),shares)
                    shares=0
                else:
                    while bp.size>0 and shares>0:
                        if bidSize[max(bp.data)]>=shares:
                            f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from BID listing priced at '+str(max(bp.data))+'\n')
                            bp.pop(max(bp.data),shares)
                            shares=0
                        else:
                            f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(bidSize[max(bp.data)])+' removed from BID listing priced at '+str(max(bp.data))+'\n')
                            shares-=bidSize[max(bp.data)]
                            bp.pop(max(bp.data),bidSize[max(bp.data)])
                    
        
    elif e=='l':
        bORs = input('enter "b" to buy and "s" to sell')
        if bORs not in 'bs':
            print()
            print('#'*20+'\nselect "b" or "s"\n'+'#'*20)
            print()
            continue
        try:
            shares=int(input("enter no. of shares"))
            price=float(input("enter price"))
        except:
            print()
            print('#'*20+'\nINVALID DATATYPE\n'+'#'*20)
            print()
            continue
        
        if bORs == 'b':
            if sp.size>0:
                if askSize[min(sp.data)]>=shares and min(sp.data)<=price:
                    f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from ASK listing priced at '+str(min(sp.data))+'\n')
                    sp.pop(min(sp.data),shares)
                    shares=0
            flag=True
            while sp.size>0 and shares>0 and flag:
                if askSize[min(sp.data)]>=shares and min(sp.data)<=price:
                    f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from ASK listing priced at '+str(min(sp.data))+'\n')
                    sp.pop(min(sp.data),shares)
                    shares=0
                    break
                if askSize[min(sp.data)]<shares and min(sp.data)<=price:
                    temp=shares
                    f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(askSize[min(sp.data)])+' removed from ASK listing priced at '+str(min(sp.data))+'\n')
                    shares-=askSize[min(sp.data)]
                    sp.pop(min(sp.data),temp)
                    #print(sp.data,shares,min(sp.data))
                elif min(sp.data)>price:
                    flag=False
                    #print(sp.data)
                
            else:
                if shares>0:
                    f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' added to BID listing priced at '+str(price)+'\n')
                    bp.push(price,shares)

        elif bORs == 's':
            if bp.size>0:
                if bidSize[max(bp.data)]>=shares and max(bp.data)>=price:
                    f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from BID listing priced at '+str(max(bp.data))+'\n')
                    bp.pop(max(bp.data),shares)
                    shares=0
            flag=True
            while bp.size>0 and shares>0 and flag:
                if bidSize[max(bp.data)]>=shares and max(bp.data)>=price:
                    f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' removed from BID listing priced at '+str(max(bp.data))+'\n')
                    bp.pop(max(bp.data),shares)
                    shares=0
                    break
                if bidSize[max(bp.data)]<shares and max(bp.data)>=price:
                    temp=shares
                    f.write(str(time.time())+' : '+str(bidSize[max(bp.data)])+' removed from BID listing priced at '+str(max(bp.data))+'\n')
                    shares-=bidSize[max(bp.data)]
                    bp.pop(max(bp.data),temp)
                elif max(bp.data)<price:
                    flag=False
            else:
                if shares>0:
                    f.write(str(datetime.now().strftime("%H:%M:%S"))+' - '+str(shares)+' added to ASK listing priced at '+str(price)+'\n')
                    sp.push(price,shares)
    f.close()
