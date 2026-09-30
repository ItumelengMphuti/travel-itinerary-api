from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Allows anyone to read an object, but only the owner can modify it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class IsItineraryOwner(BasePermission):
    """
    Allows access only to the owner of an itinerary.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsItineraryParticipant(BasePermission):
    """
    Allows access to users who participate in an itinerary.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "itinerary"):
            itinerary = obj.itinerary
        else:
            itinerary = obj

        return (
            itinerary.user == request.user
            or itinerary.participants.filter(user=request.user).exists()
        )


class IsOwnerOrParticipant(BasePermission):
    """
    Allows access to the itinerary owner or its participants.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "itinerary"):
            itinerary = obj.itinerary
        else:
            itinerary = obj

        if itinerary.user == request.user:
            return True

        return itinerary.participants.filter(user=request.user).exists()
