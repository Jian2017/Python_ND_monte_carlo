import numpy as np
import h5py
import queue

from tqdm import tqdm


## Luijten methods
## the major function of this class is to generate a list of sites

class Add_neighbours:
    
    def __init__(self,Ls,Ks,A):
        
        self.LsZero=Ls[0]
        self.LsAll=Ls
        
        self.N=len(Ls)*2-2+Ls[0]-1
        
        K=np.zeros((self.N,))
        for i in range(Ls[0]-1):
            K[i]=A*(np.pi/Ls[0])**2/(2*np.sin(np.pi*(i+1)/Ls[0])**2)
        K[0]=K[0]+Ks[0]
        K[Ls[0]-2]=K[Ls[0]-2]+Ks[0]
        j=Ls[0]-1
        for i in range(len(Ls)-1):
            K[j]=Ks[i+1]
            j=j+1
            K[j]=Ks[i+1]
            j=j+1
        #print(K)
        
        self.C=np.zeros((self.N,self.N))
        for i in range(self.N):
            Ksum=0.0
            for j in range(i,self.N):
                Ksum=Ksum+K[j]
                self.C[i,j]=1-np.exp(-2*Ksum)

        
        
    
    def generateList(self):
        #this is a random output, each time the reasult is different
        # valid output list elements {0,1,2,...,self.N-1}
                
        z=[]
        i=0
        while(i<self.N):
            r=np.random.rand()
            index=np.searchsorted(self.C[i,:], r, side='right')
            if(index<self.N):
                z.append(index)
            i=index+1
        return z

    
    def generateSite(self,site):
        # this translate the List, with respect to site
        zList=self.generateList()
        
        center=list(site)
        z=[]
        for i in zList:
            temp=center[:]
            # case one, in 0th dimension
            if(i<self.LsZero-1):
                temp[0]=(center[0]+i+1)%self.LsZero
                z.append(temp[:])                
            # case two, in other dimensions
            else:
                extraindex=i-(self.LsZero-1)
                extra_dim=extraindex//2+1
                extra_pm=1-(extraindex%2)*2
                temp[extra_dim]=(temp[extra_dim]+extra_pm)%self.LsAll[extra_dim]
                z.append(temp[:])
                
        return [tuple(x) for x in z]


# generate random number (tuple) within the Ls(tuple)
def randomND(Ls):
    # Ls is a tuple, int, Ls[0] dimensional of imaginary time, Ls[1], L[2], etc. are spacial dimensions
    # return is also a tuple
    output=[np.random.randint(n) for n in Ls]
        
    return tuple(output)

class IsingND:
    def __init__(self,Ls,Ks,A):
        # Ls is a tuple, int, Ls[0] dimensional of imaginary time, Ls[1], L[2], etc. are spacial dimensions,
        # Ks is a tuple, double, Ks[0],Ks[1],Ks[2] are the couplings
        # A is a double, it is the Ls[0] dimension's longer range interaction
        self.Ls=Ls
        self.Ks=Ks
        self.A=A
        # s is a ndarray, bool type, it is the Ising field configuration
        self.s=np.random.choice(a=[False, True], size=Ls, p=[0.5,0.5])
        # dimension of the problem
        self.dimension=len(Ls)
        self.grow=Add_neighbours(Ls,Ks,A)
        
    def updateWolff(self):
        
        initial=randomND(self.Ls)
        
        sign=self.s[initial]
        
        oppoSign=not sign
        
        flag=np.full(self.Ls, False, dtype=bool)
        
        q=queue.Queue()
        
        q.put(initial)
        flag[initial]=True
        self.s[initial]=oppoSign
        
        def updateWolff_add(i):
            # i (tuple) is the current site
            # return the connected sites around i
            # https://stackoverflow.com/questions/14368297/python-scope-inside-a-nested-function-inside-a-class
            # Python nested function, self
            
            for j in self.grow.generateSite(i):
                if(flag[j]==False and sign==self.s[j]  ):
                    q.put(j)
                    flag[j]=True
                    self.s[j]=oppoSign
                    
            pass
            # a list of tuple sites gives (0)+(3)
            
            # next check to see (1) and (2) condition
            
            # (1) needs sign and self.s[]
            
            # (2) needs flag[]

            
            # s[y] is the site to be added
            #(0) y within the interaction neighbour
            #(1) s[y] same sign as s[i] or s[initial] or sign
            #(2) y has not been added before
            #(3) p=1-e^(-2K) condition
            
        
        while(q.qsize()!=0):
            current=q.get()
            updateWolff_add(current)
            
        pass
    

    
    
    def updateMetropolis(self):
        # find the mean field of site i
        # then flip it or not
        pass        

        
        
    def s_fft(self):
        temp=self.s*2-1 #convert True/False to 1/-1
        return np.square(np.absolute(np.fft.fftn(temp)))
    
    def s_mag(self):
        temp=np.sum(self.s)*2-np.prod(list(self.Ls))
        return temp


        
            
    def run(self,fileNameHDF5,storageStep,resizeStep,gapStep):
        
        f = h5py.File(fileNameHDF5, "a")
        # a Read/write if exists, create otherwise (default)
        
        
        f.create_dataset("Ls",data=self.Ls)
        f.create_dataset("Ks",data=self.Ks)
        f.create_dataset("A",data=self.A)

        #origin=tuple(np.zeros(len(self.Ls),dtype=int))
        
        eset= f.create_dataset("bigFFT",data=np.reshape(self.s_fft(), (1,)+self.Ls ),chunks=True,maxshape=((None,)+self.Ls))
        
        #m2set=f.create_dataset("m2",(resizeStep*storageStep+1,))
        m1set=f.create_dataset("m1",(resizeStep*storageStep+1,))
        #m2set[0]=temp[origin]
        m1set[0]=self.s_mag()
        
        
        for i in tqdm(range(storageStep)):
            eset.resize(eset.shape[0]+resizeStep, axis=0)
            
            temp=np.zeros((resizeStep,)+self.Ls)
            temp2=np.zeros(resizeStep)
            
            for n in range(resizeStep):
                for pp in range(gapStep):
                    self.updateWolff()
                temp[n,:]=np.reshape(self.s_fft(),(1,)+self.Ls )
                temp2[n]=self.s_mag()
                
                #m1set[resizeStep*i+n+1]=self.s_mag()
                
            eset[-resizeStep:,:]=temp
            m1set[resizeStep*i+1:resizeStep*(i+1)+1]=temp2
            
            #m2set[resizeStep*i+1:resizeStep*(i+1)+1]=temp[(Ellipsis,)+origin]

            
        f.close()
        
