from pygame.locals import *
import pygame
import sys
import numpy as np
import random

pygame.init()

#画面表示-----------------
Sc_height=950
Sc_width=Sc_height/2
n_h=16          #高さN数
n_w=int(n_h/2)  #横N数
#-------------------------
#フォントサイズ---------------------
fontsize=50
font = pygame.font.Font(None,fontsize)
#ブロック----------------
b_h=Sc_height/n_h
b_w=Sc_width/n_w
b_n=4 #回転用(ブロック正方形1辺長さ)
block_color=((10,0,0))

#スタート画面--------------
screen = pygame.display.set_mode((Sc_width,Sc_height)) # 画面を作成
back_color=(240,255,240)
screen.fill(back_color)
pygame.display.update()  

# 初期設定----------------
i,j=int(n_w/3),1
block_choice=1
block_N=5 #ブロックの種類
# ①ブロック
BlockLoca=np.zeros([n_h+2,n_w+2])
# ②ブロック(1ターン進行)
BlockLoca_pro=np.zeros([n_h+2,n_w+2])
# ③背景
BackDisp=np.zeros([n_h+2,n_w+2]) 
BackDisp[:,0]=1
BackDisp[:,n_w+1]=1
BackDisp[n_h+1,:]=1
# ④表示用(背景+ブロック)
ShowDisp=np.zeros([n_h+2,n_w+2])
Block_small=np.zeros([b_n,b_n])
Block_small_rotate=np.zeros([b_n,b_n])
#-------------------------
def init():#リセット---------------------------------
 BackDisp[:,:]=np.zeros([n_h+2,n_w+2])
 BackDisp[:,0]=1
 BackDisp[:,n_w+1]=1
 BackDisp[n_h+1,:]=1
 BlockLoca_pro[:,:]=np.zeros([n_h+2,n_w+2])
 BlockLoca[:,:]=np.zeros([n_h+2,n_w+2])
 i,j=int(n_w/3),1
 block_choice=random.randint(1,block_N)
 ini_block(block_choice)

def escape():#ゲーム終了-----------------------------
 if event.type == QUIT:   
  pygame.quit()
  sys.exit()
 if event.key == K_ESCAPE:
  pygame.quit()
  sys.exit()         

def ini_block(block_choice):#ブロック初期設定---------------------------------   
    # L字型
    if block_choice==1:
        BlockLoca[j][i+1]=1
        BlockLoca[j+1][i+1]=1
        BlockLoca[j+2][i+1]=1
        BlockLoca[j+2][i+2]=1
    # o字型
    if block_choice==2:   
        BlockLoca[j+1][i+1]=1
        BlockLoca[j+2][i+1]=1
        BlockLoca[j+2][i+2]=1
        BlockLoca[j+1][i+2]=1
    # I字型
    if block_choice==3:
        BlockLoca[j][i+1]=1
        BlockLoca[j+1][i+1]=1
        BlockLoca[j+2][i+1]=1
        BlockLoca[j+3][i+1]=1
    # Z字型
    if block_choice==4:
        BlockLoca[j][i+1]=1
        BlockLoca[j+1][i+1]=1
        BlockLoca[j+1][i+2]=1
        BlockLoca[j+2][i+2]=1
    # 逆Z字型
    if block_choice==5:
        BlockLoca[j][i+2]=1
        BlockLoca[j+1][i+2]=1
        BlockLoca[j+1][i+1]=1
        BlockLoca[j+2][i+1]=1

def move_state_me():#どう動かすかのステート---------------------------------
 right,left,down,drop=False,False,False,False      
 if event.key==pygame.K_RIGHT: right=True #右進行
 if event.key==pygame.K_LEFT: left=True #左進行 
 if event.key==pygame.K_DOWN: down=True #下進行  
 if event.key==pygame.K_UP: drop=True #急落下  
 return right,left,down,drop

def block_move(i,j,right,left,down,drop,n_h,n_w):#ブロック移動クラス-----------------------------
 i_new,j_new = i,j

 #ドロップ
 if drop==True:
  #ブロックを仮に移動   
  for pro in range (1,n_h+2,1): 
   for m in range (1,n_w+1,1):
    for n in range (1,n_h+1,1): 
     if BlockLoca[n][m]==1:   
       BlockLoca_pro[n+pro][m]=1  
   for k in range (0,n_h+2,1):
    if max(BlockLoca_pro[k,0:n_w+2]+BackDisp[k,0:n_w+2])>1:
     i_new,j_new=i,j+pro-1
     drop=False
     break
   if drop==False:
    break
  
  BlockLoca_pro[:,:]= np.zeros([n_h+2,n_w+2])
  for m in range (1,n_w+1,1):
   for n in range (1,n_h+1,1): 
    if BlockLoca[n][m]==1:
     BlockLoca_pro[n+(j_new-j)][m]=1

 #1マス移動
 if right==True: i_new=i+1
 if left==True: i_new=i-1
 if down==True: j_new=j+1
  #ブロックを仮に移動
 for m in range (1,n_w+1,1):
  for n in range (1,n_h+1,1): 
   if BlockLoca[n][m]==1:
    BlockLoca_pro[n+(j_new-j)][m+(i_new-i)]=1

 for k in range (0,n_h+2,1):
  if max(BlockLoca_pro[k,0:n_w+2]+BackDisp[k,0:n_w+2])>1:
   i_new,j_new = i,j
   BlockLoca_pro[:,:]=BlockLoca[:,:]
   break
 return i,j,i_new,j_new

def block_90deg_rotate(i,j,b_n):#ブロック右回転クラス-----------------------------
 if i<n_w-(b_n-2) and i>0 and j<n_h-(b_n-2):   
  Block_small[0:b_n,0:b_n]=BlockLoca[j:j+b_n,i:i+b_n]
  for k in range (0,b_n,1):
   Block_small_rotate[k,:]=Block_small[::-1,k]#ここで回転
  BlockLoca[:,:]=np.zeros([n_h+2,n_w+2])
  BlockLoca[j:j+b_n,i:i+b_n]=Block_small_rotate[:,:]

def block_m90deg_rotate(i,j,b_n):#ブロック左回転クラス-----------------------------
 if i<n_w-(b_n-2) and i>0 and j<n_h-(b_n-2):   
  Block_small[0:b_n,0:b_n]=BlockLoca[j:j+b_n,i:i+b_n]
  for k in range (0,b_n,1):
   Block_small_rotate[:,k]=Block_small[k,::-1]#ここで回転
  BlockLoca[:,:]=np.zeros([n_h+2,n_w+2])
  BlockLoca[j:j+b_n,i:i+b_n]=Block_small_rotate[:,:]


def show_display(i,j,n_h,n_w):#要素01の行列データ⇒画面反映-----------------------------
 screen.fill(back_color)
 ShowDisp[:,:]=BackDisp[:,:]+BlockLoca[:,:]
 for k in range (1,n_h+2,1):
  for l in range (1,n_w+2,1):   
   if ShowDisp[k][l]>0:
       pygame.draw.rect(screen,block_color,pygame.Rect((l-1)*b_h,(k-1)*b_w, b_w-1, b_h-1))
 pygame.display.update() 


# メインプログラム
block_choice=random.randint(1,block_N)
ini_block(block_choice)
while True:   
 for event in pygame.event.get():
   if event.type == KEYDOWN:       
    BlockLoca_pro=np.zeros([n_h+2,n_w+2])  
   #ブロック移動(BlockLoca_proを求める)----------
    right,left,down,drop = move_state_me()     
#    print(BlockLoca_pro)
    i,j,i_new,j_new = block_move(i,j,right,left,down,drop,n_h,n_w)
#    print(BlockLoca_pro)
    BlockLoca[:,:]=BlockLoca_pro[:,:]
    i,j=i_new,j_new
   #ブロック回転--------------- 
    if event.key == K_f:
     block_90deg_rotate(i,j,b_n)
    if event.key == K_s: 
     block_m90deg_rotate(i,j,b_n)

    #ブロック置き---------------
    for k in range(1,n_h+1,1):
     for l in range(1,n_w+1,1):   
      if BlockLoca[k,l]==1 and BackDisp[k+1,l]== 1:##
       #背景にブロック書く
       for m in range (1,n_w+2,1):
        for n in range (1,n_h+2,1): 
         if BlockLoca[n][m]==1:
          BackDisp[n][m]=1       
       #初期化
       i,j,i_new,j_new=int(n_w/2),1,int(n_w/2),1   
       BlockLoca=np.zeros([n_h+2,n_w+2])
       block_choice=random.randint(1,block_N)
       ini_block(block_choice)
       break
   #ブロック消し---------------
    delete_lines=0
    for k in range (1,n_h+1,1):        
     if np.all(BackDisp[k,1:n_w+1])==np.all(np.ones([1,n_w])):
      BackDisp[1:k+1,1:n_w+1]=BackDisp[0:k,1:n_w+1]
   #-----------------------------"""

   #画面写し--------------------
    show_display(i,j,n_h,n_w)
   #ゲームオーバー---------------
    if np.any(BackDisp[1,1:n_w+1])>0:
     BlockLoca=np.zeros([n_h+2,n_w+2])

     screen.fill(back_color)
     pygame.display.update()

     if event.key == K_SPACE:
      init()
      
    #画面クローズ-----------------
    escape()
