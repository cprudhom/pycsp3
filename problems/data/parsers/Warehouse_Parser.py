from pycsp3.problems.data.dataparser import *

nWarehouses = number_in(line())
nStores = number_in(next_line())

data["fixedCost"] = number_in(next_line())
if next_line().startswith("capacity"):
    data["warehouseCapacities"] = numbers_in(line())
    next_line()
else:
    data["warehouseCapacities"] = [data.nStores] * data.nWarehouses
data["storeSupplyCosts"] = [numbers for numbers in [numbers_in(line) for line in remaining_lines()] if numbers]

assert nWarehouses == len(data["warehouseCapacities"]) and nStores == len(data["storeSupplyCosts"])
