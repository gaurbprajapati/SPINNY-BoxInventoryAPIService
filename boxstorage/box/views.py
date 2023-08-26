from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.utils.decorators import method_decorator
from .permissions import IsStaff
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Box
from .serializers import BoxSerializer
from .permissions import IsCreatorOrReadOnly, IsStaff
from django.utils import timezone
from datetime import timedelta
from rest_framework import status

A1 = 100
V1 = 1000
L1 = 100
L2 = 50


# Task - 4

class BoxListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]

    def get(self, request):
        boxes = Box.objects.all()
        serializer = BoxSerializer(boxes, many=True)
        return JsonResponse(serializer.data, safe=False)

    def get_boxes_added_this_week(self):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return Box.objects.filter(creation_date__range=[start_of_week, end_of_week])

    def get_user_boxes_added_this_week(self, user):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return Box.objects.filter(creator=user, creation_date__range=[start_of_week, end_of_week])

    def calculate_average_area(self, boxes):
        total_area = sum(box.length * box.breadth for box in boxes)
        return total_area / len(boxes)

    def calculate_average_volume(self, boxes):
        total_volume = sum(box.length * box.breadth *
                           box.height for box in boxes)
        return total_volume / len(boxes)

    def post(self, request):
        try:
            serializer = BoxSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(creator=request.user)

                boxes = Box.objects.all()
                average_area = self.calculate_average_area(boxes)
                if average_area > A1:
                    return JsonResponse({"error": "Average area exceeds limit"}, status=400)

                user_boxes = Box.objects.filter(creator=request.user)
                average_volume = self.calculate_average_volume(user_boxes)
                if average_volume > V1:
                    return JsonResponse({"error": "Average volume exceeds limit"}, status=400)

                total_boxes_added_this_week = self.get_boxes_added_this_week().count()
                if total_boxes_added_this_week >= L1:
                    return JsonResponse({"error": "Total boxes added this week exceeds limit"}, status=400)

                user_boxes_added_this_week = self.get_user_boxes_added_this_week(
                    request.user).count()
                if user_boxes_added_this_week >= L2:
                    return JsonResponse({"error": "Total boxes added by you this week exceeds limit"}, status=400)

                return JsonResponse(serializer.data, status=201)

            return JsonResponse(serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# Task 2
class BoxRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsStaff]

    def get_box(self, pk):
        try:
            return Box.objects.get(pk=pk)
        except Box.DoesNotExist:
            return None

    def get(self, request, pk):
        try:
            box = self.get_box(pk)
            if box:
                serializer = BoxSerializer(box)
                return Response(serializer.data)
            return Response({"error": "Box not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            box = self.get_box(pk)
            if box:
                original_creator = box.creator
                original_creation_date = box.creation_date
                original_last_updated = box.last_updated

                serializer = BoxSerializer(box, data=request.data)
                if serializer.is_valid():
                    serializer.save(creator=original_creator, creation_date=original_creation_date,
                                    last_updated=timezone.now())

                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Box not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# TASK 4 ---
class MyBoxListView(APIView):
    def get(self, request, *args, **kwargs):
        permission_classes = [IsAuthenticated, IsStaff]
        try:
            queryset = Box.objects.filter(creator=request.user)

            # Apply filters based on query parameters
            length_more_than = request.query_params.get('length_more_than')
            length_less_than = request.query_params.get('length_less_than')
            breadth_more_than = request.query_params.get('breadth_more_than')
            breadth_less_than = request.query_params.get('breadth_less_than')
            height_more_than = request.query_params.get('height_more_than')
            height_less_than = request.query_params.get('height_less_than')
            area_more_than = request.query_params.get('area_more_than')
            area_less_than = request.query_params.get('area_less_than')
            volume_more_than = request.query_params.get('volume_more_than')
            volume_less_than = request.query_params.get('volume_less_than')
            created_before = request.query_params.get('created_before')
            created_after = request.query_params.get('created_after')

            if length_more_than:
                queryset = queryset.filter(length__gt=length_more_than)
            if length_less_than:
                queryset = queryset.filter(length__lt=length_less_than)
            if breadth_more_than:
                queryset = queryset.filter(breadth__gt=breadth_more_than)
            if breadth_less_than:
                queryset = queryset.filter(breadth__lt=breadth_less_than)
            if height_more_than:
                queryset = queryset.filter(height__gt=height_more_than)
            if height_less_than:
                queryset = queryset.filter(height__lt=height_less_than)
            if area_more_than:
                queryset = queryset.filter(area__gt=area_more_than)
            if area_less_than:
                queryset = queryset.filter(area__lt=area_less_than)
            if volume_more_than:
                queryset = queryset.filter(volume__gt=volume_more_than)
            if volume_less_than:
                queryset = queryset.filter(volume__lt=volume_less_than)
            if created_before:
                queryset = queryset.filter(creation_date__lt=created_before)
            if created_after:
                queryset = queryset.filter(creation_date__gt=created_after)

            serializer = BoxSerializer(queryset, many=True)

            serialized_data = []
            for data in serializer.data:
                data['created_by'] = data['creator']
                data['area'] = data['length'] * data['breadth']
                data['volume'] = data['length'] * \
                    data['breadth'] * data['height']
                serialized_data.append(data)
            return Response(serialized_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Task - 3


class FilteredBoxListView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60))  # Cache the response for 60 seconds
    def get(self, request, *args, **kwargs):
        try:
            queryset = Box.objects.all()
            # Apply filters based on query parameters
            length_more_than = request.query_params.get('length_more_than')
            length_less_than = request.query_params.get('length_less_than')
            breadth_more_than = request.query_params.get('breadth_more_than')
            breadth_less_than = request.query_params.get('breadth_less_than')
            height_more_than = request.query_params.get('height_more_than')
            height_less_than = request.query_params.get('height_less_than')
            area_more_than = request.query_params.get('area_more_than')
            area_less_than = request.query_params.get('area_less_than')
            volume_more_than = request.query_params.get('volume_more_than')
            volume_less_than = request.query_params.get('volume_less_than')
            created_by_username = request.query_params.get(
                'created_by_username')
            created_before = request.query_params.get('created_before')
            created_after = request.query_params.get('created_after')

            if length_more_than:
                queryset = queryset.filter(length__gt=length_more_than)
            if length_less_than:
                queryset = queryset.filter(length__lt=length_less_than)
            if breadth_more_than:
                queryset = queryset.filter(breadth__gt=breadth_more_than)
            if breadth_less_than:
                queryset = queryset.filter(breadth__lt=breadth_less_than)
            if height_more_than:
                queryset = queryset.filter(height__gt=height_more_than)
            if height_less_than:
                queryset = queryset.filter(height__lt=height_less_than)
            if area_more_than:
                queryset = queryset.filter(area__gt=area_more_than)
            if area_less_than:
                queryset = queryset.filter(area__lt=area_less_than)
            if volume_more_than:
                queryset = queryset.filter(volume__gt=volume_more_than)
            if volume_less_than:
                queryset = queryset.filter(volume__lt=volume_less_than)
            if created_by_username:
                queryset = queryset.filter(
                    creator__username=created_by_username)
            if created_before:
                queryset = queryset.filter(creation_date__lt=created_before)
            if created_after:
                queryset = queryset.filter(creation_date__gt=created_after)

            serializer = BoxSerializer(queryset, many=True)

            # If user is staff, include 'created_by' and 'last_updated' fields
            # print(request.user.is_staff)
            if request.user.is_staff:
                serialized_data = []
                for data in serializer.data:
                    data['created_by'] = data['creator']
                    data['last_updated'] = Box.objects.get(
                        id=data['id']).last_updated
                    data['area'] = data['length'] * data['breadth']
                    data['volume'] = data['length'] * \
                        data['breadth'] * data['height']
                    serialized_data.append(data)
                return Response(serialized_data)

            # If user is not staff, remove 'created_by' and 'last_updated' fields
            non_staff_serialized_data = []
            for data in serializer.data:
                data.pop('creator', None)
                data.pop('last_updated', None)
                data['area'] = data['length'] * data['breadth']
                data['volume'] = data['length'] * \
                    data['breadth'] * data['height']
                non_staff_serialized_data.append(data)
            return Response(non_staff_serialized_data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Task -5

class BoxDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_box(self, pk):
        try:
            return Box.objects.get(pk=pk)
        except Box.DoesNotExist:
            return None

    def delete(self, request, pk):
        try:
            box = self.get_box(pk)
            if box:
                if box.creator == request.user:
                    box.delete()
                    return Response({"Message": "Box is Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"error": "You are not authorized to delete this box."}, status=status.HTTP_403_FORBIDDEN)
            return Response({"error": "Box not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
