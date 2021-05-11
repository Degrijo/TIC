from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


class EmployeeMixin(AccessMixin):
    login_url = reverse_lazy('login')
    permission_denied_message = 'Expected employee account'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != get_user_model().EMPLOYEE_ROLE:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ClientMixin(AccessMixin):
    login_url = reverse_lazy('login')
    permission_denied_message = 'Expected client account'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != get_user_model().CLIENT_ROLE:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ParticipantMixin(AccessMixin):
    login_url = reverse_lazy('login')
    permission_denied_message = 'Order details available only for participants'

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, id=kwargs['pk'])
        if not request.user.is_authenticated or (request.user != self.object.sender
                                                 and request.user != self.object.recipient
                                                 and request.user != self.object.employee):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ContextMixin:
    def get_context_data(self, **kwargs):
        kwargs['user_model'] = get_user_model()
        return super().get_context_data(**kwargs)
