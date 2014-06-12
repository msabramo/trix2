from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatechars
from django_cradmin.viewhelpers import objecttable
from django_cradmin.viewhelpers import create
from django_cradmin.viewhelpers import update
from django_cradmin.viewhelpers import delete
from django_cradmin import crapp
from crispy_forms import layout


from trix.trix_core.models import Assignment



class TitleColumn(objecttable.MultiActionColumn):
    modelfield = 'title'

    def get_buttons(self, assignment):
        return [
            objecttable.Button(
                label='Edit',
                url=self.reverse_appurl('edit', args=[assignment.id])),
            objecttable.Button(
                label='Delete',
                url=self.reverse_appurl('delete', args=[assignment.id]),
                buttonclass="danger"),
        ]


class TextIntroColumn(objecttable.PlainTextColumn):
    modelfield = 'text'

    def render_value(self, assignment):
        return truncatechars(assignment.text, 50)


class TagsColumn(objecttable.PlainTextColumn):
    modelfield = 'tags'

    def render_value(self, assignment):
        return ', '.join(tag.tag for tag in assignment.tags.all())



class ProductListView(objecttable.ObjectTableView):
    model = Assignment
    columns = [
        TitleColumn,
        TagsColumn,
        TextIntroColumn
    ]

    def get_queryset_for_role(self, course):
        return self.model.objects.filter(tags=course.course_tag)\
            .prefetch_related('tags')

    def get_buttons(self):
        app = self.request.cradmin_app
        return [
            objecttable.Button(_('Create'), url=app.reverse_appurl('create')),
        ]


class ProductCreateUpdateMixin(object):
    model = Assignment

    # def get_preview_url(self):
    #     return reverse('lokalt_company_product_preview')

    def get_field_layout(self):
        return [
            layout.Div('title', css_class="cradmin-focusfield cradmin-focusfield-lg"),
            layout.Fieldset(_('Organize'),
                'tags'
            ),
            layout.Div('text', css_class="cradmin-focusfield"),
            layout.Div('solution', css_class="cradmin-focusfield"),

        ]

    def get_form(self, *args, **kwargs):
        return super(ProductCreateUpdateMixin, self).get_form(*args, **kwargs)


class ProductCreateView(ProductCreateUpdateMixin, create.CreateView):
    """
    View used to create new products.
    """


class ProductUpdateView(ProductCreateUpdateMixin, update.UpdateView):
    """
    View used to create edit existing products.
    """

class ProductDeleteView(delete.DeleteView):
    """
    View used to delete existing products.
    """
    model = Assignment



class App(crapp.App):
    appurls = [
        crapp.Url(r'^$',
            ProductListView.as_view(),
            name=crapp.INDEXVIEW_NAME),
        crapp.Url(r'^create$',
            ProductCreateView.as_view(),
            name="create"),
        crapp.Url(r'^edit/(?P<pk>\d+)$',
            ProductUpdateView.as_view(),
            name="edit"),
        crapp.Url(r'^delete/(?P<pk>\d+)$',
            ProductDeleteView.as_view(),
            name="delete")
    ]
