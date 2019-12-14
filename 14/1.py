import math
import collections

class Recipe:
    def __init__(self):
        self.inputs = []
        self.input_quantities = []
        self.output = None
        self.output_quantity = 0

with open('input', 'r') as f:
    unparsed_recipes = f.read().strip().split('\n')

recipes = []
for recipe in unparsed_recipes:
    rec = Recipe()
    inp, out = recipe.split('=>')
    for chem in inp.split(','):
        q = int(chem.strip().split(' ')[0])
        n = chem.strip().split(' ')[1]
        rec.inputs.append(n)
        rec.input_quantities.append(q)
    rec.output_quantity = int(out.strip().split(' ')[0])
    rec.output = out.strip().split(' ')[1]
    recipes.append(rec)

def get_recipe_that_produces(chem, recipes):
    for r in recipes:
        if r.output == chem:
            return r
    raise Exception("recipe doesnt contain that chemical")

requirements = collections.OrderedDict()
requirements['FUEL'] = 1
excess= {}


while True:
    # print(requirements)
    # print(excess)
    if len(requirements) == 1 and 'ORE' in requirements:
        break

    #pick a item
    chem, num = requirements.popitem(last=True)
    if chem == 'ORE':
        requirements[chem] = num
        requirements.move_to_end(chem, last=False)
        continue
    # reduce required number by the excess number
    if chem in excess:
        if excess[chem] >= num:
            excess[chem] -= num
            num = 0
            continue
        else:
            num -= excess[chem]
            excess[chem] = 0

    #search for a recipe that produces this
    recipe = get_recipe_that_produces(chem, recipes)
    #check how many of this recipe we need
    batches = math.ceil(num /recipe.output_quantity)
    #add the inputs to requirements
    leftover = batches*recipe.output_quantity - num
    if chem in excess:
        excess[chem] += leftover
    else:
        excess[chem] = leftover
    for inp,quant in zip(recipe.inputs, recipe.input_quantities):
        if inp in requirements:
            requirements[inp] += batches*quant
        else:
            requirements[inp] = batches*quant


print(requirements)


