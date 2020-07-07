from decimal import Decimal
from django.conf import settings
import json

from shop.models import Product

class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.session = request.session
        cart = self.session.get(
            settings.CART_SESSION_ID
        )
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity
        """
        product_id = str(product.id)
        qty = 0
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
                'discount': str(product.percentage_discount),
                'total': 0
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
            price = product.price
            qty = int(self.cart[product_id]['quantity'])
            dis = product.percentage_discount
            total_price = price * qty
            print(total_price)
            per_dis = (dis/100) * total_price
            print(per_dis)
            total = total_price - per_dis
            print(total)
        else:
            self.cart[product_id]['quantity'] += quantity
            price = product.price
            qty = int(self.cart[product_id]['quantity'])
            dis = product.percentage_discount
            total_price = price * qty
            per_dis = (dis/100) * total_price
            total = total_price - per_dis

        self.cart[product_id]['total'] = float(total)
        self.save()

    def decrease(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] >= 1:
                self.cart[product_id]['quantity'] -= quantity
                price = product.price
                qty = int(self.cart[product_id]['quantity'])
                dis = product.percentage_discount
                total_price = price * qty
                per_dis = (dis/100) * total_price
                total = total_price - per_dis
                self.cart[product_id]['total'] = float(total)
            else:
                del self.cart[product_id]
            self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the product 
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product object and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        print(cart)
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['d'] = Decimal(item['discount']) 
            item['pd'] = item['d']/100 * item['total_price']
            item['total'] = round(Decimal(item['total_price']) - item['pd'], 2)
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        # total = sum(round((Decimal(item['price']) - (Decimal(item['discount'])/100) * (Decimal(item['price']))) * item['quantity'], 2) for item in self.cart.values())
        return sum(round(Decimal(item['total']), 2) for item in self.cart.values())
        # return total
    
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()