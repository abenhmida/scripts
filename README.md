# scripts

This a project tp gather some util scripts for doing various things.

### playbookscafold.py

this scripts help in generating a directory structure for a ansible playbook. in the form of 

`
first_playbook
|-- files
|-- group_vars
|-- host_vars
    |-- dev
    |-- uat
    |-- prd
|-- inventories
    |-- dev
    |-- uat
    |-- prd
|-- roles
|-- first_playbook.yml

`

there is plenty of rooms for enhancement.
