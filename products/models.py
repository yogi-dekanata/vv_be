# from django.db import models
#
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#
# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.PositiveIntegerField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#
#     class Meta:
#         app_label = 'products'
