from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from order.exceptions import OrderException
from .managers import LaundryOutletManager

import uuid


class LaundryOutlet(models.Model):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=100, null=False)
    phone_number = models.CharField(max_length=15, null=False)
    password = models.TextField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = LaundryOutletManager()

    address = models.TextField()
    latitude = models.FloatField(null=True, default=None)
    longitude = models.FloatField(null=True, default=None)

    total_quota = models.IntegerField(default=10)
    amount_of_active_orders = models.IntegerField(default=0)
    amount_of_reviewed_orders = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    outlet_rating = models.FloatField(default=0)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password) -> bool:
        return check_password(raw_password, self.password)

    def set_is_available(self, is_available):
        self.is_available = is_available
        self.save()

    def set_quota(self, quota):
        self.total_quota = quota
        self.save()

    def set_address(self, address):
        self.address = address
        self.save()

    def set_coordinate(self, coordinate):
        self.latitude = coordinate[0]
        self.longitude = coordinate[1]
        self.save()

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number
        self.save()

    def can_accept_order(self):
        return self.amount_of_active_orders < self.total_quota

    def get_is_available(self):
        return self.is_available

    def accept_one_order(self):
        if not self.can_accept_order():
            raise OrderException(f'Laundry outlet {self.name} has reached its maximum workload')

        elif not self.get_is_available():
            raise OrderException(f'Laundry outlet {self.name} is currently not accepting order')

        else:
            self.amount_of_active_orders += 1
            self.save()

    def finish_one_order(self):
        if self.amount_of_active_orders > 0:
            self.amount_of_active_orders -= 1
            self.save()
        else:
            raise OrderException(f'Laundry outlet {self.name} has 0 orders')

    def recompute_outlet_rating(self, new_rating):
        previous_accumulative_rating = self.outlet_rating * self.amount_of_reviewed_orders
        self.outlet_rating = (previous_accumulative_rating + new_rating) / (self.amount_of_reviewed_orders + 1)
        self.amount_of_reviewed_orders += 1
        self.save()

    def __str__(self):
        return self.email


class LaundryOutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaundryOutlet
        fields = [
            'email',
            'name',
            'phone_number',
            'address',
            'total_quota',
            'amount_of_active_orders',
            'is_available',
            'outlet_rating',
        ]


class PredeterminedServiceCategory(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        auto_created=True,
        editable=False,
    )

    category_name = models.CharField(max_length=200, null=False)


class PredeterminedServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PredeterminedServiceCategory
        fields = '__all__'


class ItemCategoryProvided(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    item_price = models.FloatField()
    service_category_id = models.UUIDField()
    laundry_outlet_email = models.EmailField()

    def set_item_price(self, item_price):
        self.item_price = item_price
        self.save()


class ItemCategoryProvidedSerializer(serializers.ModelSerializer):
    service_category_name = serializers.SerializerMethodField('get_service_category_name')

    def get_service_category_name(self, item_category_provided: ItemCategoryProvided):
        return PredeterminedServiceCategory\
            .objects\
            .get(id=item_category_provided.service_category_id)\
            .category_name

    class Meta:
        model = ItemCategoryProvided
        fields = [
            'id',
            'item_price',
            'service_category_name'
        ]
