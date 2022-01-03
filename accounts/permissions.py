from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsEvaluator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_evaluator


class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_candidate
