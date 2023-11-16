from rest_framework import serializers
from .models import Reply
from django.contrib.auth.models import User

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(ReplySerializer, self).to_representation(instance)
        rep['repliedUser'] = instance.repliedUser.username
        rep['review']=instance.review.review
        return rep

