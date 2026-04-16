from django.urls import path
from . import views

urlpatterns = [
    # Home and navigation
    path('', views.home, name='home'),
    
    # Design management
    path('designs/create/', views.create_design, name='create_design'),
    path('designs/', views.design_list, name='design_list'),
    path('designs/<int:pk>/', views.design_detail, name='design_detail'),
    path('designs/<int:pk>/edit/', views.edit_design, name='edit_design'),
    path('designs/<int:pk>/delete/', views.delete_design, name='delete_design'),
    
    # Preview and visualization
    path('designs/<int:pk>/preview-2d/', views.preview_2d, name='preview_2d'),
    
    # Report downloads
    path('designs/<int:pk>/download/quotation-pdf/', views.download_quotation_pdf, name='download_quotation_pdf'),
    path('designs/<int:pk>/download/boq-excel/', views.download_boq_excel, name='download_boq_excel'),
    path('designs/<int:pk>/download/cutting-list-excel/', views.download_cutting_list_excel, name='download_cutting_list_excel'),
    path('designs/<int:pk>/download/material-summary-pdf/', views.download_material_summary_pdf, name='download_material_summary_pdf'),
    
    # Pricing rates
    path('pricing-rates/', views.pricing_rates, name='pricing_rates'),
    path('pricing-rates/create/', views.create_pricing_rate, name='create_pricing_rate'),
    path('pricing-rates/<int:pk>/edit/', views.edit_pricing_rate, name='edit_pricing_rate'),
]
