# ChymScripts

Chym scripts to create input river networks for coupled CHyM.
Example here is for the joint Mediterranean and Black Sea basins.
The dataset used is the Hydrosheds and GLCC.

The Hydorsheds data can be obtained from:

https://www.hydrosheds.org/

The GLCC data can be otianed from the USGS:

https://doi.org/10.5066/F7GB230D

Tools used are:

* GDAL (https://gdal.org/index.html),
* NCO tools (https://nco.sourceforge.net/)
* CHyM model source code (https://github.com/ICTP/CHyM)
* original python scripts.

1) merge EU and AF hydrosheds DEM datasets at 3s over the MED. This step must
be performed if your domain area extends over multiple source tiles.
Note: A LOT of memory is required here.

```bash
    gdal_translate -ot Float32 -of netCDF -r mode \
                 -projwin -5.79 55.89 46.29 28.23 -tr 0.06 0.06  \
       hydrosheds/3sdata/eu_dem_3s.tif dem_eu_med_mode.nc
    gdal_translate -ot Float32 -of netCDF -r mode \
                 -projwin -5.79 55.89 46.29 28.23 -tr 0.06 0.06  \
       hydrosheds/3sdata/af_dem_3s.tif dem_af_med_mode.nc
    python3 merge.py dem_eu_med_mode.nc dem_af_med_mode.nc 32766
    ncrename -v Band1,dem dem_eu_med_mode.nc
    ncatted -a _FillValue,dem,d,, dem_eu_med_mode.nc
    ncap2 -s 'where(dem > 32766) dem=-1.0' dem_eu_med_mode.nc
    cp dem_med_eu_mode.nc mydem.nc
```

2) process GLCC Global Ecosystems for the MED and doctor internal waters. In
the original data a lot of lakes are present, and most importantly the Black
Sea is classified as internal waters.

```bash
    gdal_translate -ot Float32 -of netCDF -r mode \
                 -projwin -5.79 55.89 46.29 28.23 -tr 0.06 0.06 \
        GLCC/gbogegeo20.tif luc_med_eu_mode.nc
    ncrename -v Band1,luc luc_med_eu_mode.nc
    python3 fill_lakes.py luc_med_eu_mode.nc
    cp luc_med_eu_mode.nc mylnd.nc
```

3) Run modified chym preproc with the namelist. The CHyM model can be obtaind
from ICTP here: 

```bash
    here=$PWD
    cp mydem.nc mylnd.nc $CHYMDIR/bin
    cd $CHYMDIR
    patch -p1 -i chympatch.patch
    (compile chym)
    cd bin
    cp $here/namelist.in .
    mpirun -np 1 ./preprocMPI namelist.in
    cp output/* $here/chym_stk.nc
    cd $here
```

4) Mask out all the non required basins.

```bash
    python3 basinmask.py
    ncks -A mask_med.nc chym_stk.nc
    ncap2 -s 'where(mask==0){fdm=0.0;acc=0.0;dra=0.0;run=0.0;alf=0.0;}' \
          chym_stk.nc tmp.nc
    mv tmp.nc chym_stk.nc
```
