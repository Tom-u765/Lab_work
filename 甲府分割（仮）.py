
import numpy as np
import pandas as pd
import networkx as nx
from ortoolpy import graph_from_table
from ortoolpy.optimization import DijkstraPath

#Link_incre.csv")
node = pd.read_csv("Node_incre.csv")
od = pd.read_csv("OD_incre.csv",header = None)
#%% 距離を所要時間に変換

##速度の入力（0にすると整備無しの状態）
s1=25    #rank1
s2=30    #rank2
s3=35    #rank3
s4=45    #rank4
s5=80    #圏央道
s6=80    #東海環状
s7=80    #関西環状
s8=80    #中部横断（静岡・山梨区間）
s9=50    #外環内高速
s10=58   #関西環状内高速
s11=100  #新東名
s12=80   #中央道
s13=0    #中部横断（山梨・長野区間）
s14=58   #北関東自動車道


linkcount=len(edge)

for i in (range(linkcount)): 
    if edge.iat[i,3] ==1:
        edge.iat[i,5] = edge.iat[i,2]*60/s1
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==2:
        edge.iat[i,5] = edge.iat[i,2]*60/s2
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==3:
        edge.iat[i,5] = edge.iat[i,2]*60/s3
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==4:
        edge.iat[i,5] = edge.iat[i,2]*60/s4
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==5:
        edge.iat[i,5] = edge.iat[i,2]*60/s5
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==6:
        edge.iat[i,5] = edge.iat[i,2]*60/s6
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==7:
        edge.iat[i,5] = edge.iat[i,2]*60/s7
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==8:
        edge.iat[i,5] = edge.iat[i,2]*60/s8
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==9:
        edge.iat[i,5] = edge.iat[i,2]*60/s9
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==10:
        edge.iat[i,5] = edge.iat[i,2]*60/s10
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==11:
        edge.iat[i,5] = edge.iat[i,2]*60/s11
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==12:
        edge.iat[i,5] = edge.iat[i,2]*60/s12
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==13:
        edge.iat[i,5] = edge.iat[i,2]*60/s13
        edge.iat[i,2] = edge.iat[i,5]
    elif edge.iat[i,3]==14:
        edge.iat[i,5] = edge.iat[i,2]*60/s14
        edge.iat[i,2] = edge.iat[i,5]
      
#%%初期値の設定
         
col=105
nodecount=66
incre = 1
od =od/incre
#Output = np.zeros(((max(edge.iloc[:,2])+1)*(max(edge.iloc[:,2])+1)-(max(edge.iloc[:,2])+1),col))
#Output = np.full((nodecount*nodecount-nodecount,col),-1)
Output1 = np.empty((nodecount*nodecount-nodecount,col)) #内々トリップ分引かれたOD表回数分の行列を作成、列数はcol
Output2 = np.zeros((nodecount,nodecount)) #なんだこれ？
bunkatu1 = np.zeros((col+3,nodecount*nodecount-nodecount)) #スタート、ゴール、weightを入力するので行数を＋3してる？列数はOD表的なやつ
bunkatu2 = np.zeros((linkcount+3,nodecount*nodecount-nodecount+(3+incre))) #linkcountはedgeの長さ
for o in range(linkcount): #
    bunkatu2[o+3,0] = edge.iat[o,0]*1000+edge.iat[o,1]
      
#%% 分割配分の実行 
bunkatu_num = 10 #　追記

for xx in range(bunkatu_num):  #分割数だけ繰り返す  
    for r in range(1,incre+1): #(1,2)の時は1のみ
        for i in range(nodecount*nodecount-nodecount): #-nodecountすることで、内々トリップぶんが弾かれる。OD表を作るためにやってるやつ
            for j in range(col): #col回繰り返す、実際は66回あればよさそう
                Output1[i,j] = -1
        s=0
        g = graph_from_table(node, edge)[0]

        #記録
        for i in (range(nodecount+1)): #セントロイド数＋1回繰り返す
            for j in (range(nodecount+1)): #セントロイド数＋1回繰り返す
                if i != j: #内々トリップの時は除外
                    if i != 0: #ノード0は無視する
                        if j != 0: #ノード0は無視する

                            #(所要時間の記録)
                            A = DijkstraPath(edge , i, j) #ネットワークedgeにおいて、i,j間の最短経路のdfを返す
                            #print(A)
                            #print(int(sum(A['weight'])))
                            
                            Output1[s,0]=int(i) #Output1の0列目にスタートのセントロイド番号
                            Output1[s,1]=int(j) #Output1の1列目にゴールのセントロイド番号
                            Output1[s,2]=(sum(A['weight'])) #Output1の1列目にダイクストラのWeight列を代入
                            
                            #bunkatu1にnode1,node2,weightを代入
                            bunkatu1[0,s]= Output1[s,0] #上のやつを入れるnode1
                            bunkatu1[1,s]= Output1[s,1] #上のやつを入れるnode2
                            bunkatu1[2,s]= Output1[s,2] #上のやつを入れるweight
                            
                            #bunkatu2にnode1,node2,OD交通量/分割数を代入
                            bunkatu2[0,s+1]= Output1[s,0] #行に入れるnode1
                            bunkatu2[1,s+1]= Output1[s,1] #行に入れるnode2
                            bunkatu2[2,s+1]= od.iat[int(Output1[s,0]-1),int(Output1[s,1]-1)] #OD交通量/分割数?
                            
                            
                            #(最短経路の記録)
                            FF=(nx.dijkstra_path(g, i, j)) #iからjまでの最短経路のリスト
                            FF
                            
                            #print(nx.dijkstra_path(g, i, j))
                            for n in range(len(FF)): 
                                Output1[s,n+3] = int(FF[n]) #最短経路のスタートからゴールまでOutput1の3列目以降に代入してく
                                
                            #リンクの表現を変更(node1*1000+node2)しセントロイド間の経路を表示（bunkatu1)     
                            for m in range(len(FF)-1): #最短経路数-1回繰り返す
                                if Output1[s,m+3]<Output1[s,m+4]: #ノード番号の大小で判別
                                    bunkatu1[m+3,s] = Output1[s,m+3]*1000+Output1[s,m+4] #スタートとゴールを1つのセルにまとめて1つのセルに入れる
                                else:
                                    bunkatu1[m+3,s] = Output1[s,m+4]*1000+Output1[s,m+3] #スタートとゴールを1つのセルにまとめて1つのセルに入れる
                                        
                            #リンクごとの交通量を代入
                            for m in range(len(FF)-1): #最短経路数-1回繰り返す
                                a = np.where(bunkatu2[:,0] == bunkatu1[m+3,s]) #bunkatu2[:,0]= bunkatu1[m+3,s]だったらbunkatu2[:,0]をaとして取り出す。[:,0]は全ての行の0列目を取り出すという意味。
                                bunkatu2[a,s+1] = bunkatu2[2,s+1] #bunkatu2の2行s+1列目(1列目からスタート)の値をa行s+1列目に代入するという話
                                print(a)
                            
                            #記録位置の変更
                            s = s+1 #参照している列を一つずらす
        r=r+1 #rを増加させるが、for文で動かしているのにわざわざこれをやる意味がわからない
        Output1
        
        #リンクごとの交通量を分割毎に合計し、BPR関数を用いてTimeのweightを更新
        for p in range((linkcount)):#
            linksum = np.sum(bunkatu2[p+3,1:nodecount*nodecount-nodecount])
            bunkatu2[p+3,nodecount*nodecount-nodecount+r] = linksum
            bunkatu2[p+3,nodecount*nodecount-nodecount+(incre+1)] = bunkatu2[p+3,nodecount*nodecount-nodecount+(incre+1)]+bunkatu2[p+3,nodecount*nodecount-nodecount+r]
            
        c=0.48
        d=2.82
        for p in range(linkcount):
            edge.iat[p,2] = edge.iat[p,5]*(1+c*(bunkatu2[p+3,nodecount*nodecount-nodecount+(incre+1)]/edge.iat[p,4])**d)
        
        
        #分割配分終了後bunkatu1,bunkatu2がリセットされる前に止め最短経路探索を行う
        if(r == incre):
            print('分割配分終了、最短経路探索を実行')
            break
        
        #経路情報、配分されたリンクの交通量をリセット（合計は残す）
        bunkatu1[3:,0:] = 0
        bunkatu2[3:,3:nodecount*nodecount-nodecount+3] = 0    

    
#%%交通量配分後の再度最短経路探索により、セントロイド間の所要時間を計算
        
for i in range(nodecount*nodecount-nodecount):
      for j in range(col):
          Output1[i,j] = -1
s=0
g = graph_from_table(node, edge)[0]

#記録
for i in (range(nodecount+1)):
      for j in (range(nodecount+1)):
          if i is not j:
              if i != 0:
                  if j != 0:
                    
                    #(所要時間の記録)
                    A = DijkstraPath(edge , i, j)
                    #print(A)
                    #print(int(sum(A['weight'])))
                    
                    Output1[s,0]=int(i)
                    Output1[s,1]=int(j)
                    Output1[s,2]=(sum(A['weight']))
                    
                    #(最短経路の記録)
                    FF=(nx.dijkstra_path(g, i, j))
                    #print(nx.dijkstra_path(g, i, j))
                    for n in range(len(FF)):
                        Output1[s,n+3] = int(FF[n])
                        
                    #weightを行列形式に代入    
                    Output2[int(i)-1,int(j)-1] = Output1[s,2]
                    Output2[int(j)-1,int(i)-1] = Output1[s,2]
                        
                        
                    #記録位置の変更
                    s = s+1
            
Output1
#%%混雑度の算出

for p in range((linkcount)):
    bunkatu2[p+3,nodecount*nodecount-nodecount+(incre+2)] = bunkatu2[p+3,nodecount*nodecount-nodecount+(incre+1)]/edge.iat[p,4]
    
    
#%%
 
name=["start","end","weight","start1","Path2","Path3","Path4","Path5","Path6","Path7","Path8","Path9","Path10",
      "Path11","Path12","Path13","Path14","Path15","Path16","Path17","Path18","Path19","Path20","Path21","Path22","Path23","Path24","Path25","Path26","Path27",
      "Path28","Path29","Path30","Path31","Path32","Path33","Path34","Path35","Path36","Path37","Path38","Path39","Path39","Path40","Path41","Path42","Path43",
      "Path44","Path45","Path46","Path47","Path48","Path49","Path50","Path51","Path52","Path53","Path54","Path55","Path56","Path57","Path58","Path59","Path60",
      "Path61","Path62","Path63","Path64","Path65","Path66","Path67","Path68","Path69","Path70","Path71","Path72","Path73","Path74","Path75","Path76","Path77",
      "Path78","Path79","Path80","Path81","Path82","Path83","Path84","start1","Path2","Path3","Path4","Path5","Path6","Path7","Path8","Path9","Path10",
      "Path11","Path12","Path13","Path14","Path15","Path16","Path17"]

KK = pd.DataFrame(Output1,columns=name)

KK
KK.to_csv('output_increnew1.csv')


#%%

jj = pd.DataFrame(Output2)

jj
jj.to_csv('output_increnew2.csv')

#%%

oo = pd.DataFrame(bunkatu2)

oo.to_csv('output_increnew11.csv')