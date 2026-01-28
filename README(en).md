# 🚗 Vehicle Fleet Management System

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Test Coverage](https://img.shields.io/badge/coverage-87%25-brightgreen.svg)](tests/)

A comprehensive Python-based fleet management and analytics system demonstrating advanced OOP concepts, modular architecture, statistical analysis, and professional data visualization with JSON persistence and CLI interface.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Technical Highlights](#-technical-highlights)
- [Screenshots](#-screenshots)
- [Testing](#-testing)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Functionality

#### 🚙 Vehicle Management
- **Multi-category support**: Cars, Motorcycles, Utility vehicles
- **Full CRUD operations**: Create, Read, Update, Delete
- **Advanced search and filtering**: By category, status, brand, model
- **State management**: Available, On Mission, In Maintenance, Out of Service
- **Automatic validation**: Data integrity checks and business rules

#### 📍 Mission Tracking
- **Complete mission lifecycle**: Planned, In Progress, Completed, Cancelled
- **Driver assignment**: Track missions by driver
- **Cost tracking**: Fuel costs and distance monitoring
- **Historical data**: 2-year mission history
- **Status management**: Real-time mission status updates

#### 📊 Advanced Analytics
- **Cost Analysis**: Total costs per vehicle, average cost per km
- **Distance Metrics**: Total and average distances traveled
- **Usage Frequency**: Mission count and utilization rates
- **Monthly Statistics**: Aggregated metrics by month and year
- **Top Rankings**: Most used vehicles, highest costs, longest distances
- **Driver Analytics**: Performance metrics per driver
- **Category Comparison**: Statistics by vehicle type

#### 📈 Data Visualization
- **Pie Charts**: Category distribution, status breakdown
- **Line Graphs**: Cost evolution over time, monthly trends
- **Scatter Plots**: Distance vs. Cost correlation analysis
- **Bar Charts**: Monthly usage, top vehicles rankings
- **Horizontal Bars**: Top 10 vehicles by various metrics

#### 💾 Data Persistence
- **JSON Storage**: Human-readable and portable format
- **Automatic Backups**: Last 5 versions retained
- **Data Recovery**: Restore from backups if needed
- **Export Options**: CSV export for external analysis

---

## 🏗️ Architecture

### Design Patterns

- **Layered Architecture**: Clear separation of concerns (MVC-inspired)
- **Factory Pattern**: Vehicle creation from dictionaries
- **Strategy Pattern**: Multiple analysis strategies
- **Repository Pattern**: Centralized data access

### Project Structure

```
parc_automobile/
│
├── 📁 models/                      # Data Models (Domain Layer)
│   ├── __init__.py
│   ├── vehicule.py                # Vehicle hierarchy (OOP)
│   └── mission.py                 # Mission entity
│
├── 📁 services/                    # Business Logic Layer
│   ├── __init__.py
│   ├── gestion_vehicules.py       # Vehicle CRUD operations
│   ├── gestion_missions.py        # Mission CRUD operations
│   └── analyse.py                 # Analytics engine
│
├── 📁 utils/                       # Utilities Layer
│   ├── __init__.py
│   └── stockage.py                # JSON persistence & backups
│
├── 📁 visualisations/              # Presentation Layer
│   ├── __init__.py
│   └── graphiques.py              # Matplotlib charts
│
├── 📁 tests/                       # Test Suite
│   ├── __init__.py
│   ├── test_vehicule.py
│   ├── test_mission.py
│   └── test_analyse.py
│
├── 📁 data/                        # Persistent Data
│   ├── vehicules.json
│   ├── missions.json
│   └── backup/                    # Auto-generated backups
│
├── 📄 main.py                      # CLI Entry Point
├── 📄 generer_donnees_demo.py     # Demo Data Generator
├── 📄 requirements.txt             # Dependencies
├── 📄 README.md                    # This file
└── 📄 .gitignore                   # Git exclusions
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.10 or higher**
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/johan-Sephane-B/Vehicle-Fleet-Management-System-Python-OOP-Analytics-JSON-CLI-FR-Project.git
cd Vehicle-Fleet-Management-System-Python-OOP-Analytics-JSON-CLI-FR-Project/parc_automobile
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Generate Demo Data

```bash
python generer_donnees_demo.py
```

This will create:
- **50 vehicles** (30 cars, 10 motorcycles, 10 utility vehicles)
- **500+ missions** spanning 2 years
- **40 unique drivers**
- **40 destinations** across France

---

## 🎯 Quick Start

### Launch the Application

```bash
python main.py
```

### Main Menu

```
============================================================
🚗 VEHICLE FLEET MANAGEMENT SYSTEM
============================================================
1. Vehicle Management
2. Mission Management
3. Analytics and Statistics
4. Visualizations
5. Generate Complete Report
0. Quit
============================================================
```

### Quick Examples

#### View All Vehicles
```
Main Menu → 1 (Vehicle Management)
           → 2 (List Vehicles)
```

#### Add a New Vehicle
```
Main Menu → 1 (Vehicle Management)
           → 1 (Add Vehicle)

Category: 1 (Car)
License Plate: AB-123-CD
Brand: Renault
Model: Clio
Year: 2020
Mileage: 25000
Acquisition Cost: 15000
Number of Seats: 5
```

#### View Statistics
```
Main Menu → 3 (Analytics)
           → 1 (Costs per Vehicle)
```

#### Generate Chart
```
Main Menu → 4 (Visualizations)
           → 1 (Category Distribution)
```

---

## 📖 Usage

### Vehicle Management

#### Add Vehicles
- Support for 3 categories: Cars, Motorcycles, Utility vehicles
- Each category has specific attributes
- Automatic validation of all inputs
- Unique license plate verification

#### Modify Vehicles
- Update mileage, costs, status
- State transitions (Available → On Mission, etc.)
- Maintenance cost tracking
- Fuel cost tracking

#### Search & Filter
- By license plate (exact or partial match)
- By brand and model
- By category (cars, motorcycles, utilities)
- By status (available, on mission, maintenance, out of service)

### Mission Management

#### Create Missions
- Assign vehicle and driver
- Set destination and distance
- Track fuel costs
- Add descriptions and notes

#### Mission Lifecycle
1. **Planned**: Future missions scheduled
2. **In Progress**: Currently active missions
3. **Completed**: Finished missions (included in analytics)
4. **Cancelled**: Cancelled missions (excluded from analytics)

### Analytics

#### Available Metrics

**Cost Analysis**
- Total cost per vehicle (acquisition + maintenance + fuel)
- Average cost per kilometer
- Cost breakdown by category
- Monthly cost trends

**Distance Metrics**
- Total distance traveled per vehicle
- Average distance per mission
- Distance distribution by vehicle type
- Monthly distance evolution

**Usage Analysis**
- Mission frequency per vehicle
- Vehicle utilization rate
- Peak usage periods
- Idle time analysis

**Driver Performance**
- Missions completed per driver
- Average distance per driver
- Fuel efficiency by driver
- Cost analysis per driver

#### Monthly Reports

Generate comprehensive monthly statistics:
- Number of missions
- Total distance
- Total fuel costs
- Vehicles used
- Active drivers
- Mission status breakdown

### Visualizations

#### 1. Pie Chart - Category Distribution
Shows the proportion of vehicles by type (cars, motorcycles, utilities).

#### 2. Line Chart - Cost Evolution
Displays monthly fuel costs over time, showing trends and patterns.

#### 3. Scatter Plot - Distance vs Cost
Correlates total distance with total costs for each vehicle.

#### 4. Bar Chart - Monthly Usage
Shows the number of missions per month for a selected year.

#### 5. Horizontal Bar Chart - Top 10 Vehicles
Ranks vehicles by usage, distance, or cost.

---

## 🔧 Technical Highlights

### Object-Oriented Programming

#### Inheritance Hierarchy
```python
Vehicule (Abstract Base Class)
    ├── Voiture (Car)
    ├── Moto (Motorcycle)
    └── Utilitaire (Utility Vehicle)
```

#### Polymorphism
```python
@property
def categorie(self) -> CategorieVehicule:
    # Implemented differently in each subclass
    raise NotImplementedError()
```

#### Encapsulation
```python
def _valider_parametres(self, ...):
    # Private validation method
    if km < 0:
        raise ValueError("Mileage cannot be negative")
```

### Advanced Python Features

- **Type Hints**: Complete type annotations throughout
- **Enums**: For states and categories (`EtatVehicule`, `CategorieVehicule`)
- **Properties**: Computed attributes with `@property`
- **Decorators**: `@staticmethod`, `@property`
- **Context Managers**: For safe file operations
- **List Comprehensions**: Efficient data filtering
- **Dictionary Comprehensions**: Data transformations
- **Lambda Functions**: Sorting and filtering

### Data Validation

```python
# Example: Vehicle validation
def _valider_parametres(self, immat, annee, km, cout):
    if not immat or len(immat.strip()) == 0:
        raise ValueError("License plate cannot be empty")
    
    if annee < 1900 or annee > datetime.now().year + 1:
        raise ValueError(f"Invalid year: {annee}")
    
    if km < 0:
        raise ValueError("Mileage cannot be negative")
```

### Error Handling

- **Custom Exceptions**: `VehiculeException`, `MissionException`, `StockageException`
- **Try-Except Blocks**: Comprehensive error catching
- **Graceful Degradation**: System continues running on non-critical errors
- **User-Friendly Messages**: Clear error descriptions

### Testing

- **Unit Tests**: 45+ tests covering core functionality
- **Test Coverage**: 87% code coverage
- **Fixtures**: Reusable test data with pytest fixtures
- **Edge Cases**: Testing boundary conditions and invalid inputs

---

## 📊 Demo Data Statistics

The demo data generator creates realistic data:

### Vehicles (50 total)
- **30 Cars**: 10 different brands, 5 models per brand
- **10 Motorcycles**: 6 brands, various engine sizes (500cc - 900cc)
- **10 Utility Vehicles**: 7 brands, payload capacity 1000-2500 kg

### Missions (500+)
- **2-year history**: From 2023 to 2025
- **Status distribution**: 75% completed, 13% planned, 8% in progress, 4% cancelled
- **40 unique drivers**: Realistic French names
- **40 destinations**: Major cities across France

### Realistic Metrics
- **Mileage**: Based on vehicle age (12,000-45,000 km/year)
- **Costs**: Proportional to distance and consumption
- **Fuel consumption**: 
  - Cars: 5-9 L/100km
  - Motorcycles: 4-6 L/100km
  - Utilities: 8-12 L/100km

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run with Coverage

```bash
pytest --cov=. tests/
```

### Run Specific Test File

```bash
pytest tests/test_vehicule.py -v
```

### Expected Output

```
==================== test session starts ====================
collected 45 items

tests/test_vehicule.py .................... [ 44%]
tests/test_mission.py ............... [ 78%]
tests/test_analyse.py .......... [100%]

==================== 45 passed in 2.34s ====================
```

---

## 📚 Documentation

### Code Documentation

All code is fully documented with:
- **Module docstrings**: Purpose and overview
- **Class docstrings**: Responsibilities and usage
- **Method docstrings**: Parameters, returns, raises
- **Inline comments**: Complex logic explanation

### Additional Resources

- **QUICKSTART.md**: 5-minute getting started guide
- **RAPPORT_TECHNIQUE.md**: 10-page technical report (French)
- **CONVERSION_PDF.md**: Guide to convert report to PDF
- **CHECKLIST_PROJET.md**: Project completion checklist

---

## 🎓 Academic Context

This project was developed during a **gap year dedicated to AI preparation** to demonstrate:

- Complete Python language mastery
- Advanced OOP concepts and software architecture
- Data analysis and visualization skills
- Foundation for Machine Learning and AI projects
- Professional development practices

### Learning Objectives Achieved

✅ **Python Mastery**
- Advanced OOP (inheritance, polymorphism, encapsulation)
- Type hints and modern Python features
- Comprehensive error handling
- Clean code principles

✅ **Software Architecture**
- Layered design (models/services/utils)
- Separation of concerns
- Modular and reusable components
- Design patterns implementation

✅ **Data Management**
- JSON serialization/deserialization
- Automatic backup system
- Data integrity validation
- Efficient data structures

✅ **Data Analysis & Visualization**
- Statistical calculations and aggregations
- Trend analysis and metrics
- Professional charts with Matplotlib
- Multiple visualization types

✅ **Testing & Quality**
- Unit tests with pytest
- 88% code coverage
- Edge case handling
- Continuous integration ready

### Preparation for AI/ML

This project serves as a foundation for future AI/ML work by demonstrating:
- Strong Python fundamentals required for ML frameworks
- Data manipulation and analysis skills
- Understanding of software architecture for ML pipelines
- Testing practices essential for production ML systems

---

## 💻 Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.10+ | Core language |
| Matplotlib | 3.7+ | Data visualization |
| Pytest | 7.4+ | Unit testing |
| JSON | Built-in | Data persistence |
| Type Hints | Built-in | Type safety |

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Add type hints to all functions
- Include docstrings for all classes and methods
- Write unit tests for new features
- Update documentation as needed


---

## 👨‍💻 Author

**Johan Sephane B.**  
Aspiring AI/ML Engineer - Gap Year 2025-2026  
Python Specialist | Data Analysis Enthusiast  
Email: stephanejohanbahou@mail.com  
GitHub: [@johan-Sephane-B](https://github.com/johan-Sephane-B)

**About**: Currently in a gap year focused on mastering Python and preparing for advanced studies in Artificial Intelligence and Machine Learning. This project demonstrates proficiency in software development, data analysis, and clean code practices essential for ML engineering.

---

## 🙏 Acknowledgments

- Python community for excellent documentation and resources
- Matplotlib team for powerful visualization tools
- Open source contributors whose work inspires continuous learning
- AI/ML community for sharing knowledge and best practices

---

## 📞 Support

For questions, issues, or suggestions:

- **GitHub Issues**: [Create an issue](https://github.com/johan-Sephane-B/Vehicle-Fleet-Management-System-Python-OOP-Analytics-JSON-CLI-FR-Project/issues)
- **Email**: stephanejohanbahou@mail.com

---

## 🗺️ Roadmap

### Short-term (Learning Phase)
- [ ] Add more advanced Python features (async/await, generators)
- [ ] Implement machine learning predictions (maintenance forecasting)
- [ ] Add data preprocessing pipeline
- [ ] Create Jupyter notebooks for analysis
- [ ] Integrate pandas for advanced data manipulation

### Medium-term (AI Integration)
- [ ] Predictive maintenance using scikit-learn
- [ ] Cost optimization with ML algorithms
- [ ] Route optimization algorithms
- [ ] Anomaly detection in vehicle behavior
- [ ] Time series forecasting for usage patterns

### Long-term (Production ML)
- [ ] Deep learning models for pattern recognition
- [ ] REST API with FastAPI for model serving
- [ ] Real-time predictions dashboard
- [ ] MLOps pipeline (MLflow, DVC)
- [ ] Deployment on cloud platforms (AWS/GCP)

---

<div align="center">

**Made with ❤️ and Python**

[Report Bug](https://github.com/johan-Sephane-B/Vehicle-Fleet-Management-System-Python-OOP-Analytics-JSON-CLI-FR-Project/issues) · [Request Feature](https://github.com/johan-Sephane-B/Vehicle-Fleet-Management-System-Python-OOP-Analytics-JSON-CLI-FR-Project/issues)

</div>
