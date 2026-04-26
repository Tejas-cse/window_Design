from django import forms
from .models import WindowDoorDesign, PricingRate


class WindowDoorDesignForm(forms.ModelForm):
    """Form for creating and editing window/door designs"""
    
    class Meta:
        model = WindowDoorDesign
        fields = [
            'name', 'code', 'width', 'height', 'type_choice', 
            'glass_type', 'has_mesh', 'finish_type', 'material', 'number_of_units'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Living Room Window',
                'required': True
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., WD-001',
                'required': True
            }),
            'width': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Width in meters',
                'step': '0.01',
                'min': '0.1',
                'required': True
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Height in meters',
                'step': '0.01',
                'min': '0.1',
                'required': True
            }),
            'type_choice': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'glass_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'has_mesh': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'finish_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'material': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'number_of_units': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of units',
                'min': '1',
                'required': True
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')
        type_choice = cleaned_data.get('type_choice')
        glass_type = cleaned_data.get('glass_type')
        
        # Validation: dimensions must be reasonable
        if width and height:
            if width > 10 or height > 10:
                raise forms.ValidationError(
                    "Invalid dimensions. Width and height should not exceed 10 meters."
                )
            if width < 0.1 or height < 0.1:
                raise forms.ValidationError(
                    "Invalid dimensions. Width and height should be at least 0.1 meters."
                )
        
        # If type is 'door', glass_type is not required
        if type_choice == 'door':
            cleaned_data['glass_type'] = None
            # Don't validate glass_type for doors
            if 'glass_type' in self.errors:
                del self.errors['glass_type']
        elif type_choice == 'window' and not glass_type:
            # If type is 'window', glass_type is required
            raise forms.ValidationError(
                "Glass type is required for windows."
            )
        
        return cleaned_data


class PricingRateForm(forms.ModelForm):
    """Form for managing pricing rates"""
    
    class Meta:
        model = PricingRate
        fields = [
            'material_type', 'rate_per_sqft', 'labor_cost_per_unit',
            'glass_cost_per_sqft', 'mesh_cost_per_sqft', 'profile_cost_per_meter'
        ]
        widgets = {
            'material_type': forms.Select(attrs={'class': 'form-control'}),
            'rate_per_sqft': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'labor_cost_per_unit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'glass_cost_per_sqft': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'mesh_cost_per_sqft': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'profile_cost_per_meter': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
