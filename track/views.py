from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Tracker
from .serializers import TrackerSerializer
from .blockchain import Blockchain
               

# Initialize blockchain
blockchain = Blockchain()


# ---------------------------------------------------
# STAGE ORDER CONTROL
# ---------------------------------------------------
STAGE_ORDER = ["Farm", "Sorting", "Dispatch", "Market"]


def is_valid_stage_transition(batch_id, new_stage):
    previous = Tracker.objects.filter(batch_id=batch_id).order_by("-created_at").first()
    if not previous:
        return True  # first stage is allowed

    try:
        prev_index = STAGE_ORDER.index(previous.stage)
        new_index = STAGE_ORDER.index(new_stage)
        return new_index == prev_index + 1  # must move forward one step
    except ValueError:
        return False


# ---------------------------------------------------
# MAIN VIEWSET
# ---------------------------------------------------
class TrackerViewSet(viewsets.ModelViewSet):
    queryset = Tracker.objects.all()
    serializer_class = TrackerSerializer

    # 🔐 CREATE TRACK RECORD
    def create(self, request, *args, **kwargs):
        data = request.data
        batch_id = data.get("batch_id")
        stage = data.get("stage")

        # 🚫 Stage order protection
        if not is_valid_stage_transition(batch_id, stage):
            return Response(
                {"error": "Invalid stage transition"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ⛓️ Generate blockchain hash
        block_hash = blockchain.add_block(data)

        data["block_hash"] = block_hash
        serializer = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ---------------------------------------------------
    # ✅ VERIFY STAGE ENDPOINT
    # POST /api/track/verify/
    # ---------------------------------------------------
    @action(detail=False, methods=["post"])
    def verify(self, request):
        batch_id = request.data.get("batch_id")
        verifier = request.data.get("verified_by")

        record = Tracker.objects.filter(batch_id=batch_id).order_by("-created_at").first()

        if not record:
            return Response({"error": "Batch not found"}, status=404)

        record.verified = True
        record.verified_by = verifier
        record.verified_at = timezone.now()
        record.save()

        return Response({"message": "Stage verified successfully"})
      