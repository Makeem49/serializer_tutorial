from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics

'''class base APIView '''

class SnippetView(APIView):
    """List snippet or create a new snippet"""
    
    def get(self, request, format=None):
        """List snippets"""

        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """Create a new snippets"""

        data = request.data
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):

    def get_details(self, pk):
        """Get the snippet from db"""
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            return Http404

    def get(self, request, pk , format=None):
        """Get method """
        snippet = self.get_details(pk)
        serializer = SnippetSerializer(snippet) 
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        """update item"""
        snippet = self.get_details(pk)
        data = request.data 
        serializer = SnippetSerializer(snippet, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, format=None):
        """delete item"""
        snippet = self.get_details(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''Using mixins'''

class SnippetViewMixins(
                    mixins.ListModelMixin, 
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):

    """Mixins class sample for create and list view"""

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *arsg, **kwargs):
        """List of snippet"""
        return self.list(request, *arsg, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create a snippet"""
        return self.create(request, *args, **kwargs)


class SnippetDetailMixins(
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):

    """Mixins class sample fo retrieve, update and delete"""

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        """Retrieve a particular item"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Update snippet"""
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        """Delete snippet"""
        return self.destroy(request, *args, **kwargs)
    

'''Generic view'''

class SnippetListGeneric(generics.ListCreateAPIView):
    """Create or list API using generic view"""

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

class SnippetDetailGeneric(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete API using generic view"""

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


'''Function base view'''

@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)