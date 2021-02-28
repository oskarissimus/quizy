from rest_framework import serializers

class RankingSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'username': instance['user__username'],
            'points': instance['points'],
        }