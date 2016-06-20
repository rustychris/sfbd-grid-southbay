from __future__ import print_function
import unstructured_grid
from delft import dfm_grid
import utils
from shapely import geometry

## 
reload(unstructured_grid)
reload(dfm_grid)
g=unstructured_grid.UnTRIM08Grid("SFEI_SSFB_fo.grd")
#g.make_cell_nodes_from_edge_nodes()
g.report_orthogonality()

# => 
#    Mean circumcenter error: 0.00246137
#    Max circumcenter error: 0.172258
#  Recalculating edge to cells
#    Mean angle error: 0.29 deg
#    Max angle error: 24.32 deg


## 

circ_errs=g.circum_errors()
angle_errs=g.angle_errors()
angle_errs *= 180/np.pi
## 

plt.figure(1).clf()
fig,(ax1,ax2)=plt.subplots(1,2,sharex=True,sharey=True,num=1)

nontri=g.cells['nodes'][:,3]>=0
coll1=g.plot_cells(values=circ_errs[nontri],mask=nontri,ax=ax1,lw=0)
sel=angle_errs
coll2=g.plot_edges(values=angle_errs,ax=ax2)
coll2.set_clim([0,5])
ax1.axis('equal')

## 

plt.figure(1).clf()
coll=g.plot_cells(values=g.cells['depth_mean'],lw=0)
plt.axis('equal')

## 
# No useful depth info in the new grid, and the bathy in the rest of the grid has 
# been lost - bring in depth info from existing sfbd grid, set the new portions as
# -999
gsfbd=dfm_grid.DFMGrid(fn="../../cascade2/baydeltamodel/dec1999_mar2000/r14c_net.nc")
# has nodes['depth'], no cell or edge bathy

# Just for plotting:
cell_bathy=gsfbd.interp_node_to_cell(gsfbd.nodes['depth'])
gsfbd.add_cell_field('depth',cell_bathy)


## 

new_depths=np.nan*np.zeros(g.Nnodes(),'f8')

# match up new nodes to the old, copying depth
for ni,n in enumerate(g.valid_node_iter()):
    if ni%5000==0:
        print(ni)

    nold=gsfbd.select_nodes_nearest( g.nodes['x'][n] )
    if 0:# not robust to choose just by distance
        l=utils.dist(g.nodes['x'][n]-gsfbd.nodes['x'][nold])
        # one node is within 2.0
        if l<2.0:
            continue
    new_depths[n]=gsfbd.nodes['depth'][nold]


## 

try:
    g.nodes['depth']=new_depths
except ValueError:
    g.add_node_field('depth',new_depths)

## 

new_poly=geometry.Polygon([[  553270.22303312,  4182842.35987478],
                           [  557575.63187278,  4185671.62854085],
                           [  560281.88885771,  4185302.59349745],
                           [  573751.66794181,  4184256.99420782],
                           [  595340.2179807 ,  4149444.68844709],
                           [  595524.7355024 ,  4138004.6021017 ],
                           [  565940.42618984,  4140280.31820266],
                           [  552962.69383028,  4162729.95000949],
                           [  553147.21135198,  4181243.20802005]] )

mask=g.select_nodes_intersecting(new_poly)
## 
g.nodes['depth'][mask]=np.nan

## 
# with a distance cutoff of 5.0m, seems to grab all of the correct
# cells, plus about 5 extras in south bay.
# but why is the cell interpolated value missing a few cells here and
# there? fixed.

plt.figure(1).clf()
fig,(ax1,ax2)=plt.subplots(1,2,sharex=True,sharey=True,num=1)

for ax,gg in zip( [ax1,ax2],
                  [g,gsfbd] ):
    #coll=gg.plot_cells(values=gg.interp_node_to_cell(gg.nodes['depth']),lw=0,ax=ax)
    #coll.set_clim([-50,0])
    coll_e=gg.plot_edges(ax=ax,color='0.5',lw=0.2)
    sel=np.isnan(gg.nodes['depth'])
    coll_n=gg.plot_nodes(ax=ax,lw=0,mask=sel)
    coll_n.set_clim([-50,0])

# coll=g.plot_cells(values=g.interp_node_to_cell(g.nodes['depth']),lw=0)

ax1.axis('equal')

## 

# ah, but delta shell does not care for nans.
g.nodes['depth'][ np.isnan(g.nodes['depth']) ] = -9999

## 

dfm_grid.write_dfm(g,"SFEI_SSFB_fo_net.nc",overwrite=True)
