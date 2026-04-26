# Window & Door Design System

A comprehensive web-based design system for creating, calculating, and exporting window and door specifications using Django and Python.

## Features

### Core Functionality
- **Design Creation**: Create window/door designs with customizable parameters:
  - Dimensions (width/height in meters)
  - Type (sliding, casement, awning, tilt & turn, fixed, bifold, revolving)
  - Glass type (clear, tinted, frosted, double glazed, tempered)
  - Material (aluminum, UPVC, steel, wood)
  - Finish type (anodized, powder coated, raw, painted, natural wood)
  - Mesh option (yes/no for mosquito mesh)
  - Number of units

### Automatic Calculations
- **Material Requirements**: Automatic calculation of:
  - Profile lengths needed
  - Glass area required
  - Mesh area (if applicable)
  - Frame dimensions
  
- **Cost Estimation**: Based on predefined rates:
  - Material cost
  - Labor cost
  - Glass cost
  - Mesh cost
  - Profile cost
  - Total cost

### Report Generation
Export professional reports in multiple formats:
- **Quotation (PDF)**: Professional quotation with cost breakdown
- **Bill of Quantities (BOQ) (Excel)**: Detailed BOQ with all specifications
- **Cutting List (Excel)**: Exact cutting sizes for materials
- **Material Summary (PDF)**: Overview of material requirements

### Visualization
- **2D Preview**: Visual representation of your window/door design in a canvas
- Mobile-friendly responsive design

### Validation
- Rule-based dimension validation
- Reasonable dimension constraints (0.1m to 10m)
- Unique design code enforcement

## Technical Stack

- **Backend**: Django 4.2.11
- **Database**: SQLite3
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Report Generation**: ReportLab (PDF), OpenPyXL (Excel)
- **Python**: 3.8+

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Navigate to project directory**:
   ```bash
   cd /Users/tejassantoshdhembe/Downloads/Design/window_door_design
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**:
   ```bash
   python manage.py migrate
   ```

5. **Create default pricing rates** (optional):
   ```bash
   python manage.py shell
   ```
   Then in the shell:
   ```python
   from design_system.models import PricingRate
   
   materials = ['aluminum', 'upvc', 'steel', 'wood']
   for material in materials:
       PricingRate.objects.get_or_create(
           material_type=material,
           defaults={
               'rate_per_sqft': 150,
               'labor_cost_per_unit': 200,
               'glass_cost_per_sqft': 100,
               'mesh_cost_per_sqft': 50,
               'profile_cost_per_meter': 150,
           }
       )
   exit()
   ```

6. **Run development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Open browser and go to `http://localhost:8000`
   - Home page with navigation and features overview
   - Start creating designs from "New Design" button

## Usage

### Creating a Design

1. Click "New Design" button on the home page
2. Fill in design details:
   - Design name and unique code
   - Dimensions in meters
   - Type and material
   - Glass and finish types
   - Add mesh if needed
   - Set number of units
3. Click "Save Design"

### Viewing Design Details

1. Click on a design from the list
2. View:
   - All specifications
   - 2D preview canvas
   - Material requirements
   - Cost breakdown
3. Download reports as needed

### Managing Pricing Rates

1. Go to "Pricing" in navigation
2. View all material types and their rates
3. Click "Edit" to modify rates:
   - Rate per square foot
   - Labor cost per unit
   - Glass, mesh, and profile costs

### Downloading Reports

From the design detail page:
- **Quotation PDF**: Professional quotation with cost breakdown
- **BOQ Excel**: Detailed bill of quantities
- **Cutting List Excel**: Exact cutting measurements
- **Material Summary PDF**: Material requirements overview

## Project Structure

```
window_door_design/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── config/                   # Django project configuration
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI application
├── design_system/           # Main Django app
│   ├── models.py            # Database models
│   ├── forms.py             # Django forms
│   ├── views.py             # View functions
│   ├── urls.py              # App URL routing
│   ├── apps.py              # App configuration
│   ├── business_logic.py    # Calculation engine
│   └── report_generator.py  # Report generation
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── home.html            # Home page
│   ├── create_design.html   # Create/edit design form
│   ├── design_detail.html   # Design details with preview
│   ├── design_list.html     # List all designs
│   ├── confirm_delete.html  # Delete confirmation
│   ├── pricing_rates.html   # Pricing rates list
│   └── edit_pricing_rate.html # Edit pricing rate
└── static/                  # Static files
    ├── css/                 # Stylesheets
    └── js/                  # JavaScript files
```

## API Endpoints

### Designs
- `GET /` - Home page
- `GET /designs/` - List all designs
- `GET /designs/create/` - Create design form
- `POST /designs/create/` - Save new design
- `GET /designs/<id>/` - View design details
- `GET /designs/<id>/edit/` - Edit design form
- `POST /designs/<id>/edit/` - Update design
- `GET /designs/<id>/delete/` - Delete confirmation
- `POST /designs/<id>/delete/` - Delete design

### Reports
- `GET /designs/<id>/preview-2d/` - Get 2D preview data (JSON)
- `GET /designs/<id>/download/quotation-pdf/` - Download quotation
- `GET /designs/<id>/download/boq-excel/` - Download BOQ
- `GET /designs/<id>/download/cutting-list-excel/` - Download cutting list
- `GET /designs/<id>/download/material-summary-pdf/` - Download material summary

### Pricing
- `GET /pricing-rates/` - List all pricing rates
- `GET /pricing-rates/create/` - Create rate form
- `POST /pricing-rates/create/` - Save new rate
- `GET /pricing-rates/<id>/edit/` - Edit rate form
- `POST /pricing-rates/<id>/edit/` - Update rate

## Calculation Methods

### Material Requirements
- **Profile Length**: `2 × (width + height) × number_of_units`
- **Glass Area**: `width × height × number_of_units`
- **Mesh Area**: Same as glass area if mesh is enabled

### Cost Calculation
```
Total Cost = Material Cost + Labor Cost + Glass Cost + Mesh Cost + Profile Cost

Where:
- Material Cost = rate_per_sqft × area × units
- Labor Cost = labor_cost_per_unit × units
- Glass Cost = glass_cost_per_sqft × area × units
- Mesh Cost = mesh_cost_per_sqft × area × units (if applicable)
- Profile Cost = profile_cost_per_meter × perimeter × units
```

### Cutting Sizes
All measurements calculated with standard allowances:
- Vertical rails: height (mm) - 100mm
- Horizontal rails: width (mm) - 100mm
- Glass sizes: width (mm) - 20mm, height (mm) - 20mm

## Validation Rules

- Dimensions must be between 0.1m and 10m
- Design code must be unique
- Number of units must be at least 1
- Pricing rates must have positive values

## Browser Compatibility

- Chrome/Edge (latest versions)
- Firefox (latest versions)
- Safari (latest versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Notes

- SQLite database suitable for small to medium deployments
- Static files served through Django in development
- PDF generation using ReportLab is fast
- Excel file generation using OpenPyXL is efficient

## Future Enhancements

- User authentication and role-based access
- Design templates and presets
- Multiple quotation versions
- Inventory management
- Client database integration
- Email report delivery
- Advanced 3D visualization
- Multi-language support
- Custom branding in reports
- Design history and versioning

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions, please review the code documentation or check Django and related package documentation.

---

**Created**: 2026  
**Version**: 1.0.0
