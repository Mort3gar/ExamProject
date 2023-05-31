from app import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcode = db.Column(db.BigInteger, nullable=False, unique=True)
    code = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)
    packageWeight = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    typeId = db.Column(db.Integer, db.ForeignKey('productTypes.id'), nullable=False)
    # def __str__(self) -> str:
    #     return f"{self.barcode} {self.code} {self.name} {self.packageWeight} {self.price}"

    def __repr__(self) -> str:
        return f"{self.barcode} {self.code} {self.name} {self.packageWeight} {self.price}"


class ProductAvailability(db.Model):
    __tablename__ = "productsAvailability"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productID = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship(Product)
    curAmount = db.Column(db.Integer, nullable=False)
    deadlineDate = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"{self.productID} {self.product} {self.curAmount} {self.deadlineDate}"

class ProductType(db.Model):
    __tablename__ = "productTypes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(10), nullable=False, unique=True)


class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    cardID = db.Column(db.Integer, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"{self.name} {self.cardID}"


class Shop(db.Model):
    __tablename__ = "shops"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.Text, nullable=False)


class Sale(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerId = db.Column(db.Integer, db.ForeignKey("customers.id"))
    customer = db.relationship(Customer)
    productId = db.Column(db.Integer, db.ForeignKey("products.id"))
    product = db.relationship(Product)
    amount = db.Column(db.Integer, nullable=False)
    shopId = db.Column(db.Integer, db.ForeignKey("shops.id"))
    shop = db.relationship(Shop)

