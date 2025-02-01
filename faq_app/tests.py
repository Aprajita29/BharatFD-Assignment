import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import FAQ

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_faq():
    return FAQ.objects.create(
        question="What is Django?",
        answer="Django is a high-level Python web framework."
    )

@pytest.mark.django_db
def test_faq_list(api_client, sample_faq):
    url = reverse('faq-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['question'] == sample_faq.question

@pytest.mark.django_db
def test_faq_detail(api_client, sample_faq):
    url = reverse('faq-detail', kwargs={'pk': sample_faq.pk})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['question'] == sample_faq.question

@pytest.mark.django_db
def test_faq_list_with_language(api_client, sample_faq):
    url = reverse('faq-list') + '?lang=hi'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['question'] == sample_faq.question_hi

@pytest.mark.django_db
def test_faq_model_translation(sample_faq):
    assert sample_faq.question_hi != ""
    assert sample_faq.question_bn != ""
    assert sample_faq.answer_hi != ""
    assert sample_faq.answer_bn != ""

