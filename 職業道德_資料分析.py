#匯入職業道德，處理文字

import re
import random

with open(r"職業道德107年版.txt", mode="r", encoding="utf-8") as file:
     content=file.read()
#------------------------------------------------------------------------------------------
     #c=re.sub('\n+','',content) #換行符號用空白字元取代     
     x=re.sub('第\s[0-9]+\s頁，\s共\s[0-9]+\s頁','',content) #去掉頁數頁碼
     title=re.sub('Part II：職業道德\n答案 題號\n題 目','',x) #去掉題目
     c=re.sub('\n+','',title)
     z=re.sub('\(\s[1-4]\s\)\s','\n',c)
     k=list(z)
     k.pop(0)
     a=''.join(k)
     cc=a.split('\n')   
# =============================================================================
##答案
     ans=[]
     ans=re.findall('\s(\d)\s(?!\w)',content)   #全部615題的答案
# =============================================================================
#題目
     que=[]
     for i in range(0,615):
         que.append(re.split('\(1\)',cc[i]))
         
         if que[i][1]!='':
              que[i]=que[i][0]
         que[i]=re.split('^\d+',que[i])
         if que[i][0]=='':
              que[i]=que[i][1]
# =============================================================================     
#選項
     opt=[]
     opt1=[]

     for i in range(0,615):
         opt1_test=re.split('\(1\)',cc[i])
         opt2_test=opt1_test[0]
         opt1_test=cc[i].replace(opt2_test ,'')     
         opt1.append(re.split('\(2\)',opt1_test))
         if opt1[0][-1]!='':
              opt1[0]=opt1[0][0]
         
         opt1_test=re.split('\(2\)',cc[i])
         opt2_test=opt1_test[0]
         opt1_test=cc[i].replace(opt2_test ,'')     
         opt2_test=re.split('\(3\)',opt1_test)
         if opt2_test[0][-1]!='':
              opt1.append( opt2_test[0] )
              
         opt1_test=re.split('\(3\)',cc[i]) 
         opt2_test=opt1_test[0]
         opt1_test=cc[i].replace(opt2_test ,'')     
         opt2_test=re.split('\(4\)',opt1_test)
         if opt2_test[0][-1]!='':
              opt1.append( opt2_test[0] )
         
         opt2_test= opt1_test.replace( opt2_test[0],'')
         opt1.append( opt2_test)

         opt.append(opt1)
         opt1=[]
         
# =============================================================================
# =============================================================================         
#GUI 配置 (答案:ans[]、問題:que[]、選項:opt[]) 
ran_num=[]
ran_que=[]
ran_ans=[]
ran_opt=[]
vv=[]
all_label=[]
ans_label=[]
wr=0     

import sys
import tkinter as tk

class App():
    def __init__(self, que,ans,opt,ran_num,ran_que,ran_ans,ran_opt,vv,all_label,ans_label,wr):
        self.que=que
        self.opt=opt
        self.ans=ans
        self.ran_num=ran_num
        self.ran_que=ran_que
        self.ran_opt=ran_opt
        self.ran_ans=ran_ans
        self.vv=vv  #存放intvar
        self.all_label=all_label #存放顯現出答案的Label
        self.ans_label=ans_label #存放顯現出答案的Label
        self.wr=wr
        
        global root
        root=tk.Tk()
        root.title("職業道德")
        root.resizable(0,0)  #視窗大小不能縮放
        #螢幕滑輪        
        sizex = 1335
        sizey = 700
        posx  = 100
        posy  = 100
        root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
        # myframe=tk.Frame(root,relief=tk.GROOVE,width=200,height=150,bd=1)
        # myframe.place(x=10,y=10)        
        self.canvas=tk.Canvas(root,bg='white')
        self.canvas.bind_all("<MouseWheel>",self. mousewheel) #使得滑鼠滾輪可以滾動整個頁面
        frame=tk.Frame(self.canvas,width=1300,height=600,bg='white')        
        myscrollbar=tk.Scrollbar(root,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=frame,anchor='nw')
        frame.bind("<Configure>",self.myfunction)
        
        #主要程式都放在frm_2之下
        frm_2=tk.Frame(frame,bg='white')
        frm_2.grid(row=0 ,column=0,sticky='w')
        
        self.new()
        t='white' 
        self.data(frm_2,t)
        
        
        again_btn=tk.Button(root,text='產生新題目', command= refresh)
        again_btn.place(x=100, y=650,anchor="center", width=100, height=50)
        
        btn=tk.Button(root,text='交卷' , command=self.check)
        btn.place(x=250, y=650,anchor="center", width=100, height=50)
        
        
        #分數
        self.score_label=tk.Label(root,font='32')
        self.score_label.place(x=350, y=650,anchor="center", width=100, height=50)

     
        root.mainloop()
        
# =============================================================================
    def myfunction(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=1300,height=600)    
    #使得滑鼠滾輪可以滾動scrollbar
    # https://t.codebug.vip/questions-1870109.htm
    def mousewheel(self,event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")
# =============================================================================
    def new(self):
        #亂數抽取題目，抽取50題   
        # ran_num=[]
        ran=[i for i in range(615)]
        self.ran_num.clear()
        self.ran_que.clear()
        self.ran_ans.clear()
        self.ran_opt.clear()
        self.vv.clear()
        self.all_label.clear()
        self.ans_label.clear()
        
        self.ran_num=random.sample(ran,50)
        #ran_num和真實題號差一
        for ra in self.ran_num:
            self.ran_que.append(self.que[ra])
            self.ran_ans.append(self.ans[ra])
            self.ran_opt.append(self.opt[ra])
        for q in range(50):
            kk=tk.IntVar()
            kk.set(q+5)
            self.vv.append(kk)
            lvv = tk.Label()            
            self.all_label.append(lvv)
            llvv = tk.Label()
            self.ans_label.append(llvv)

                
    def data(self,frm_2,t):               
        for z in vv:
            #題目
            que_label=tk.Label(frm_2,
                                text=str( vv.index(z) +1)+self.ran_que[ vv.index(z) ],
                                bg='white',
                                wraplength=1000,
                                font='20',
                                anchor='nw',
                                justify = 'left')
            que_label.grid(row=(vv.index(z))*8+0,column=0,sticky='w')
            
            #單選選項  
            for i in range(0,4):
                      
                rad=tk.Radiobutton(frm_2,text=self.ran_opt[vv.index(z)][i], variable=z , 
                                    value=i+1,bg='white',font='20')
                rad.grid(row=(vv.index(z))*8+i+1,column=0,sticky='w')

            #印出答案
            self.ans_label[ vv.index(z) ]=tk.Label(frm_2,text='',fg=t ,bg='white')
            self.ans_label[ vv.index(z) ].grid(row=(vv.index(z))*8+5,column=0,sticky='w')
            
            self.all_label[ vv.index(z) ]=tk.Label(frm_2,textvariable=z,fg=t ,bg='white',font='20')
            self.all_label[ vv.index(z) ].grid(row=(vv.index(z))*8+6,column=0,sticky='w')
            
            
            
            #分隔線
            que_label=tk.Label(frm_2,text='---------'*30,bg='white')
            que_label.grid(row=(vv.index(z))*8+7,column=0,sticky='w')
        
    #成績顯示的按鈕
    def check(self):
        for i in range(0,50):
            if self.vv[i].get()<5:
                if self.vv[i].get()==int(ran_ans[i]):
                      t='white'
                      self.wr=self.wr+1
                      self.score_label['text']='分數 :   '+str( self.wr)+'/ 50'
                      self.all_label[i]['bg']=t                
                else:
                      t='red'                     
                      self.all_label[i]['bg']='white'
                      self.ans_label[i]['text']='正確答案 : '+ ran_ans[i]
                      self.ans_label[i]['bg']=t
            else:
                t='red'
                self.ans_label[i]['text']='沒有選擇答案 '
                self.ans_label[i]['bg']=t
    
         
if __name__ == '__main__':
    def refresh():
        root.destroy()      
        App(que,ans,opt,ran_num,ran_que,ran_ans,ran_opt,vv,all_label,ans_label,wr)
    
    App(que,ans,opt,ran_num,ran_que,ran_ans,ran_opt,vv,all_label,ans_label,wr)