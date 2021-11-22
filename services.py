from typing import List

service_name = {
    1 : "Warranty repair",
    2 : "Out of warranty repair",
    3 : "Device change",
    4 : "Sale of repaired equipment"
}

service_price = {
    1 : 0,
    2 : 350, 
    3 : 500,
    4 : 750
}

def is_repair(service):
    return service == 1 or service == 2

def is_change(service):
    return service == 3

def needs_tech(service):
    return service != 4
