from rest_framework import serializers

from .models import Event, VoteEvent, EventComment

class VoteEventSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    event = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = VoteEvent
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    votes=VoteEventSerializer(many=True,read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'user', 'content', 'event_image', 'created_at', 'updated_at','category', 'votes']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventComment
        fields = "__all__"


    comment = serializers.CharField(max_length=300)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    event = serializers.PrimaryKeyRelatedField(read_only=True)

    def save(self, **kwargs):
        print(kwargs)
        self.event = kwargs["event"]
        return super().save(**kwargs)