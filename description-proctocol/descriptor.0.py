class Positive:
    def __get__(self, instance, owner):
        return instance._value

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Value must be positive")
        instance._value = value


class Account:
    balance = Positive()   # descriptor

    def __init__(self, balance):
        self.balance = balance


a = Account(100)
print(a.balance)     # 100

a.balance = 200
print(a.balance)     # 200

# a.balance = -50      # ValueError