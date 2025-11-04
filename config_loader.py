"""
Configuration Loader
Loads instruments and forecasts from YAML files
"""

import yaml
import os

class ConfigLoader:
    """Loads configuration from YAML files"""
    
    def __init__(self, config_dir=None):
        if config_dir is None:
            config_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_dir = config_dir
        
    def load_instruments(self):
        """Load instruments configuration"""
        config_path = os.path.join(self.config_dir, 'instruments_config.yaml')
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Instruments config not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            instruments = yaml.safe_load(f)
        
        # Remove metadata and templates, keep only instruments
        if instruments:
            instruments = {k: v for k, v in instruments.items() if isinstance(v, dict) and 'type' in v}
        
        return instruments
    
    def load_forecasts(self):
        """Load forecasts configuration"""
        config_path = os.path.join(self.config_dir, 'forecasts_config.yaml')
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Forecasts config not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            forecasts = yaml.safe_load(f)
        
        return forecasts
    
    def get_cbr_scenarios(self):
        """Get CBR rate scenarios"""
        forecasts = self.load_forecasts()
        cbr_data = forecasts.get('cbr_scenarios', {})
        
        scenarios = {}
        for scenario_name, scenario_data in cbr_data.items():
            if isinstance(scenario_data, dict) and 'rates' in scenario_data:
                scenarios[scenario_name] = scenario_data['rates']
        
        return scenarios
    
    def get_fx_scenarios(self):
        """Get FX rate scenarios"""
        forecasts = self.load_forecasts()
        fx_data = forecasts.get('fx_scenarios', {})
        
        scenarios = {}
        for scenario_name, scenario_data in fx_data.items():
            if isinstance(scenario_data, dict) and 'rates' in scenario_data:
                scenarios[scenario_name] = scenario_data['rates']
        
        return scenarios
    
    def get_structured_bond_coupons(self, bond_name='Структурная облигация Сбер'):
        """Get structured bond monthly coupon forecast"""
        forecasts = self.load_forecasts()
        bond_data = forecasts.get('structured_bond_coupons', {}).get(bond_name, {})
        
        if 'monthly_coupons' in bond_data:
            # Extract just the coupon values
            coupons = [month_data['coupon'] for month_data in bond_data['monthly_coupons']]
            return coupons
        
        return []
    
    def update_instrument_with_forecast(self, instrument_name, instrument_data):
        """Update instrument data with forecast information"""
        
        # For structured bonds, add monthly coupon forecast
        if instrument_data.get('variable_coupon', False):
            coupons = self.get_structured_bond_coupons(instrument_name)
            if coupons:
                instrument_data['coupon_forecast'] = coupons
        
        return instrument_data
    
    def get_all_config(self):
        """Get complete configuration"""
        return {
            'instruments': self.load_instruments(),
            'cbr_scenarios': self.get_cbr_scenarios(),
            'fx_scenarios': self.get_fx_scenarios()
        }


if __name__ == "__main__":
    # Test the loader
    loader = ConfigLoader()
    
    print("="*80)
    print("CONFIGURATION LOADER TEST")
    print("="*80)
    
    # Test instruments
    print("\n1. Loading instruments...")
    instruments = loader.load_instruments()
    print(f"   ✅ Loaded {len(instruments)} instruments:")
    for name in instruments.keys():
        print(f"      - {name}")
    
    # Test CBR scenarios
    print("\n2. Loading CBR scenarios...")
    cbr_scenarios = loader.get_cbr_scenarios()
    print(f"   ✅ Loaded {len(cbr_scenarios)} CBR scenarios:")
    for name, rates in cbr_scenarios.items():
        print(f"      - {name}: {rates}")
    
    # Test FX scenarios
    print("\n3. Loading FX scenarios...")
    fx_scenarios = loader.get_fx_scenarios()
    print(f"   ✅ Loaded {len(fx_scenarios)} FX scenarios:")
    for name, rates in fx_scenarios.items():
        print(f"      - {name}: {rates}")
    
    # Test structured bond coupons
    print("\n4. Loading structured bond coupons...")
    coupons = loader.get_structured_bond_coupons()
    print(f"   ✅ Loaded {len(coupons)} monthly coupons:")
    print(f"      Min: {min(coupons)}%, Max: {max(coupons)}%, Avg: {sum(coupons)/len(coupons):.2f}%")
    
    print("\n" + "="*80)
    print("✅ ALL CONFIGURATION LOADED SUCCESSFULLY!")
    print("="*80)

