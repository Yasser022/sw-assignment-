from abc import ABC, abstractmethod

class InventoryManager:
    _instance = None
    _inventory = {
        "Margherita": 10,
        "Pepperoni": 10,
        "Cheese": 15,
        "Olives": 10,
        "Mushrooms": 12,
    }

    def check_and_decrement(self, item: str) -> bool:
        if self._inventory.get(item, 0) > 0:
            self._inventory[item] -= 1
            return True
        return False

    def get_inventory(self):
        return self._inventory

class Pizza(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass


class Margherita(Pizza):
    def get_description(self) -> str:
        return "Margherita"

    def get_cost(self) -> float:
        return 5.0

class Pepperoni(Pizza):
    def get_description(self) -> str:
        return "Pepperoni"

    def get_cost(self) -> float:
        return 6.0

# Pizza Factory
class PizzaFactory:
    @staticmethod
    def create_pizza(pizza_type: str) -> Pizza:
        inventory = InventoryManager()
        if pizza_type == "Margherita" and inventory.check_and_decrement("Margherita"):
            return Margherita()
        elif pizza_type == "Pepperoni" and inventory.check_and_decrement("Pepperoni"):
            return Pepperoni()
        else:
            raise ValueError("Pizza type unavailable or out of stock!")


class ToppingDecorator(Pizza):
    def __init__(self, pizza: Pizza):
        self._pizza = pizza

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass

class Cheese(ToppingDecorator):
    def get_description(self) -> str:
        return self._pizza.get_description() + ", Cheese"

    def get_cost(self) -> float:
        return self._pizza.get_cost() + 1.0

class Olives(ToppingDecorator):
    def get_description(self) -> str:
        return self._pizza.get_description() + ", Olives"

    def get_cost(self) -> float:
        return self._pizza.get_cost() + 0.5

class Mushrooms(ToppingDecorator):
    def get_description(self) -> str:
        return self._pizza.get_description() + ", Mushrooms"

    def get_cost(self) -> float:
        return self._pizza.get_cost() + 0.7


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass

class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid ${amount:.2f} using PayPal.")

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> None:
        print(f"Paid ${amount:.2f} using Credit Card.")

# Main Function
def main():
    inventory_manager = InventoryManager()

    print("Welcome to the Pizza Restaurant!")

    while True:
        print("\nChoose your base pizza:")
        print("1. Margherita ($5.0)")
        print("2. Pepperoni ($6.0)")
        print("0 => to exit")
        pizza_choice = input("Enter the number of your choice: ")
        if pizza_choice == '0':
            break

        try:
            if pizza_choice == "1":
                pizza = PizzaFactory.create_pizza("Margherita")
            elif pizza_choice == "2":
                pizza = PizzaFactory.create_pizza("Pepperoni")
            else:
                print("Invalid choice!")
                continue

            while True:
                print("\nAvailable toppings:")
                print("1. Cheese ($1.0)")
                print("2. Olives ($0.5)")
                print("3. Mushrooms ($0.7)")
                print("4. Finish order")
                topping_choice = input("Enter the number of your choice: ")

                if topping_choice == "1" and inventory_manager.check_and_decrement("Cheese"):
                    pizza = Cheese(pizza)
                elif topping_choice == "2" and inventory_manager.check_and_decrement("Olives"):
                    pizza = Olives(pizza)
                elif topping_choice == "3" and inventory_manager.check_and_decrement("Mushrooms"):
                    pizza = Mushrooms(pizza)
                elif topping_choice == "4":
                    break
                else:
                    print("Topping unavailable or out of stock!")

            print("\nYour order:")
            print(f"Description: {pizza.get_description()}")
            print(f"Total cost: ${pizza.get_cost():.2f}")

            print("\nChoose payment method:")
            print("1. PayPal")
            print("2. Credit Card")
            payment_choice = input("Enter the number of your choice: ")

            if payment_choice == "1":
                payment_method = PayPalPayment()
            elif payment_choice == "2":
                payment_method = CreditCardPayment()
            else:
                print("Invalid payment method!")
                continue

            payment_method.pay(pizza.get_cost())
            print("Payment successful!")

        except ValueError as e:
            print(e)

        print("\nRemaining Inventory:")
        print(inventory_manager.get_inventory())

if __name__ == "__main__":
    main()
