from decimal import Decimal
from design_system.models import PricingRate, WindowDoorDesign


class DesignCalculator:
    """Business logic for window/door calculations"""
    
    def __init__(self, design: WindowDoorDesign):
        self.design = design
        try:
            self.pricing = PricingRate.objects.get(material_type=design.material)
        except PricingRate.DoesNotExist:
            # Create default pricing if not exists
            self.pricing = PricingRate.objects.create(material_type=design.material)
    
    def calculate_material_requirements(self):
        """Calculate material requirements based on dimensions"""
        width = float(self.design.width)
        height = float(self.design.height)
        units = self.design.number_of_units
        
        # Profile calculations
        perimeter = (2 * (width + height))  # meters
        profile_length = perimeter * units
        
        # Glass area
        glass_area = width * height * units  # square meters
        
        # Mesh area (if applicable)
        mesh_area = glass_area if self.design.has_mesh else 0
        
        return {
            'profile_length_meters': round(profile_length, 2),
            'glass_area_sqm': round(glass_area, 4),
            'mesh_area_sqm': round(mesh_area, 4),
            'frame_width_mm': 50,  # Standard frame width
            'frame_height_mm': 50,  # Standard frame height
        }
    
    def calculate_cutting_sizes(self):
        """Calculate exact cutting sizes for materials"""
        width_mm = float(self.design.width) * 1000
        height_mm = float(self.design.height) * 1000
        units = self.design.number_of_units
        
        # Standard allowances
        vertical_cut = height_mm - 100  # 50mm top + 50mm bottom
        horizontal_cut = width_mm - 100  # 50mm left + 50mm right
        
        cuts = []
        for i in range(units):
            cuts.append({
                'unit': i + 1,
                'vertical_rail_mm': vertical_cut,
                'horizontal_rail_mm': horizontal_cut,
                'glass_width_mm': width_mm - 20,
                'glass_height_mm': height_mm - 20,
            })
        
        return cuts
    
    def calculate_cost(self):
        """Calculate total estimated cost"""
        width = float(self.design.width)
        height = float(self.design.height)
        units = self.design.number_of_units
        
        # Base material cost
        area = width * height
        material_cost = float(self.pricing.rate_per_sqft) * area * units
        
        # Labor cost
        labor_cost = float(self.pricing.labor_cost_per_unit) * units
        
        # Glass cost
        glass_cost = float(self.pricing.glass_cost_per_sqft) * area * units
        
        # Mesh cost (if applicable)
        mesh_cost = float(self.pricing.mesh_cost_per_sqft) * area * units if self.design.has_mesh else 0
        
        # Profile cost
        perimeter = 2 * (width + height)
        profile_cost = float(self.pricing.profile_cost_per_meter) * perimeter * units
        
        total_cost = material_cost + labor_cost + glass_cost + mesh_cost + profile_cost
        
        return {
            'material_cost': round(Decimal(str(material_cost)), 2),
            'labor_cost': round(Decimal(str(labor_cost)), 2),
            'glass_cost': round(Decimal(str(glass_cost)), 2),
            'mesh_cost': round(Decimal(str(mesh_cost)), 2),
            'profile_cost': round(Decimal(str(profile_cost)), 2),
            'total_cost': round(Decimal(str(total_cost)), 2),
        }
    
    def get_bill_of_quantities(self):
        """Generate bill of quantities data"""
        materials_req = self.calculate_material_requirements()
        cost_breakdown = self.calculate_cost()
        
        boq = {
            'design_name': self.design.name,
            'design_code': self.design.code,
            'design_type': self.design.get_type_choice_display(),
            'material_type': self.design.get_material_display(),
            'number_of_units': self.design.number_of_units,
            'width_m': float(self.design.width),
            'height_m': float(self.design.height),
            'total_area_sqm': float(self.design.total_area),
            'glass_type': self.design.get_glass_type_display(),
            'has_mesh': self.design.has_mesh,
            'finish_type': self.design.get_finish_type_display(),
            'materials': materials_req,
            'costs': cost_breakdown,
        }
        
        return boq
    
    def get_quotation_data(self):
        """Generate quotation data"""
        boq = self.get_bill_of_quantities()
        
        quotation = {
            'design_name': boq['design_name'],
            'design_code': boq['design_code'],
            'description': f"{boq['design_type']} - {boq['material_type']} {boq['number_of_units']} units",
            'dimensions': f"{boq['width_m']}m W x {boq['height_m']}m H",
            'total_area': boq['total_area_sqm'],
            'unit_price': boq['costs']['total_cost'] / boq['number_of_units'],
            'total_price': boq['costs']['total_cost'],
            'cost_breakdown': boq['costs'],
        }
        
        return quotation
