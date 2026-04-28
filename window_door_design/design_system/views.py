from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import os
from datetime import datetime
from pathlib import Path

from .models import WindowDoorDesign, PricingRate, DesignReport
from .forms import WindowDoorDesignForm, PricingRateForm
from .business_logic import DesignCalculator
from .report_generator import ReportGenerator


def home(request):
    """Home page with navigation"""
    designs = WindowDoorDesign.objects.all()
    context = {
        'total_designs': designs.count(),
        'recent_designs': designs[:5],
    }
    return render(request, 'home.html', context)


def create_design(request):
    """Create a new window/door design"""
    if request.method == 'POST':
        form = WindowDoorDesignForm(request.POST)
        if form.is_valid():
            design = form.save()
            return redirect('design_detail', pk=design.pk)
    else:
        form = WindowDoorDesignForm()
    
    context = {'form': form, 'page_title': 'Create New Design'}
    return render(request, 'create_design.html', context)


def design_detail(request, pk):
    """Display design details with calculations and preview"""
    design = get_object_or_404(WindowDoorDesign, pk=pk)
    calculator = DesignCalculator(design)
    
    # Get all calculated data
    material_req = calculator.calculate_material_requirements()
    cost_breakdown = calculator.calculate_cost()
    boq = calculator.get_bill_of_quantities()
    
    context = {
        'design': design,
        'material_requirements': material_req,
        'cost_breakdown': cost_breakdown,
        'boq': boq,
    }
    
    return render(request, 'design_detail.html', context)


def edit_design(request, pk):
    """Edit an existing design"""
    design = get_object_or_404(WindowDoorDesign, pk=pk)
    
    if request.method == 'POST':
        form = WindowDoorDesignForm(request.POST, instance=design)
        if form.is_valid():
            design = form.save()
            return redirect('design_detail', pk=design.pk)
    else:
        form = WindowDoorDesignForm(instance=design)
    
    context = {'form': form, 'design': design, 'page_title': f'Edit {design.name}'}
    return render(request, 'create_design.html', context)


def delete_design(request, pk):
    """Delete a design"""
    design = get_object_or_404(WindowDoorDesign, pk=pk)
    
    if request.method == 'POST':
        design.delete()
        return redirect('home')
    
    context = {'design': design}
    return render(request, 'confirm_delete.html', context)


def design_list(request):
    """List all designs"""
    designs = WindowDoorDesign.objects.all().order_by('-created_at')
    
    context = {
        'designs': designs,
        'page_title': 'All Designs',
    }
    
    return render(request, 'design_list.html', context)


@require_http_methods(["GET"])
def preview_2d(request, pk):
    """Generate 2D preview canvas data as JSON"""
    design = get_object_or_404(WindowDoorDesign, pk=pk)
    
    # Canvas dimensions
    canvas_width = 800
    canvas_height = 600
    
    # Scale factor to fit design into canvas
    width_mm = float(design.width) * 1000
    height_mm = float(design.height) * 1000
    
    scale = min(canvas_width / width_mm, canvas_height / height_mm) * 0.8
    
    # Calculate scaled dimensions
    scaled_width = width_mm * scale
    scaled_height = height_mm * scale
    
    # Center the design in canvas
    start_x = (canvas_width - scaled_width) / 2
    start_y = (canvas_height - scaled_height) / 2
    
    preview_data = {
        'canvas_width': canvas_width,
        'canvas_height': canvas_height,
        'window': {
            'x': start_x,
            'y': start_y,
            'width': scaled_width,
            'height': scaled_height,
            'color': '#1f4788',
            'label': f"{design.width}m x {design.height}m"
        },
        'frame': {
            'x': start_x - 5,
            'y': start_y - 5,
            'width': scaled_width + 10,
            'height': scaled_height + 10,
            'stroke_width': 2,
            'color': '#666666'
        },
        'units': design.number_of_units,
        'type': design.get_type_choice_display(),
        'design_name': design.name,
    }
    
    return JsonResponse(preview_data)


def preview_3d(request, pk):
    """Generate 3D preview template with context"""
    design = get_object_or_404(WindowDoorDesign, pk=pk)
    
    context = {
        'design': design,
        'width': float(design.width),
        'height': float(design.height),
        'type': design.get_type_choice_display().lower(),
        'material': design.get_material_display().lower(),
        'glass': design.get_glass_type_display().lower() if design.glass_type else 'none',
        'page_title': f'3D Preview - {design.name}',
    }
    
    return render(request, '3d_view.html', context)
@require_http_methods(["GET"])
def download_quotation_pdf(request, pk):
    """Download quotation as PDF"""
    design = get_object_or_404(WindowDoorDesign, pk=pk)
    report_gen = ReportGenerator(design)
    
    pdf_buffer = report_gen.generate_pdf_quotation()
    
    filename = f"Quotation_{design.code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    return FileResponse(
        pdf_buffer,
        as_attachment=True,
        filename=filename,
        content_type='application/pdf'
    )


@require_http_methods(["GET"])
def download_boq_excel(request, pk):
    """Download Bill of Quantities as Excel"""
    design = get_object_or_404(WindowDoorDesign, pk=pk)
    report_gen = ReportGenerator(design)
    
    excel_buffer = report_gen.generate_excel_boq()
    
    filename = f"BOQ_{design.code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    return FileResponse(
        excel_buffer,
        as_attachment=True,
        filename=filename,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@require_http_methods(["GET"])
def download_cutting_list_excel(request, pk):
    """Download cutting list as Excel"""
    design = get_object_or_404(WindowDoorDesign, pk=pk)
    report_gen = ReportGenerator(design)
    
    excel_buffer = report_gen.generate_excel_cutting_list()
    
    filename = f"CuttingList_{design.code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    return FileResponse(
        excel_buffer,
        as_attachment=True,
        filename=filename,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@require_http_methods(["GET"])
def download_material_summary_pdf(request, pk):
    """Download material summary as PDF"""
    design = get_object_or_404(WindowDoorDesign, pk=pk)
    report_gen = ReportGenerator(design)
    
    pdf_buffer = report_gen.generate_material_summary_pdf()
    
    filename = f"MaterialSummary_{design.code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    return FileResponse(
        pdf_buffer,
        as_attachment=True,
        filename=filename,
        content_type='application/pdf'
    )


def pricing_rates(request):
    """Manage pricing rates"""
    rates = PricingRate.objects.all()
    context = {'rates': rates, 'page_title': 'Pricing Rates'}
    return render(request, 'pricing_rates.html', context)


def edit_pricing_rate(request, pk):
    """Edit pricing rate"""
    rate = get_object_or_404(PricingRate, pk=pk)
    
    if request.method == 'POST':
        form = PricingRateForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
            return redirect('pricing_rates')
    else:
        form = PricingRateForm(instance=rate)
    
    context = {'form': form, 'rate': rate, 'page_title': f'Edit {rate.get_material_type_display()}'}
    return render(request, 'edit_pricing_rate.html', context)


def create_pricing_rate(request):
    """Create new pricing rate"""
    if request.method == 'POST':
        form = PricingRateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pricing_rates')
    else:
        form = PricingRateForm()
    
    context = {'form': form, 'page_title': 'Create Pricing Rate'}
    return render(request, 'edit_pricing_rate.html', context)


def get_design_recommendation(request):
    """
    Get AI-powered design recommendation based on user inputs
    Handles both GET (display form) and POST (get prediction)
    """
    try:
        from .predict import DesignPredictor, get_recommendation_details
    except ImportError:
        context = {
            'error': 'ML model not available. Please train the model first.',
            'page_title': 'Design Recommendation'
        }
        return render(request, 'recommendation.html', context)
    
    if request.method == 'POST':
        # Collect user inputs
        input_data = {
            'room_size': request.POST.get('room_size'),
            'budget': request.POST.get('budget'),
            'noise_level': request.POST.get('noise_level'),
            'sunlight': request.POST.get('sunlight'),
            'room_type': request.POST.get('room_type'),
        }
        
        # Check for missing values
        if any(v is None for v in input_data.values()):
            context = {
                'error': 'Please fill in all fields',
                'valid_values': DesignPredictor().get_valid_values(),
                'page_title': 'Design Recommendation'
            }
            return render(request, 'recommendation.html', context)
        
        # Make prediction
        try:
            predictor = DesignPredictor()
            prediction = predictor.predict(input_data)
            recommendation = get_recommendation_details(prediction)
            
            context = {
                'user_input': input_data,
                'prediction': prediction,
                'recommendation': recommendation,
                'valid_values': predictor.get_valid_values(),
                'page_title': 'Design Recommendation'
            }
            return render(request, 'recommendation.html', context)
        except FileNotFoundError:
            context = {
                'error': 'ML model not trained yet. Please run training script first.',
                'valid_values': DesignPredictor().get_valid_values() if Path(__file__).parent.joinpath('encoders.pkl').exists() else {},
                'page_title': 'Design Recommendation'
            }
            return render(request, 'recommendation.html', context)
        except Exception as e:
            context = {
                'error': f'Error during prediction: {str(e)}',
                'valid_values': DesignPredictor().get_valid_values(),
                'page_title': 'Design Recommendation'
            }
            return render(request, 'recommendation.html', context)
    
    # GET request - show form with valid values
    try:
        predictor = DesignPredictor()
        valid_values = predictor.get_valid_values()
    except Exception:
        valid_values = {
            'room_size': ['small', 'medium', 'large'],
            'budget': ['low', 'medium', 'high'],
            'noise_level': ['low', 'medium', 'high'],
            'sunlight': ['low', 'medium', 'high'],
            'room_type': ['bedroom', 'kitchen', 'office', 'living']
        }
    
    context = {
        'valid_values': valid_values,
        'page_title': 'Design Recommendation'
    }
    return render(request, 'recommendation.html', context)
