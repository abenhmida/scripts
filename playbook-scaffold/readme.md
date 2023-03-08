
### playbookscafold.py

this scripts helps in generating a directory structure for a ansible playbook. in the form of 

```
playbook
    |-- files
    |-- group_vars
        |-- dev
        |-- uat
        |-- prd
    |-- host_vars
        |-- dev
        |-- uat
        |-- prd
    |-- inventories
        |-- dev
        |-- uat
        |-- prd
    |-- roles
    |-- playbook.yml
    |-- requirements.txt

```