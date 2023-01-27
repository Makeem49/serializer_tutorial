from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.Serializer):
    """Definning each field explicitly"""
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

class SnippetSerializer(serializers.ModelSerializer):
    """Define the field to use the same field as the Model snippet"""
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']

"""
# Explanation of converting from python datatype to json

## From python data type to json 

from rest_framework.renderers import JSONRenderer

1. create a model instance and save

snippet = Snippet(code='foo = "bar"\n')
snippet.save()

2. pass the instance into a serializer 

serializer = SnippetSerializer(snippet)

3. pass the serializer instance into JSONRenderer().renderer(serializer data into here) method 

content = JSONRenderer().render(serializer.data)

The content variable now hold a json data that can be send to user

"""

"""

# Explanation of converting from json to python data type

from rest_framework.parsers import JSONParser

1. We convert the json data into stream using python io module 

content = b'{"name" : "john"}' ---> json data 

import io 

stream = io.io.BytesIO(content)

2. convert the stream into data using the JSONParser().parse(pass stream data here)

data = JSONParser().parse(stream)

data is now a valid python datatype {"name" : "john"}

3. Convert the data to an instance of Serializers class 

serializer = SnippetSerializer(data=data)

4. Check if the data is valid with the serializer class 

serializer.is_valid() # Either True or False 

5. Get the validated data from the instance of the SnippetSerializer class 

serializer.validated_data

5. Save the instance to db 

serializer.save()



"""