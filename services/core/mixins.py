class ActionSerializersViewSetMixin:
    ACTION_SERIALIZERS = {}
    
    def get_serializer_class(self):
        return self.ACTION_SERIALIZERS.get(self.action, self.serializer_class)
    