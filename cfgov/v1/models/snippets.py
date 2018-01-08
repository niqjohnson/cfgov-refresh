from django.core.validators import URLValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, StreamFieldPanel, PageChooserPanel)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from v1 import blocks as v1_blocks
from v1.atomic_elements import molecules

# We import ReusableTextChooserBlock here because this is where it used to
# live. That caused circular imports when it was imported into models. It's no
# longer imported into models from this file, but there are migrations which
# still look for it here.
from v1.blocks import ReusableTextChooserBlock  # noqa


@python_2_unicode_compatible
@register_snippet
class ReusableText(index.Indexed, models.Model):
    title = models.CharField(
        verbose_name='Snippet title (internal only)',
        max_length=255
    )
    sidefoot_heading = models.CharField(
        blank=True,
        max_length=255,
        help_text='Applies "slug" style heading. '
                  'Only for use in sidebars and prefooters '
                  '(the "sidefoot"). See '
                  '[GHE]/flapjack/Modules-V1/wiki/Atoms#slugs'
    )
    text = RichTextField()

    search_fields = [
        index.SearchField('title', partial_match=True),
        index.SearchField('sidefoot_heading', partial_match=True),
        index.SearchField('text', partial_match=True),
    ]

    def __str__(self):
        return self.title


@python_2_unicode_compatible
@register_snippet
class Contact(models.Model):
    heading = models.CharField(verbose_name=('Heading'), max_length=255,
                               help_text=("The snippet heading"))
    body = RichTextField(blank=True)

    contact_info = StreamField([
        ('email', molecules.ContactEmail()),
        ('phone', molecules.ContactPhone()),
        ('address', molecules.ContactAddress()),
    ], blank=True)

    panels = [
        FieldPanel('heading'),
        FieldPanel('body'),
        StreamFieldPanel('contact_info'),
    ]

    def __str__(self):
        return self.heading


class ResourceTag(TaggedItemBase):
    content_object = ParentalKey('v1.Resource', related_name='tagged_items')


class TaggableSnippetManager(models.Manager):
    def filter_by_tags(self, tags):
        snippets = self.all()
        for tag in tags or []:
            snippets = snippets.filter(tags__name=tag)

        return snippets


@python_2_unicode_compatible
@register_snippet
class Resource(ClusterableModel):
    title = models.CharField(max_length=255)
    desc = RichTextField(verbose_name='Description', blank=True)

    thumbnail = models.ForeignKey(
        'v1.CFGOVImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    related_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    alternate_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    link = models.URLField(
        blank=True,
        help_text='Example: URL to order a few copies of a printed piece.',
        validators=[URLValidator]
    )

    alternate_link = models.URLField(
        blank=True,
        help_text='Example: a URL to for ordering bulk copies.',
        validators=[URLValidator]
    )

    order = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Snippets will be listed alphabetically by title in a '
        'Snippet List module, unless any in the list have a number in this '
        'field; those with an order value will appear at the bottom of the '
        'list, in ascending order.'
    )

    tags = TaggableManager(
        through=ResourceTag,
        blank=True,
        help_text='Tags can be used to filter snippets in a Snippet List.'
    )

    objects = TaggableSnippetManager()

    panels = [
        FieldPanel('title'),
        FieldPanel('desc'),
        ImageChooserPanel('thumbnail'),
        DocumentChooserPanel('related_file'),
        DocumentChooserPanel('alternate_file'),
        FieldPanel('link'),
        FieldPanel('alternate_link'),
        FieldPanel('order'),
        FieldPanel('tags'),
    ]

    # Makes fields available to the Actions chooser in a Snippet List module
    snippet_list_field_choices = [
        ('related_file', 'Related file'),
        ('alternate_file', 'Alternate file'),
        ('link', 'Link'),
        ('alternate_link', 'Alternate link'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('order', 'title')


@python_2_unicode_compatible
@register_snippet
class MenuItem(models.Model):
    link_text = models.CharField(
        max_length=255,
        help_text="Display text for menu link")

    external_link = models.CharField(
        null=True,
        blank=True,
        max_length=1000,
        help_text="Enter url for page outside Wagtail.",
        default="#")

    page_link = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        help_text='Link to a page in Wagtail.'
    )

    order = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Determines order in which this menu item appears in nav.'
    )

    column_1 = StreamField([
        ('nav_group', v1_blocks.NavGroup(
            label="Nav items group"),)
    ], blank=True)

    column_2 = StreamField([
        ('nav_group', v1_blocks.NavGroup(
            label="Nav items group"))
    ], blank=True)

    column_3 = StreamField([
        ('nav_group', v1_blocks.NavGroup(
            label="Nav items group"))
    ], blank=True)

    column_4 = StreamField([
        ('nav_group', v1_blocks.NavGroup(
            label="Nav items group")),
        ('featured_content', v1_blocks.FeaturedMenuContent(
            label="Featured content module"))
    ], blank=True)

    footer = StreamField([
        ('footer', blocks.StructBlock([
            ('draft', blocks.BooleanBlock(required=False)),
            ('content', blocks.RichTextBlock(required=False))
        ]))
    ], blank=True)

    panels = [
         MultiFieldPanel([
            FieldPanel('link_text'),
            PageChooserPanel('page_link'),
            FieldPanel('external_link'),
        ], heading='Link'),
        FieldPanel('order'),
        StreamFieldPanel('column_1'),
        StreamFieldPanel('column_2'),
        StreamFieldPanel('column_3'),
        StreamFieldPanel('column_4'),
        StreamFieldPanel('footer'),
    ]

    def __str__(self):
        return self.link_text

    def get_content(self, draft):
        """
        Filter menu item column content by by draft/live state
        and structure it for display in menu template.
        """
        cols = [getattr(self, 'column_' + str(i)) for i in range(1, 5)]
        self.nav_groups = filter(None, [self.get_active_block(col, draft)
                                        for col in cols])
        self.featured_content = self.nav_groups.pop() if len(self.nav_groups) \
            and self.nav_groups[-1].block_type == "featured_content" else None
        self.footer = self.get_active_block(self.nav_footer, draft)
        return self

    @staticmethod
    def get_active_block(blocks, draft):
        """
        Returns first block whose state matches draft
        parameter. If draft parameter is true, will
        return last live block if there are no draft blocks.
        """
        return next((block for i, block in enumerate(blocks) if
                    block.value.get('draft', '') == draft or
                    (draft and i == len(blocks) - 1)), None)
