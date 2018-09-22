# Python_ND_monte_carlo

```python
from MONTECARLO import IsingND
p=IsingND((32,),(1.0,),0.5)
p.run("somename.hdf5",200,1000,1)
```
    
    1 is gap step
    1000 is group step
    200 is group numbers
    total 1000x200x1 steps
    
    
```python
from MONTECARLO import IsingND
p=IsingND((32,32),(0.2,0.2),0.1)
p.run("somename2.hdf5",50,200,6)
```
    in this case there are 500x200x6 steps running
    but only 500x200 is stored, because the step gap is 6
