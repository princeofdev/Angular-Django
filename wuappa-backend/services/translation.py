from modeltranslation.translator import register, TranslationOptions

from services.models import Category, Service


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'preparation')
