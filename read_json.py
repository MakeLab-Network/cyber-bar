import json
with open("texts\\recipes.json", 'rb') as f:
   recipes = json.load(f)
recepies = recipes['10_dispensers']
cocktails = recipes['cocktails']
ingredients = recipes['ingredients']
with open("texts\\questions1.json", 'rb') as f:
   questions = json.load(f)
questions = questions['questions']