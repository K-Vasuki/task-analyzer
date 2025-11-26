from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .scoring import analyze_tasks, suggest_top_3
from rest_framework import generics
from .models import Task
from .serializers import TaskModelSerializer
@api_view(['POST'])
def analyze_tasks_view(request):
    data = request.data
    if not isinstance(data, list):
        return Response({"error": "Tasks must be sent as JSON array"}, status=400)

    mode = request.query_params.get("mode", "smart")

    results = analyze_tasks(data, mode)
    return Response(results, status=200)

@api_view(['POST'])
def suggest_tasks_view(request):
    data = request.data
    mode = request.query_params.get("mode", "smart")

    top = suggest_top_3(data, mode)
    return Response(top, status=200)


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer

class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
