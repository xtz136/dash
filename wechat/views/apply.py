from django.views.generic.edit import CreateView
from django.urls import reverse
from django.shortcuts import render, redirect
from core.models import Apply


class ApplyCreateView(CreateView):
    model = Apply
    fields = ['name', 'title', 'info', 'phone']
    template_name = 'wechat/apply.html'

    def get(self, request, **kwargs):
        try:
            obj = Apply.objects.get(user=request.user)
        except Apply.DoesNotExist:
            return super(ApplyCreateView, self).get(request, **kwargs)

        if obj.state == 'new':
            return redirect(self.get_success_url() + "?message=申请认证成功。")
        elif obj.state == 'denied':
            return redirect(self.get_success_url() + "?message=认证失败，请联系客服处理。")
        elif obj.state == 'approved':
            return redirect(reverse('wechat:index'))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ApplyCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('wechat:apply-success')


def apply_success_view(request):
    return render(request, 'wechat/apply_success.html', {
        'message': request.GET.get('message', '申请认证成功，我们会尽快处理你的申请。')
    })
