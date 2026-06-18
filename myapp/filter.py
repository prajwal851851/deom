from .models import blog
import django_filters

class blogFilter(django_filters.FilterSet):
    author=django_filters.CharFilter(lookup_expr='icontains')
    title=django_filters.CharFilter(lookup_expr='icontains')
    creted_at=django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = blog
        fields = ['author','title','creted_at']
        