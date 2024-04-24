from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Service


class ServiceView(TemplateView):
    template_name = 'services/check.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_service = Service.objects.order_by('-created_at').first()
        print(latest_service)
        context['latest_service'] = latest_service
        return context


def options_view(request):
    if request.method == 'POST':
        service_type = request.POST.get('serviceType')
        if service_type:
            latest_service = Service.objects.filter(type=service_type).order_by('-created_at').first()
            if latest_service:
                latest_service.number += 1
                latest_service.save()
            else:
                latest_service = Service.objects.create(type=service_type, number=1)
        return redirect('service:service')

    return render(request, 'services/options.html')
