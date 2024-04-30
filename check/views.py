
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils import timezone
from .models import Service


class ServiceView(TemplateView):
    template_name = 'services/check.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_service = Service.objects.order_by('-created_at').first()
        services = Service.objects.all().order_by('-created_at')

        context['latest_service'] = latest_service
        context['services'] = services
        return context


def options_view(request):
    if request.method == 'POST':
        service_type = request.POST.get('serviceType')
        service_num = request.POST.get('serviceNum')

        if service_type and service_num:
            latest_service = Service.objects.filter(type=service_type).first()
            if latest_service:
                latest_service.created_at = timezone.now()
                latest_service.number += 1
                latest_service.windows = int(service_num)

                latest_service.save()
            else:
                latest_service = Service.objects.create(type=service_type, number=1, windows=service_num)

        return redirect('service:service')
    return render(request, 'services/options.html')