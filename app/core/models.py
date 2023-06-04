"""
Django custom user model
"""
import os
import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, mobile, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        if not mobile:
            raise ValueError("User must have a mobile number.")
        user = self.model(
            email=self.normalize_email(email), mobile=mobile, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, mobile, password):
        """Create and return a new superuser."""
        user = self.create_user(email, mobile, password)
        user.is_superuser = True
        user.is_delivery_partner = True
        user.is_employee = True
        user.is_distributer = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model for register the user on the site for different purposes
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    mobile = models.BigIntegerField(blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_delivery_partner = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_distributer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["mobile"]

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class State(models.Model):
    """State for regieste avelable state option in which city in the system."""

    state = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.state


class District(models.Model):
    """District for regieste avelable state option in which city in the system."""

    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=False, null=False)
    district = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.district


class City(models.Model):
    """
    City model for regieste avelable delevery option in which
    city in the system.
    """

    district = models.ForeignKey(
        District, on_delete=models.CASCADE, blank=False, null=False
    )
    city = models.CharField(max_length=30, unique=True)
    is_delevery_available = models.BooleanField(default=False)

    def __str__(self):
        return self.city


class PinCode(models.Model):
    """PinCode model for register pincodes of different cities."""

    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=False, null=False)
    pincode = models.IntegerField(blank=False, unique=True)

    def __str__(self):
        return str(self.pincode)


class ConnectionPurpose(models.Model):
    """
    ConnectionPerpose model for request for delership or distributer
    """

    connection_purpose = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.connection_purpose


class RegisterDocumentType(models.Model):
    """
    RegisterDocumentType model for request for delership or distributer.
    """

    register_document_type = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.register_document_type


def verification_document_upload_path(instance, filename):
    """
    Return the path for the image upload of document verification.
    """
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("document", filename)


class RequestForConnectWithUs(models.Model):
    """
    RequestForConnectWithUs model for request for delership or distributer
    in the system.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    connection_purpose = models.ForeignKey(
        ConnectionPurpose, on_delete=models.CASCADE, blank=False, null=False
    )
    registered_name = models.CharField(max_length=255, blank=False)
    registered_mobile = models.BigIntegerField(blank=False, unique=True)
    registered_email = models.EmailField(max_length=255, unique=True)
    register_address = models.TextField(max_length=255, blank=False)
    register_land_mark = models.CharField(max_length=255, blank=False, null=True)
    register_state = models.ForeignKey(
        State, on_delete=models.CASCADE, blank=False, null=False
    )
    register_district = models.ForeignKey(
        District, on_delete=models.CASCADE, blank=False, null=False
    )
    register_city = models.ForeignKey(
        City, on_delete=models.CASCADE, blank=False, null=False
    )
    register_pincode = models.ForeignKey(
        PinCode, on_delete=models.CASCADE, blank=False, null=False
    )
    register_document_type = models.ForeignKey(
        RegisterDocumentType, on_delete=models.CASCADE, blank=False, null=False
    )
    register_document_number = models.CharField(max_length=255, blank=False)
    register_document = models.ImageField(
        upload_to=verification_document_upload_path, blank=False, null=False
    )

    def __str__(self):
        return self.user.name


class Address(models.Model):
    """
    Address model for storing the different address for delevery
    product in the system.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False)
    mobile = models.BigIntegerField(blank=False)
    secondary_mobile = models.BigIntegerField(blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=False, null=False)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, blank=False, null=False
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=False, null=False)
    pincode = models.ForeignKey(
        PinCode, on_delete=models.CASCADE, blank=False, null=False
    )
    address_in_detail = models.TextField(max_length=255, blank=False)
    land_mark = models.CharField(max_length=255, blank=False, null=True)
    home_time = models.BooleanField(default=True)
    office_time = models.BooleanField(default=False)

    def __str__(self):
        return self.name + "," + self.address_in_detail


class UserAddress(models.Model):
    """
    UserAddress more select the address to the user with product item for delever
    the product in the system.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, blank=False, null=False
    )

    def __str__(self):
        return self.user.name


def image_upload_path(instance, filename):
    """Return the path for the image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("product", filename)


class Category(models.Model):
    """Product Type in the system."""

    category = models.CharField(max_length=30, unique=True)
    category_discription = models.TextField(max_length=255, blank=False)

    def __str__(self):
        return self.category


class SubCategory(models.Model):
    """Product Sub Type in the system."""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=False, null=False
    )
    sub_category = models.CharField(max_length=30, unique=True)
    sub_category_discription = models.TextField(max_length=255, blank=False)

    def __str__(self):
        return self.sub_category


class BrandName(models.Model):
    """Brand Name in the system."""

    brand_name = models.CharField(max_length=30, unique=True)
    brand_discription = models.TextField(max_length=255, blank=False)

    def __str__(self):
        return self.brand_name


# creating a mode for product
class Product(models.Model):
    """Product in detail the system."""

    registered_user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False
    )
    name = models.CharField(max_length=255)
    product_image1 = models.ImageField(
        upload_to=image_upload_path, blank=True, null=True
    )
    product_image2 = models.ImageField(
        upload_to=image_upload_path, blank=True, null=True
    )
    product_image3 = models.ImageField(
        upload_to=image_upload_path, blank=True, null=True
    )
    product_image4 = models.ImageField(
        upload_to=image_upload_path, blank=True, null=True
    )
    product_image5 = models.ImageField(
        upload_to=image_upload_path, blank=True, null=True
    )
    brand = models.ForeignKey(
        BrandName,
        on_delete=models.CASCADE,
        blank=False,
    )
    product_categoty = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    product_sub_categoty = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, blank=False, null=False
    )
    dicription = models.TextField(max_length=255, blank=False)
    is_available = models.BooleanField(default=True)
    product_created = models.DateTimeField(auto_now_add=True)
    product_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductVarient(models.Model):
    """Product Varient in the system."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=False, null=False
    )
    varient = models.CharField(max_length=255, blank=False)
    price = models.IntegerField(blank=False)
    discount_price = models.IntegerField(blank=False)
    quantity_in_stock = models.IntegerField(blank=False, null=False)
    is_available = models.BooleanField(default=True)
    product_created = models.DateTimeField(auto_now_add=True)
    product_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.varient


class ProductConfiguration(models.Model):
    """
    Product cofiguration to connect product with different categories in the system.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=False, null=False
    )
    product_varient = models.ForeignKey(
        ProductVarient, on_delete=models.CASCADE, blank=False, null=False
    )

    def __str__(self):
        return self.product.name


class ProductReview(models.Model):
    """
    Product Review in the system.
    """

    """
    Notr: adding the validattors for the rating field we need to handel it
    manually for handeling this we have to vall 'full_clean()' method in the
    'views.py or serializers.py'
    articale link #https://docs.djangoproject.com/en/4.1/ref/models/instances/#django.db.models.Model.full_clean
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=False, null=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    review = models.TextField(max_length=255, blank=False)
    rating = models.IntegerField(
        blank=False,
    )
    review_created = models.DateTimeField(auto_now_add=True)
    review_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name + "," + self.product.name + "," + str(self.rating)


class Cart(models.Model):
    """Cart model for manage the cart item if the user"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    product_id = models.ManyToManyField(
        ProductConfiguration,
    )

    def __str__(self):
        return str(self.user.id)


class PaymetType(models.Model):
    """PaymetType model for manage the paymet type if the user"""

    payment_type = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.payment_type


class Order(models.Model):
    """Order model for manage the order item if the user"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(
        ProductConfiguration, on_delete=models.SET_NULL, blank=False, null=True
    )
    payment_type = models.ForeignKey(
        PaymetType, on_delete=models.SET_NULL, blank=False, null=True
    )
    shipping_address = models.ForeignKey(
        UserAddress, on_delete=models.SET_NULL, blank=False, null=True
    )
    order_date = models.DateTimeField(auto_now_add=True)
    delevered_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.user.name


class PaymentDetails(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, blank=False)
    payment_status = models.BooleanField(default=False)
    payment_type = models.ForeignKey(
        PaymetType, on_delete=models.CASCADE, blank=False, null=False
    )
    payment_id = models.CharField(max_length=50)
    payment_signature = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
