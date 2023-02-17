from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True,
                                 blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def filtered_reviews(self):
        return self.product_reviews.filter(stars__gte=4)

    def category_name(self):
        try:
            return self.category.name
        except:
            return ''


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,
                                related_name='product_reviews')
    text = models.TextField()
    stars = models.IntegerField(choices=(
        (1, '*'),
        (2, '* *'),
        (3, '* * *'),
        (4, '* * * *'),
        (5, '* * * * *'),
    ), default=5)

    def __str__(self):
        return self.text
