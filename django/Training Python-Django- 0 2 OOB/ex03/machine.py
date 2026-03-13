import random
from beverages import HotBeverage


class CoffeeMachine:
	def __init__(self):
		self.drinks = 0
		self.is_broken = False

	class Emptycup(HotBeverage):
		def __init__(self):
			self.name = "empty cup"
			self.price = 0.90

		def description(self):
			return "An empty cup?! Gimme my money back!"

	class BrokenMachineException(Exception):
		def __init__(self):
			super().__init__("This coffee machine has to be repaired.")

	def repair(self):
		self.drinks = 0
		self.is_broken = False

	def serve(self, beverage):
		if self.is_broken:
			raise self.BrokenMachineException()
		self.drinks += 1
		if self.drinks > 10:
			self.is_broken = True
		if random.choice([True, False]):
			return beverage()
		else:
			return self.Emptycup()


if __name__ == "__main__":
	from beverages import Coffee, Tea, Chocolate, Cappuccino

	machine = CoffeeMachine()
	beverages_list = [Coffee, Tea, Chocolate, Cappuccino]

	print("test")
	try:
		for i in range(11):
			beverage_class = random.choice(beverages_list)
			drink = machine.serve(beverage_class)
			print(f"Bebida #{i+1}: {drink.name}")
	except CoffeeMachine.BrokenMachineException as e:
		print(f"\n {e}")

	machine.repair()

	print("test post repair")
	try:
		for i in range(11):
			beverage_class = random.choice(beverages_list)
			drink = machine.serve(beverage_class)
			print(f"Bebida #{i}: {drink.name}")
	except CoffeeMachine.BrokenMachineException as e:
		print(f"\n {e}")
