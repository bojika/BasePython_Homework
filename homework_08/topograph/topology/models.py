from django.db import models
from django.urls import reverse_lazy


# Create your models here.


class Topology(models.Model):
    description = models.CharField(max_length=255, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    # owner = models.ForeignKey(User, related_name='begin', on_delete=models.CASCADE, null=False),
    # group = models.ManyToManyField('User')

    def get_absolute_url(self):
        return reverse_lazy('topology_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.description}'


class Node(models.Model):
    label = models.CharField(max_length=255)
    meta_data = models.JSONField(null=False, default=dict)
    # owner = models.ForeignKey(User, related_name='begin', on_delete=models.CASCADE, null=False),

    def get_absolute_url(self):
        return reverse_lazy('node_detail', kwargs={'pk': self.pk})

    #        return f"<{self.__class__.__name__} {self.label!r} {self.meta_data!r}>"
    def __str__(self):
        return f"<{self.__class__.__name__} {self.label!r} {self.meta_data!r}>"
            # f'{self.label}'


class Edge(models.Model):
    topology = models.ForeignKey(Topology, on_delete=models.CASCADE, null=False)
    begin = models.ForeignKey(Node, related_name='begin', on_delete=models.CASCADE, null=False)
    end = models.ForeignKey(Node, related_name='end', on_delete=models.CASCADE, null=False)
    cost = models.IntegerField(default=0)
    meta_data = models.JSONField(null=False, default=dict)

    def get_absolute_url(self):
        return reverse_lazy('edge_detail', kwargs={'pk': self.pk})

    def __str__(self):
       return f"{self.__class__.__name__}: <<topology: {self.topology!r}, begin: {self.begin!r}, end: {self.end!r}, cost: {self.cost!r}, meta: {self.meta_data!r}>>"




