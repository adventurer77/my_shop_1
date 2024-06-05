from django.db import models

from users.models import User
from goods.models import Products

# Create your models here.

class Cartqueryset(models.QuerySet):
    def total_cart_price(self):
        return sum(cart.product_price() for cart in self)
    
    def total_cart_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0
    

class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "Cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["-created_timestamp"]

    objects = Cartqueryset().as_manager()

    def product_price(self):
        return round(self.product.total_price() * self.quantity,2)

    def __str__(self):
        if self.user:
            return f"Cart {self.user.username} | Product {self.product.name} | Quantity {self.quantity} "

        return f"Unauthorized user's shopping cart| Product {self.product.name} | Quantity {self.quantity} "
