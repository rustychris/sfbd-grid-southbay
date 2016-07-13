import matplotlib.pyplot as plt
import numpy as np
import unstructured_grid
from delft import dfm_grid
import plot_utils
import utils
## 

g=dfm_grid.DFMGrid('SFEI_SSFB_fo_dwrbathy_net.nc')

## 


## 

vc=g.cells_center()

ec=g.edges_center()
g.edge_to_cells()

c2c =utils.dist( vc[g.edges['cells'][:,0]] - vc[g.edges['cells'][:,1]] )
A=g.cells_area()
Acc= A[g.edges['cells']].sum(axis=1)
c2c=c2c / np.sqrt(Acc) # normalized
c2c[ np.any(g.edges['cells']<0,axis=1) ] = np.inf



## 

# show center-to-center spacings
# 

plt.figure(1).clf()
fig,ax=plt.subplots(1,1,num=1)
thresh=0.06

# show the 21 worst offenders:
coll_base=g.plot_edges(ax=ax,lw=0.1,color='0.5')
colle=g.plot_edges(ax=ax,values=c2c,mask=c2c<thresh)
colle.set_clim([0,thresh])
colle.set_lw(2)

plot_utils.cbar(colle)
