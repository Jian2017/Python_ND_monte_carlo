# Python_ND_monte_carlo
```python
p=IsingND(Ls,Ks,A)
```
where Ls and Ks must be python tuple, even it is one dimension, it should be written as (32,)  
Ls is the system dimension  
Ks is the nearest coupling  
A is the longer range coupling in Ls[0] dimension

## 1-d monte carlo 

```python
from MONTECARLO import IsingND
p=IsingND((32,),(1.0,),0.5)
p.run("somename.hdf5",200,1000,1)
```
    
    1 is gap step
    1000 is group step
    200 is group numbers
    total 1000x200x1 steps
    
## 2-d monte carlo    
```python
from MONTECARLO import IsingND
p=IsingND((32,32),(0.2,0.2),0.1)
p.run("somename2.hdf5",50,200,6)
```
    in this case there are 500x200x6 steps running
    but only 500x200 is stored, because the step gap is 6
    
    
## high-d monte carlo
yes, it can go to arbitary dimension.\
but the speed is slow, as the system size goes\
c++ is a better alternative
    
    
## what is the output?
the output is a hdf5 format file\
![alt text](/image/h5file2.png "Logo Title Text 1")\
`m1` is the spin sum
`bigFFT` is the n-d Fourier transform then square of the Ising field
![alt text](/image/h5file1.png "Logo Title Text 1")\


## analysis data, be patient!

in the `ANALYSIS.py` package, I wrote function to read the hdf5 file
```python
from ANALYSIS import readm1
m1=readm1("somename2.hdf5")
```
`analysis1_binderRatio_with_error.py` provides function to estimate the Binder ratio and its error

to find the phase boundary is not an easy job, especially for the active scaling type

![alt text](/image/binder_ratio.png "Logo Title Text 1")\
![alt text](/image/binder_ratio_zoom.png "Logo Title Text 1")\





