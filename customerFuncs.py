import uuid

class Customer:
    Database = None

    @classmethod
    def setDatabase(cls, Database:object) -> None:
        cls.Database = Database

    def __init__(self, id:int=None, firstName:str=None, Surname:str=None, email:str=None, phoneNumber:int=None) -> None:
        self.firstName = firstName
        self.Surname = Surname
        self.email = email
        self.id = id
        self.phoneNumber = phoneNumber

        if self.id:
            self.firstName, self.Surname, self.email, self.phoneNumber = Customer.Database.getRecords('Customers', 'firstName, Surname, Email, phoneNumber', f'ID = {self.id}')
        else:
            self.id = uuid.uuid4().int & (1<<32)-1

    def getID(self) -> int:
        return self.id

    def getName(self) -> str:
        return self.name
    
    def getEmail(self) -> str:
        return self.email
    
    def submitToDB(self) -> None:
        self.Database.addRecords('Customers', (self.name, self.email))
    
class Customers:
    def __init__(self, Database) -> None:
        self.allCustomers = dict()
        self.Database = Database

    def getAllCustomersFromDB(self) -> dict:
        customers = self.Database.getRecords('Customers', 'ID')
        for customer in customers:
            self.allCustomers[customer[0]] = Customer(customer[0])
        return self.allCustomers
    
    def addCustomer(self, customer:object) -> None:
        self.allCustomers[customer.id] = customer
    
    def newCustomer(self, firstName, Surname, email) -> object:
        newCustomer = Customer(None, firstName, Surname, email)
        self.addCustomer(newCustomer)
        # newCustomer.submitToDB()
        return newCustomer
    
    def getStoredCustomer(self, customerID) -> object:
        return self.allCustomers.get(customerID, None)
    
    def getCustomer(self, customerID:int) -> object:
        return self.allCustomers.get(customerID, None)
    