import networkx as nx
import linecache
import numpy as np
import random
import math
import time

start=time.clock()
def net_dic(nnode,file1):
    G_array=np.zeros((nnode,nnode))
    G = nx.Graph()
    node_dic={}
    count=1
    f1=open(file1,'r')
    for lines in f1.readlines()[5:nnode+5]:
        G.add_node(count)
        node_dic[lines[2:-3]]=count
        count+=1
    f1.seek(0)
    for datas in f1.readlines()[nnode+6:]:
        data=datas.rstrip().split()
        m=int(data[0])
        n=int(data[1])
        G_array[m-1,n-1]=1
        G.add_edge(m,n)
    f1.close()
    print('nodes:', G.number_of_nodes(), 'edges:', G.number_of_edges())
    return node_dic,G,G_array

def getSim(file2,nnodes1,nnodes2,G1_dict,G2_dict):
    sim_array = np.zeros((nnodes1, nnodes2))
    f2 = open(file2, 'r')
    for lines in f2.readlines():
        line = lines.rstrip().split()
        if line[0] in G1_dict and line[1] in G2_dict:
            si = G1_dict[line[0]]
            sj = G2_dict[line[1]]
            sim_array[int(si)-1,int(sj)-1] = line[2]
    return sim_array

def getConserved(nnodes1,G1,G2,align):
    v_list=[1]*nnodes1
    alignment = {}
    for data in range(nnodes1):
        if align[data]!=-1:
            alignment[data+1] = align[data]+1
    totalScore=0
    #for each node i in first network
    for i in G1.nodes():
        #for each neighbor j of node i
        for j in G1.neighbors(i):
            #for each neighbor l of a node in second network that is aligned with node i
            if i in alignment.keys() and alignment[i] != -1:
                for l in G2.neighbors(alignment[i]):
                    if j in alignment.keys() and l==alignment[j]:
                        v_list[i-1]=0
                        v_list[j-1] = 0
                        totalScore+=1
    return totalScore/2,v_list

def random_change(nnodes1,permutation,dis_per):
    per=permutation.copy()
    change_index=[]
    for ra in range(nnodes1):
        if dis_per[ra]==-2:
            change_index.append(ra)
    change_index=random.sample(change_index,len(change_index))
    for pd in range(int(len(change_index)/2)):
        rb_temp=per[change_index[pd]]
        per[change_index[pd]] = per[change_index[-pd-1]]
        per[change_index[-pd - 1]]=rb_temp
    return per

def getPositon(arr):
    raw, column = arr.shape
    _positon = np.argmax(arr)
    m, n = divmod(_positon, column)
    return m,n

def greedy(cost):
    aligned=[-1]*nnode1
    Cost=cost.copy()
    while(True):
        ai,aj=getPositon(Cost)
        if Cost[ai,aj]!=0:
            aligned[ai]=aj
            Cost[ai]=0
            Cost[:,aj]=0
        else:
            break
    return aligned

def Bat(greedy_align,nnodes1,nnodes2,G1,G2,Population,N_gen,alpha,gamma):
    N_iterations=10
    r0 = 0.1
    A0 = [1] * Population
    r = [0.1] * Population
    v=[]
    Soultion = []  # solution generated randomly
    Fitness = []  # score of solution
    ############Initailizatoin
    i_temp = random.sample(range(nnodes2), nnodes2)
    i_t = list(set(i_temp) - set(greedy_align))
    v1 = [0] * nnodes1
    unalign_index=[]
    for ib in range(nnodes1):
        if greedy_align[ib] == -1:
            unalign_index.append(ib)
    for p in range(Population):
        x_greedy=greedy_align.copy()
        i_te = random.sample(i_t, len(i_t))
        for ic in range(len(unalign_index)):
                v1[unalign_index[ic]]=1
                x_greedy[unalign_index[ic]] = i_te[ic]
        v.append(v1)
        Soultion.append(x_greedy)
        Fit,v_f= getConserved(nnodes1, G1, G2, x_greedy)
        Fitness.append(Fit)
    ####Iteration
    fmax = max(Fitness)  # score of optimal solution
    best = Soultion[Fitness.index(max(Fitness))]  # optimal solution
    fmax_max=[0]*10
    for t in range(N_gen):
        for i in range(Population):
            Q=np.random.uniform(0, 1)
            x_new=Soultion[i]
            v[i] = [int(round(v[i][a]*Q)) if x_new[a] != best[a] else v[i][a] for a in range(nnodes1)]
            x_negative = [-2 if ne == -1 or nf == 1 else ne for ne, nf in zip(x_new, v[i])]
            x_temp = random.sample(range(nnodes2), nnodes2)
            x_t = list(set(x_temp) - set(x_negative))
            x_te = random.sample(x_t, len(x_t))
            x_index = 0
            for e in range(nnode1):
                if x_negative[e] == -2:
                    x_new[e] = x_te[x_index]
                    x_index += 1
            fnew,v_t= getConserved(nnodes1, G1, G2, x_new)
            if np.random.uniform(0, 1) > r[i]:  # local search
                x_local =random_change(nnodes1,x_new,x_negative)
                flocal,v_l=getConserved(nnodes1, G1, G2, x_local)
                if flocal>fnew:
                    fnew=flocal
                    x_new=x_local
                    v_t=v_l

            if np.random.uniform(0, 1) < A0[i] and fnew > Fitness[i]:
                Soultion[i] = x_new
                Fitness[i] = fnew
                A0[i] = alpha * A0[i]
                r[i] = r0 * (1 - math.exp(-1 * gamma * t))
                v[i]=v_t
            if fnew > fmax:
                best = x_new
                fmax = fnew
        print("Iteration %d" % t)
        sort_fit=np.argsort(np.array(Fitness))
        for sa in range(int(Population/2)):
            Soultion[sort_fit[sa]]=Soultion[sort_fit[-1-sa]]
            v[sort_fit[sa]]=v[sort_fit[-1-sa]]
        fmax_max[t%N_iterations]=fmax
        if sum(fmax_max)==fmax_max[-1]*N_iterations:
            print('The optimal solution was not updated after ' + str(N_iterations) + ' iterations.Finish!')
            break
    return best, fmax

path=input('the path:')+'\\'
filename1=path+input('small network:')
filename2=path+input('big network:')
filename_w2=path+input('aligned filename:')+'.align'
pop=40
TN_alpha=float(input('TN_alpha:'))
N_gen=1000
nnode1 = int(linecache.getline(filename1, 5).strip())
nnode2 = int(linecache.getline(filename2, 5).strip())
G1_dict,G1,G1_array= net_dic(nnode1,filename1)
G2_dict,G2,G2_array= net_dic(nnode2,filename2)
new_G1_dict={f:e for e,f in G1_dict.items()}
new_G2_dict={g:h for h,g in G2_dict.items()}
filename3 = path + input('sequence file:')
Cost1 = getSim(filename3, nnode1, nnode2, G1_dict, G2_dict)
Cost=TN_alpha*Cost1+(1-TN_alpha)*np.dot(np.dot(G1_array, Cost1), G2_array.T)
greedy_align=greedy(Cost)
best,fmax=Bat(greedy_align,nnode1,nnode2,G1,G2,pop,N_gen,0.9,0.9)
f_w=open(filename_w2,'w')
count_1=0
for a_index in range(len(best)):
    if best[a_index]!=-1:
        f_w.write(new_G1_dict[a_index+1]+' '+new_G2_dict[best[a_index]+1]+'\n')
    else:
        count_1 += 1
f_w.close()
