# vagrant-edfcellinsight
Thermo CellInsight plate reader allows imaging of six channels. These can also be used to 
record different focus levels of the same fluorescent channel. This script uses an
ImageJ Extended Depth of Field plugin to combine such data.

[http://bigwww.epfl.ch/demo/edf/]
[https://github.com/fiji-BIG/Extended_Depth_Field] 

```
# clone this repository
git clone https://github.com/UH-LMU/vagrant-edfcellinsight.git

# create folders in the repository folder (these will be shared with the VM)
mkdir data
mkdir output

# copy data
cp CELLINSIGHTDATA ./data/
 
# create and start virtual machine
vagrant up

# log in to virtual machine
vagrant ssh -- -X

# run script (data and output folders are in /vagrant)
# indicate which slices to combine with option -s
python /vagrant/mp_edf_cellomics.py /vagrant/data/TIF/LMU-CELLINSIGHT_160510170001 /vagrant/output/ -s d1,d2
```

