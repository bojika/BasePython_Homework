import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.models import User

from .models import *
from .forms import *
from .parsers import get_lsdb
import datetime


# Create your views here.


def index(request):
    return render(request, 'topology/home.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def topology_view(request):
    edges = [{"from": edge.begin.pk,
              "to": edge.end.pk,
              "label": edge.cost,
              "font": {"aligin": "middle"},
              "title": f'id: {edge.id}, meta: {edge.meta_data}'} for edge in Edge.objects.all()]

    nodes = [{"id": node.pk,
              "label": node.label,
              "title": node.meta_data} for node in Node.objects.all()]

    context = {'edges': edges, 'nodes': nodes}
    return render(request, 'topology/topology_view.html', context=context)


class UserLoginView(LoginView):
    template_name = "topology/login.html"
    form_class = AuthUserForm
    # это не работает
    # success_url = reverse_lazy('login')
    # работает код ниже или ещё можно в settings.py задать константу LOGIN_REDIRECT_URL

    def get_success_url(self):
        return reverse_lazy('home')


class UserCreateView(CreateView):
    form_class = RegisterUserForm
    template_name = "topology/register.html"
    success_url = reverse_lazy('login')
    success_msg = "Пользователь успешно создан"

    def form_valid(self, form):
        # сохранить пользователя в DB
        user = form.save()
        login(self.request, user)
        return redirect('home')

def import_topology(request):
    if request.method == 'POST':
        form = ImportTopologyForm(request.POST)
        if form.is_valid():

            # topology = form.cleaned_data['topology']
            edges_raw = get_lsdb(form.cleaned_data['raw_data'])
            x = list({edge[1] for edge in edges_raw} | {edge[2] for edge in edges_raw})
            nodes_raw = {node: Node(label=node, meta_data=node) for node in x}
            for node in nodes_raw:
                nodes_raw[node].save()
            topology = Topology(description=datetime.datetime.now())
            topology.save()
            edges = [Edge(topology=topology,
                          begin=nodes_raw[edge[1]],
                          end=nodes_raw[edge[2]],
                          cost=int(edge[3]),
                          meta_data=edge[4]) for edge in edges_raw]
            for i in edges:
                i.save()

    else:
        form = ImportTopologyForm()
    return render(request, 'topology/topology_import.html', {'form': form})


class EdgeDetailedView(DetailView):
    model = Edge


class EdgeCreateView(CreateView):
    model = Edge
    fields = ['begin', 'end', 'cost', 'meta_data', 'topology']


class EdgeUpdateView(UpdateView):
    model = Edge
    fields = ['begin', 'end', 'cost', 'meta_data', 'topology']


class EdgeDeleteView(DeleteView):
    model = Edge
    success_url = "/edge/list"


class EdgeListView(ListView):
    form = SelectTopologyForm()

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        topology = self.request.POST.get('topology')
        if topology:
            return Edge.objects.filter(topology__pk__exact=topology)
        return Edge.objects.all()

    extra_context = {'form': form}


class NodeCreateView(CreateView):
    model = Node
    fields = ['label', 'meta_data']


class NodeUpdateView(UpdateView):
    model = Node
    fields = ['label', 'meta_data']


class NodeDeleteView(DeleteView):
    model = Node
    success_url = "/node/list"


class NodeDetailedView(DetailView):
    model = Node


class NodeListView(ListView):
    model = Node


class TopologyCreateView(CreateView):
    model = Topology
    fields = ['description']


class TopologyUpdateView(UpdateView):
    model = Topology
    fields = ['description']


class TopologyDeleteView(DeleteView):
    model = Topology
    success_url = "/topology/list"


class TopologyDetailedView(DetailView):
    model = Topology


class TopologyListView(ListView):
    model = Topology

# class LoginUser(DataMixin, LoginView):
#     form_class = AuthenticationForm
#     template_name = "topology/login.html"
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Авторизация")
#         return dict(list(context.items()) + list(c_def.items()))
