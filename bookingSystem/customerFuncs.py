import uuid
import regex as re


class Customer:
    Database = None

    @classmethod
    def setDatabase(cls, Database: object) -> None:
        cls.Database = Database

    def __init__(self, id: int = None, firstName: str = None, Surname: str = None, email: str = None,
                 phoneNumber: int = None) -> None:
        self.firstName = firstName
        self.Surname = Surname
        self.email = email
        self.id = id
        self.phoneNumber = phoneNumber

        if self.id:
            try:
                self.id, self.firstName, self.Surname, self.email, self.phoneNumber = self.Database.getCustomerInfoByID(ID=self.id)[0]
            except IndexError:
                self.id = uuid.uuid4().int & (1 << 32) - 1
        else:
            self.id = uuid.uuid4().int & (1 << 32) - 1

    def getID(self) -> int:
        return self.id

    def getName(self) -> str:
        return self.firstName + ' ' + self.Surname

    def getFirstName(self) -> str:
        return self.firstName

    def getSurname(self) -> str:
        return self.Surname

    def getPhoneNumber(self) -> int:
        return self.phoneNumber

    def getEmail(self) -> str:
        return self.email

    def submitToDB(self) -> bool:
        if self.Database.newCustomer(self):
            return True

        return False


class Customers:
    def __init__(self, Database) -> None:
        self.allCustomers: {int: Customer} = dict()
        self.Database = Database

    def getAllCustomersFromDB(self) -> dict:
        customers = self.Database.getAllCustomers()
        for customer in customers:
            self.allCustomers[customer[0]] = Customer(customer[0], customer[1], customer[2], customer[3])
        return self.allCustomers

    def getAllCustomerInfoFromDB(self, *args: str) -> dict:
        args = list(args)
        if 'Name' in args:
            args[args.index('Name')] = 'firstName'
            args.insert(args.index('firstName') + 1, 'Surname')

        info = self.Database.getAllCustomerInfo(args)

        return info

    def getCustomerByID(self, customerID: int) -> object:
        customer = Customer(id=customerID)
        self.allCustomers[customerID] = customer

        return customer

    def addCustomer(self, customer: object) -> None:
        self.allCustomers[customer.id] = customer

    def newCustomer(self, firstName, surname, email, phoneNumber, inDB=True) -> object:
        # Detail validation
        if len(phoneNumber) != 11 or not re.match(r'^07[0-9]{9}$', phoneNumber) or not re.match(
                r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return None

        newCustomer = Customer(None, firstName, surname, email, phoneNumber)
        self.addCustomer(newCustomer)
        if not inDB:
            newCustomer.submitToDB()
        return newCustomer

    def getStoredCustomer(self, customerID) -> object:
        if customerID in self.allCustomers.keys():
            return self.allCustomers.get(customerID, None)
        return None

    def getCustomer(self, customerID: int) -> object:
        return self.allCustomers.get(customerID, None)
