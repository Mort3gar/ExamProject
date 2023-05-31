import pymysql.err
import sqlalchemy.exc
from datetime import datetime
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import select
from app.models import Product, ProductAvailability, Customer, Shop, Sale, ProductType
from sqlalchemy.orm import aliased

@app.route("/", methods=["GET"])
def home_page():
    try:
        db.session.add_all([
            ProductType(type="piece"),
            ProductType(type="weight")
        ])
        db.session.commit()
    except Exception:
        pass
    if request.method == "GET":
        return render_template("home.html")

@app.route('/base', methods=["GET"])
def base_page():
    if request.method == "GET":
        return render_template("base.html")


@app.route("/newproduct", methods=["GET", "POST"])
def newProduct_page():
    if request.method == "POST":
        error = None
        barcode = request.form["productBarcode"]
        if len(barcode) == 13:
            barcode = int(barcode)
        else:
            error = "Barcode must be 13 digits"
            flash(error)

        code = request.form["productCode"]
        if len(code) == 2:
            code = int(code)
        else:
            error = "Code must be 2 digits"
            flash(error)
        name = request.form["productName"]

        packageWeight = int(request.form["packageWeight"])

        productType = request.form["productType"]

        price = int(request.form["productPrice"])
        if error is None:
            try:
                if productType == "piece":
                    product = Product(barcode=barcode,
                                           code=code,
                                           name=name,
                                           packageWeight=packageWeight,
                                           price=price,
                                           typeId=1
                                           )
                else:
                    product = Product(barcode=barcode,
                                      code=code,
                                      name=name,
                                      packageWeight=packageWeight,
                                      price=price,
                                      typeId=2
                                      )
                db.session.add(product)
                db.session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                error = e
                flash(e.args[0])
            if error is None:
                return redirect(url_for("home_page"))

    return render_template("newProduct.html")

@app.route("/newshop", methods=["GET", "POST"])
def newShop_page():
    if request.method == "POST":
        error = None
        address = request.form["shopAddress"]
        try:
            db.session.add(Shop(address=address))
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            error = e
            flash(e.args[0])
        if error is None:
            return redirect(url_for("home_page"))
    return render_template("newShop.html")

@app.route("/newcustomer", methods=["GET", "POST"])
def newCustomer_page():
    if request.method == "POST":
        error = None
        name = request.form["customerName"]
        cardId = request.form["cardId"]
        if len(cardId) == 4:
            cardId = int(cardId)
        else:
            error = "Card ID must be 4 digits"
            flash(error)

        if error is None:
            try:
                db.session.add(Customer(name=name,
                                        cardID=cardId))
                db.session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                error = e.args[0]
                flash(error)
            if error is None:
                return redirect(url_for("home_page"))
    return render_template("newCustomer.html")

@app.route("/newsupply", methods=["GET", "POST"])
def newSupply_page():
    if request.method == "POST":
        error = None
        productId = int(request.form["productId"])
        amount = int(request.form["amount"])
        date = request.form["date"]
        temp = date.split("-")
        date = datetime(int(temp[0]), int(temp[1]), int(temp[2]))
        temp = aliased(Product)
        product = db.session.execute(select(Product).where(Product.id == productId)).fetchone()
        try:
            db.session.add(ProductAvailability(
                productID=productId,
                product=product["Product"],
                curAmount=amount,
                deadlineDate=date
            ))
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            error = e.args[0]
            flash(error)
        if error is None:
            return redirect(url_for("home_page"))
    products = db.session.execute(select(Product.id, Product.name)).all()
    return render_template("newSupply.html", products=products)

@app.route("/newsale", methods=["GET", "POST"])
def newSale_page():
    if request.method == "POST":
        error = None
        customerId = int(request.form["customerId"])
        customer = db.session.execute(select(Customer).where(Customer.id==customerId)).fetchone()
        customer = customer["Customer"]


        productId = int(request.form["productId"])
        productAvailability = db.session.execute(select(ProductAvailability).where(ProductAvailability.id==productId)).fetchone()
        productAvailability = productAvailability["ProductAvailability"]

        product = db.session.execute(select(Product).where(Product.id==productAvailability.productID)).fetchone()
        product = product["Product"]

        amount = int(request.form["amount"])

        shopId = int(request.form["shopId"])
        shop = db.session.execute(select(Shop).where(Shop.id==shopId)).fetchone()
        shop = shop["Shop"]
        if amount <= productAvailability.curAmount:
            if productAvailability.curAmount - amount > 0:
                print("Okay")
                productAvailability.curAmount -= amount
            else:
                db.session.delete(productAvailability)
            db.session.commit()
        else:
            error = "Amount bigger than current amount"
            flash(error)
        if error is None:
            try:
                db.session.add(Sale(
                    customerId=customerId,
                    customer=customer,
                    productId=product.id,
                    product=product,
                    amount=amount,
                    shopId=shopId,
                    shop=shop
                ))
                db.session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                error = e.args[0]
                flash(error)
            if error is None:
                return redirect(url_for("home_page"))
    customers = db.session.execute(select(Customer.id, Customer.name)).all()
    productsAvailability = db.session.execute(select(ProductAvailability.id, ProductAvailability.productID)).all()
    productsList=[]
    for item in productsAvailability:
        temp = db.session.execute(select(Product).where(Product.id==item[1])).fetchone()
        temp = temp["Product"]
        productsList.append({"id":item[0],"name":temp.name})
    shops = db.session.execute(select(Shop.id, Shop.address)).all()
    if len(customers) == 0 or len(productsList)==0 or len(shops) == 0:
        message = ""
        if len(customers) == 0:
            message = "No customers"
        elif len(productsList) == 0:
            message = "No available products"
        else:
            message = "No shops"
        return render_template("error.html", message=message)
    return render_template("newSale.html",
                           customers=customers,
                           products=productsList,
                           shops=shops
                           )

@app.route("/products", methods=["GET"])
def products_page():
    products = db.session.execute(select(Product.id,
                                         Product.barcode,
                                         Product.code,
                                         Product.name,
                                         Product.packageWeight,
                                         Product.price
                                         )).all()
    return render_template("products.html", products=products)

@app.route("/productsavailability", methods=["GET"])
def productsAvailability_page():
    products = db.session.execute(select(ProductAvailability.id,
                               ProductAvailability.productID,
                               ProductAvailability.curAmount,
                               ProductAvailability.deadlineDate
                                         )).all()
    return render_template("productsAvailability.html", products=products)

@app.route("/customers", methods=["GET"])
def customers_page():
    customers = db.session.execute(select(Customer.id,
                                         Customer.name,
                                         Customer.cardID
                                         )).all()
    return render_template("customers.html", customers=customers)
@app.route("/shopss", methods=["GET"])
def shops_page():
    shops = db.session.execute(select(Shop.id,
                                          Shop.address
                                         )).all()
    return render_template("shops.html", shops=shops)

@app.route("/sales", methods=["GET"])
def sales_page():
    sales = db.session.execute(select(Sale.id,
                                          Sale.customerId,
                                          Sale.productId,
                                          Sale.amount,
                                          Sale.shopId
                                         )).all()
    print(sales)
    return render_template("sales.html", sales=sales)