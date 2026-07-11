import random

random.randint(1, 10)    # Integer in [1, 10] (inclusive)

random.random()          # Float in [0.0, 1.0)
random.randrange(1, 10)  # Integer from 1 to 9
random.uniform(1, 10)    # Float in [1.0, 10.0]

lst = [89, 45, 93]
random.choice(lst)       # Random element from a list
random.sample(lst, 3)    # 3 unique random elements
random.shuffle(lst)      # Shuffle list in place