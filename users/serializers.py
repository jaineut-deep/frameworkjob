from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from syllabus.services import get_prod_id, get_price_id, get_session
from users.models import Payment, CustomUser


@extend_schema_serializer(
    examples = [
         OpenApiExample(
            'Valid example 1',
            summary='short summary',
            description='longer description',
            value={
                "course": 3
            },
        ),
    ]
)
class PaymentSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(max_length=100, required=False)
    price_id = serializers.CharField(max_length=100, required=False)
    session_id = serializers.CharField(max_length=100, required=False)

    def create(self, validated_data):
        request = self.context.get("request")
        course = validated_data.pop("course")
        product_id = self.receive_prod_id(course)
        price_id = self.receive_price_id(product_id, course.price)
        session = self.receive_session(price_id)
        validated_data["user"] = request.user
        validated_data["total_amount"] = course.price
        validated_data["product_id"] = product_id
        validated_data["price_id"] = price_id
        validated_data["session_id"] = session.get("id")
        validated_data["payment_status"] = session.get("payment_status")
        validated_data["payment_url"] = session.get("url")
        validated_data["course"] = course
        validated_data.pop("product_id", None)
        validated_data.pop("price_id", None)
        validated_data.pop("session_id", None)
        return super().create(validated_data)

    def receive_prod_id(self, course):
        return get_prod_id(course.title, course.description)

    def receive_price_id(self, prod_id, amount):
        return get_price_id(prod_id, amount)

    def receive_session(self, price_id):
        return get_session(price_id)

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["product_id", "price_id", "session_id", "payment_status", "payment_url", "total_amount",
                            "user"]


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]
