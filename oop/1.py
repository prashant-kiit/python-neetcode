"""
This is docstring of OOP concepts
"""

class Car:
    def __init__(self, mileage, speed):
        self.mileage = mileage
        self.speed = speed
    
    def getMileage(self):
        return self.mileage
    
    def getSpeed(self):
        return self.speed

    def setMileage(self, mileage):
        self.mileage = mileage

    def setSpeed(self, speed):
        self.speed = speed

def main():
    car = Car(50, 100)
    car.setMileage(60)
    print(car.getMileage())

if __name__ == "__main__":
    main()
        
