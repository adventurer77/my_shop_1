from django.db import models
from django.urls import reverse

# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    sort = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["sort"]

    # def __iter__(self):
    #     for item in self.portfolios.all():
    #         yield item

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="goods_images", blank=True, null=True)
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)

    class Meta:
        db_table = "product"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("id",)

    def __str__(self):
        return self.name

    def display_id(self):
        return f"id: {self.id:05}"

    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})

    def total_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)

        return self.price
