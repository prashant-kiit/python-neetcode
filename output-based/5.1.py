class Meta(type):
    def __new__(mcs, name, bases, ns):
        print(f"Creating {name}")
        ns['created_by'] = mcs.__name__
        return super().__new__(mcs, name, bases, ns)

class Base(metaclass=Meta):
    pass

class Child(Base):
    pass

print(Child.created_by)
print(Base.created_by)