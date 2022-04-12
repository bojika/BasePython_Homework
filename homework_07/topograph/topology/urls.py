from django.urls import path, re_path
from .views import *

import topology.views as topology

urlpatterns = [
    path('', topology.index, name='home'),
    path('topology/import/', topology.import_topology, name='import_topology'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', topology.logout_user, name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('edge/create/', topology.EdgeCreateView.as_view(), name='edge_create'),
    path('edge/update/<int:pk>/', topology.EdgeUpdateView.as_view(), name='edge_update'),
    path('edge/delete/<int:pk>', topology.EdgeDeleteView.as_view(), name='edge_delete'),
    path('edge/detail/<int:pk>', topology.EdgeDetailedView.as_view(), name='edge_detail'),
    path('edge/list/', topology.EdgeListView.as_view(), name='edge_list'),
    path('node/create/', topology.NodeCreateView.as_view(), name='node_create'),
    path('node/update/<int:pk>/', topology.NodeUpdateView.as_view(), name='node_update'),
    path('node/delete/<int:pk>', topology.NodeDeleteView.as_view(), name='node_delete'),
    path('node/detail/<int:pk>/', topology.NodeDetailedView.as_view(), name='node_detail'),
    path('node/list/', topology.NodeListView.as_view(), name='node_list'),
    path('topology/create/', topology.TopologyCreateView.as_view(), name='topology_create'),
    path('topology/update/<int:pk>/', topology.TopologyUpdateView.as_view(), name='topology_update'),
    path('topology/delete/<int:pk>/', topology.TopologyDeleteView.as_view(), name='topology_delete'),
    path('topology/detail/<int:pk>/', topology.TopologyDetailedView.as_view(), name='topology_detail'),
    path('topology/list/', topology.TopologyListView.as_view(), name='topology_list'),
    path('topology/view/', topology.topology_view, name='topology_view'),
]