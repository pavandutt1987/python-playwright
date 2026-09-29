class Employee:
    company = "OpenTech" # class varaible 

    def __init__(self,name,salary):
        self.name = name
        self.salary = salary

    #1 . Instance method
    def show_details(self):
        print(self.name)
        print(self.salary)
        print(self.company)
    #2. class method
    @classmethod
    def change_companyname(cls,new_company):
        cls.company = new_company
    @staticmethod
    def is_valid_salary(sla):
        return sla >0


# creating a object

emp = Employee("pavan","20000")
#instance Methos
emp.show_details()

# static method
print(Employee.is_valid_salary(2000))

# class Method 

Employee.change_companyname("TechGroup")

emp.show_details()