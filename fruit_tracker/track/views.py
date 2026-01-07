from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .blockchain import Blockchain
from .models import Tracker
from .serializers import TrackerSerializer

blockchain = Blockchain()

@api_view(["POST"])
def add_tracker_event(request):
    serializer = TrackerSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data

        block_data = {
            "batch_id": data["batch_id"],   
            "fruit_type": data["fruit_type"],
            "quantity_kg": data["quantity_kg"],
            "stage": data["stage"],
            "location": data["location"],
            "handled_by": data["handled_by"],
        }   
    
        block = blockchain.add_block(block_data)

        tracker = Tracker.objects.create(
            **data,
            block_hash=block.hash
        )

        return Response(
            TrackerSerializer(tracker).data,
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
@api_view(["GET"])
def get_batch_history(request, batch_id):
    records = Tracker.objects.filter(batch_id=batch_id)

    if not records.exists():
        return Response(
            {"error": "Batch not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TrackerSerializer(records, many=True)
    return Response({
        "batch_id": batch_id,
        "history": serializer.data
    })


@api_view(["GET"])
def list_all_tracking(request):
    records = Tracker.objects.all()
    serializer = TrackerSerializer(records, many=True)
    return Response(serializer.data)

