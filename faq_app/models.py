from djongo import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from googletrans import Translator

class FAQ(models.Model):
    question = models.TextField(_("Question"))
    answer = RichTextField(_("Answer"))
    question_hi = models.TextField(_("Question (Hindi)"), blank=True)
    question_bn = models.TextField(_("Question (Bengali)"), blank=True)
    answer_hi = RichTextField(_("Answer (Hindi)"), blank=True)
    answer_bn = RichTextField(_("Answer (Bengali)"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        if not self.pk:  # Only translate on creation
            translator = Translator()
            self.question_hi = translator.translate(self.question, dest='hi').text
            self.question_bn = translator.translate(self.question, dest='bn').text
            self.answer_hi = translator.translate(self.answer, dest='hi').text
            self.answer_bn = translator.translate(self.answer, dest='bn').text
        super().save(*args, **kwargs)

    def get_translated_text(self, field, lang):
        if lang == 'en':
            return getattr(self, field)
        elif lang in ['hi', 'bn']:
            return getattr(self, f"{field}_{lang}") or getattr(self, field)
        else:
            return getattr(self, field)

    class Meta:
        db_table = 'faq'

