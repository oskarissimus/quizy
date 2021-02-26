from rest_framework import serializers

class RankingSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
#            'place': instance.place,
            'username': instance.username,
            'points': instance.points,
        }