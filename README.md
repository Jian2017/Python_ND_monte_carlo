# Python_ND_monte_carlo


from MONTECARLO import IsingND
p=IsingND((32,),(1.0,),0.5)
p.run("somename.hdf5",200,1000,1)
    
    1 is gap step
    1000 is group step
    200 is group numbers
    total 1000x200x1 steps
