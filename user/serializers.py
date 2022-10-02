from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User



class RegisterSerializer(serializers.ModelSerializer):
   
    username = serializers.CharField(
            max_length=30,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    first_name = serializers.CharField(
            max_length=30,
            
            )
    last_name = serializers.CharField()
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    
    def create(self, validated_data):
        user = User.objects.create(
        username=validated_data['username'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        email=validated_data['email'],
    
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('pk', 'username', 'password','first_name','last_name','email')
