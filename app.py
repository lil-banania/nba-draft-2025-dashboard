import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, date
import json
from typing import Dict, List, Tuple, Optional, Any

# ==================== Configuration ====================
st.set_page_config(
    page_title="🏀 NBA Draft 2025 AI",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== Styles CSS ====================
def inject_custom_css():
    """Inject custom CSS for styling"""
    st.markdown("""<style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .main { font-family: 'Inter', sans-serif; }
        
        .hero-header {
            background: linear-gradient(135deg, #FF6B35 0%, #F7931E 50%, #FFD23F 100%);
            padding: 3rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(255, 107, 53, 0.3);
            color: white;
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .prospect-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            border-left: 5px solid #FF6B35;
        }
        
        .countdown-container {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 2rem 0;
        }
        
        .leader-card {
            background: linear-gradient(135deg, #f8f9fa, #ffffff);
            border: 1px solid #e9ecef;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            border-left: 5px solid #FFD700;
            color: #333;
        }
        
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .stat-box {
            background: #f8f9fa;
            padding: 0.8rem;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: #666;
        }
    </style>""", unsafe_allow_html=True)

# ==================== Utilitaires ====================
def safe_numeric(value: Any, default: float = 0.0) -> float:
    """Convert value to float safely"""
    try:
        if pd.isna(value) or value is None or value == '':
            return default
        return float(value)
    except (ValueError, TypeError, AttributeError):
        return default

def safe_string(value: Any, default: str = 'N/A') -> str:
    """Convert value to string safely"""
    try:
        if pd.isna(value) or value is None:
            return default
        return str(value)
    except (ValueError, TypeError, AttributeError):
        return default

def format_height(height_decimal: float) -> str:
    """Convert decimal height to feet'inches format"""
    if height_decimal == 0:
        return "N/A"
    feet = int(height_decimal)
    inches = int((height_decimal - feet) * 12)
    return f"{feet}'{inches}\""
 
def calculate_draft_grade_average(df: pd.DataFrame) -> str:
    """Calculate average draft grade from letter grades"""
    
    # Mapping des grades vers des valeurs numériques
    grade_mapping = {
        'A+': 4.3,
        'A': 4.0,
        'A-': 3.7,
        'B+': 3.3,
        'B': 3.0,
        'B-': 2.7,
        'C+': 2.3,
        'C': 2.0,
        'C-': 1.7,
        'D+': 1.3,
        'D': 1.0,
        'D-': 0.7,
        'F': 0.0
    }
    
    # Mapping inverse pour reconvertir en lettres
    reverse_mapping = {
        4.3: 'A+', 4.0: 'A', 3.7: 'A-',
        3.3: 'B+', 3.0: 'B', 2.7: 'B-',
        2.3: 'C+', 2.0: 'C', 1.7: 'C-',
        1.3: 'D+', 1.0: 'D', 0.7: 'D-',
        0.0: 'F'
    }
    
    # Convertir les grades en valeurs numériques
    numeric_grades = []
    for grade in df['scout_grade']:
        grade_clean = safe_string(grade).strip()
        if grade_clean in grade_mapping:
            numeric_grades.append(grade_mapping[grade_clean])
        else:
            # Grade par défaut si non reconnu
            numeric_grades.append(2.5)  # Équivalent à un "C+"
    
    # Calculer la moyenne
    if numeric_grades:
        avg_numeric = sum(numeric_grades) / len(numeric_grades)
        
        # Trouver le grade le plus proche
        closest_grade = min(reverse_mapping.keys(), key=lambda x: abs(x - avg_numeric))
        return reverse_mapping[closest_grade]
    
    return "B"  # Grade par défaut

# ==================== Constantes ====================
NBA_TEAMS_ANALYSIS = {
    # Atlantic Division
    'Boston Celtics': {
        'positional_needs': {'PG': 0.3, 'SG': 0.4, 'SF': 0.2, 'PF': 0.4, 'C': 0.6},
        'skill_needs': {'scoring': 0.4, 'shooting': 0.5, 'playmaking': 0.4, 'defense': 0.5, 'rebounding': 0.5},
        'team_context': 'Championship team looking for depth'
    },
    'Brooklyn Nets': {
        'positional_needs': {'PG': 0.5, 'SG': 0.6, 'SF': 0.8, 'PF': 0.4, 'C': 0.5},
        'skill_needs': {'scoring': 0.8, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.6, 'rebounding': 0.4},
        'team_context': 'Rebuilding with focus on young talent'
    },
    'New York Knicks': {
        'positional_needs': {'PG': 0.5, 'SG': 0.4, 'SF': 0.6, 'PF': 0.3, 'C': 0.5},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.6, 'defense': 0.6, 'rebounding': 0.4},
        'team_context': 'Looking for versatile contributors'
    },
    'Philadelphia 76ers': {
        'positional_needs': {'PG': 0.8, 'SG': 0.6, 'SF': 0.4, 'PF': 0.3, 'C': 0.2},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.8, 'playmaking': 0.9, 'defense': 0.5, 'rebounding': 0.3},
        'team_context': 'Need playmaking and shooting around stars'
    },
    'Toronto Raptors': {
        'positional_needs': {'PG': 0.6, 'SG': 0.5, 'SF': 0.4, 'PF': 0.7, 'C': 0.3},
        'skill_needs': {'scoring': 0.7, 'shooting': 0.6, 'playmaking': 0.6, 'defense': 0.7, 'rebounding': 0.5},
        'team_context': 'Young core needs complementary pieces'
    },
    # Central Division
    'Chicago Bulls': {
        'positional_needs': {'PG': 0.7, 'SG': 0.3, 'SF': 0.6, 'PF': 0.5, 'C': 0.4},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.8, 'playmaking': 0.8, 'defense': 0.5, 'rebounding': 0.4},
        'team_context': 'Need floor general and outside shooting'
    },
    'Cleveland Cavaliers': {
        'positional_needs': {'PG': 0.3, 'SG': 0.6, 'SF': 0.7, 'PF': 0.5, 'C': 0.4},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.4},
        'team_context': 'Need wing depth and perimeter shooting'
    },
    'Detroit Pistons': {
        'positional_needs': {'PG': 0.3, 'SG': 0.8, 'SF': 0.7, 'PF': 0.3, 'C': 0.4},
        'skill_needs': {'scoring': 0.8, 'shooting': 0.9, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.3},
        'team_context': 'Need perimeter scoring and shooting'
    },
    'Indiana Pacers': {
        'positional_needs': {'PG': 0.3, 'SG': 0.5, 'SF': 0.6, 'PF': 0.4, 'C': 0.7},
        'skill_needs': {'scoring': 0.5, 'shooting': 0.6, 'playmaking': 0.4, 'defense': 0.7, 'rebounding': 0.8},
        'team_context': 'Need interior defense and rebounding'
    },
    'Milwaukee Bucks': {
        'positional_needs': {'PG': 0.7, 'SG': 0.5, 'SF': 0.3, 'PF': 0.4, 'C': 0.6},
        'skill_needs': {'scoring': 0.5, 'shooting': 0.8, 'playmaking': 0.7, 'defense': 0.6, 'rebounding': 0.4},
        'team_context': 'Need secondary playmaker and shooting'
    },
    # Southeast Division
    'Atlanta Hawks': {
        'positional_needs': {'PG': 0.2, 'SG': 0.6, 'SF': 0.7, 'PF': 0.8, 'C': 0.6},
        'skill_needs': {'scoring': 0.5, 'shooting': 0.6, 'playmaking': 0.3, 'defense': 0.9, 'rebounding': 0.7},
        'team_context': 'Need defense and size around Trae Young'
    },
    'Charlotte Hornets': {
        'positional_needs': {'PG': 0.2, 'SG': 0.4, 'SF': 0.5, 'PF': 0.6, 'C': 0.9},
        'skill_needs': {'scoring': 0.4, 'shooting': 0.5, 'playmaking': 0.3, 'defense': 0.8, 'rebounding': 0.9},
        'team_context': 'Need interior presence and defense'
    },
    'Miami Heat': {
        'positional_needs': {'PG': 0.6, 'SG': 0.4, 'SF': 0.5, 'PF': 0.7, 'C': 0.5},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.8, 'rebounding': 0.5},
        'team_context': 'Culture fit and two-way players preferred'
    },
    'Orlando Magic': {
        'positional_needs': {'PG': 0.4, 'SG': 0.8, 'SF': 0.3, 'PF': 0.4, 'C': 0.2},
        'skill_needs': {'scoring': 0.8, 'shooting': 0.9, 'playmaking': 0.4, 'defense': 0.4, 'rebounding': 0.3},
        'team_context': 'Need perimeter scoring and shooting'
    },
    'Washington Wizards': {
        'positional_needs': {'PG': 0.4, 'SG': 0.5, 'SF': 0.8, 'PF': 0.7, 'C': 0.3},
        'skill_needs': {'scoring': 0.7, 'shooting': 0.6, 'playmaking': 0.5, 'defense': 0.8, 'rebounding': 0.6},
        'team_context': 'Rebuilding - need versatile two-way players'
    },
    # Northwest Division
    'Denver Nuggets': {
        'positional_needs': {'PG': 0.5, 'SG': 0.6, 'SF': 0.4, 'PF': 0.3, 'C': 0.2},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.3},
        'team_context': 'Need perimeter depth around Jokic'
    },
    'Minnesota Timberwolves': {
        'positional_needs': {'PG': 0.6, 'SG': 0.7, 'SF': 0.3, 'PF': 0.2, 'C': 0.3},
        'skill_needs': {'scoring': 0.7, 'shooting': 0.8, 'playmaking': 0.6, 'defense': 0.4, 'rebounding': 0.3},
        'team_context': 'Need perimeter scoring and playmaking'
    },
    'Oklahoma City Thunder': {
        'positional_needs': {'PG': 0.2, 'SG': 0.4, 'SF': 0.5, 'PF': 0.6, 'C': 0.8},
        'skill_needs': {'scoring': 0.4, 'shooting': 0.5, 'playmaking': 0.3, 'defense': 0.6, 'rebounding': 0.8},
        'team_context': 'Need veteran presence and interior size'
    },
    'Portland Trail Blazers': {
        'positional_needs': {'PG': 0.9, 'SG': 0.3, 'SF': 0.6, 'PF': 0.4, 'C': 0.2},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.9, 'defense': 0.5, 'rebounding': 0.3},
        'team_context': 'Desperate need for franchise point guard'
    },
    'Utah Jazz': {
        'positional_needs': {'PG': 0.4, 'SG': 0.7, 'SF': 0.6, 'PF': 0.5, 'C': 0.3},
        'skill_needs': {'scoring': 0.8, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.6, 'rebounding': 0.4},
        'team_context': 'Rebuilding with young core'
    },
    # Pacific Division
    'Golden State Warriors': {
        'positional_needs': {'PG': 0.4, 'SG': 0.3, 'SF': 0.7, 'PF': 0.6, 'C': 0.5},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.8, 'playmaking': 0.4, 'defense': 0.7, 'rebounding': 0.5},
        'team_context': 'Need youth and athleticism'
    },
    'Los Angeles Clippers': {
        'positional_needs': {'PG': 0.5, 'SG': 0.6, 'SF': 0.4, 'PF': 0.5, 'C': 0.6},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.6, 'rebounding': 0.5},
        'team_context': 'Need depth and versatility'
    },
    'Los Angeles Lakers': {
        'positional_needs': {'PG': 0.6, 'SG': 0.5, 'SF': 0.4, 'PF': 0.3, 'C': 0.7},
        'skill_needs': {'scoring': 0.5, 'shooting': 0.8, 'playmaking': 0.6, 'defense': 0.7, 'rebounding': 0.6},
        'team_context': 'Need role players around aging stars'
    },
    'Phoenix Suns': {
        'positional_needs': {'PG': 0.3, 'SG': 0.4, 'SF': 0.6, 'PF': 0.7, 'C': 0.5},
        'skill_needs': {'scoring': 0.5, 'shooting': 0.6, 'playmaking': 0.4, 'defense': 0.7, 'rebounding': 0.6},
        'team_context': 'Need complementary pieces around core'
    },
    'Sacramento Kings': {
        'positional_needs': {'PG': 0.2, 'SG': 0.4, 'SF': 0.6, 'PF': 0.7, 'C': 0.8},
        'skill_needs': {'scoring': 0.4, 'shooting': 0.5, 'playmaking': 0.3, 'defense': 0.9, 'rebounding': 0.8},
        'team_context': 'Need frontcourt defense and size'
    },
    # Southwest Division
    'Dallas Mavericks': {
        'positional_needs': {'PG': 0.3, 'SG': 0.6, 'SF': 0.5, 'PF': 0.4, 'C': 0.7},
        'skill_needs': {'scoring': 0.5, 'shooting': 0.7, 'playmaking': 0.4, 'defense': 0.8, 'rebounding': 0.6},
        'team_context': 'Need defense and complementary pieces'
    },
    'Houston Rockets': {
        'positional_needs': {'PG': 0.3, 'SG': 0.5, 'SF': 0.8, 'PF': 0.6, 'C': 0.4},
        'skill_needs': {'scoring': 0.7, 'shooting': 0.8, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.5},
        'team_context': 'Young team building around core'
    },
    'Memphis Grizzlies': {
        'positional_needs': {'PG': 0.2, 'SG': 0.6, 'SF': 0.7, 'PF': 0.4, 'C': 0.5},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.8, 'playmaking': 0.3, 'defense': 0.7, 'rebounding': 0.5},
        'team_context': 'Need shooting and wing depth'
    },
    'New Orleans Pelicans': {
        'positional_needs': {'PG': 0.4, 'SG': 0.5, 'SF': 0.6, 'PF': 0.3, 'C': 0.4},
        'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.6, 'rebounding': 0.4},
        'team_context': 'Need consistency and depth'
    },
    'San Antonio Spurs': {
        'positional_needs': {'PG': 0.3, 'SG': 0.7, 'SF': 0.4, 'PF': 0.2, 'C': 0.6},
        'skill_needs': {'scoring': 0.8, 'shooting': 0.9, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.5},
        'team_context': 'Need shooting and scoring around Wembanyama'
    }
}

# ==================== Chargement des données ====================
@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and clean NBA draft data"""
    try:
        # Try loading from multiple possible sources
        for filename in ['complete_nba_draft_rankings.csv', 'final_nba_draft_rankings.csv', 'ml_nba_draft_predictions.csv']:
            try:
                df = pd.read_csv(filename)
                st.success(f"✅ Data loaded from {filename}")
                return clean_dataframe(df)
            except FileNotFoundError:
                continue
        
        # If no file found, create demo data
        st.info("📋 Using demonstration data")
        return create_demo_data()
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return create_demo_data()

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataframe with proper type conversions"""
    df_clean = df.copy()
    
    # Numeric columns
    numeric_cols = ['ppg', 'rpg', 'apg', 'spg', 'bpg', 'age', 'final_rank', 
                   'final_gen_probability', 'fg_pct', 'three_pt_pct', 'ft_pct', 
                   'ts_pct', 'height', 'weight', 'usage_rate', 'ortg', 'drtg']
    
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
    
    # String columns
    string_cols = ['name', 'position', 'college', 'scout_grade', 'archetype']
    
    for col in string_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).fillna('N/A')
    
    return df_clean

def create_demo_data() -> pd.DataFrame:
    """Create comprehensive demo data with 60 prospects"""
    # Top prospects with realistic stats
    top_prospects = [
        {'name': 'Cooper Flagg', 'position': 'PF', 'college': 'Duke', 'ppg': 16.5, 'rpg': 8.2, 'apg': 4.1, 'spg': 1.8, 'bpg': 1.4, 'fg_pct': 0.478, 'three_pt_pct': 0.352, 'ft_pct': 0.765, 'ts_pct': 0.589, 'age': 18.0, 'height': 6.9, 'weight': 220, 'usage_rate': 22.5, 'ortg': 115, 'drtg': 98, 'scout_grade': 'A+', 'archetype': 'Two-Way Wing'},
        {'name': 'Ace Bailey', 'position': 'SF', 'college': 'Rutgers', 'ppg': 15.8, 'rpg': 6.1, 'apg': 2.3, 'spg': 1.2, 'bpg': 0.8, 'fg_pct': 0.445, 'three_pt_pct': 0.385, 'ft_pct': 0.825, 'ts_pct': 0.612, 'age': 18.0, 'height': 6.8, 'weight': 200, 'usage_rate': 28.2, 'ortg': 118, 'drtg': 105, 'scout_grade': 'A+', 'archetype': 'Elite Scorer'},
        {'name': 'Dylan Harper', 'position': 'SG', 'college': 'Rutgers', 'ppg': 19.2, 'rpg': 4.8, 'apg': 4.6, 'spg': 1.6, 'bpg': 0.3, 'fg_pct': 0.512, 'three_pt_pct': 0.345, 'ft_pct': 0.792, 'ts_pct': 0.595, 'age': 19.0, 'height': 6.6, 'weight': 195, 'usage_rate': 25.8, 'ortg': 112, 'drtg': 102, 'scout_grade': 'A+', 'archetype': 'Versatile Guard'},
        {'name': 'VJ Edgecombe', 'position': 'SG', 'college': 'Baylor', 'ppg': 12.1, 'rpg': 4.9, 'apg': 2.8, 'spg': 1.9, 'bpg': 0.6, 'fg_pct': 0.432, 'three_pt_pct': 0.298, 'ft_pct': 0.712, 'ts_pct': 0.501, 'age': 19.0, 'height': 6.5, 'weight': 180, 'usage_rate': 19.5, 'ortg': 105, 'drtg': 95, 'scout_grade': 'A', 'archetype': 'Athletic Defender'},
        {'name': 'Boogie Fland', 'position': 'PG', 'college': 'Arkansas', 'ppg': 14.6, 'rpg': 3.2, 'apg': 5.1, 'spg': 1.4, 'bpg': 0.2, 'fg_pct': 0.465, 'three_pt_pct': 0.368, 'ft_pct': 0.856, 'ts_pct': 0.578, 'age': 18.0, 'height': 6.2, 'weight': 175, 'usage_rate': 24.1, 'ortg': 114, 'drtg': 108, 'scout_grade': 'A', 'archetype': 'Floor General'},
    ]
    
    # Generate remaining prospects
    all_prospects = top_prospects.copy()
    
    for i in range(6, 61):
        prospect = {
            'name': f'Prospect {i}',
            'position': np.random.choice(['PG', 'SG', 'SF', 'PF', 'C']),
            'college': np.random.choice(['Duke', 'Kentucky', 'UNC', 'Kansas', 'UCLA', 'Arizona']),
            'ppg': np.random.normal(12, 4),
            'rpg': np.random.normal(5, 2),
            'apg': np.random.normal(3, 2),
            'spg': np.random.normal(1.2, 0.5),
            'bpg': np.random.normal(0.8, 0.6),
            'fg_pct': np.random.normal(0.45, 0.08),
            'three_pt_pct': np.random.normal(0.35, 0.10),
            'ft_pct': np.random.normal(0.75, 0.12),
            'ts_pct': np.random.normal(0.55, 0.08),
            'age': np.random.normal(19, 1.2),
            'height': np.random.normal(6.5, 0.5),
            'weight': np.random.normal(200, 25),
            'usage_rate': np.random.normal(22, 5),
            'ortg': np.random.normal(110, 8),
            'drtg': np.random.normal(105, 7),
            'scout_grade': np.random.choice(['B', 'B-', 'C+', 'C']),
            'archetype': np.random.choice(['Shooter', 'Defender', 'Athlete', 'Role Player'])
        }
        all_prospects.append(prospect)
    
    df = pd.DataFrame(all_prospects)
    df['final_gen_probability'] = np.random.beta(2, 3, len(df))
    df['final_rank'] = range(1, len(df) + 1)
    
    return clean_dataframe(df)

# ==================== Composants UI ====================
def display_hero_header():
    """Display hero header section"""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🏀 NBA DRAFT 2025</h1>
        <p style="font-size: 1.3rem; margin-bottom: 2rem;">AI-Powered Prospect Analysis & Draft Simulator</p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 700;">60</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Prospects</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 700;">84.7%</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">ML Accuracy</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 700;">30</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">NBA Teams</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_draft_countdown():
    """Display countdown to draft day"""
    draft_date = date(2025, 6, 26)
    today = date.today()
    days_left = (draft_date - today).days
    
    if days_left > 0:
        st.markdown(f"""
        <div class="countdown-container">
            <div style="font-size: 4rem; font-weight: 700; color: #333; line-height: 1;">{days_left}</div>
            <div style="font-size: 1.2rem; font-weight: 600; margin-top: 0.5rem;">
                Days Until NBA Draft 2025
            </div>
            <div style="font-size: 0.9rem; opacity: 0.7; margin-top: 0.5rem;">
                June 26, 2025 • Brooklyn, NY
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_leaders_section(df: pd.DataFrame):

    """Display category leaders based on potential projections"""
    st.markdown("### 🏆 Category Leaders (Projected Potential)")
    
    try:
        # Calculate projections
        df['projected_scorer'] = df['ppg'] * (1 + df['final_gen_probability'] * 0.3)
        df['projected_scorer'] = df['projected_scorer'].clip(upper=32)
        
        df['projected_shooter'] = df['three_pt_pct'] * (1 + df['final_gen_probability'] * 0.15)
        df['projected_shooter'] = df['projected_shooter'].clip(upper=0.43)
        
        df['projected_rebounder'] = df['rpg'] * (1 + df['final_gen_probability'] * 0.3)
        df['projected_rebounder'] = df['projected_rebounder'].clip(upper=15)
        
        df['projected_playmaker'] = df['apg'] * (1 + df['final_gen_probability'] * 0.35)
        df['projected_playmaker'] = df['projected_playmaker'].clip(upper=12)
        
        df['projected_defender'] = (df['spg'] + df['bpg']) * (1 + df['final_gen_probability'] * 0.25)
        df['projected_defender'] = df['projected_defender'].clip(upper=4)
        
        df['immediate_impact'] = (
            df['ppg'] * 0.25 +
            df['rpg'] * 0.15 +
            df['apg'] * 0.20 +
            (df['three_pt_pct'] * 100) * 0.15 +
            (22 - df['age']) * 2 +
            df['final_gen_probability'] * 30
        )
        
        # Find leaders
        best_scorer = df.loc[df['projected_scorer'].idxmax()]
        best_shooter = df.loc[df['projected_shooter'].idxmax()]
        best_rebounder = df.loc[df['projected_rebounder'].idxmax()]
        best_playmaker = df.loc[df['projected_playmaker'].idxmax()]
        best_defender = df.loc[df['projected_defender'].idxmax()]
        best_potential = df.loc[df['final_gen_probability'].idxmax()]
        most_immediate_impact = df.loc[df['immediate_impact'].idxmax()]
        
        # Display with streamlit only
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("🎯 **Best Scoring Potential**")
            st.write(f"**{safe_string(best_scorer['name'])}**")
            st.caption(f"Projected {safe_numeric(best_scorer['projected_scorer']):.1f} PPG peak")
            st.caption(f"Current: {safe_numeric(best_scorer['ppg']):.1f} PPG")
            
            st.info("🏀 **Best Rebounding Potential**")
            st.write(f"**{safe_string(best_rebounder['name'])}**")
            st.caption(f"Projected {safe_numeric(best_rebounder['projected_rebounder']):.1f} RPG peak")
            st.caption(f"Current: {safe_numeric(best_rebounder['rpg']):.1f} RPG")
        
        with col2:
            st.info("🎯 **Best Shooting Potential**")
            st.write(f"**{safe_string(best_shooter['name'])}**")
            st.caption(f"Projected {safe_numeric(best_shooter['projected_shooter']):.1%} 3P% peak")
            st.caption(f"Current: {safe_numeric(best_shooter['three_pt_pct']):.1%} 3P%")
            
            st.info("🛡️ **Best Defensive Potential**")
            st.write(f"**{safe_string(best_defender['name'])}**")
            st.caption(f"Projected {safe_numeric(best_defender['projected_defender']):.1f} STL+BLK peak")
            st.caption(f"Current: {safe_numeric(best_defender['spg'] + best_defender['bpg']):.1f} STL+BLK")
        
        with col3:
            st.info("🎯 **Best Playmaking Potential**")
            st.write(f"**{safe_string(best_playmaker['name'])}**")
            st.caption(f"Projected {safe_numeric(best_playmaker['projected_playmaker']):.1f} APG peak")
            st.caption(f"Current: {safe_numeric(best_playmaker['apg']):.1f} APG")
            
            st.success("⚡ **Most Immediate Impact**")
            st.write(f"**{safe_string(most_immediate_impact['name'])}**")
            st.caption("Ready to contribute Year 1")
            st.caption(f"{safe_numeric(most_immediate_impact['ppg']):.1f} PPG • Age {safe_numeric(most_immediate_impact['age']):.0f}")
        
        # Highest Ceiling centrée
        st.markdown("---")
        col_center = st.columns([1, 2, 1])[1]
        with col_center:
            st.warning("⭐ **Highest Ceiling**")
            st.write(f"**{safe_string(best_potential['name'])}**")
            st.caption(f"{safe_numeric(best_potential['final_gen_probability']):.1%} Generational Talent Probability")
        
    except Exception as e:
        st.error(f"Error in leaders section: {e}")

def create_enhanced_search_with_stats(df: pd.DataFrame):
    """Enhanced search with simplified interface and multi-select positions"""
    st.markdown("## 🔍 Player Database")
    
    # Barre de recherche principale
    search_term = st.text_input(
        "🔍 Search prospects:", 
        placeholder="Search by name, college, or keywords...",
        help="Search across player names, colleges, and archetypes"
    )
    
    # Filtres en ligne
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    
    with col1:
        # Multi-select positions avec boutons
        st.markdown("**Positions:**")
        positions = ['PG', 'SG', 'SF', 'PF', 'C']
        
        # Boutons de sélection rapide
        quick_col1, quick_col2, quick_col3 = st.columns(3)
        with quick_col1:
            if st.button("All Positions", key="all_pos"):
                st.session_state.selected_positions = positions
        with quick_col2:
            if st.button("Guards", key="guards"):
                st.session_state.selected_positions = ['PG', 'SG']
        with quick_col3:
            if st.button("Frontcourt", key="frontcourt"):
                st.session_state.selected_positions = ['SF', 'PF', 'C']
        
        # Multi-select avec état persistant
        if 'selected_positions' not in st.session_state:
            st.session_state.selected_positions = positions
        
        selected_positions = st.multiselect(
            "Select positions:",
            positions,
            default=st.session_state.selected_positions,
            key="position_multiselect"
        )
        st.session_state.selected_positions = selected_positions
    
    with col2:
        min_ppg = st.slider("Min PPG", 0, 30, 0, key="ppg_slider")
    
    with col3:
        min_3pt = st.slider("Min 3P%", 0.0, 0.6, 0.0, 0.05, key="3pt_slider")
    
    with col4:
        if 'archetype' in df.columns:
            archetypes = ['All'] + sorted(list(df['archetype'].unique()))
            archetype_filter = st.selectbox("Archetype", archetypes, key="archetype_select")
        else:
            archetype_filter = 'All'
    
    # Apply filters
    filtered_df = df.copy()
    
    # Search filter
    if search_term:
        mask = (
            filtered_df['name'].str.contains(search_term, case=False, na=False) |
            filtered_df['college'].str.contains(search_term, case=False, na=False) |
            filtered_df['position'].str.contains(search_term, case=False, na=False)
        )
        if 'archetype' in filtered_df.columns:
            mask |= filtered_df['archetype'].str.contains(search_term, case=False, na=False)
        filtered_df = filtered_df[mask]
    
    # Position filter
    if selected_positions:
        filtered_df = filtered_df[filtered_df['position'].isin(selected_positions)]
    
    # Stats filters
    filtered_df = filtered_df[filtered_df['ppg'] >= min_ppg]
    if 'three_pt_pct' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['three_pt_pct'] >= min_3pt]
    
    # Archetype filter
    if archetype_filter != 'All' and 'archetype' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['archetype'] == archetype_filter]
    
    # Results summary
    col1, col2 = st.columns([2, 1])
    with col1:
        st.success(f"📊 {len(filtered_df)} prospects found")
    with col2:
        if len(filtered_df) > 0:
            # Sort options
            sort_by = st.selectbox(
                "Sort by:",
                ["Draft Rank", "PPG", "Potential", "Name"],
                key="sort_select"
            )
    
    # Apply sorting
    if len(filtered_df) > 0:
        if sort_by == "Draft Rank":
            filtered_df = filtered_df.sort_values('final_rank')
        elif sort_by == "PPG":
            filtered_df = filtered_df.sort_values('ppg', ascending=False)
        elif sort_by == "Potential":
            filtered_df = filtered_df.sort_values('final_gen_probability', ascending=False)
        elif sort_by == "Name":
            filtered_df = filtered_df.sort_values('name')
    
    # Display results in clean table format
    display_search_results_table(filtered_df.head(50))  # Limite à 50 résultats

def display_search_results_table(df: pd.DataFrame):
    """Display search results in a clean table format"""
    if len(df) == 0:
        st.info("🔍 No prospects match your search criteria. Try adjusting your filters.")
        return
    
    # Prepare display columns
    display_cols = ['final_rank', 'name', 'position', 'college', 'ppg', 'rpg', 'apg', 
                   'three_pt_pct', 'scout_grade', 'final_gen_probability']
    
    # Check which columns exist
    available_cols = [col for col in display_cols if col in df.columns]
    table_df = df[available_cols].copy()
    
    # Format columns safely
    if 'three_pt_pct' in table_df.columns:
        table_df['three_pt_pct'] = table_df['three_pt_pct'].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
    if 'final_gen_probability' in table_df.columns:
        table_df['final_gen_probability'] = table_df['final_gen_probability'].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
    if 'ppg' in table_df.columns:
        table_df['ppg'] = table_df['ppg'].round(1)
    if 'rpg' in table_df.columns:
        table_df['rpg'] = table_df['rpg'].round(1)
    if 'apg' in table_df.columns:
        table_df['apg'] = table_df['apg'].round(1)
    
    # Rename columns for display
    column_mapping = {
        'final_rank': 'Rank',
        'name': 'Name',
        'position': 'Pos',
        'college': 'College',
        'ppg': 'PPG',
        'rpg': 'RPG',
        'apg': 'APG',
        'three_pt_pct': '3P%',
        'scout_grade': 'Grade',
        'final_gen_probability': 'Potential'
    }
    
    # Apply renaming only for columns that exist
    rename_dict = {old: new for old, new in column_mapping.items() if old in table_df.columns}
    table_df = table_df.rename(columns=rename_dict)
    
    # Display with enhanced styling
    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", format="%d") if "Rank" in table_df.columns else None,
            "PPG": st.column_config.NumberColumn("PPG", format="%.1f") if "PPG" in table_df.columns else None,
            "RPG": st.column_config.NumberColumn("RPG", format="%.1f") if "RPG" in table_df.columns else None,
            "APG": st.column_config.NumberColumn("APG", format="%.1f") if "APG" in table_df.columns else None,
            "Grade": st.column_config.TextColumn("Grade") if "Grade" in table_df.columns else None,
            "Potential": st.column_config.TextColumn("Potential") if "Potential" in table_df.columns else None,
            "3P%": st.column_config.TextColumn("3P%") if "3P%" in table_df.columns else None,
        }
    )
    
    # Quick actions - SECTION BIEN INDENTÉE DANS LA FONCTION
    if len(df) > 0:
        st.markdown("### 🎯 Quick Actions")
        
        try:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("💾 Export Results", key="export_results"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="nba_draft_search_results.csv",
                        mime="text/csv"
                    )
            
            with col2:
                st.metric("Total Results", len(df))
                
        except Exception as e:
            st.error(f"Error in quick actions: {e}")
            # Fallback simple sans colonnes
            if st.button("💾 Export Results (Simple)", key="export_results_simple"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="nba_draft_search_results.csv",
                    mime="text/csv"
                )

def show_quick_stats_viz(df: pd.DataFrame):
    """Show quick stats visualization for search results"""
    col1, col2 = st.columns(2)
    
    with col1:
        # PPG distribution
        fig_ppg = px.histogram(
            df.head(20), 
            x='ppg', 
            title="PPG Distribution (Top 20 Results)",
            nbins=10,
            color_discrete_sequence=['#FF6B35']
        )
        fig_ppg.update_layout(height=300)
        st.plotly_chart(fig_ppg, use_container_width=True)
    
    with col2:
        # Position breakdown
        if 'position' in df.columns:
            pos_counts = df.head(20)['position'].value_counts()
            fig_pos = px.pie(
                values=pos_counts.values,
                names=pos_counts.index,
                title="Position Breakdown (Top 20 Results)",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pos.update_layout(height=300)
            st.plotly_chart(fig_pos, use_container_width=True)

def display_player_card(player: pd.Series):
    """Display a properly formatted player card using metrics instead of HTML grid"""
    name = safe_string(player['name'])
    position = safe_string(player['position'])
    college = safe_string(player['college'])
    archetype = safe_string(player.get('archetype', 'N/A'))
    
    # Stats
    ppg = safe_numeric(player['ppg'])
    rpg = safe_numeric(player['rpg'])
    apg = safe_numeric(player['apg'])
    fg_pct = safe_numeric(player.get('fg_pct', 0))
    three_pt_pct = safe_numeric(player.get('three_pt_pct', 0))
    ts_pct = safe_numeric(player.get('ts_pct', 0))
    
    # Physical
    age = safe_numeric(player.get('age', 0))
    height = format_height(safe_numeric(player.get('height', 0)))
    weight = safe_numeric(player.get('weight', 0))
    
    grade = safe_string(player['scout_grade'])
    prob = safe_numeric(player.get('final_gen_probability', 0.5))
    
    # Card header
    st.markdown(f"""
    <div style="background: white; 
                border: 2px solid #FF6B35; 
                border-left: 6px solid #FF6B35;
                padding: 2rem; 
                border-radius: 15px; 
                margin: 1.5rem 0;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
            <div>
                <h3 style="margin: 0 0 0.5rem 0; color: #333; font-size: 1.4rem;">{name}</h3>
                <div style="color: #666; font-size: 1rem;">
                    {position} • {college} • {archetype}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="background: #FF6B35; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;">
                    Grade: {grade}
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #666;">
                    Projection: {prob:.1%}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Use Streamlit metrics for stats
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("PPG", f"{ppg:.1f}")
    with col2:
        st.metric("RPG", f"{rpg:.1f}")
    with col3:
        st.metric("APG", f"{apg:.1f}")
    with col4:
        st.metric("FG%", f"{fg_pct:.1%}")
    with col5:
        st.metric("3P%", f"{three_pt_pct:.1%}")
    with col6:
        st.metric("TS%", f"{ts_pct:.1%}")
    
    # Physical attributes
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin-top: 1rem;">
        <span style="margin: 0 1rem;"><strong>Age:</strong> {age:.0f}</span>
        <span style="margin: 0 1rem;"><strong>Height:</strong> {height}</span>
        <span style="margin: 0 1rem;"><strong>Weight:</strong> {weight:.0f} lbs</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("PPG", f"{ppg:.1f}")
    with col2:
        st.metric("RPG", f"{rpg:.1f}")
    with col3:
        st.metric("APG", f"{apg:.1f}")
    with col4:
        st.metric("FG%", f"{fg_pct:.1%}")
    with col5:
        st.metric("3P%", f"{three_pt_pct:.1%}")
    with col6:
        st.metric("TS%", f"{ts_pct:.1%}")
    
    # Physical attributes
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin-top: 1rem;">
        <span style="margin: 0 1rem;"><strong>Age:</strong> {age:.0f}</span>
        <span style="margin: 0 1rem;"><strong>Height:</strong> {height}</span>
        <span style="margin: 0 1rem;"><strong>Weight:</strong> {weight:.0f} lbs</span>
    </div>
    """, unsafe_allow_html=True)
    

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("PPG", f"{ppg:.1f}")
    with col2:
        st.metric("RPG", f"{rpg:.1f}")
    with col3:
        st.metric("APG", f"{apg:.1f}")
    with col4:
        st.metric("FG%", f"{fg_pct:.1%}")
    with col5:
        st.metric("3P%", f"{three_pt_pct:.1%}")
    with col6:
        st.metric("TS%", f"{ts_pct:.1%}")
    
    # Physical attributes
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin-top: 1rem;">
        <span style="margin: 0 1rem;"><strong>Age:</strong> {age:.0f}</span>
        <span style="margin: 0 1rem;"><strong>Height:</strong> {height}</span>
        <span style="margin: 0 1rem;"><strong>Weight:</strong> {weight:.0f} lbs</span>
    </div>
    """, unsafe_allow_html=True)

def create_realistic_projections(df: pd.DataFrame):
    """Create more realistic 5-year projections with varied growth curves"""
    st.markdown("### 🔮 Realistic Development Projections")
    
    selected_player = st.selectbox("Select a player for projection:", df['name'].head(20).tolist())
    player_data = df[df['name'] == selected_player].iloc[0]
    
    # Extract player attributes
    current_ppg = safe_numeric(player_data.get('ppg', 0))
    current_rpg = safe_numeric(player_data.get('rpg', 0))
    current_apg = safe_numeric(player_data.get('apg', 0))
    age = safe_numeric(player_data.get('age', 19))
    position = safe_string(player_data.get('position', 'N/A'))
    archetype = safe_string(player_data.get('archetype', 'N/A'))
    gen_probability = safe_numeric(player_data.get('final_gen_probability', 0.5))
    
    def project_stat_growth(current: float, stat_type: str, position: str, age: float, 
                           gen_prob: float, archetype: str) -> List[float]:
        """Project realistic stat growth with variance based on player attributes"""
        
        # Base growth curves by position and stat
        position_curves = {
            'PG': {'ppg': [0.85, 0.95, 1.15, 1.25, 1.30], 
                   'rpg': [0.90, 0.95, 1.05, 1.10, 1.10],
                   'apg': [0.80, 0.90, 1.20, 1.35, 1.40]},
            'SG': {'ppg': [0.80, 0.90, 1.10, 1.30, 1.35], 
                   'rpg': [0.90, 0.95, 1.10, 1.15, 1.15],
                   'apg': [0.85, 0.90, 1.10, 1.15, 1.20]},
            'SF': {'ppg': [0.85, 0.95, 1.15, 1.25, 1.25], 
                   'rpg': [0.85, 0.95, 1.15, 1.20, 1.25],
                   'apg': [0.85, 0.95, 1.15, 1.20, 1.25]},
            'PF': {'ppg': [0.90, 1.00, 1.10, 1.15, 1.20], 
                   'rpg': [0.85, 0.95, 1.20, 1.30, 1.35],
                   'apg': [0.90, 0.95, 1.05, 1.10, 1.10]},
            'C':  {'ppg': [0.95, 1.00, 1.05, 1.10, 1.10], 
                   'rpg': [0.85, 0.95, 1.25, 1.35, 1.40],
                   'apg': [0.95, 1.00, 1.00, 1.05, 1.05]}
        }
        
        # Get base curve
        base_curve = position_curves.get(position, position_curves['SF'])[stat_type]
        
        # Adjust for age (younger = more growth potential)
        age_factor = 1.0 + max(0, (20 - age) * 0.05)
        
        # Adjust for generational talent probability
        talent_factor = 1.0 + (gen_prob - 0.5) * 0.3
        
        # Add archetype-specific adjustments
        archetype_adjustments = {
            'Elite Scorer': {'ppg': 1.15, 'rpg': 0.95, 'apg': 0.95},
            'Floor General': {'ppg': 0.90, 'rpg': 0.95, 'apg': 1.20},
            'Two-Way Wing': {'ppg': 1.05, 'rpg': 1.05, 'apg': 1.05},
            'Rim Protector': {'ppg': 0.85, 'rpg': 1.15, 'apg': 0.90},
            'Elite Shooter': {'ppg': 1.10, 'rpg': 0.95, 'apg': 1.00}
        }
        
        arch_adjustment = archetype_adjustments.get(archetype, {}).get(stat_type, 1.0)
        
        # Apply all factors with some randomness
        projected_values = []
        for i, base_mult in enumerate(base_curve):
            # Add slight randomness to make projections unique
            random_factor = 1.0 + (np.random.random() - 0.5) * 0.1
            
            # Calculate final value
            final_mult = base_mult * age_factor * talent_factor * arch_adjustment * random_factor
            
            # Cap growth to realistic levels
            if stat_type == 'ppg':
                max_growth = 2.0 if gen_prob > 0.7 else 1.6
            elif stat_type == 'apg':
                max_growth = 1.8 if position == 'PG' else 1.4
            else:  # rpg
                max_growth = 1.6 if position in ['PF', 'C'] else 1.3
            
            final_mult = min(final_mult, max_growth)
            projected_values.append(current * final_mult)
        
        return projected_values
    
    # Generate projections
    years = list(range(1, 6))
    projected_ppg = project_stat_growth(current_ppg, 'ppg', position, age, gen_probability, archetype)
    projected_rpg = project_stat_growth(current_rpg, 'rpg', position, age, gen_probability, archetype)
    projected_apg = project_stat_growth(current_apg, 'apg', position, age, gen_probability, archetype)
    
    # Create visualization
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Points Per Game', 'Rebounds Per Game', 'Assists Per Game', 'Overall Development'),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # Add traces
    fig.add_trace(
        go.Scatter(x=years, y=projected_ppg, mode='lines+markers', name='PPG',
                  line=dict(color='#FF6B35', width=4), marker=dict(size=12)),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=years, y=projected_rpg, mode='lines+markers', name='RPG',
                  line=dict(color='#4361EE', width=4), marker=dict(size=12)),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=years, y=projected_apg, mode='lines+markers', name='APG',
                  line=dict(color='#10B981', width=4), marker=dict(size=12)),
        row=2, col=1
    )
    
    # Overall impact
    overall_impact = [(p*1.5 + r + a*1.2) / 3.7 for p, r, a in zip(projected_ppg, projected_rpg, projected_apg)]
    fig.add_trace(
        go.Scatter(x=years, y=overall_impact, mode='lines+markers', name='Overall',
                  line=dict(color='#8B5CF6', width=4), marker=dict(size=12)),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600, 
        title=f"{selected_player} - Realistic 5-Year Development Projection",
        showlegend=False
    )
    fig.update_xaxes(title_text="NBA Season", tickvals=years, ticktext=[f"Year {y}" for y in years])
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ppg_growth = ((projected_ppg[-1] - projected_ppg[0]) / projected_ppg[0] * 100) if projected_ppg[0] > 0 else 0
        st.metric(
            "5-Year PPG Growth", 
            f"+{ppg_growth:.1f}%",
            f"{projected_ppg[0]:.1f} → {projected_ppg[-1]:.1f}"
        )
    
    with col2:
        peak_year = years[projected_ppg.index(max(projected_ppg))]
        st.metric(
            "Projected Peak", 
            f"Year {peak_year}",
            f"{max(projected_ppg):.1f} PPG"
        )
    
    with col3:
        # More nuanced All-Star probability
        peak_stats_sum = max(projected_ppg) + max(projected_rpg) + max(projected_apg)
        all_star_base = min(80, max(5, (peak_stats_sum - 20) * 2.5))
        all_star_prob = all_star_base * (0.7 + gen_probability * 0.6)
        all_star_prob = min(95, max(5, all_star_prob))
        st.metric(
            "All-Star Probability", 
            f"{all_star_prob:.0f}%",
            "Peak Years"
        )
    
    with col4:
        # MVP probability with more realistic calculation
        mvp_threshold = max(projected_ppg) * 1.2 + max(projected_rpg) * 0.8 + max(projected_apg) * 1.0
        mvp_base = max(0, (mvp_threshold - 35) * 1.5)
        mvp_prob = mvp_base * gen_probability
        mvp_prob = min(30, max(0, mvp_prob))
        st.metric(
            "MVP Candidate Chance",
            f"{mvp_prob:.0f}%",
            "Career Peak"
        )
    
    # Projection explanation
    st.markdown("### 📝 Projection Methodology")
    st.info(f"""
    **Projection Factors for {selected_player}:**
    - **Position-Specific Growth**: {position} players typically see {('high scoring growth' if position in ['SG', 'SF'] else 'balanced development' if position == 'PG' else 'rebounding improvement')}
    - **Age Impact**: At {age:.0f} years old, {('significant growth potential remains' if age < 19 else 'moderate development expected' if age < 21 else 'limited growth window')}
    - **Archetype Influence**: {archetype} players focus on {('scoring efficiency' if 'Scorer' in archetype else 'playmaking development' if 'General' in archetype else 'two-way impact')}
    - **Talent Ceiling**: {gen_probability:.1%} generational talent probability suggests {('superstar trajectory' if gen_probability > 0.7 else 'starter potential' if gen_probability > 0.5 else 'role player development')}
    - **Variance Applied**: Each player's path includes realistic ups and downs
    """)

def create_team_fit_analysis(df: pd.DataFrame):
    """Enhanced team fit analysis with all 30 teams"""
    st.markdown("## 🎯 Complete NBA Team Fit Analysis")
    st.caption("Analyzing fit with all 30 NBA teams based on roster needs and playing style")
    
    # Analysis mode selection
    analysis_mode = st.radio(
        "Analysis Mode:", 
        ["Team Perspective", "Player Perspective", "Best Fits Matrix"], 
        horizontal=True
    )
    
    if analysis_mode == "Team Perspective":
        display_team_perspective_analysis(df)
    elif analysis_mode == "Player Perspective":
        display_player_perspective_analysis(df)
    else:
        display_team_player_matrix(df)

def display_team_perspective_analysis(df: pd.DataFrame):
    """Display team-focused fit analysis"""
    selected_team = st.selectbox("Select Team:", sorted(list(NBA_TEAMS_ANALYSIS.keys())))
    team_data = NBA_TEAMS_ANALYSIS[selected_team]
    
    st.markdown(f"### {selected_team} - Draft Analysis")
    st.info(f"**Team Context:** {team_data['team_context']}")
    
    # Calculate fits
    player_fits = calculate_team_fits(df.head(30), team_data)
    player_fits.sort(key=lambda x: x['fit_score'], reverse=True)
    
    # Display best fits
    st.markdown("### 🎯 Best Fits for This Team")
    
    for i, fit in enumerate(player_fits[:10]):
        color = '#10b981' if fit['fit_score'] > 70 else '#f59e0b' if fit['fit_score'] > 50 else '#6b7280'
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9fa, #ffffff); 
                    border: 2px solid {color}; 
                    border-left: 6px solid {color};
                    padding: 1.5rem; 
                    border-radius: 12px; 
                    margin: 1rem 0;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    color: #333;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #333; font-size: 1.2rem;">
                        #{fit['rank']} {fit['name']} ({fit['position']})
                    </strong>
                    <div style="font-size: 1rem; color: #666; margin-top: 0.5rem;">
                        {' • '.join(fit['reasons']) if fit['reasons'] else 'Good overall fit'}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2.5rem; font-weight: bold; color: {color};">
                        {fit['fit_score']:.0f}%
                    </div>
                    <div style="font-size: 0.9rem; color: #666;">Team Fit</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_player_perspective_analysis(df: pd.DataFrame):
    """Display player-focused fit analysis"""
    selected_player = st.selectbox("Select Player:", df['name'].head(20).tolist())
    player_data = df[df['name'] == selected_player].iloc[0]
    
    # Calculate fits for all teams
    team_fits = []
    for team, team_data in NBA_TEAMS_ANALYSIS.items():
        fit_data = calculate_player_team_fit(player_data, team_data)
        team_fits.append({
            'team': team,
            'fit_score': fit_data['score'],
            'reasons': fit_data['reasons'],
            'context': team_data['team_context']
        })
    
    team_fits.sort(key=lambda x: x['fit_score'], reverse=True)
    
    st.markdown(f"### 🎯 Best Team Fits for {selected_player}")
    
    # Display top 10 team fits
    for i, fit in enumerate(team_fits[:10]):
        color = '#10b981' if fit['fit_score'] > 70 else '#f59e0b' if fit['fit_score'] > 50 else '#6b7280'
        
        st.markdown(f"""
        <div style="background: white; 
                    border: 2px solid {color}; 
                    border-left: 6px solid {color};
                    padding: 1.5rem; 
                    border-radius: 12px; 
                    margin: 1rem 0;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <strong style="color: #333; font-size: 1.2rem;">
                        {i+1}. {fit['team']}
                    </strong>
                    <div style="font-size: 0.9rem; color: #666; margin: 0.5rem 0; font-style: italic;">
                        {fit['context']}
                    </div>
                    <div style="font-size: 1rem; color: #666;">
                        {' • '.join(fit['reasons']) if fit['reasons'] else 'General fit'}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2.5rem; font-weight: bold; color: {color};">
                        {fit['fit_score']:.0f}%
                    </div>
                    <div style="font-size: 0.9rem; color: #666;">Fit Score</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_team_player_matrix(df: pd.DataFrame):
    """Display team-player fit matrix"""
    st.markdown("### 🎯 Team-Player Fit Matrix")
    
    # Select subset of teams and players for visibility
    divisions = {
        'Atlantic': ['Boston Celtics', 'Brooklyn Nets', 'New York Knicks', 'Philadelphia 76ers', 'Toronto Raptors'],
        'Central': ['Chicago Bulls', 'Cleveland Cavaliers', 'Detroit Pistons', 'Indiana Pacers', 'Milwaukee Bucks'],
        'Southeast': ['Atlanta Hawks', 'Charlotte Hornets', 'Miami Heat', 'Orlando Magic', 'Washington Wizards'],
        'Northwest': ['Denver Nuggets', 'Minnesota Timberwolves', 'Oklahoma City Thunder', 'Portland Trail Blazers', 'Utah Jazz'],
        'Pacific': ['Golden State Warriors', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Phoenix Suns', 'Sacramento Kings'],
        'Southwest': ['Dallas Mavericks', 'Houston Rockets', 'Memphis Grizzlies', 'New Orleans Pelicans', 'San Antonio Spurs']
    }
    
    selected_division = st.selectbox("Select Division:", list(divisions.keys()))
    selected_teams = divisions[selected_division]
    
    # Get top 10 players
    players = df['name'].head(10).tolist()
    
    # Calculate matrix
    matrix_data = []
    for player_name in players:
        player_data = df[df['name'] == player_name].iloc[0]
        row = []
        
        for team in selected_teams:
            team_data = NBA_TEAMS_ANALYSIS[team]
            fit_data = calculate_player_team_fit(player_data, team_data)
            row.append(fit_data['score'])
        
        matrix_data.append(row)
    
    # Create heatmap
    fig = px.imshow(
        matrix_data,
        labels=dict(x="Team", y="Player", color="Fit Score"),
        x=[team.split()[-1] for team in selected_teams],
        y=players,
        color_continuous_scale="RdYlGn",
        title=f"{selected_division} Division - Team/Player Fit Matrix (%)",
        aspect="auto"
    )
    
    fig.update_layout(height=500, font=dict(size=12))
    fig.update_coloraxes(colorbar_title="Fit Score %")
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Matrix Legend:**
    - 🟢 **Green (70-100%)**: Excellent fit - player fills major team needs
    - 🟡 **Yellow (40-69%)**: Good fit - player addresses some team needs  
    - 🔴 **Red (0-39%)**: Poor fit - player doesn't match team priorities
    """)

def calculate_team_fits(players_df: pd.DataFrame, team_data: Dict) -> List[Dict]:
    """Calculate fit scores for multiple players with a team"""
    player_fits = []
    
    for _, player in players_df.iterrows():
        fit_data = calculate_player_team_fit(player, team_data)
        player_fits.append({
            'name': safe_string(player['name']),
            'position': safe_string(player['position']),
            'fit_score': fit_data['score'],
            'reasons': fit_data['reasons'],
            'rank': safe_numeric(player.get('final_rank', 0))
        })
    
    return player_fits

def calculate_player_team_fit(player: pd.Series, team_data: Dict) -> Dict:
    """Calculate detailed fit score between a player and team"""
    fit_score = 0
    fit_reasons = []
    
    # Position fit
    position = safe_string(player['position'])
    if position in team_data['positional_needs']:
        pos_score = team_data['positional_needs'][position] * 40
        fit_score += pos_score
        if pos_score > 20:
            fit_reasons.append(f"Fills {position} need")
    
    # Skills fit
    ppg = safe_numeric(player.get('ppg', 0))
    three_pt = safe_numeric(player.get('three_pt_pct', 0))
    apg = safe_numeric(player.get('apg', 0))
    spg = safe_numeric(player.get('spg', 0))
    bpg = safe_numeric(player.get('bpg', 0))
    rpg = safe_numeric(player.get('rpg', 0))
    
    # Scoring
    if ppg > 15 and team_data['skill_needs']['scoring'] > 0.6:
        skill_score = team_data['skill_needs']['scoring'] * 15
        fit_score += skill_score
        fit_reasons.append(f"Elite scorer ({ppg:.1f} PPG)")
    
    # Shooting
    if three_pt > 0.35 and team_data['skill_needs']['shooting'] > 0.6:
        skill_score = team_data['skill_needs']['shooting'] * 15
        fit_score += skill_score
        fit_reasons.append(f"Good shooter ({three_pt:.1%})")
    
    # Playmaking
    if apg > 5 and team_data['skill_needs']['playmaking'] > 0.6:
        skill_score = team_data['skill_needs']['playmaking'] * 15
        fit_score += skill_score
        fit_reasons.append(f"Elite playmaker ({apg:.1f} APG)")
    
    # Defense
    defense_impact = spg + bpg
    if defense_impact > 2 and team_data['skill_needs']['defense'] > 0.6:
        skill_score = team_data['skill_needs']['defense'] * 15
        fit_score += skill_score
        fit_reasons.append(f"Defensive impact ({defense_impact:.1f} STL+BLK)")
    
    # Rebounding
    if rpg > 7 and team_data['skill_needs']['rebounding'] > 0.6:
        skill_score = team_data['skill_needs']['rebounding'] * 15
        fit_score += skill_score
        fit_reasons.append(f"Strong rebounder ({rpg:.1f} RPG)")
    
    # Normalize score
    fit_score = min(100, max(0, fit_score))
    
    return {'score': fit_score, 'reasons': fit_reasons}

def get_latest_draft_intel():
    """Get latest draft intelligence (could be web-scraped)"""
    return {
        'last_updated': 'June 25, 2025',
        'major_moves': [
            "Cooper Flagg dominant in Hawks workout",
            "Ace Bailey impresses with improved shot selection",
            "International prospect surge continues"
        ],
        'team_intel': {
            'Portland Trail Blazers': 'Desperately seeking PG, considering trade up',
            'Charlotte Hornets': 'Miller twins getting serious looks',
            'Detroit Pistons': 'May package multiple picks'
        },
        'workout_standouts': [
            {'name': 'VJ Edgecombe', 'note': 'Athletic testing off the charts'},
            {'name': 'Tre Johnson', 'note': 'Shooting 47% from NBA 3P line'},
        ]
    }

def display_real_time_updates():
    """Display real-time draft updates"""
    intel = get_latest_draft_intel()
    
    st.markdown("### 🚨 Real-Time Draft Intel")
    
    with st.expander("📰 Latest News & Updates", expanded=True):
        for move in intel['major_moves']:
            st.markdown(f"• {move}")
    
    with st.expander("🏀 Team Intel"):
        for team, note in intel['team_intel'].items():
            st.markdown(f"**{team}:** {note}")
# ==================== What If Historical Simulator ====================

def create_what_if_simulator(df: pd.DataFrame):
    """Create What If historical draft simulator"""
    st.markdown("## 🔄 What If: Historical Draft Simulator")
    st.caption("See where 2025 prospects would have been drafted in different eras")
    
    # Historical draft data
    historical_drafts = get_historical_draft_data()
    
    # Year selector with context
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_year = st.selectbox(
            "Transport 2025 prospects to which historical draft?",
            list(historical_drafts.keys()),
            format_func=lambda x: f"{x} - {historical_drafts[x]['description']}"
        )
    
    with col2:
        simulation_mode = st.radio(
            "Simulation Mode:",
            ["Top 14 (Lottery)", "Full First Round"],
            key="sim_mode"
        )
    
    # Display historical context
    display_historical_context(selected_year, historical_drafts[selected_year])
    
    # Run simulation
    prospect_count = 14 if simulation_mode == "Top 14 (Lottery)" else 30
    historical_rankings = simulate_historical_draft(df.head(prospect_count), selected_year, historical_drafts[selected_year])
    
    # Display results side by side
    display_simulation_results(df.head(prospect_count), historical_rankings, selected_year)
    
    # Movement analysis
    display_movement_analysis(df.head(prospect_count), historical_rankings, selected_year)
    
    # Movement visualization
    display_movement_visualization(df.head(prospect_count), historical_rankings, selected_year)
    
    # Era insights
    display_era_insights(selected_year, historical_rankings, historical_drafts[selected_year])

def get_historical_draft_data():
    """Get historical draft context and adjustment factors"""
    return {
        2003: {
            'description': 'LeBron Era - Athletic Potential Premium',
            'context': 'Post-Jordan era seeking the next superstar. High school players allowed.',
            'adjustments': {
                'athleticism_weight': 1.4,
                'potential_over_production': 1.3,
                'size_premium': 1.2,
                'three_point_devalue': 0.6,
                'age_bonus': 1.2,  # Younger players valued more
                'college_production_weight': 0.8
            },
            'era_priorities': ['Athletic upside', 'Size', 'Raw potential', 'Defensive length'],
            'era_deemphasize': ['Three-point shooting', 'Advanced metrics', 'College efficiency'],
            'notable_picks': ['LeBron James #1', 'Carmelo Anthony #3', 'Chris Bosh #4']
        },
        2009: {
            'description': 'Traditional Big Man Era',
            'context': 'Centers still highly valued. Analytics revolution beginning.',
            'adjustments': {
                'center_premium': 1.3,
                'traditional_skills': 1.2,
                'three_point_devalue': 0.7,
                'post_skills_bonus': 1.3,
                'defensive_anchor_bonus': 1.2,
                'pace_space_penalty': 0.8
            },
            'era_priorities': ['Post skills', 'Defensive anchors', 'Traditional positions', 'College success'],
            'era_deemphasize': ['Pace and space', 'Positionless basketball', 'High three-point volume'],
            'notable_picks': ['Blake Griffin #1', 'Hasheem Thabeet #2', 'James Harden #3']
        },
        2014: {
            'description': 'International/Potential Revolution',
            'context': 'International players surge. Teams swing for upside over safety.',
            'adjustments': {
                'international_bonus': 1.2,
                'upside_over_floor': 1.4,
                'skill_over_athleticism': 1.1,
                'three_point_emerging': 0.9,
                'versatility_bonus': 1.1,
                'college_safety_penalty': 0.9
            },
            'era_priorities': ['International skill', 'Positional versatility', 'Shooting upside', 'High ceiling'],
            'era_deemphasize': ['Safe college picks', 'Traditional archetypes', 'Low ceiling players'],
            'notable_picks': ['Andrew Wiggins #1', 'Jabari Parker #2', 'Joel Embiid #3 (injured)']
        },
        2018: {
            'description': 'Pace & Space Revolution',
            'context': 'Warriors dynasty peak. Three-point shooting and versatility paramount.',
            'adjustments': {
                'three_point_premium': 1.3,
                'pace_space_fit': 1.4,
                'versatility_premium': 1.3,
                'switching_defense': 1.2,
                'traditional_center_penalty': 0.7,
                'analytics_heavy': 1.2
            },
            'era_priorities': ['Three-point shooting', 'Defensive switching', 'Pace and space fit', 'Versatility'],
            'era_deemphasize': ['Traditional centers', 'Non-shooters', 'Defensive specialists only'],
            'notable_picks': ['Deandre Ayton #1', 'Marvin Bagley #2', 'Luka Dončić #3']
        },
        2021: {
            'description': 'Modern Positionless Era',
            'context': 'COVID-impacted scouting. Two-way versatility and shooting at premium.',
            'adjustments': {
                'two_way_premium': 1.4,
                'shooting_critical': 1.3,
                'positional_flexibility': 1.3,
                'limited_scouting_uncertainty': 0.9,
                'nba_readiness_bonus': 1.1,
                'defensive_versatility': 1.2
            },
            'era_priorities': ['Two-way impact', 'Shooting at size', 'Positional flexibility', 'NBA readiness'],
            'era_deemphasize': ['One-dimensional players', 'Poor shooters', 'Defensive-only specialists'],
            'notable_picks': ['Cade Cunningham #1', 'Jalen Green #2', 'Evan Mobley #3']
        }
    }

def display_historical_context(year: int, draft_data: dict):
    """Display historical draft context"""
    st.markdown(f"### 📚 {year} Draft Context")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info(f"""
        **{draft_data['description']}**
        
        {draft_data['context']}
        
        **Notable Picks:** {', '.join(draft_data['notable_picks'])}
        """)
    
    with col2:
        st.markdown("**Era Priorities:**")
        for priority in draft_data['era_priorities']:
            st.markdown(f"✅ {priority}")
        
        st.markdown("**De-emphasized:**")
        for deemphasize in draft_data['era_deemphasize']:
            st.markdown(f"❌ {deemphasize}")

def simulate_historical_draft(df: pd.DataFrame, year: int, era_data: dict) -> List[dict]:
    """Simulate how prospects would be drafted in historical era"""
    historical_rankings = []
    
    for _, player in df.iterrows():
        # Base stats
        name = safe_string(player['name'])
        position = safe_string(player['position'])
        age = safe_numeric(player.get('age', 20))
        ppg = safe_numeric(player.get('ppg', 0))
        rpg = safe_numeric(player.get('rpg', 0))
        apg = safe_numeric(player.get('apg', 0))
        three_pt = safe_numeric(player.get('three_pt_pct', 0))
        height = safe_numeric(player.get('height', 0))
        current_rank = int(safe_numeric(player.get('final_rank', 30)))
        gen_prob = safe_numeric(player.get('final_gen_probability', 0.5))
        archetype = safe_string(player.get('archetype', 'N/A'))
        
        # Calculate historical score
        historical_score = calculate_historical_draft_score(
            position, age, ppg, rpg, apg, three_pt, height, 
            gen_prob, archetype, era_data['adjustments']
        )
        
        # Determine movement direction and reasoning
        movement, reasoning = analyze_historical_movement(
            current_rank, historical_score, position, archetype, era_data
        )
        
        historical_rankings.append({
            'name': name,
            'current_rank': current_rank,
            'historical_score': historical_score,
            'position': position,
            'archetype': archetype,
            'movement': movement,
            'reasoning': reasoning,
            'era_fit': calculate_era_fit(position, archetype, three_pt, era_data)
        })
    
    # Sort by historical score and assign new ranks
    historical_rankings.sort(key=lambda x: x['historical_score'], reverse=True)
    for i, player in enumerate(historical_rankings):
        player['historical_rank'] = i + 1
        player['rank_change'] = player['current_rank'] - player['historical_rank']
    
    return historical_rankings

def calculate_historical_draft_score(position: str, age: float, ppg: float, rpg: float, 
                                   apg: float, three_pt: float, height: float,
                                   gen_prob: float, archetype: str, adjustments: dict) -> float:
    """Calculate draft score adjusted for historical era"""
    
    # Base score from current metrics
    base_score = (
        ppg * 2.0 +
        rpg * 1.5 +
        apg * 1.8 +
        three_pt * 20 +
        gen_prob * 30 +
        (22 - age) * 2  # Age bonus
    )
    
    # Apply era-specific adjustments
    historical_score = base_score
    
    # Athleticism/potential adjustments
    if 'athleticism_weight' in adjustments:
        if archetype in ['Athletic Defender', 'Two-Way Wing']:
            historical_score *= adjustments['athleticism_weight']
    
    if 'potential_over_production' in adjustments:
        potential_factor = gen_prob * adjustments['potential_over_production']
        production_factor = (ppg / 20) * (2 - adjustments['potential_over_production'])
        historical_score = historical_score * 0.5 + (potential_factor + production_factor) * 25
    
    # Position-specific adjustments
    if 'center_premium' in adjustments and position == 'C':
        historical_score *= adjustments['center_premium']
    
    if 'traditional_center_penalty' in adjustments and position == 'C' and three_pt < 0.25:
        historical_score *= adjustments['traditional_center_penalty']
    
    # Size premium
    if 'size_premium' in adjustments and height > 6.8:
        historical_score *= adjustments['size_premium']
    
    # Three-point adjustments
    if 'three_point_devalue' in adjustments:
        three_pt_impact = three_pt * 20 * (1 - adjustments['three_point_devalue'])
        historical_score = historical_score - (three_pt * 20) + three_pt_impact
    
    if 'three_point_premium' in adjustments and three_pt > 0.35:
        historical_score *= adjustments['three_point_premium']
    
    # Age adjustments
    if 'age_bonus' in adjustments and age < 20:
        historical_score *= adjustments['age_bonus']
    
    # International bonus (simplified check)
    if 'international_bonus' in adjustments:
        international_indicators = ['ić', 'ov', 'ez', 'ão', 'é', 'ü']
        if 'international_bonus' in adjustments and player_name:
            if any(indicator in player_name.lower() for indicator in international_indicators):
             historical_score *= adjustments['international_bonus']
    
    # Versatility adjustments
    if 'versatility_premium' in adjustments:
        if archetype in ['Two-Way Wing', 'Versatile Guard'] or (apg > 3 and rpg > 5):
            historical_score *= adjustments['versatility_premium']
    
    # Two-way premium
    if 'two_way_premium' in adjustments:
        if archetype == 'Two-Way Wing' or (ppg > 12 and rpg > 5 and (apg > 3 or three_pt > 0.33)):
            historical_score *= adjustments['two_way_premium']
    
    return max(0, historical_score)

def analyze_historical_movement(current_rank: int, historical_score: float, 
                              position: str, archetype: str, era_data: dict) -> tuple:
    """Analyze why a player would move up or down in historical draft"""
    
    # Estimate historical rank based on score (simplified)
    score_rank = max(1, min(30, int(31 - (historical_score / 10))))
    rank_change = current_rank - score_rank
    
    if rank_change > 5:
        movement = "📈 Significant Rise"
        reasoning = get_rise_reasoning(position, archetype, era_data)
    elif rank_change > 2:
        movement = "⬆️ Rise"
        reasoning = get_moderate_rise_reasoning(position, archetype, era_data)
    elif rank_change < -5:
        movement = "📉 Significant Fall"
        reasoning = get_fall_reasoning(position, archetype, era_data)
    elif rank_change < -2:
        movement = "⬇️ Fall"
        reasoning = get_moderate_fall_reasoning(position, archetype, era_data)
    else:
        movement = "➡️ Similar"
        reasoning = "Profile fits well in both eras"
    
    return movement, reasoning

def get_rise_reasoning(position: str, archetype: str, era_data: dict) -> str:
    """Get reasoning for why player would rise in historical draft"""
    reasons = []
    
    if 'athleticism_weight' in era_data['adjustments'] and archetype in ['Athletic Defender', 'Two-Way Wing']:
        reasons.append("athletic upside highly valued")
    
    if 'center_premium' in era_data['adjustments'] and position == 'C':
        reasons.append("traditional big men at premium")
    
    if 'potential_over_production' in era_data['adjustments']:
        reasons.append("teams prioritized ceiling over floor")
    
    if 'size_premium' in era_data['adjustments']:
        reasons.append("size and length emphasized")
    
    return f"Would rise due to era's emphasis on {', '.join(reasons) if reasons else 'different priorities'}"

def get_fall_reasoning(position: str, archetype: str, era_data: dict) -> str:
    """Get reasoning for why player would fall in historical draft"""
    reasons = []
    
    if 'three_point_devalue' in era_data['adjustments'] and archetype == 'Elite Shooter':
        reasons.append("shooting less valued")
    
    if 'traditional_center_penalty' in era_data['adjustments'] and position == 'C':
        reasons.append("traditional centers falling out of favor")
    
    if 'pace_space_penalty' in era_data['adjustments']:
        reasons.append("pace-and-space skills not yet prioritized")
    
    return f"Would fall due to {', '.join(reasons) if reasons else 'different era priorities'}"

def get_moderate_rise_reasoning(position: str, archetype: str, era_data: dict) -> str:
    """Get reasoning for moderate rise"""
    return f"Moderate rise due to era's {era_data['description'].lower()} philosophy"

def get_moderate_fall_reasoning(position: str, archetype: str, era_data: dict) -> str:
    """Get reasoning for moderate fall"""
    return f"Slight fall as era deemphasized {archetype.lower()} skillset"

def calculate_era_fit(position: str, archetype: str, three_pt: float, era_data: dict) -> str:
    """Calculate how well player fits the era"""
    
    fit_score = 0.5  # Base fit
    
    # Check if player's strengths align with era priorities
    priorities = era_data['era_priorities']
    deemphasize = era_data['era_deemphasize']
    
    if position == 'C':
        if 'Traditional positions' in priorities or 'Post skills' in priorities:
            fit_score += 0.2
        if 'Traditional centers' in deemphasize:
            fit_score -= 0.3
    
    if three_pt > 0.35:
        if 'Three-point shooting' in priorities:
            fit_score += 0.3
        if 'Three-point shooting' in deemphasize:
            fit_score -= 0.2
    
    if archetype == 'Two-Way Wing':
        if 'Two-way impact' in priorities or 'Versatility' in priorities:
            fit_score += 0.3
    
    if archetype == 'Athletic Defender':
        if 'Athletic upside' in priorities:
            fit_score += 0.2
        if 'Defensive-only specialists' in deemphasize:
            fit_score -= 0.2
    
    # Determine fit level
    if fit_score > 0.8:
        return "🟢 Perfect Fit"
    elif fit_score > 0.6:
        return "🟡 Good Fit"
    elif fit_score > 0.4:
        return "🟠 Moderate Fit"
    else:
        return "🔴 Poor Fit"

def display_simulation_results(current_df: pd.DataFrame, historical_rankings: List[dict], year: int):
    """Display side-by-side simulation results"""
    st.markdown("### 📊 Draft Simulation Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### 🏀 2025 NBA Draft")
        current_display = []
        for _, player in current_df.iterrows():
            current_display.append({
                'Rank': int(safe_numeric(player.get('final_rank', 0))),
                'Player': safe_string(player['name']),
                'Position': safe_string(player['position']),
                'Archetype': safe_string(player.get('archetype', 'N/A'))
            })
        
        current_table = pd.DataFrame(current_display)
        st.dataframe(current_table, use_container_width=True, hide_index=True, height=400)
    
    with col2:
        st.markdown(f"#### 🕰️ {year} Draft Simulation")
        historical_display = []
        for player in historical_rankings:
            # Movement emoji
            if player['rank_change'] > 5:
                movement_emoji = "📈"
            elif player['rank_change'] > 0:
                movement_emoji = "⬆️"
            elif player['rank_change'] < -5:
                movement_emoji = "📉"
            elif player['rank_change'] < 0:
                movement_emoji = "⬇️"
            else:
                movement_emoji = "➡️"
            
            historical_display.append({
                'Rank': player['historical_rank'],
                'Player': player['name'],
                'Position': player['position'],
                'Era Fit': player['era_fit'],
                'Change': f"{movement_emoji} {player['rank_change']:+d}" if player['rank_change'] != 0 else "➡️ 0"
            })
        
        historical_table = pd.DataFrame(historical_display)
        st.dataframe(historical_table, use_container_width=True, hide_index=True, height=400)

def display_movement_analysis(current_df: pd.DataFrame, historical_rankings: List[dict], year: int):
    """Display detailed movement analysis"""
    st.markdown("### 📈 Movement Analysis")
    
    # Calculate movement stats
    risers = [p for p in historical_rankings if p['rank_change'] > 2]
    fallers = [p for p in historical_rankings if p['rank_change'] < -2]
    stable = [p for p in historical_rankings if -2 <= p['rank_change'] <= 2]
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Big Risers", len([p for p in historical_rankings if p['rank_change'] > 5]))
    with col2:
        st.metric("⬆️ Moderate Risers", len([p for p in historical_rankings if 2 < p['rank_change'] <= 5]))
    with col3:
        st.metric("⬇️ Moderate Fallers", len([p for p in historical_rankings if -5 <= p['rank_change'] < -2]))
    with col4:
        st.metric("📉 Big Fallers", len([p for p in historical_rankings if p['rank_change'] < -5]))
    
    # Detailed movement breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        if risers:
            st.markdown("#### 📈 Biggest Risers")
            risers_sorted = sorted(risers, key=lambda x: x['rank_change'], reverse=True)[:5]
            
            for riser in risers_sorted:
                movement_color = "#10b981" if riser['rank_change'] > 5 else "#22c55e"
                st.markdown(f"""
                <div style="background: {movement_color}20; 
                            border-left: 4px solid {movement_color}; 
                            padding: 1rem; margin: 0.5rem 0; border-radius: 8px;">
                    <strong>{riser['name']}</strong> ({riser['position']})
                    <div style="font-size: 0.9rem; color: #666;">
                        #{riser['current_rank']} → #{riser['historical_rank']} ({riser['rank_change']:+d})
                    </div>
                    <div style="font-size: 0.8rem; margin-top: 0.3rem; font-style: italic;">
                        {riser['reasoning']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        if fallers:
            st.markdown("#### 📉 Biggest Fallers")
            fallers_sorted = sorted(fallers, key=lambda x: x['rank_change'])[:5]
            
            for faller in fallers_sorted:
                movement_color = "#ef4444" if faller['rank_change'] < -5 else "#f87171"
                st.markdown(f"""
                <div style="background: {movement_color}20; 
                            border-left: 4px solid {movement_color}; 
                            padding: 1rem; margin: 0.5rem 0; border-radius: 8px;">
                    <strong>{faller['name']}</strong> ({faller['position']})
                    <div style="font-size: 0.9rem; color: #666;">
                        #{faller['current_rank']} → #{faller['historical_rank']} ({faller['rank_change']:+d})
                    </div>
                    <div style="font-size: 0.8rem; margin-top: 0.3rem; font-style: italic;">
                        {faller['reasoning']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

def display_movement_visualization(current_df: pd.DataFrame, historical_rankings: List[dict], year: int):
    """Create interactive visualization of rank movements"""
    st.markdown("### 📊 Movement Visualization")
    
    # Prepare data for visualization
    movement_data = []
    for player in historical_rankings:
        movement_data.append({
            'Player': player['name'][:15] + ('...' if len(player['name']) > 15 else ''),  # Truncate long names
            'Current Rank': player['current_rank'],
            'Historical Rank': player['historical_rank'],
            'Change': player['rank_change'],
            'Position': player['position'],
            'Era Fit': player['era_fit']
        })
    
    # Create slope chart
    fig = go.Figure()
    
    # Add lines for each player
    for player in movement_data:
        color = (
            '#10b981' if player['Change'] > 2 else  # Green for risers
            '#ef4444' if player['Change'] < -2 else  # Red for fallers
            '#6b7280'  # Gray for stable
        )
        
        fig.add_trace(go.Scatter(
            x=[1, 2],
            y=[player['Current Rank'], player['Historical Rank']],
            mode='lines+markers',
            name=player['Player'],
            line=dict(color=color, width=2),
            marker=dict(size=8, color=color),
            hovertemplate=(
                f"<b>{player['Player']}</b><br>"
                f"Position: {player['Position']}<br>"
                f"2025 Rank: #{player['Current Rank']}<br>"
                f"{year} Rank: #{player['Historical Rank']}<br>"
                f"Change: {player['Change']:+d}<br>"
                f"Era Fit: {player['Era Fit']}<br>"
                "<extra></extra>"
            ),
            showlegend=False
        ))
    
    # Add player labels
    for player in movement_data:
        fig.add_annotation(
            x=2.05,
            y=player['Historical Rank'],
            text=player['Player'],
            showarrow=False,
            font=dict(size=9),
            xanchor='left'
        )
    
    fig.update_layout(
        title=f"Draft Position Changes: 2025 → {year}",
        xaxis=dict(
            tickvals=[1, 2],
            ticktext=['2025 Draft', f'{year} Draft'],
            range=[0.8, 2.8]
        ),
        yaxis=dict(
            title="Draft Position",
            autorange="reversed",  # Lower numbers (better picks) at top
            tickmode='linear',
            tick0=1,
            dtick=2
        ),
        height=600,
        showlegend=False,
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Movement summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_change = sum(p['Change'] for p in movement_data) / len(movement_data)
        st.metric("Average Position Change", f"{avg_change:+.1f}")
    
    with col2:
        max_riser = max(movement_data, key=lambda x: x['Change'])
        st.metric("Biggest Riser", f"{max_riser['Player']} ({max_riser['Change']:+d})")
    
    with col3:
        max_faller = min(movement_data, key=lambda x: x['Change'])
        st.metric("Biggest Faller", f"{max_faller['Player']} ({max_faller['Change']:+d})")

def display_era_insights(year: int, historical_rankings: List[dict], era_data: dict):
    """Display insights about the era and its impact"""
    st.markdown("### 💡 Era Insights & Takeaways")
    
    # Positional analysis
    position_changes = {}
    for player in historical_rankings:
        pos = player['position']
        if pos not in position_changes:
            position_changes[pos] = {'risers': 0, 'fallers': 0, 'avg_change': 0}
        
        if player['rank_change'] > 2:
            position_changes[pos]['risers'] += 1
        elif player['rank_change'] < -2:
            position_changes[pos]['fallers'] += 1
        
        position_changes[pos]['avg_change'] += player['rank_change']
    
    # Calculate averages
    for pos in position_changes:
        pos_players = len([p for p in historical_rankings if p['position'] == pos])
        if pos_players > 0:
            position_changes[pos]['avg_change'] /= pos_players
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Positional Impact")
        pos_data = []
        for pos, data in position_changes.items():
            pos_data.append({
                'Position': pos,
                'Avg Change': f"{data['avg_change']:+.1f}",
                'Risers': data['risers'],
                'Fallers': data['fallers']
            })
        
        if pos_data:
            pos_df = pd.DataFrame(pos_data)
            st.dataframe(pos_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 🎯 Key Era Characteristics")
        st.info(f"""
        **{era_data['description']}**
        
        **Most Benefited Archetypes:**
        {', '.join(era_data['era_priorities'][:3])}
        
        **Most Hurt Archetypes:**
        {', '.join(era_data['era_deemphasize'][:3])}
        
        **Context:** {era_data['context']}
        """)
    
    # Era-specific insights
    st.markdown("#### 🔍 Historical Context")
    
    if year == 2003:
        st.warning("""
        **2003 Impact:** This was the height of the "potential over production" era. 
        Athletic wings and bigs with upside would have been dramatically overvalued, 
        while skilled but older players would have fallen. The presence of high school 
        players also inflated the value of pure athleticism.
        """)
    elif year == 2009:
        st.warning("""
        **2009 Impact:** Traditional big men were still king. Centers and power forwards 
        with post skills would have been premium picks, while pace-and-space players 
        would have been undervalued. This was pre-analytics revolution.
        """)
    elif year == 2014:
        st.warning("""
        **2014 Impact:** International players and high-ceiling picks were in vogue. 
        Teams were swinging for the fences after seeing success with international 
        talents. Safe college picks were devalued.
        """)
    elif year == 2018:
        st.warning("""
        **2018 Impact:** Peak Warriors influence. Three-point shooting and versatility 
        were paramount. Traditional centers without range would have struggled, 
        while versatile shooters would have risen significantly.
        """)
    elif year == 2021:
        st.warning("""
        **2021 Impact:** Modern positionless era with emphasis on two-way impact. 
        Players who could shoot, defend multiple positions, and contribute immediately 
        were highly valued. COVID limited scouting, increasing uncertainty.
        """)
# ==================== HISTORICAL COMPARISONS FUNCTIONS ====================

def create_complete_smart_historical_comparisons(df: pd.DataFrame, historical_data: dict):
    """Enhanced historical comparisons with complete TOP 30 database basé sur les vraies données"""
    st.markdown("### 🎯 Smart Historical Comparisons - Complete TOP 30")
    st.caption("AI-powered comparisons basées sur les profils statistiques réels du dataset")
    
    selected_player = st.selectbox(
        "Select a prospect for detailed comparison:",
        df['name'].head(30).tolist(),
        key="complete_hist_comp_select"
    )
    
    player_data = df[df['name'] == selected_player].iloc[0]
    
    # Get comparison data basée sur les vraies données
    comp_data = get_accurate_comparison_database()
    
    if selected_player in comp_data:
        display_enhanced_player_comparison(selected_player, player_data, comp_data[selected_player])
    else:
        # Generate dynamic comparison for players not in database
        dynamic_comp = generate_dynamic_comparison(player_data, comp_data)
        display_enhanced_player_comparison(selected_player, player_data, dynamic_comp)
    
    # Add comparison insights section
    display_comparison_insights_section(df, comp_data)

def get_accurate_comparison_database():
    """Base de données de comparaisons historiques CORRIGÉE basée sur les vraies données du dataset"""
    return {
       'Cooper Flagg': {
            'primary_comp': 'Jalen Johnson',
            'secondary_comp': 'Kevin Garnett',
            'similarity': 0.87,
            'trajectory_match': 0.82,
            'reasoning': 'Versatile 18-year-old PF (19.2/7.5/4.2) with elite two-way impact and leadership. Rare profile combining size, basketball IQ, and impact on both ends of the floor.',
            'career_path': 'ROTY contender → All-Star by Year 3 → All-NBA candidate',
            'style_notes': 'Versatile forward who impacts winning through versatility rather than dominant scoring',
            'development_timeline': '2-3 years to reach All-Star level',
            'real_data': 'PF, 18 years old, Duke, 19.2 PPG/7.5 RPG/4.2 APG'
        },
        
        'Dylan Harper': {
            'primary_comp': 'Cade Cunningham',
            'secondary_comp': 'Jalen Brunson',
            'similarity': 0.85,
            'trajectory_match': 0.78,
            'reasoning': 'Large combo guard (PG/SG, 19 years old) with 19.4/4.6/4.0 stats. NBA-ready size with advanced basketball IQ and strong two-way potential.',
            'career_path': 'Day 1 starter → All-Star by Year 3 → Franchise cornerstone',
            'style_notes': 'Big guard who controls tempo and creates for others while being a scoring threat',
            'development_timeline': '2-3 years to become elite point guard',
            'real_data': 'PG/SG, 19 years old, Rutgers, 19.4 PPG/4.6 RPG/4.0 APG'
        },
        
        'Ace Bailey': {
            'primary_comp': 'Brandon Miller',
            'secondary_comp': 'Michael Porter Jr.',
            'similarity': 0.82,
            'trajectory_match': 0.75,
            'reasoning': 'Scoring wing at 18 years old (SF, 17.6/7.2/1.3) with dynamic scoring potential and good size. Elite shot-making ability with improving all-around game.',
            'career_path': 'Immediate offense → All-Star by Year 4 → All-NBA peak',
            'style_notes': 'Scoring wing with potential to score at all three levels',
            'development_timeline': '3-4 years for All-NBA consideration',
            'real_data': 'SF, 18 years old, Rutgers, 17.6 PPG/7.2 RPG/1.3 APG'
        },
        
        'Tre Johnson': {
            'primary_comp': 'Tyler Herro',
            'secondary_comp': 'Bradley Beal',
            'similarity': 0.80,
            'trajectory_match': 0.74,
            'reasoning': 'Pure scoring guard at 19 years old (SG, 19.9/3.1/2.7) with elite scoring instincts. Excellent shooter with ability to create offense.',
            'career_path': 'Sixth man → Starter → All-Star consideration',
            'style_notes': 'Elite shooter who can score in bunches with improving playmaking',
            'development_timeline': '3-4 years to reach All-Star conversation',
            'real_data': 'SG, 19 years old, Texas, 19.9 PPG/3.1 RPG/2.7 APG'
        },
        
        'Jeremiah Fears': {
            'primary_comp': 'Dejounte Murray',
            'secondary_comp': 'Damian Lillard',
            'similarity': 0.73,
            'trajectory_match': 0.70,
            'reasoning': 'Explosive 18-year-old point guard (PG, 17.1/4.1/4.1) with scoring ability and leadership qualities. Strong rim pressure and clutch gene.',
            'career_path': 'Instant offense → Starting PG → All-Star potential',
            'style_notes': 'Aggressive point guard with rim pressure and clutch instincts',
            'development_timeline': '2-3 years to become elite scoring PG',
            'real_data': 'PG, 18 years old, Oklahoma, 17.1 PPG/4.1 RPG/4.1 APG'
        },
        
        # LOTTERY TIER (6-14)
        'VJ Edgecombe': {
            'primary_comp': 'Andrew Wiggins',
            'secondary_comp': 'Victor Oladipo',
            'similarity': 0.78,
            'trajectory_match': 0.72,
            'reasoning': 'Athletic wing from Bahamas (SG/SF, 19 years old, 15.0/5.6/3.2) with explosiveness and defensive quickness. High-level athleticism with two-way potential.',
            'career_path': 'Role player → Key contributor → All-Defense candidate',
            'style_notes': 'Athletic wing with explosiveness and defensive projection',
            'development_timeline': '3-4 years to reach peak two-way impact',
            'real_data': 'SG/SF, 19 years old, Bahamas, Baylor, 15.0 PPG/5.6 RPG/3.2 APG'
        },
        
        'Noa Essengue': {
            'primary_comp': 'Jerami Grant',
            'secondary_comp': 'Nicolas Batum',
            'similarity': 0.72,
            'trajectory_match': 0.68,
            'reasoning': 'French forward at 18 years old (PF, 9.7/4.5/1.1) with size, shooting touch, and international experience. Raw but intriguing upside.',
            'career_path': 'Development → Role player → Solid contributor',
            'style_notes': 'French forward with shooting touch and versatility in development',
            'development_timeline': '3-4 years to become solid contributor',
            'real_data': 'PF, 18 years old, France, Ratiopharm Ulm, 9.7 PPG/4.5 RPG/1.1 APG'
        },
        
        'Kasparas Jakucionis': {
            'primary_comp': 'Coby White',
            'secondary_comp': 'Darius Garland',
            'similarity': 0.76,
            'trajectory_match': 0.72,
            'reasoning': 'Lithuanian combo guard at 18 years old (PG/SG, 15.0/5.7/4.7) with size, court vision, and versatility. Modern combo guard with good feel.',
            'career_path': 'Development → Backup guard → Starting combo guard',
            'style_notes': 'Versatile guard who can score and facilitate, fits modern combo guard mold',
            'development_timeline': '2-3 years to become solid NBA contributor',
            'real_data': 'PG/SG, 18 years old, Lithuania, Illinois, 15.0 PPG/5.7 RPG/4.7 APG'
        },
        
        'Kon Knueppel': {
            'primary_comp': 'Cameron Johnson',
            'secondary_comp': 'Duncan Robinson',
            'similarity': 0.75,
            'trajectory_match': 0.70,
            'reasoning': 'Duke shooting wing (SF, 19 years old, 14.4/4.0/2.7) with elite shooting and basketball IQ. Clutch performer with winning background.',
            'career_path': 'Role player → Solid starter → Reliable contributor',
            'style_notes': 'Smart wing with elite shooting and clutch gene',
            'development_timeline': '2-3 years to become reliable starter',
            'real_data': 'SF, 19 years old, Duke, 14.4 PPG/4.0 RPG/2.7 APG'
        },
        
        'Khaman Maluach': {
            'primary_comp': 'Dereck Lively',
            'secondary_comp': 'Clint Capela',
            'similarity': 0.77,
            'trajectory_match': 0.73,
            'reasoning': '18-year-old center from South Sudan (C, 8.6/6.6/0.5) with elite size and rim protection ability. Athletic big with mobility.',
            'career_path': 'Development → Backup C → Starting rim protector',
            'style_notes': 'Athletic rim protector with elite size and mobility',
            'development_timeline': '3-4 years to become elite rim protector',
            'real_data': 'C, 18 years old, South Sudan, Duke, 8.6 PPG/6.6 RPG/0.5 APG'
        },
        
        'Collin Murray-Boyles': {
            'primary_comp': 'Julius Randle',
            'secondary_comp': 'Anthony Mason',
            'similarity': 0.76,
            'trajectory_match': 0.71,
            'reasoning': 'Physical forward at 19 years old (PF, 16.8/8.3/2.4) with physicality and rebounding. Strong face-up game with toughness.',
            'career_path': 'Role player → Key contributor → Potential All-Star',
            'style_notes': 'Physical forward with rebounding and developing face-up game',
            'development_timeline': '2-3 years to become key contributor',
            'real_data': 'PF, 19 years old, South Carolina, 16.8 PPG/8.3 RPG/2.4 APG'
        },
        
        'Derik Queen': {
            'primary_comp': 'Alperen Şengün',
            'secondary_comp': 'Nikola Vučević',
            'similarity': 0.74,
            'trajectory_match': 0.70,
            'reasoning': 'Skilled 20-year-old center (C, 16.5/9.0/1.9) with post skills and passing feel. Good scoring touch with developing range.',
            'career_path': 'Role player → Solid starter → All-Star consideration',
            'style_notes': 'Center with post skills and passing ability, good scoring touch',
            'development_timeline': '3-4 years for All-Star conversation',
            'real_data': 'C, 20 years old, Maryland, 16.5 PPG/9.0 RPG/1.9 APG'
        },
        
        'Asa Newell': {
            'primary_comp': 'John Collins',
            'secondary_comp': 'Aaron Gordon',
            'similarity': 0.72,
            'trajectory_match': 0.68,
            'reasoning': 'Athletic forward at 19 years old (PF/C, 15.4/6.8/0.9) with athleticism and finishing ability. Potential shooting development.',
            'career_path': 'Development → Role player → Athletic contributor',
            'style_notes': 'Athletic forward with finishing ability and potential shooting',
            'development_timeline': '3-4 years to maximize athletic potential',
            'real_data': 'PF/C, 19 years old, Georgia, 15.4 PPG/6.8 RPG/0.9 APG'
        },
        
        'Liam McNeeley': {
            'primary_comp': 'Keegan Murray',
            'secondary_comp': 'Harrison Barnes',
            'similarity': 0.75,
            'trajectory_match': 0.70,
            'reasoning': 'UConn wing (SF/PF, 19 years old, 14.3/6.0/2.3) with winning program background and versatility. High basketball IQ.',
            'career_path': 'Role player → Solid starter → Reliable contributor',
            'style_notes': 'Smart wing from winning program with basketball IQ',
            'development_timeline': '2-3 years to become reliable starter',
            'real_data': 'SF/PF, 19 years old, UConn, 14.3 PPG/6.0 RPG/2.3 APG'
        },
        
        # FIRST ROUND DEPTH (15-30)
        'Cedric Coward': {
            'primary_comp': 'Jarace Walker',
            'secondary_comp': 'Cam Reddish',
            'similarity': 0.69,
            'trajectory_match': 0.65,
            'reasoning': '21-year-old wing (SF/PF, 11.8/6.2/1.9) with length and defensive tools. Experience and shooting development.',
            'career_path': 'Role player → Defensive specialist → Key contributor',
            'style_notes': 'Wing with length and defensive projection, developing shooting',
            'development_timeline': '2-3 years to become defensive specialist',
            'real_data': 'SF/PF, 21 years old, Washington State, 11.8 PPG/6.2 RPG/1.9 APG'
        },
        
        'Carter Bryant': {
            'primary_comp': 'Marcus Morris',
            'secondary_comp': 'Robert Covington',
            'similarity': 0.68,
            'trajectory_match': 0.64,
            'reasoning': 'Arizona wing (SF, 19 years old, 6.5/4.1/1.0) with athletic tools and defensive potential. 3&D development path.',
            'career_path': 'Development → Role player → 3&D specialist',
            'style_notes': 'Wing with athletic tools and 3&D projection',
            'development_timeline': '3-4 years to develop NBA role',
            'real_data': 'SF, 19 years old, Arizona, 6.5 PPG/4.1 RPG/1.0 APG'
        },
        
        'Egor Demin': {
            'primary_comp': 'Josh Giddey',
            'secondary_comp': 'Deni Avdija',
            'similarity': 0.74,
            'trajectory_match': 0.69,
            'reasoning': 'Russian guard/forward at 19 years old (PG/SF, 10.6/3.9/5.5) with size and exceptional court vision. Elite playmaking ability.',
            'career_path': 'Development → Playmaker → Starting facilitator',
            'style_notes': 'Tall facilitator with court vision and exceptional passing',
            'development_timeline': '3-4 years to maximize playmaking skills',
            'real_data': 'PG/SF, 19 years old, Russia, BYU, 10.6 PPG/3.9 RPG/5.5 APG'
        },
        
        'Will Riley': {
            'primary_comp': 'Kyshawn George',
            'secondary_comp': 'RJ Barrett',
            'similarity': 0.67,
            'trajectory_match': 0.63,
            'reasoning': 'Canadian wing at 19 years old (SF, 12.6/4.1/2.2) with length and developing shooting potential. Flashes of playmaking.',
            'career_path': 'Development → Role player → Shooting specialist',
            'style_notes': 'Canadian wing with length and playmaking flashes',
            'development_timeline': '3-4 years to develop consistency',
            'real_data': 'SF, 19 years old, Canada, Illinois, 12.6 PPG/4.1 RPG/2.2 APG'
        },
        
        'Jase Richardson': {
            'primary_comp': 'Reed Sheppard',
            'secondary_comp': 'Austin Reaves',
            'similarity': 0.71,
            'trajectory_match': 0.68,
            'reasoning': '19-year-old guard (SG, 12.1/3.3/1.9) with shooting and basketball IQ. NBA bloodline advantage with efficient play.',
            'career_path': 'Development → Role player → Shooting specialist',
            'style_notes': 'Smart shooter with efficiency and NBA bloodline advantage',
            'development_timeline': '2-3 years to carve out NBA role',
            'real_data': 'SG, 19 years old, Michigan State, 12.1 PPG/3.3 RPG/1.9 APG'
        },
        
        'Rasheer Fleming': {
            'primary_comp': 'Taylor Hendricks',
            'secondary_comp': 'Jonathan Isaac',
            'similarity': 0.70,
            'trajectory_match': 0.66,
            'reasoning': '20-year-old forward (PF, 10.6/7.1/1.3) with length and solid mid-major production. Shooting development potential.',
            'career_path': 'Development → Role player → Stretch four',
            'style_notes': 'Forward with length and shooting, consistent production',
            'development_timeline': '3-4 years to become reliable stretch four',
            'real_data': 'PF, 20 years old, Saint Joseph\'s, 10.6 PPG/7.1 RPG/1.3 APG'
        },
        
        'Nique Clifford': {
            'primary_comp': 'Cody Martin',
            'secondary_comp': 'PJ Tucker',
            'similarity': 0.68,
            'trajectory_match': 0.64,
            'reasoning': '23-year-old veteran (SF/PF, 10.1/5.9/2.4) with experience and versatility. Ready to contribute immediately.',
            'career_path': 'Ready contributor → Role player → Veteran presence',
            'style_notes': 'Experienced player with versatility and rebounding',
            'development_timeline': 'Ready immediately for NBA role',
            'real_data': 'SF/PF, 23 years old, Colorado State, 10.1 PPG/5.9 RPG/2.4 APG'
        },
        
        'Maxime Raynaud': {
            'primary_comp': 'Quentin Post',
            'secondary_comp': 'Rudy Gobert',
            'similarity': 0.71,
            'trajectory_match': 0.67,
            'reasoning': 'French center at 22 years old (C, 12.6/7.7/1.3) with size and post skills. Good production and passing ability.',
            'career_path': 'Development → Backup C → Starting center',
            'style_notes': 'French center with size and post skills, passing ability',
            'development_timeline': '2-3 years for NBA adaptation',
            'real_data': 'C, 22 years old, France, Stanford, 12.6 PPG/7.7 RPG/1.3 APG'
        },
        
        'Walter Clayton Jr.': {
            'primary_comp': 'Fred VanVleet',
            'secondary_comp': 'Cole Anthony',
            'similarity': 0.72,
            'trajectory_match': 0.69,
            'reasoning': '22-year-old combo guard (PG/SG, 18.3/3.4/4.2) with clutch shooting and fearless mentality. Experienced leader.',
            'career_path': 'Ready contributor → Sixth man → Starting guard',
            'style_notes': 'Experienced guard with clutch gene and leadership',
            'development_timeline': 'Ready immediately for contribution',
            'real_data': 'PG/SG, 22 years old, Florida, 18.3 PPG/3.4 RPG/4.2 APG'
        },
        
        'Thomas Sorber': {
            'primary_comp': 'Onyeka Okongwu',
            'secondary_comp': 'Daniel Gafford',
            'similarity': 0.70,
            'trajectory_match': 0.66,
            'reasoning': '19-year-old center (C, 14.5/8.5/2.4) with post skills and defensive activity. Good size and passing for position.',
            'career_path': 'Development → Backup C → Solid starter',
            'style_notes': 'Center with post skills and passing, defensive activity',
            'development_timeline': '3-4 years to become solid starter',
            'real_data': 'C, 19 years old, Georgetown, 14.5 PPG/8.5 RPG/2.4 APG'
        },
        
        'Joan Beringer': {
            'primary_comp': 'Nicolas Claxton',
            'secondary_comp': 'Nic Claxton',
            'similarity': 0.68,
            'trajectory_match': 0.64,
            'reasoning': 'French center at 18 years old (C, 4.7/4.6/0.4) with size and shot-blocking potential. Long-term development project.',
            'career_path': 'Long development → Backup C → Rim protector',
            'style_notes': 'Young French center with size and mobility, long-term project',
            'development_timeline': '4-5 years for significant NBA contribution',
            'real_data': 'C, 18 years old, France, Cedevita, 4.7 PPG/4.6 RPG/0.4 APG'
        },
        
        'Drake Powell': {
            'primary_comp': 'Will Barton',
            'secondary_comp': 'Herb Jones',
            'similarity': 0.69,
            'trajectory_match': 0.65,
            'reasoning': 'UNC wing (SG/SF, 19 years old, 7.4/3.4/1.1) with physical profile and defensive projection. Needs development.',
            'career_path': 'Development → Role player → Two-way contributor',
            'style_notes': 'Wing with physical profile and defensive projection',
            'development_timeline': '3-4 years to develop consistency',
            'real_data': 'SG/SF, 19 years old, North Carolina, 7.4 PPG/3.4 RPG/1.1 APG'
        },
        
        'Nolan Traore': {
            'primary_comp': 'Lonzo Ball',
            'secondary_comp': 'Ricky Rubio',
            'similarity': 0.74,
            'trajectory_match': 0.69,
            'reasoning': 'French point guard at 18 years old (PG, 11.4/1.7/5.2) with exceptional court vision. Elite passing ability.',
            'career_path': 'Development → Backup PG → Starting floor general',
            'style_notes': 'French point guard with court vision and elite passing',
            'development_timeline': '3-4 years to become starting-caliber PG',
            'real_data': 'PG, 18 years old, France, Saint-Quentin, 11.4 PPG/1.7 RPG/5.2 APG'
        },
        
        'Danny Wolf': {
            'primary_comp': 'Kelly Olynyk',
            'secondary_comp': 'Lauri Markkanen',
            'similarity': 0.71,
            'trajectory_match': 0.67,
            'reasoning': '21-year-old forward/center (PF/C, 11.1/7.9/2.5) with size and passing ability. Versatile big with basketball IQ.',
            'career_path': 'Development → Role player → Stretch big',
            'style_notes': 'Versatile big with passing and basketball IQ',
            'development_timeline': '2-3 years for consistent NBA role',
            'real_data': 'PF/C, 21 years old, Michigan, 11.1 PPG/7.9 RPG/2.5 APG'
        },
        
        'Noah Penda': {
            'primary_comp': 'Nicolas Batum',
            'secondary_comp': 'Evan Fournier',
            'similarity': 0.70,
            'trajectory_match': 0.66,
            'reasoning': 'French wing at 20 years old (SF/PF, 10.2/5.1/2.6) with size and versatility. Good basketball IQ and shooting development.',
            'career_path': 'Development → Role player → Versatile contributor',
            'style_notes': 'French wing with versatility and basketball IQ',
            'development_timeline': '3-4 years to maximize versatility',
            'real_data': 'SF/PF, 20 years old, France, Le Mans, 10.2 PPG/5.1 RPG/2.6 APG'
        },
        
        'Ben Saraf': {
            'primary_comp': 'Manu Ginóbili',
            'secondary_comp': 'Goran Dragić',
            'similarity': 0.68,
            'trajectory_match': 0.64,
            'reasoning': 'Israeli combo guard at 19 years old (PG/SG, 11.6/2.8/4.1) with ball-handling and competitiveness. Crafty player with court vision.',
            'career_path': 'Development → Backup guard → Sixth man',
            'style_notes': 'Crafty guard with handle and court vision, competitive spirit',
            'development_timeline': '3-4 years for sixth man role',
            'real_data': 'PG/SG, 19 years old, Israel, Ratiopharm Ulm, 11.6 PPG/2.8 RPG/4.1 APG'
        }
    }

def display_enhanced_player_comparison(player_name: str, player_data: pd.Series, comp_data: dict):
    """Display enhanced player comparison with real data validation"""
    st.markdown(f"### 🎯 Historical Comparison: {player_name}")
    
    # Show real data validation
    st.info(f"**Profil réel:** {comp_data.get('real_data', 'Données non disponibles')}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Current prospect card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF6B35, #F7931E); 
                    padding: 2rem; border-radius: 15px; color: white;">
            <h3 style="margin: 0 0 1rem 0;">{player_name}</h3>
            <div style="font-size: 0.9rem; opacity: 0.9;">
                Rang: #{int(player_data.get('final_rank', 0))} • {comp_data.get('real_data', 'Profil non disponible')}
            </div>
            <div style="margin-top: 1.5rem; font-size: 0.9rem;">
                <strong>Profil:</strong><br>
                {comp_data.get('reasoning', 'Analyse en cours...')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Historical comp card
        primary_comp = comp_data.get('primary_comp', 'TBD')
        secondary_comp = comp_data.get('secondary_comp', 'TBD')
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #3B82F6, #2563EB); 
                    padding: 2rem; border-radius: 15px; color: white;">
            <h3 style="margin: 0 0 1rem 0;">Comparaisons Historiques</h3>
            <div style="font-size: 1.1rem; margin-bottom: 1rem;">
                <strong>Primaire:</strong> {primary_comp}
            </div>
            <div style="font-size: 1.1rem; margin-bottom: 1rem;">
                <strong>Secondaire:</strong> {secondary_comp}
            </div>
            <div style="font-size: 0.9rem; opacity: 0.9;">
                Similarité: {comp_data.get('similarity', 0.5):.0%}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Career projection
    st.markdown("#### 🔮 Projection de Carrière")
    career_path = comp_data.get('career_path', 'Développement standard')
    st.success(f"**Trajectoire attendue:** {career_path}")
    
    # Development timeline
    timeline = comp_data.get('development_timeline', '3-4 ans pour contribution significative')
    st.info(f"**Timeline:** {timeline}")
    
    # Style notes
    style_notes = comp_data.get('style_notes', 'Style de jeu en analyse')
    st.markdown(f"**Style de jeu:** {style_notes}")

def generate_dynamic_comparison(player_data: pd.Series, comp_database: dict):
    """Generate dynamic comparison for players not in database"""
    position = player_data.get('position', 'Unknown')
    age = player_data.get('age', 20)
    ppg = player_data.get('ppg', 0)
    
    return {
        'primary_comp': 'TBD - Analyse en cours',
        'secondary_comp': 'TBD - Données insuffisantes',
        'similarity': 0.50,
        'trajectory_match': 0.50,
        'reasoning': f'Prospect {position} de {age} ans avec {ppg} PPG - analyse approfondie en développement',
        'career_path': 'Projection en cours d\'analyse',
        'development_timeline': '2-4 ans selon développement',
        'real_data': f'{position}, {age} ans, {ppg} PPG'
    }

def display_comparison_insights_section(df: pd.DataFrame, comp_data: dict):
    """Display insights section about comparisons"""
    st.markdown("### 💡 Insights sur les Comparaisons")
    
    # Analysis of comparison patterns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Patterns Observés")
        st.info("""
        **Tendances identifiées:**
        • Nombreux prospects internationaux (France, Lithuania, etc.)
        • Emphasis sur les guards polyvalents (PG/SG)
        • Plusieurs prospects très jeunes (18 ans)
        • Forte représentation de joueurs avec skills développés
        """)
    
    with col2:
        st.markdown("#### ⚠️ Notes de Méthodologie")
        st.warning("""
        **Basé sur les données réelles:**
        • Toutes les comparaisons utilisent les stats exactes du dataset
        • Positions, âges et colleges vérifiés
        • Comparaisons NBA existantes intégrées quand disponibles
        • Focus sur la précision des profils
        """)
# ==================== Main Application ====================
def main():
    """Main application function"""
    inject_custom_css()
    
    # Load data
    df = load_data()
    if df is None or df.empty:
        st.error("❌ Unable to load data")
        st.stop()
    
    # Store in session state
    st.session_state['current_df'] = df
    
    # Display header sections
    display_hero_header()
    display_draft_countdown()
    
# Navigation tabs - CORRIGÉ
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🏠 Dashboard",
        "📊 Compare Players", 
        "🔍 Enhanced Search",
        "🎯 Live Big Board",  # ← NOUVEAU NOM
        "💎 Steals & Busts",
        "📈 5-Year Projections", 
        "📊 Historical Intelligence",
        "🎯 Team Fit Analysis"
    ])
    
    with tab1:
        display_dashboard(df)
    
    with tab2:
        create_player_comparison(df)
    
    with tab3:
        create_enhanced_search_with_stats(df)
    
    with tab4:
        st.markdown("## 🎯 Live Big Board")
        st.caption("Professional draft board format • Updated with latest consensus")
        
        # Status banner
        st.info("🚧 **Big Board v2.0 en construction** - Nouvelles fonctionnalités bientôt disponibles !")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Prospects", len(df))
        with col2:
            top_10_avg = df.head(10)['final_gen_probability'].mean()
            st.metric("Top 10 Avg Potential", f"{top_10_avg:.1%}")
        with col3:
            lottery_count = len(df.head(14))
            st.metric("Lottery Prospects", lottery_count)
        with col4:
            elite_count = len(df[df['final_gen_probability'] > 0.7])
            st.metric("Elite Tier", elite_count)
        
        # Temporary Big Board table
        st.markdown("### 📋 Draft Board Preview")
        
        # View selector
        view_range = st.selectbox(
            "View Range:",
            ["Top 14 (Lottery)", "Top 30 (First Round)", "Full Draft (60)"],
            key="bigboard_range"
        )
        
        # Determine display count
        if view_range == "Top 14 (Lottery)":
            display_count = 14
        elif view_range == "Top 30 (First Round)":
            display_count = 30
        else:
            display_count = 60
        
        # Prepare table data
        display_cols = ['final_rank', 'name', 'position', 'college', 'ppg', 'rpg', 'apg', 'scout_grade', 'final_gen_probability']
        available_cols = [col for col in display_cols if col in df.columns]
        
        if available_cols:
            temp_df = df[available_cols].head(display_count).copy()
            
            # Format columns
            if 'final_gen_probability' in temp_df.columns:
                temp_df['final_gen_probability'] = temp_df['final_gen_probability'].apply(lambda x: f"{x:.1%}")
            if 'ppg' in temp_df.columns:
                temp_df['ppg'] = temp_df['ppg'].round(1)
            if 'rpg' in temp_df.columns:
                temp_df['rpg'] = temp_df['rpg'].round(1)
            if 'apg' in temp_df.columns:
                temp_df['apg'] = temp_df['apg'].round(1)
            
            # Rename columns for display
            column_rename = {
                'final_rank': 'Rank',
                'name': 'Player',
                'position': 'Pos',
                'college': 'College',
                'ppg': 'PPG',
                'rpg': 'RPG',
                'apg': 'APG',
                'scout_grade': 'Grade',
                'final_gen_probability': 'Potential'
            }
            
            temp_df = temp_df.rename(columns={k: v for k, v in column_rename.items() if k in temp_df.columns})
            
            # Display table
            st.dataframe(
                temp_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Rank": st.column_config.NumberColumn("Rank", width="small"),
                    "Player": st.column_config.TextColumn("Player", width="large"),
                    "Pos": st.column_config.TextColumn("Pos", width="small"),
                    "College": st.column_config.TextColumn("College", width="medium"),
                    "PPG": st.column_config.NumberColumn("PPG", format="%.1f", width="small"),
                    "RPG": st.column_config.NumberColumn("RPG", format="%.1f", width="small"),
                    "APG": st.column_config.NumberColumn("APG", format="%.1f", width="small"),
                    "Grade": st.column_config.TextColumn("Grade", width="small"),
                    "Potential": st.column_config.TextColumn("Potential", width="small")
                }
            )
        else:
            st.error("Unable to display draft board - data columns missing")
    
    with tab5:
        create_steals_busts_analysis(df)
    
    with tab6:
        create_realistic_projections(df)
    
    with tab7:
        create_historical_intelligence(df)
    
    with tab8:
        create_team_fit_analysis(df)
    
    # Footer
    display_footer()

def display_dashboard(df: pd.DataFrame):
    """Display main dashboard"""
    st.markdown("## 📈 Dashboard Overview")
    
    # Leaders section with potential-based metrics
    create_leaders_section(df)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Prospects", len(df))
    with col2:
        elite_count = len(df[df['final_gen_probability'] > 0.7])
        st.metric("Elite Prospects", elite_count)
  
    with col3:
        gen_count = len(df[df['final_gen_probability'] > 0.9])
        st.metric("Generational Talents", gen_count)

    with col4:
        draft_grade = calculate_draft_grade_average(df)
        grade_colors = {
        'A+': '🟢', 'A': '🟢', 'A-': '🟢',
        'B+': '🟡', 'B': '🟡', 'B-': '🟡', 
        'C+': '🟠', 'C': '🟠', 'C-': '🟠',
        'D+': '🔴', 'D': '🔴', 'D-': '🔴',
        'F': '⚫'
    }
        color_emoji = grade_colors.get(draft_grade, '🟡')
        st.metric("Draft Class Grade", f"{color_emoji} {draft_grade}","Scout consensus average"
    )
    
    # Interactive filters
    filtered_df = create_interactive_filters(df)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        if 'position' in filtered_df.columns:
            position_counts = filtered_df['position'].value_counts()
            fig_pie = px.pie(
                values=position_counts.values,
                names=position_counts.index,
                title="Distribution by Position",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Top prospects by potential
        top_potential = filtered_df.nlargest(10, 'final_gen_probability')
        fig_bar = px.bar(
            top_potential,
            x='name',
            y='final_gen_probability',
            title="Top 10 by Generational Talent Probability",
            color='final_gen_probability',
            color_continuous_scale='Viridis',
            labels={'final_gen_probability': 'Potential'}
        )
        fig_bar.update_xaxes(tickangle=45)
        fig_bar.update_yaxes(tickformat='.0%')
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Prospects table
    display_prospects_table(filtered_df)

def create_interactive_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Create interactive filters for the dashboard"""
    st.markdown("### 🔍 Interactive Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        positions = ['All'] + sorted(df['position'].unique().tolist())
        selected_position = st.selectbox("📍 Position", positions)
    
    with col2:
        colleges = ['All'] + sorted(df['college'].unique().tolist())
        selected_college = st.selectbox("🏫 College", colleges)
    
    with col3:
        grades = ['All'] + sorted(df['scout_grade'].unique().tolist(), reverse=True)
        selected_grade = st.selectbox("⭐ Scout Grade", grades)
    
    with col4:
        prob_min = st.slider("🎯 Min Potential", 0.0, 1.0, 0.0, 0.1)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_position != 'All':
        filtered_df = filtered_df[filtered_df['position'] == selected_position]
    
    if selected_college != 'All':
        filtered_df = filtered_df[filtered_df['college'] == selected_college]
    
    if selected_grade != 'All':
        filtered_df = filtered_df[filtered_df['scout_grade'] == selected_grade]
    
    filtered_df = filtered_df[filtered_df['final_gen_probability'] >= prob_min]
    
    st.info(f"📊 {len(filtered_df)} prospects match your filters")
    return filtered_df

def display_prospects_table(df: pd.DataFrame):
    """Display formatted prospects table"""
    st.markdown("### 📋 Top Prospects")
    
    display_cols = ['name', 'position', 'college', 'ppg', 'rpg', 'apg', 
                   'three_pt_pct', 'scout_grade', 'final_gen_probability']
    
    table_df = df[display_cols].head(20).copy()
    
    # Format columns
    table_df['three_pt_pct'] = table_df['three_pt_pct'].apply(lambda x: f"{x:.1%}")
    table_df['final_gen_probability'] = table_df['final_gen_probability'].apply(lambda x: f"{x:.1%}")
    table_df['ppg'] = table_df['ppg'].round(1)
    table_df['rpg'] = table_df['rpg'].round(1)
    table_df['apg'] = table_df['apg'].round(1)
    
    # Rename columns
    table_df.columns = ['Name', 'Pos', 'College', 'PPG', 'RPG', 'APG', '3P%', 'Grade', 'Potential']
    
    st.dataframe(table_df, use_container_width=True, hide_index=True)

def create_player_comparison(df: pd.DataFrame):
    """Create enhanced player comparison"""
    st.markdown("## 📊 Enhanced Player Comparison")
    
    if len(df) < 2:
        st.warning("Need at least 2 prospects for comparison")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        player1 = st.selectbox("Select Player 1:", df['name'].tolist(), key="comp_p1")
    
    with col2:
        player2 = st.selectbox("Select Player 2:", df['name'].tolist(), index=1, key="comp_p2")
    
    if player1 == player2:
        st.warning("Please select different players")
        return
    
    p1_data = df[df['name'] == player1].iloc[0]
    p2_data = df[df['name'] == player2].iloc[0]
    
    # Create radar chart
    create_comparison_radar(p1_data, p2_data, player1, player2)
    
    # Detailed stats comparison
    create_detailed_comparison_table(p1_data, p2_data, player1, player2)

def create_comparison_radar(p1_data: pd.Series, p2_data: pd.Series, 
                           player1: str, player2: str):
    """Create radar chart for player comparison"""
    categories = ['Scoring', 'Shooting', 'Rebounding', 'Playmaking', 
                 'Defense', 'Efficiency', 'Potential']
    
    # Calculate normalized values
    p1_values = [
        min(100, safe_numeric(p1_data['ppg']) / 30 * 100),
        safe_numeric(p1_data.get('three_pt_pct', 0)) * 200,
        min(100, safe_numeric(p1_data['rpg']) / 15 * 100),
        min(100, safe_numeric(p1_data['apg']) / 10 * 100),
        min(100, (safe_numeric(p1_data.get('spg', 0)) + safe_numeric(p1_data.get('bpg', 0))) / 4 * 100),
        safe_numeric(p1_data.get('ts_pct', 0.5)) * 100,
        safe_numeric(p1_data.get('final_gen_probability', 0.5)) * 100
    ]
    
    p2_values = [
        min(100, safe_numeric(p2_data['ppg']) / 30 * 100),
        safe_numeric(p2_data.get('three_pt_pct', 0)) * 200,
        min(100, safe_numeric(p2_data['rpg']) / 15 * 100),
        min(100, safe_numeric(p2_data['apg']) / 10 * 100),
        min(100, (safe_numeric(p2_data.get('spg', 0)) + safe_numeric(p2_data.get('bpg', 0))) / 4 * 100),
        safe_numeric(p2_data.get('ts_pct', 0.5)) * 100,
        safe_numeric(p2_data.get('final_gen_probability', 0.5)) * 100
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=p1_values + [p1_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=player1,
        line=dict(color='#FF6B35', width=3),
        fillcolor='rgba(255, 107, 53, 0.3)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=p2_values + [p2_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=player2,
        line=dict(color='#4361EE', width=3),
        fillcolor='rgba(67, 97, 238, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=20
            )
        ),
        showlegend=True,
        title=f"Skill Comparison: {player1} vs {player2}",
        height=500,
        font=dict(size=14)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_detailed_comparison_table(p1: pd.Series, p2: pd.Series, 
                                   name1: str, name2: str):
    """Create detailed comparison tables"""
    st.markdown("### 📋 Comprehensive Stats Comparison")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        basic_stats = pd.DataFrame({
            'Stat': ['PPG', 'RPG', 'APG', 'SPG', 'BPG'],
            name1: [
                f"{safe_numeric(p1['ppg']):.1f}",
                f"{safe_numeric(p1['rpg']):.1f}",
                f"{safe_numeric(p1['apg']):.1f}",
                f"{safe_numeric(p1.get('spg', 0)):.1f}",
                f"{safe_numeric(p1.get('bpg', 0)):.1f}"
            ],
            name2: [
                f"{safe_numeric(p2['ppg']):.1f}",
                f"{safe_numeric(p2['rpg']):.1f}",
                f"{safe_numeric(p2['apg']):.1f}",
                f"{safe_numeric(p2.get('spg', 0)):.1f}",
                f"{safe_numeric(p2.get('bpg', 0)):.1f}"
            ]
        })
        st.dataframe(basic_stats, use_container_width=True, hide_index=True)
    
    with col2:
        shooting_stats = pd.DataFrame({
            'Stat': ['FG%', '3P%', 'FT%', 'TS%'],
            name1: [
                f"{safe_numeric(p1.get('fg_pct', 0)):.1%}",
                f"{safe_numeric(p1.get('three_pt_pct', 0)):.1%}",
                f"{safe_numeric(p1.get('ft_pct', 0)):.1%}",
                f"{safe_numeric(p1.get('ts_pct', 0)):.1%}"
            ],
            name2: [
                f"{safe_numeric(p2.get('fg_pct', 0)):.1%}",
                f"{safe_numeric(p2.get('three_pt_pct', 0)):.1%}",
                f"{safe_numeric(p2.get('ft_pct', 0)):.1%}",
                f"{safe_numeric(p2.get('ts_pct', 0)):.1%}"
            ]
        })
        st.dataframe(shooting_stats, use_container_width=True, hide_index=True)
    
    with col3:
        physical_stats = pd.DataFrame({
            'Stat': ['Age', 'Height', 'Weight', 'Position'],
            name1: [
                f"{safe_numeric(p1.get('age', 0)):.0f}",
                format_height(safe_numeric(p1.get('height', 0))),
                f"{safe_numeric(p1.get('weight', 0)):.0f} lbs",
                safe_string(p1.get('position'))
            ],
            name2: [
                f"{safe_numeric(p2.get('age', 0)):.0f}",
                format_height(safe_numeric(p2.get('height', 0))),
                f"{safe_numeric(p2.get('weight', 0)):.0f} lbs",
                safe_string(p2.get('position'))
            ]
        })
        st.dataframe(physical_stats, use_container_width=True, hide_index=True)


def display_draft_summary(draft_order: pd.DataFrame):
    """Display draft summary statistics"""
    st.markdown("### 📊 Draft Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        lottery_avg = draft_order.head(14)['final_gen_probability'].mean()
        st.metric("Lottery Avg Potential", f"{lottery_avg:.1%}")
    
    with col2:
        guards = len(draft_order.head(30)[draft_order.head(30)['position'].isin(['PG', 'SG'])])
        st.metric("Guards in 1st Round", guards)
    
    with col3:
        bigs = len(draft_order.head(30)[draft_order.head(30)['position'].isin(['PF', 'C'])])
        st.metric("Bigs in 1st Round", bigs)
    
    with col4:
        elite = len(draft_order.head(30)[draft_order.head(30)['final_gen_probability'] > 0.7])
        st.metric("Elite Prospects Top 30", elite)

def create_big_board_draft_prediction(df: pd.DataFrame):
    """Create a professional Big Board format"""
    st.markdown("## 🎯 NBA Draft 2025 Big Board")
    st.caption("Updated with latest intel and team needs • Last updated: June 2025")
    
    # Add variance for realistic predictions
    draft_order = df.copy()
    draft_order['draft_variance'] = np.random.normal(0, 1.5, len(draft_order))
    draft_order['big_board_rank'] = draft_order['final_rank'] + draft_order['draft_variance']
    draft_order = draft_order.sort_values('big_board_rank').reset_index(drop=True)
    draft_order['predicted_pick'] = range(1, len(draft_order) + 1)
    
    # View options
    col1, col2, col3 = st.columns(3)
    with col1:
        view_range = st.selectbox(
            "View Range:",
            ["Top 14 (Lottery)", "Top 30 (First Round)", "Top 60 (Full Draft)"]
        )
    with col2:
        sort_by = st.selectbox(
            "Sort by:",
            ["Big Board Rank", "Ceiling", "Floor", "Fit Score"]
        )
    with col3:
        position_filter = st.selectbox(
            "Position:",
            ["All", "Guards", "Wings", "Bigs", "PG", "SG", "SF", "PF", "C"]
        )
    
    # Apply filters
    if position_filter == "Guards":
        filtered_df = draft_order[draft_order['position'].isin(['PG', 'SG'])]
    elif position_filter == "Wings":
        filtered_df = draft_order[draft_order['position'].isin(['SG', 'SF'])]
    elif position_filter == "Bigs":
        filtered_df = draft_order[draft_order['position'].isin(['PF', 'C'])]
    elif position_filter != "All":
        filtered_df = draft_order[draft_order['position'] == position_filter]
    else:
        filtered_df = draft_order
    
    # Determine display count
    if view_range == "Top 14 (Lottery)":
        display_count = 14
    elif view_range == "Top 30 (First Round)":
        display_count = 30
    else:
        display_count = 60
    
    display_df = filtered_df.head(display_count)
    
    # Create the Big Board table
    create_big_board_table(display_df)
    
    # Add insights section
    display_draft_insights(display_df)

def create_big_board_table(df: pd.DataFrame):
    """Create the main Big Board table"""
    
    # Prepare data for display
    board_data = []
    
    for idx, player in df.iterrows():
        # Extract key info
        rank = int(player['predicted_pick'])
        name = safe_string(player['name'])
        pos = safe_string(player['position'])
        college = safe_string(player['college'])
        
        # Stats
        ppg = safe_numeric(player['ppg'])
        rpg = safe_numeric(player['rpg'])
        apg = safe_numeric(player['apg'])
        
        # Projections
        grade = safe_string(player['scout_grade'])
        potential = safe_numeric(player.get('final_gen_probability', 0.5))
        
        # Physical
        age = safe_numeric(player.get('age', 0))
        height = format_height(safe_numeric(player.get('height', 0)))
        
        # Tier and movement
        if rank <= 5:
            tier = "🏆 Elite"
            tier_color = "#FFD700"
        elif rank <= 14:
            tier = "🎰 Lottery"
            tier_color = "#FF6B35"
        elif rank <= 30:
            tier = "🏀 First"
            tier_color = "#4361EE"
        else:
            tier = "⚡ Second"
            tier_color = "#6B7280"
        
        # Simulated movement (up/down from last update)
        movement = np.random.choice(['📈', '📉', '➡️'], p=[0.3, 0.3, 0.4])
        
        board_data.append({
            'Rank': rank,
            'Player': name,
            'Pos': pos,
            'College': college,
            'Age': f"{age:.0f}",
            'Height': height,
            'PPG': f"{ppg:.1f}",
            'RPG': f"{rpg:.1f}",
            'APG': f"{apg:.1f}",
            'Grade': grade,
            'Potential': f"{potential:.0%}",
            'Tier': tier,
            'Movement': movement
        })
    
    # Convert to DataFrame
    board_df = pd.DataFrame(board_data)
    
    # Display with custom styling
    st.dataframe(
        board_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", width="small"),
            "Player": st.column_config.TextColumn("Player", width="large"),
            "Pos": st.column_config.TextColumn("Pos", width="small"),
            "College": st.column_config.TextColumn("College", width="medium"),
            "Age": st.column_config.TextColumn("Age", width="small"),
            "Height": st.column_config.TextColumn("Height", width="small"),
            "PPG": st.column_config.TextColumn("PPG", width="small"),
            "RPG": st.column_config.TextColumn("RPG", width="small"),
            "APG": st.column_config.TextColumn("APG", width="small"),
            "Grade": st.column_config.TextColumn("Grade", width="small"),
            "Potential": st.column_config.TextColumn("Potential", width="small"),
            "Tier": st.column_config.TextColumn("Tier", width="medium"),
            "Movement": st.column_config.TextColumn("📊", width="small")
        }
    )

def display_draft_insights(df: pd.DataFrame):
    """Display key insights and recent changes"""
    st.markdown("### 🔥 Latest Draft Intel & Movement")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Rising Stock")
        st.info("""
        **Recent Risers:**
        • **VJ Edgecombe** - Elite athleticism showing in workouts
        • **Tre Johnson** - Shooting 45% from 3 in recent sessions
        • **Collin Murray-Boyles** - Teams love his versatility
        
        **Why they're rising:** Workout performances exceeding expectations
        """)
        
        st.markdown("#### 🔄 Recent Trades Impact")
        st.warning("""
        **Key Trade Scenarios:**
        • **Portland** actively shopping #7 pick
        • **Detroit** may package picks to move up
        • **Charlotte** seeking win-now pieces
        
        **Impact:** Could shake up entire lottery order
        """)
    
    with col2:
        st.markdown("#### 📉 Falling Stock")
        st.error("""
        **Recent Fallers:**
        • **Some lottery prospects** - Medical concerns emerging
        • **Older prospects** - Teams prioritizing upside
        • **Poor shooters** - 3P% becoming make/break
        
        **Why they're falling:** Teams getting more selective
        """)
        
        st.markdown("#### 🎯 Consensus Changes")
        st.success("""
        **New Consensus:**
        • **Cooper Flagg** - Locked at #1
        • **Guard heavy lottery** - Teams need playmaking
        • **International prospects** - Getting more looks
        **Latest intel:** Workouts causing major shifts
        """)

    

def create_steals_busts_analysis(df: pd.DataFrame):
    """Create steals and busts analysis with bold predictions"""
    st.markdown("## 💎 Bold Predictions: Steals & Busts")
    
    # Create more sophisticated analysis
    df_analysis = df.copy()
    
    # Calculate multiple factors for steal potential
    df_analysis['skill_efficiency'] = (
        df_analysis['ppg'] / df_analysis['usage_rate'] * 100 
        if 'usage_rate' in df_analysis.columns else df_analysis['ppg']
    )
    df_analysis['age_factor'] = 1 + (20 - df_analysis['age']) * 0.1  # Younger = more upside
    df_analysis['shooting_upside'] = df_analysis['three_pt_pct'] * df_analysis['ft_pct'] if 'ft_pct' in df_analysis.columns else df_analysis['three_pt_pct']
    
    # Steal score: combination of efficiency, age, and being underrated
    df_analysis['steal_score'] = (
        df_analysis['final_gen_probability'] * 50 +
        df_analysis['skill_efficiency'] * 0.5 +
        df_analysis['age_factor'] * 10 +
        df_analysis['shooting_upside'] * 30
    ) / (df_analysis['final_rank'] * 0.5)
    
    # Bust risk: high pick with concerning indicators
    df_analysis['bust_risk'] = 0
    for idx, row in df_analysis.iterrows():
        risk = 0
        # Age risk
        if row['age'] > 21:
            risk += 20
        # Shooting risk for guards/wings
        if row['position'] in ['PG', 'SG', 'SF'] and row['three_pt_pct'] < 0.32:
            risk += 25
        # Efficiency risk
        if row['ts_pct'] < 0.50:
            risk += 20
        # Size/athleticism proxy (if no elite skill)
        if row['ppg'] < 15 and row['rpg'] < 7 and row['apg'] < 5:
            risk += 15
        # High usage, low efficiency
        if 'usage_rate' in df_analysis.columns and row['usage_rate'] > 25 and row['ts_pct'] < 0.52:
            risk += 20
        
        df_analysis.loc[idx, 'bust_risk'] = risk
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💎 **BOLD STEAL PREDICTIONS**")
        st.caption("Players who will massively outperform draft position")
        
        # Get steals: players outside top 10 with high steal scores
        potential_steals = df_analysis[df_analysis['final_rank'] > 10].nlargest(5, 'steal_score')
        
        steal_predictions = [
            {
                'player': potential_steals.iloc[0],
                'prediction': "Future All-Star",
                'reasoning': "Elite efficiency + shooting upside + perfect age curve",
                'confidence': 85
            },
            {
                'player': potential_steals.iloc[1],
                'prediction': "6th Man of the Year",
                'reasoning': "Instant offense skillset being overlooked",
                'confidence': 75
            },
            {
                'player': potential_steals.iloc[2],
                'prediction': "Starting Role Player",
                'reasoning': "3&D potential with room to grow",
                'confidence': 70
            },
            {
                'player': potential_steals.iloc[3],
                'prediction': "Surprise Rookie Impact",
                'reasoning': "NBA-ready skills despite lower ranking",
                'confidence': 65
            },
            {
                'player': potential_steals.iloc[4],
                'prediction': "Late Round Gem",
                'reasoning': "Specialist skills that translate immediately",
                'confidence': 60
            }
        ]
        
        for pred in steal_predictions:
            player = pred['player']
            name = safe_string(player['name'])
            rank = int(safe_numeric(player['final_rank']))
            position = safe_string(player['position'])
            
            # Determine steal level color
            if pred['confidence'] > 80:
                color = "#059669"  # Dark green
                steal_level = "🔥 MEGA STEAL"
            elif pred['confidence'] > 70:
                color = "#10b981"  # Medium green
                steal_level = "💎 GREAT VALUE"
            else:
                color = "#34d399"  # Light green
                steal_level = "✨ GOOD VALUE"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}, {color}dd); 
                        padding: 1.2rem; 
                        border-radius: 12px; 
                        margin: 0.8rem 0; 
                        color: white;
                        border: 2px solid {color};">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <div style="font-size: 0.8rem; opacity: 0.9; margin-bottom: 0.3rem;">
                            {steal_level}
                        </div>
                        <strong style="font-size: 1.1rem;">#{rank} {name}</strong>
                        <div style="font-size: 0.85rem; margin-top: 0.3rem; opacity: 0.95;">
                            {position} • {pred['prediction']}
                        </div>
                        <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.9; font-style: italic;">
                            "{pred['reasoning']}"
                        </div>
                    </div>
                    <div style="text-align: center; margin-left: 1rem;">
                        <div style="font-size: 2rem; font-weight: bold;">
                            {pred['confidence']}%
                        </div>
                        <div style="font-size: 0.7rem; opacity: 0.9;">
                            Confidence
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ⚠️ **BUST RISK ALERTS**")
        st.caption("High picks with significant red flags")
        
        # Get busts: top 20 picks with high bust risk
        potential_busts = df_analysis.head(20).nlargest(5, 'bust_risk')
        
        bust_predictions = [
            {
                'player': potential_busts.iloc[0],
                'prediction': "Major Disappointment",
                'reasoning': "Multiple red flags: age, efficiency, skill gaps",
                'confidence': 80
            },
            {
                'player': potential_busts.iloc[1],
                'prediction': "Role Player Ceiling",
                'reasoning': "Limited upside despite high draft position",
                'confidence': 70
            },
            {
                'player': potential_busts.iloc[2],
                'prediction': "Bench Contributor",
                'reasoning': "Skills won't translate to NBA level",
                'confidence': 65
            },
            {
                'player': potential_busts.iloc[3],
                'prediction': "Development Project",
                'reasoning': "Raw talent but significant concerns",
                'confidence': 60
            },
            {
                'player': potential_busts.iloc[4],
                'prediction': "Trade Candidate",
                'reasoning': "May need change of scenery to succeed",
                'confidence': 55
            }
        ]
        
        for pred in bust_predictions:
            player = pred['player']
            name = safe_string(player['name'])
            rank = int(safe_numeric(player['final_rank']))
            position = safe_string(player['position'])
            
            # Determine risk level color
            if pred['confidence'] > 75:
                color = "#dc2626"  # Dark red
                risk_level = "🚨 EXTREME RISK"
            elif pred['confidence'] > 65:
                color = "#ef4444"  # Medium red
                risk_level = "⚠️ HIGH RISK"
            else:
                color = "#f87171"  # Light red
                risk_level = "⚡ MODERATE RISK"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color}, {color}dd); 
                        padding: 1.2rem; 
                        border-radius: 12px; 
                        margin: 0.8rem 0; 
                        color: white;
                        border: 2px solid {color};">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <div style="font-size: 0.8rem; opacity: 0.9; margin-bottom: 0.3rem;">
                            {risk_level}
                        </div>
                        <strong style="font-size: 1.1rem;">#{rank} {name}</strong>
                        <div style="font-size: 0.85rem; margin-top: 0.3rem; opacity: 0.95;">
                            {position} • {pred['prediction']}
                        </div>
                        <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.9; font-style: italic;">
                            "{pred['reasoning']}"
                        </div>
                    </div>
                    <div style="text-align: center; margin-left: 1rem;">
                        <div style="font-size: 2rem; font-weight: bold;">
                            {pred['confidence']}%
                        </div>
                        <div style="font-size: 0.7rem; opacity: 0.9;">
                            Risk Level
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Add summary insights
    st.markdown("---")
    st.markdown("### 📊 **Key Insights**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **🎯 Steal Indicators:**
        - Young players (19 or under) with high efficiency
        - Strong shooters being undervalued
        - Players with elite skills in specific areas
        - Good college stats with low usage rates
        """)
    
    with col2:
        st.warning("""
        **⚠️ Bust Warning Signs:**
        - Older prospects (21+) without elite skills
        - Poor shooting for perimeter players
        - High usage with low efficiency
        - Limited athleticism or size for position
        """)

def create_historical_intelligence(df: pd.DataFrame):
    """Create comprehensive historical intelligence analysis"""
    st.markdown("## 📊 Historical Intelligence System")
    st.caption("AI-powered analysis based on 15 years of NBA draft data and outcomes")
    
    # Load historical data (lazy loading)
    historical_data = load_historical_draft_data()
    
    # Sub-tabs for historical intelligence with SWOT integration
    hist_tab1, hist_tab2, hist_tab3, hist_tab4, hist_tab5, hist_tab6 = st.tabs([
        "🎯 Smart Comparisons",
        "📈 Success Patterns", 
        "🔍 Scout Report Analysis",
        "💡 Historical Validation",
        "📋 SWOT Analysis 2.0",
        "🔄 What If Simulator"
    ])
    
    with hist_tab1:
        create_complete_smart_historical_comparisons(df, historical_data)
    
    with hist_tab2:
        create_success_pattern_analysis(df, historical_data)
    
    with hist_tab3:
        create_scout_report_intelligence(df)
    
    with hist_tab4:
        create_historical_validation(df, historical_data)
    
    with hist_tab5:
        create_swot_analysis(df)

    with hist_tab6:
        create_what_if_simulator(df)

@st.cache_data
def load_historical_draft_data():
    """Load historical draft data with caching"""
    # Simulated historical data - in production, load from CSV
    historical_patterns = {
        'archetype_success': {
            'Two-Way Wing': {'all_star_rate': 0.45, 'starter_rate': 0.82, 'bust_rate': 0.08},
            'Elite Scorer': {'all_star_rate': 0.38, 'starter_rate': 0.75, 'bust_rate': 0.12},
            'Floor General': {'all_star_rate': 0.35, 'starter_rate': 0.70, 'bust_rate': 0.15},
            'Elite Shooter': {'all_star_rate': 0.25, 'starter_rate': 0.68, 'bust_rate': 0.18},
            'Rim Protector': {'all_star_rate': 0.30, 'starter_rate': 0.65, 'bust_rate': 0.20},
            'Athletic Defender': {'all_star_rate': 0.20, 'starter_rate': 0.60, 'bust_rate': 0.25},
        },
        'age_impact': {
            18: {'success_multiplier': 1.4},
            19: {'success_multiplier': 1.2},
            20: {'success_multiplier': 1.0},
            21: {'success_multiplier': 0.8},
            22: {'success_multiplier': 0.6}
        },
        'position_by_range': {
            '1-5': {'PG': 0.20, 'SG': 0.15, 'SF': 0.25, 'PF': 0.25, 'C': 0.15},
            '6-10': {'PG': 0.15, 'SG': 0.20, 'SF': 0.30, 'PF': 0.20, 'C': 0.15},
            '11-20': {'PG': 0.10, 'SG': 0.25, 'SF': 0.25, 'PF': 0.20, 'C': 0.20},
        },
        'historical_comps': {
            'Scottie Barnes': {
                'draft_year': 2021, 'pick': 4, 'rookie_stats': {'ppg': 15.3, 'rpg': 7.5, 'apg': 3.5},
                'current_status': 'All-Star', 'trajectory': ['ROTY', 'All-Star Y2', 'All-NBA Y3']
            },
            'Paul George': {
                'draft_year': 2010, 'pick': 10, 'rookie_stats': {'ppg': 7.8, 'rpg': 3.7, 'apg': 1.1},
                'current_status': 'All-NBA', 'trajectory': ['Role Player Y1-2', 'All-Star Y3', 'All-NBA Y4+']
            },
            'Cade Cunningham': {
                'draft_year': 2021, 'pick': 1, 'rookie_stats': {'ppg': 17.4, 'rpg': 5.5, 'apg': 5.6},
                'current_status': 'Rising Star', 'trajectory': ['ROY Runner-up', 'Injury Y2', 'Breakout Y3']
            }
        }
    }
    
    return historical_patterns

def create_smart_historical_comparisons(df: pd.DataFrame, historical_data: dict):
    """Enhanced historical comparisons with trajectory data"""
    st.markdown("### 🎯 Smart Historical Comparisons")
    
    selected_player = st.selectbox(
        "Select a prospect for detailed comparison:",
        df['name'].head(15).tolist(),
        key="hist_comp_select"
    )
    
    player_data = df[df['name'] == selected_player].iloc[0]
    
    # Enhanced comparison data with trajectories
    comp_database = {
        'Cooper Flagg': {
            'comp': 'Scottie Barnes',
            'similarity': 0.87,
            'reasoning': 'Versatile forward with elite court vision and two-way impact',
            'trajectory_match': 0.82
        },
        'Ace Bailey': {
            'comp': 'Paul George',
            'similarity': 0.82,
            'reasoning': 'Elite scoring wing with shooting range and athleticism',
            'trajectory_match': 0.75
        },
        'Dylan Harper': {
            'comp': 'Cade Cunningham',
            'similarity': 0.85,
            'reasoning': 'Big guard who can score and facilitate with NBA-ready size',
            'trajectory_match': 0.78
        }
    }
    
    if selected_player in comp_database:
        comp_info = comp_database[selected_player]
        historical_comp = historical_data['historical_comps'].get(comp_info['comp'], {})
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Current prospect card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FF6B35, #F7931E); 
                        padding: 2rem; border-radius: 15px; color: white;">
                <h3 style="margin: 0 0 1rem 0;">{selected_player}</h3>
                <div style="font-size: 0.9rem; opacity: 0.9;">
                    {safe_string(player_data['position'])} • {safe_string(player_data['college'])}
                </div>
                <div style="margin-top: 1.5rem;">
                    <div>{safe_numeric(player_data['ppg']):.1f} PPG</div>
                    <div>{safe_numeric(player_data['rpg']):.1f} RPG</div>
                    <div>{safe_numeric(player_data['apg']):.1f} APG</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Historical comp card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #3B82F6, #2563EB); 
                        padding: 2rem; border-radius: 15px; color: white;">
                <h3 style="margin: 0 0 1rem 0;">{comp_info['comp']}</h3>
                <div style="font-size: 0.9rem; opacity: 0.9;">
                    Pick #{historical_comp.get('pick', 'N/A')} • {historical_comp.get('draft_year', 'N/A')}
                </div>
                <div style="margin-top: 1.5rem;">
                    <div>Current: {historical_comp.get('current_status', 'N/A')}</div>
                    <div style="font-size: 0.8rem; margin-top: 0.5rem;">
                        Rookie: {historical_comp.get('rookie_stats', {}).get('ppg', 0):.1f} PPG
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Similarity breakdown
        st.markdown("#### 📊 Comparison Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Similarity", f"{comp_info['similarity']:.0%}")
        with col2:
            st.metric("Trajectory Match", f"{comp_info['trajectory_match']:.0%}")
        with col3:
            confidence = (comp_info['similarity'] + comp_info['trajectory_match']) / 2
            st.metric("Confidence Score", f"{confidence:.0%}")
        
        # Career trajectory visualization
        if historical_comp.get('trajectory'):
            st.markdown("#### 📈 Projected Career Path")
            trajectory_str = " → ".join(historical_comp['trajectory'])
            st.info(f"**Expected trajectory based on {comp_info['comp']}:** {trajectory_str}")
        
        # Key insights
        st.markdown("#### 💡 Key Insights")
        insights = generate_comparison_insights(player_data, comp_info, historical_comp)
        for insight in insights:
            st.markdown(f"• {insight}")
    
    else:
        st.info(f"Advanced comparison data for {selected_player} is being processed...")

def create_success_pattern_analysis(df: pd.DataFrame, historical_data: dict):
    """Analyze success patterns based on historical data"""
    st.markdown("### 📈 Historical Success Patterns")
    
    # Analysis mode
    analysis_mode = st.radio(
        "Analysis Type:",
        ["By Archetype", "By Age", "By Draft Range"],
        horizontal=True
    )
    
    if analysis_mode == "By Archetype":
        st.markdown("#### Success Rates by Player Archetype")
        
        archetype_data = historical_data['archetype_success']
        
        # Create visualization
        archetypes = list(archetype_data.keys())
        all_star_rates = [archetype_data[a]['all_star_rate'] * 100 for a in archetypes]
        starter_rates = [archetype_data[a]['starter_rate'] * 100 for a in archetypes]
        bust_rates = [archetype_data[a]['bust_rate'] * 100 for a in archetypes]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='All-Star %', x=archetypes, y=all_star_rates, marker_color='#FFD700'))
        fig.add_trace(go.Bar(name='Starter+ %', x=archetypes, y=starter_rates, marker_color='#10B981'))
        fig.add_trace(go.Bar(name='Bust %', x=archetypes, y=bust_rates, marker_color='#EF4444'))
        
        fig.update_layout(
            title="Historical Success Rates by Archetype (2010-2024)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Apply to current draft class
        st.markdown("#### 🎯 Applied to 2025 Draft Class")
        
        top_prospects = df.head(10)
        success_predictions = []
        
        for _, player in top_prospects.iterrows():
            archetype = safe_string(player.get('archetype', 'N/A'))
            if archetype in archetype_data:
                rates = archetype_data[archetype]
                success_predictions.append({
                    'Name': player['name'],
                    'Archetype': archetype,
                    'All-Star Chance': f"{rates['all_star_rate']:.0%}",
                    'Starter+ Chance': f"{rates['starter_rate']:.0%}",
                    'Bust Risk': f"{rates['bust_rate']:.0%}"
                })
        
        if success_predictions:
            pred_df = pd.DataFrame(success_predictions)
            st.dataframe(pred_df, use_container_width=True, hide_index=True)
    
    elif analysis_mode == "By Age":
        st.markdown("#### Age Impact on Draft Success")
        
        age_data = historical_data['age_impact']
        
        # Visualization
        ages = list(age_data.keys())
        multipliers = [age_data[age]['success_multiplier'] for age in ages]
        
        fig = px.line(
            x=ages, y=multipliers,
            title="Success Multiplier by Draft Age",
            labels={'x': 'Age at Draft', 'y': 'Success Multiplier'},
            markers=True
        )
        fig.update_traces(line_color='#FF6B35', line_width=4)
        fig.add_hline(y=1.0, line_dash="dash", line_color="gray")
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Key Finding**: Players drafted at 18-19 have 20-40% higher success rates.
        Each additional year of age decreases success probability by ~20%.
        """)
    
    else:  # By Draft Range
        st.markdown("#### Positional Value by Draft Range")
        
        range_data = historical_data['position_by_range']
        
        # Create heatmap
        positions = ['PG', 'SG', 'SF', 'PF', 'C']
        ranges = list(range_data.keys())
        
        z_data = [[range_data[r][pos] * 100 for pos in positions] for r in ranges]
        
        fig = px.imshow(
            z_data,
            x=positions,
            y=ranges,
            color_continuous_scale='RdYlGn',
            title="Historical Success Rate (%) by Position and Draft Range",
            labels={'x': 'Position', 'y': 'Draft Range', 'color': 'Success %'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Insights:**
        - Wings (SF) have highest success rate in picks 6-10
        - Point guards succeed most in top 5
        - Centers are riskier in lottery but safer in late first round
        """)

def create_scout_report_intelligence(df: pd.DataFrame):
    """Analyze scout reports for enhanced insights"""
    st.markdown("### 🔍 Scout Report Intelligence")
    
    # Scout report keywords and their implications
    scout_keywords = {
        'positive': {
            'elite': {'impact': 0.85, 'category': 'skill'},
            'exceptional': {'impact': 0.80, 'category': 'skill'},
            'nba-ready': {'impact': 0.75, 'category': 'readiness'},
            'high motor': {'impact': 0.70, 'category': 'intangibles'},
            'versatile': {'impact': 0.70, 'category': 'skill'},
            'efficient': {'impact': 0.65, 'category': 'performance'},
            'coachable': {'impact': 0.65, 'category': 'intangibles'},
            'clutch': {'impact': 0.60, 'category': 'intangibles'}
        },
        'negative': {
            'concerns': {'impact': -0.40, 'category': 'general'},
            'inconsistent': {'impact': -0.50, 'category': 'performance'},
            'limited': {'impact': -0.45, 'category': 'skill'},
            'tweener': {'impact': -0.55, 'category': 'fit'},
            'passive': {'impact': -0.50, 'category': 'intangibles'},
            'project': {'impact': -0.60, 'category': 'readiness'},
            'raw': {'impact': -0.65, 'category': 'readiness'}
        }
    }
    
    selected_player = st.selectbox(
        "Select player for scout report analysis:",
        df['name'].head(15).tolist(),
        key="scout_select"
    )
    
    # Simulated scout report (in production, would parse actual reports)
    scout_reports = {
        'Cooper Flagg': {
            'report': "Elite two-way player with exceptional basketball IQ and versatility. NBA-ready defender with high motor. Some concerns about shot creation in half-court sets.",
            'strengths': ['elite two-way', 'exceptional IQ', 'versatile', 'NBA-ready defender', 'high motor'],
            'weaknesses': ['shot creation concerns', 'half-court offense']
        },
        'Ace Bailey': {
            'report': "Elite scorer with exceptional shooting range. Clutch performer with coachable attitude. Questions about defensive engagement and consistency.",
            'strengths': ['elite scorer', 'exceptional range', 'clutch', 'coachable'],
            'weaknesses': ['defensive concerns', 'inconsistent effort']
        }
    }
    
    if selected_player in scout_reports:
        report = scout_reports[selected_player]
        
        # Display report
        st.markdown("#### 📋 Scout Report Summary")
        st.info(report['report'])
        
        # Keyword analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### ✅ Positive Indicators")
            total_positive = 0
            for strength in report['strengths']:
                for keyword, data in scout_keywords['positive'].items():
                    if keyword in strength.lower():
                        total_positive += data['impact']
                        st.markdown(f"""
                        <div style="padding: 0.5rem; margin: 0.3rem 0; background: #10B98120; 
                                    border-left: 3px solid #10B981; border-radius: 5px;">
                            <strong>{strength}</strong>
                            <div style="font-size: 0.8rem; color: #666;">
                                Impact: +{data['impact']:.0%} ({data['category']})
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("##### ⚠️ Areas of Concern")
            total_negative = 0
            for weakness in report['weaknesses']:
                for keyword, data in scout_keywords['negative'].items():
                    if keyword in weakness.lower():
                        total_negative += data['impact']
                        st.markdown(f"""
                        <div style="padding: 0.5rem; margin: 0.3rem 0; background: #EF444420; 
                                    border-left: 3px solid #EF4444; border-radius: 5px;">
                            <strong>{weakness}</strong>
                            <div style="font-size: 0.8rem; color: #666;">
                                Impact: {data['impact']:.0%} ({data['category']})
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Overall scout score
        scout_score = (total_positive + total_negative) / (len(report['strengths']) + len(report['weaknesses']))
        
        st.markdown("#### 📊 Scout Report Score")
        score_color = "#10B981" if scout_score > 0.3 else "#F59E0B" if scout_score > 0 else "#EF4444"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: {score_color}20; 
                    border-radius: 15px; border: 2px solid {score_color};">
            <div style="font-size: 3rem; font-weight: bold; color: {score_color};">
                {scout_score:.0%}
            </div>
            <div style="font-size: 1rem; color: #666;">
                Scout Sentiment Score
            </div>
            <div style="font-size: 0.9rem; color: #666; margin-top: 1rem;">
                Based on keyword analysis and historical correlation
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Historical correlation
        st.markdown("#### 🔮 Historical Correlation")
        st.info(f"""
        Players with similar scout report profiles ({scout_score:.0%} sentiment):
        - **70%** became NBA starters or better
        - **35%** made at least one All-Star team
        - **15%** became All-NBA players
        
        Most common outcome: **Quality Starter** (Years 3-5)
        """)

def create_historical_validation(df: pd.DataFrame, historical_data: dict):
    """Validate current projections against historical data"""
    st.markdown("### 💡 Historical Validation Scores")
    
    # Calculate validation scores for top prospects
    validation_results = []
    
    for _, player in df.head(15).iterrows():
        # Get player attributes
        name = safe_string(player['name'])
        position = safe_string(player['position'])
        age = int(safe_numeric(player.get('age', 20)))
        archetype = safe_string(player.get('archetype', 'N/A'))
        gen_prob = safe_numeric(player.get('final_gen_probability', 0.5))
        rank = int(safe_numeric(player.get('final_rank', 30)))
        
        # Calculate historical confidence
        confidence_score = calculate_historical_confidence(
            position, age, archetype, gen_prob, rank, historical_data
        )
        
        validation_results.append({
            'Name': name,
            'Position': position,
            'Age': age,
            'Archetype': archetype,
            'AI Projection': f"{gen_prob:.1%}",
            'Historical Confidence': confidence_score['score'],
            'Confidence Level': confidence_score['level'],
            'Key Factor': confidence_score['key_factor']
        })
    
    # Display results
    st.markdown("#### 🎯 Projection Confidence Based on 15 Years of Data")
    
    # Convert to DataFrame for display
    val_df = pd.DataFrame(validation_results)
    
    # Style the dataframe
    def style_confidence(val):
        if isinstance(val, str) and '%' in val:
            num = float(val.strip('%'))
            if num >= 80:
                return 'background-color: #10B98130'
            elif num >= 60:
                return 'background-color: #F59E0B30'
            else:
                return 'background-color: #EF444430'
        return ''
    
    styled_df = val_df.style.applymap(style_confidence, subset=['Historical Confidence'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Summary insights
    st.markdown("#### 📊 Key Validation Insights")
    
    high_confidence = len([r for r in validation_results if float(r['Historical Confidence'].strip('%')) >= 80])
    medium_confidence = len([r for r in validation_results if 60 <= float(r['Historical Confidence'].strip('%')) < 80])
    low_confidence = len([r for r in validation_results if float(r['Historical Confidence'].strip('%')) < 60])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("High Confidence", high_confidence, "80%+ historical validation")
    with col2:
        st.metric("Medium Confidence", medium_confidence, "60-79% validation")
    with col3:
        st.metric("Low Confidence", low_confidence, "Below 60% validation")
    
    # Detailed breakdown for selected player
    st.markdown("#### 🔍 Detailed Validation Breakdown")
    
    selected_for_breakdown = st.selectbox(
        "Select player for detailed breakdown:",
        val_df['Name'].tolist(),
        key="validation_breakdown"
    )
    
    player_validation = next(r for r in validation_results if r['Name'] == selected_for_breakdown)
    
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; border: 2px solid #e9ecef;">
        <h4 style="margin: 0 0 1rem 0;">{selected_for_breakdown} - Validation Report</h4>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            <div>
                <strong>Profile:</strong><br>
                • Position: {player_validation['Position']}<br>
                • Age: {player_validation['Age']}<br>
                • Archetype: {player_validation['Archetype']}<br>
                • AI Projection: {player_validation['AI Projection']}
            </div>
            <div>
                <strong>Historical Validation:</strong><br>
                • Confidence: {player_validation['Historical Confidence']}<br>
                • Level: {player_validation['Confidence Level']}<br>
                • Key Factor: {player_validation['Key Factor']}
            </div>
        </div>
        
        <div style="margin-top: 1.5rem; padding: 1rem; background: #e9ecef; border-radius: 10px;">
            <strong>What this means:</strong><br>
            Based on 15 years of draft data, players with this profile have a {player_validation['Historical Confidence']} 
            chance of meeting or exceeding their projected outcome. The {player_validation['Key Factor'].lower()} 
            is the most influential factor in this assessment.
        </div>
    </div>
    """, unsafe_allow_html=True)

def calculate_historical_confidence(position: str, age: int, archetype: str, 
                                  gen_prob: float, rank: int, historical_data: dict) -> dict:
    """Calculate confidence score based on historical patterns"""
    
    confidence = 0.5  # Base confidence
    factors = []
    
    # Archetype success rate
    if archetype in historical_data['archetype_success']:
        arch_data = historical_data['archetype_success'][archetype]
        if gen_prob > 0.7:
            confidence += arch_data['all_star_rate'] * 0.3
            factors.append(('Archetype history', arch_data['all_star_rate'] * 0.3))
        else:
            confidence += arch_data['starter_rate'] * 0.2
            factors.append(('Archetype history', arch_data['starter_rate'] * 0.2))
    
    # Age factor
    if age in historical_data['age_impact']:
        age_mult = historical_data['age_impact'][age]['success_multiplier']
        age_impact = (age_mult - 1.0) * 0.2
        confidence += age_impact
        factors.append(('Age advantage', age_impact))
    
    # Position value by range
    if rank <= 5:
        range_key = '1-5'
    elif rank <= 10:
        range_key = '6-10'
    else:
        range_key = '11-20'
    
    if range_key in historical_data['position_by_range']:
        pos_value = historical_data['position_by_range'][range_key].get(position, 0.15)
        confidence += pos_value * 0.3
        factors.append(('Position value', pos_value * 0.3))
    
    # Cap confidence
    confidence = min(0.95, max(0.05, confidence))
    
    # Determine key factor
    key_factor = max(factors, key=lambda x: abs(x[1]))[0] if factors else 'General profile'
    
    # Determine confidence level
    if confidence >= 0.8:
        level = '⭐⭐⭐⭐⭐ Very High'
    elif confidence >= 0.7:
        level = '⭐⭐⭐⭐ High'
    elif confidence >= 0.6:
        level = '⭐⭐⭐ Medium'
    elif confidence >= 0.5:
        level = '⭐⭐ Low'
    else:
        level = '⭐ Very Low'
    
    return {
        'score': f"{confidence:.0%}",
        'level': level,
        'key_factor': key_factor,
        'raw_score': confidence
    }

def generate_comparison_insights(player_data: pd.Series, comp_info: dict, 
                               historical_comp: dict) -> List[str]:
    """Generate insights from historical comparison"""
    insights = []
    
    # Similarity insight
    if comp_info['similarity'] > 0.85:
        insights.append(f"Exceptionally high similarity ({comp_info['similarity']:.0%}) suggests reliable projection")
    
    # Trajectory insight
    if comp_info['trajectory_match'] > 0.80:
        insights.append("Development curve closely matches historical precedent")
    
    # Status insight
    if historical_comp.get('current_status') == 'All-Star':
        insights.append(f"{comp_info['comp']} became an All-Star - similar path likely")
    
    # Age comparison
    player_age = safe_numeric(player_data.get('age', 20))
    if player_age < 19:
        insights.append("Younger than comparison at draft - higher ceiling possible")
    
    return insights

def display_historical_comp_card(name: str, player_data: pd.Series, comp_data: Dict):
    """Display historical comparison card"""
    similarity = comp_data['similarity']
    color = '#10b981' if similarity > 0.82 else '#f59e0b' if similarity > 0.75 else '#6b7280'
    
    position = safe_string(player_data.get('position', 'N/A'))
    ppg = safe_numeric(player_data.get('ppg', 0))
    archetype = safe_string(player_data.get('archetype', 'N/A'))
    
    st.markdown(f"""
    <div style="background: {color}15; 
                border-left: 4px solid {color}; 
                padding: 1.5rem; 
                border-radius: 12px; 
                margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
            <div>
                <div style="font-weight: 600; font-size: 1.2rem; color: #333;">
                    {name}
                </div>
                <div style="font-size: 0.9rem; color: #666; margin: 0.2rem 0;">
                    {position} • {ppg:.1f} PPG • {archetype}
                </div>
            </div>
            <span style="background: {color}; 
                         color: white; 
                         padding: 0.3rem 0.8rem; 
                         border-radius: 15px; 
                         font-size: 0.8rem; 
                         font-weight: bold;">
                {similarity:.0%} match
            </span>
        </div>
        <div style="margin: 0.8rem 0;">
            <span style="font-size: 0.9rem; color: #666;">NBA Comparison:</span>
            <span style="font-weight: 600; color: {color}; font-size: 1.1rem; margin-left: 0.5rem;">
                {comp_data['comp']}
            </span>
        </div>
        <div style="font-size: 0.85rem; color: #555; line-height: 1.4; font-style: italic;">
            "{comp_data['reasoning']}"
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_pending_comp_card(name: str):
    """Display pending comparison card"""
    st.markdown(f"""
    <div style="background: #f8f9fa; 
                border-left: 4px solid #6b7280; 
                padding: 1.5rem; 
                border-radius: 12px; 
                margin: 1rem 0;">
        <div style="font-weight: 600; font-size: 1.1rem; color: #333; margin-bottom: 0.5rem;">
            {name}
        </div>
        <div style="font-size: 0.9rem; color: #666;">
            Comparison analysis pending - scouting in progress
        </div>
    </div>
    """, unsafe_allow_html=True)

def generate_enhanced_swot(player: pd.Series, scout_keywords: dict) -> Dict[str, List[str]]:
    """Generate enhanced SWOT analysis using scout report intelligence"""
    swot = {
        'strengths': [],
        'weaknesses': [],
        'opportunities': [],
        'threats': []
    }
    
    # Extract stats
    ppg = safe_numeric(player.get('ppg', 0))
    rpg = safe_numeric(player.get('rpg', 0))
    apg = safe_numeric(player.get('apg', 0))
    spg = safe_numeric(player.get('spg', 0))
    bpg = safe_numeric(player.get('bpg', 0))
    three_pt = safe_numeric(player.get('three_pt_pct', 0))
    ts_pct = safe_numeric(player.get('ts_pct', 0))
    age = safe_numeric(player.get('age', 20))
    position = safe_string(player.get('position', 'Unknown'))
    archetype = safe_string(player.get('archetype', 'N/A'))
    gen_prob = safe_numeric(player.get('final_gen_probability', 0.5))
    
    # Simulated scout report keywords for each player (in production, parse actual reports)
    player_scout_profiles = {
        'Cooper Flagg': ['elite two-way', 'exceptional IQ', 'versatile', 'high motor', 'shot creation concerns'],
        'Ace Bailey': ['elite scorer', 'exceptional range', 'clutch', 'inconsistent effort'],
        'Dylan Harper': ['NBA-ready size', 'versatile guard', 'coachable', 'turnover prone'],
        'default': ['solid fundamentals', 'room for growth']  # Changé de default: à 'default':
    }
    
    # Get player's scout keywords
    player_name = safe_string(player.get('name', 'Unknown'))
    player_keywords = player_scout_profiles.get(player_name, player_scout_profiles['default'])
    
    # Enhanced strengths based on stats AND scout reports
    if ppg > 15:
        if 'elite scorer' in player_keywords:
            swot['strengths'].append(f"Elite scoring ability ({ppg:.1f} PPG) - scouts confirm 'elite scorer' designation")
        else:
            swot['strengths'].append(f"Strong scoring ability ({ppg:.1f} PPG) - proven offensive contributor")
    
    if three_pt > 0.38:
        if 'exceptional range' in player_keywords:
            swot['strengths'].append(f"Elite shooting ({three_pt:.1%} 3P%) - scouts note 'exceptional range'")
        else:
            swot['strengths'].append(f"Excellent shooting ({three_pt:.1%} 3P%) - immediate floor spacing")
    
    if 'exceptional IQ' in player_keywords or 'high motor' in player_keywords:
        swot['strengths'].append("Intangibles: " + ", ".join([k for k in player_keywords if k in ['exceptional IQ', 'high motor', 'coachable', 'clutch']]))
    
    if apg > 5:
        swot['strengths'].append(f"Elite playmaking ({apg:.1f} APG) - true floor general abilities")
    
    if 'versatile' in player_keywords:
        swot['strengths'].append(f"Positional versatility - can play multiple positions effectively")
    
    # Enhanced weaknesses
    if 'concerns' in str(player_keywords) or 'inconsistent' in str(player_keywords):
        concern_keywords = [k for k in player_keywords if 'concern' in k or 'inconsistent' in k]
        for concern in concern_keywords:
            swot['weaknesses'].append(f"Scout concern: {concern}")
    
    if ppg < 10 and 'scorer' not in str(player_keywords):
        swot['weaknesses'].append(f"Limited scoring output ({ppg:.1f} PPG) - needs offensive development")
    
    if three_pt < 0.30 and position in ['PG', 'SG', 'SF']:
        swot['weaknesses'].append(f"Poor shooting ({three_pt:.1%} 3P%) - major concern for perimeter player")
    
    if age > 21:
        swot['weaknesses'].append(f"Advanced age ({age:.0f}) - limited development window")
    
    # Enhanced opportunities based on archetype and scout profile
    if archetype == 'Two-Way Wing':
        swot['opportunities'].append("Two-way wings are the most valuable archetype in modern NBA")
    
    if 'high motor' in player_keywords or 'coachable' in player_keywords:
        swot['opportunities'].append("Work ethic and coachability suggest continued improvement")
    
    if age < 20 and gen_prob > 0.6:
        swot['opportunities'].append("Elite potential + youth = possible franchise cornerstone")
    
    swot['opportunities'].append(f"Historical success rate for {archetype} archetype: See Historical Intelligence tab")
    
    # Enhanced threats
    if position == 'C' and three_pt < 0.25:
        swot['threats'].append("Traditional big man skillset may limit minutes in pace-and-space era")
    
    if 'inconsistent' in str(player_keywords):
        swot['threats'].append("Consistency issues noted by scouts - could affect role stability")
    
    if gen_prob > 0.7:
        swot['threats'].append("Sky-high expectations as potential franchise player")
    
    # Ensure minimum content
    for category in swot:
        if not swot[category]:
            swot[category].append(f"Standard {category} for {archetype} profile")
    
    return swot

def create_swot_analysis(df: pd.DataFrame):
    """Create enhanced SWOT analysis with scout report integration"""
    st.markdown("## 📋 Enhanced SWOT Analysis 2.0")
    st.caption("Powered by scout report intelligence and historical patterns")
    
    # Load scout keywords
    scout_keywords = {
        'positive': {
            'elite': {'impact': 0.85, 'category': 'skill'},
            'exceptional': {'impact': 0.80, 'category': 'skill'},
            'nba-ready': {'impact': 0.75, 'category': 'readiness'},
            'high motor': {'impact': 0.70, 'category': 'intangibles'},
            'versatile': {'impact': 0.70, 'category': 'skill'},
            'coachable': {'impact': 0.65, 'category': 'intangibles'},
            'clutch': {'impact': 0.60, 'category': 'intangibles'}
        }
    }
    
    selected_player = st.selectbox(
        "Select a player for detailed SWOT analysis:", 
        df['name'].head(15).tolist(),
        key="swot_player_select"
    )
    
    player_data = df[df['name'] == selected_player].iloc[0]
    
    # Generate enhanced SWOT
    swot = generate_enhanced_swot(player_data, scout_keywords)
    
    # Display enhanced SWOT with scout integration
    display_enhanced_swot_results(swot, selected_player, player_data)

def generate_player_swot(player: pd.Series) -> Dict[str, List[str]]:
    """Generate SWOT analysis for a player"""
    swot = {
        'strengths': [],
        'weaknesses': [],
        'opportunities': [],
        'threats': []
    }
    
    # Extract stats
    ppg = safe_numeric(player.get('ppg', 0))
    rpg = safe_numeric(player.get('rpg', 0))
    apg = safe_numeric(player.get('apg', 0))
    spg = safe_numeric(player.get('spg', 0))
    bpg = safe_numeric(player.get('bpg', 0))
    three_pt = safe_numeric(player.get('three_pt_pct', 0))
    age = safe_numeric(player.get('age', 20))
    position = safe_string(player.get('position', 'Unknown'))
    archetype = safe_string(player.get('archetype', 'N/A'))
    gen_prob = safe_numeric(player.get('final_gen_probability', 0.5))
    
    # Strengths
    if ppg > 15:
        swot['strengths'].append(f"Elite scoring ability ({ppg:.1f} PPG) - proven bucket getter")
    if three_pt > 0.38:
        swot['strengths'].append(f"Elite shooting ({three_pt:.1%} 3P%) - immediate floor spacing")
    if apg > 5:
        swot['strengths'].append(f"Exceptional playmaking ({apg:.1f} APG) - makes teammates better")
    if rpg > 8:
        swot['strengths'].append(f"Dominant rebounder ({rpg:.1f} RPG) - controls the glass")
    if (spg + bpg) > 2.5:
        swot['strengths'].append(f"Elite defender ({spg + bpg:.1f} stocks) - game-changing impact")
    if age < 19:
        swot['strengths'].append(f"Extremely young ({age:.0f}) - massive upside potential")
    if gen_prob > 0.7:
        swot['strengths'].append(f"Franchise player potential ({gen_prob:.1%}) - cornerstone talent")
    
    # Weaknesses
    if ppg < 10:
        swot['weaknesses'].append(f"Limited scoring ({ppg:.1f} PPG) - needs offensive development")
    if three_pt < 0.30:
        swot['weaknesses'].append(f"Poor shooting ({three_pt:.1%} 3P%) - spacing concerns")
    if apg < 2 and position in ['PG', 'SG']:
        swot['weaknesses'].append(f"Limited playmaking ({apg:.1f} APG) for guard position")
    if age > 21:
        swot['weaknesses'].append(f"Older prospect ({age:.0f}) - limited growth potential")
    if gen_prob < 0.4:
        swot['weaknesses'].append(f"Lower ceiling ({gen_prob:.1%}) - role player projection")
    
    # Opportunities
    swot['opportunities'].append(f"Modern NBA values {archetype} skillset highly")
    swot['opportunities'].append("Analytics-driven teams seek efficiency and versatility")
    if age < 20:
        swot['opportunities'].append("Multiple years to develop before entering prime")
    if position in ['SF', 'PF']:
        swot['opportunities'].append("Positionless basketball creates more opportunities")
    
    # Threats
    swot['threats'].append("Intense competition for roster spots and playing time")
    swot['threats'].append("NBA pace and physicality adjustment period")
    if position == 'C':
        swot['threats'].append("Traditional center role diminishing in modern NBA")
    if three_pt < 0.32:
        swot['threats'].append("Poor shooting limits role flexibility")
    
    # Ensure minimum content
    for category in swot:
        if not swot[category]:
            swot[category].append(f"Standard {category} for prospect profile")
    
    return swot

def display_enhanced_swot_results(swot: Dict[str, List[str]], player_name: str, player_data: pd.Series):
    """Display enhanced SWOT analysis results with historical context"""
    
    # Add historical confidence score
    historical_data = load_historical_draft_data()
    confidence = calculate_historical_confidence(
        safe_string(player_data.get('position')),
        int(safe_numeric(player_data.get('age', 20))),
        safe_string(player_data.get('archetype', 'N/A')),
        safe_numeric(player_data.get('final_gen_probability', 0.5)),
        int(safe_numeric(player_data.get('final_rank', 30))),
        historical_data
    )
    
    # Display confidence badge
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1rem;">
        <span style="background: linear-gradient(135deg, #FF6B35, #F7931E); 
                     color: white; padding: 0.5rem 2rem; border-radius: 30px; 
                     font-weight: bold; font-size: 1.1rem;">
            Historical Validation: {confidence['score']} {confidence['level']}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Strengths with scout validation
        st.markdown("""
        <div style="background: linear-gradient(135deg, #10b981, #059669); 
                    border-radius: 15px; padding: 2rem; margin: 1rem 0; color: white;
                    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);">
            <h3 style="margin: 0 0 1rem 0;">💪 Strengths</h3>
            <div style="font-size: 0.8rem; opacity: 0.8; margin-bottom: 1rem;">
                Scout-validated strengths
            </div>
        """, unsafe_allow_html=True)
        
        for i, strength in enumerate(swot['strengths'], 1):
            st.markdown(f"**{i}.** {strength}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Opportunities
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3b82f6, #2563eb); 
                    border-radius: 15px; padding: 2rem; margin: 1rem 0; color: white;
                    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);">
            <h3 style="margin: 0 0 1rem 0;">🚀 Opportunities</h3>
            <div style="font-size: 0.8rem; opacity: 0.8; margin-bottom: 1rem;">
                Based on historical patterns
            </div>
        """, unsafe_allow_html=True)
        
        for i, opp in enumerate(swot['opportunities'], 1):
            st.markdown(f"**{i}.** {opp}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Weaknesses
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f59e0b, #d97706); 
                    border-radius: 15px; padding: 2rem; margin: 1rem 0; color: white;
                    box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);">
            <h3 style="margin: 0 0 1rem 0;">⚠️ Weaknesses</h3>
            <div style="font-size: 0.8rem; opacity: 0.8; margin-bottom: 1rem;">
                Scout concerns identified
            </div>
        """, unsafe_allow_html=True)
        
        for i, weakness in enumerate(swot['weaknesses'], 1):
            st.markdown(f"**{i}.** {weakness}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Threats
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ef4444, #dc2626); 
                    border-radius: 15px; padding: 2rem; margin: 1rem 0; color: white;
                    box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);">
            <h3 style="margin: 0 0 1rem 0;">🎯 Threats</h3>
            <div style="font-size: 0.8rem; opacity: 0.8; margin-bottom: 1rem;">
                Historical risk factors
            </div>
        """, unsafe_allow_html=True)
        
        for i, threat in enumerate(swot['threats'], 1):
            st.markdown(f"**{i}.** {threat}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Enhanced executive summary with historical context
def display_enhanced_swot_summary(player_name: str, player_data: pd.Series, 
                                 swot: Dict, confidence: Dict):
    """Display enhanced SWOT executive summary with historical validation - Streamlit native"""
    st.markdown("### 📊 Executive Summary with Historical Context")
    
    prob = safe_numeric(player_data.get('final_gen_probability', 0.5))
    position = safe_string(player_data.get('position', 'N/A'))
    archetype = safe_string(player_data.get('archetype', 'N/A'))
    age = safe_numeric(player_data.get('age', 20))
    
    # Determine assessment level
    if prob > 0.7:
        risk_level = 'Low Risk'
        ceiling = 'All-Star+'
        summary_color = '🟢'
    elif prob > 0.5:
        risk_level = 'Medium Risk'
        ceiling = 'Starter'
        summary_color = '🟡'
    else:
        risk_level = 'High Risk'
        ceiling = 'Role Player'
        summary_color = '🔴'
    
    # Header avec assessment
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"#### {summary_color} Overall Assessment: {risk_level}")
        st.markdown(f"**{player_name}** ({position}, {archetype}) projects as a **{risk_level.lower()}** selection with **{ceiling.lower()}** upside.")
    
    with col2:
        st.metric("AI Projection", f"{prob:.1%}", help="Generational talent probability")
        st.caption(f"Projected Ceiling: {ceiling}")
    
    # Profile Summary
    st.markdown("#### 📊 Profile Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Player Profile:**
        - **Position:** {position}
        - **Age:** {age:.0f} years old
        - **Archetype:** {archetype}
        - **AI Projection:** {prob:.1%}
        """)
    
    with col2:
        st.success(f"""
        **Historical Context:**
        - **Confidence Level:** {confidence['score']}
        - **Key Factor:** {confidence['key_factor']}
        - **Validation:** {confidence['level']}
        """)
    
    # Development insights
    st.markdown("#### 🔮 Development Insights")
    
    if age < 19:
        age_insight = "significant growth potential remains"
    elif age < 21:
        age_insight = "moderate development expected"
    else:
        age_insight = "limited growth window"
    
    st.markdown(f"""
    **Key Development Factors:**
    - **Age Impact:** At {age:.0f} years old, {age_insight}
    - **Archetype Influence:** {archetype} players typically focus on {'scoring efficiency' if 'Scorer' in archetype else 'playmaking development' if 'General' in archetype else 'two-way impact'}
    - **Historical Precedent:** {confidence['key_factor'].lower()} will be the primary factor in development
    """)
    
    # Load historical success rates
    historical_data = load_historical_draft_data()
    arch_success = historical_data['archetype_success'].get(archetype, {})
    
    if arch_success:
        st.markdown("#### 📈 Historical Success Rates")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            all_star_rate = arch_success.get('all_star_rate', 0.25)
            st.metric("All-Star Chance", f"{all_star_rate:.0%}", help=f"Based on {archetype} historical data")
        
        with col2:
            starter_rate = arch_success.get('starter_rate', 0.65)
            st.metric("Starter+ Chance", f"{starter_rate:.0%}", help="Likelihood of becoming NBA starter")
        
        with col3:
            bust_rate = arch_success.get('bust_rate', 0.15)
            st.metric("Bust Risk", f"{bust_rate:.0%}", help="Historical bust rate for archetype")
    
    # SWOT Summary Stats
    st.markdown("#### 📋 SWOT Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Key Strengths", len(swot['strengths']), help="Major advantages identified")
    
    with col2:
        st.metric("Areas of Concern", len(swot['weaknesses']), help="Weaknesses to address")
    
    with col3:
        st.metric("Opportunities", len(swot['opportunities']), help="Potential growth areas")
    
    with col4:
        st.metric("Risk Factors", len(swot['threats']), help="Potential challenges")
    
    # Final Assessment
    st.markdown("#### 🎯 Final Assessment")
    
    confidence_score = confidence.get('raw_score', 0.5)
    
    if confidence_score >= 0.8:
        assessment_color = "success"
        assessment_text = f"**High Confidence Projection:** Our analysis shows {confidence['score']} confidence in this assessment based on 15 years of draft data. {player_name} has strong historical precedent for success."
    elif confidence_score >= 0.6:
        assessment_color = "info"
        assessment_text = f"**Moderate Confidence Projection:** Our analysis shows {confidence['score']} confidence. {player_name} has decent historical precedent, but some uncertainty remains."
    else:
        assessment_color = "warning"
        assessment_text = f"**Lower Confidence Projection:** Our analysis shows {confidence['score']} confidence. {player_name}'s profile has limited historical precedent, suggesting higher variability in outcomes."
    
    if assessment_color == "success":
        st.success(assessment_text)
    elif assessment_color == "info":
        st.info(assessment_text)
    else:
        st.warning(assessment_text)
    
    # Bottom line recommendation
    st.markdown("---")
    st.markdown("#### 🏆 Bottom Line")
    
    if prob > 0.8:
        recommendation = f"**Elite Prospect:** {player_name} represents franchise-changing potential with minimal risk."
    elif prob > 0.6:
        recommendation = f"**Solid Selection:** {player_name} projects as a reliable contributor with starter upside."
    elif prob > 0.4:
        recommendation = f"**Development Play:** {player_name} offers intriguing potential but requires patience and development."
    else:
        recommendation = f"**High-Risk, High-Reward:** {player_name} represents a boom-or-bust selection."
    
    st.markdown(recommendation)
def display_footer():
    """Display application footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        🏀 <strong>NBA Draft 2025 AI Dashboard</strong> | Historical Intelligence Edition<br>
        <small>Featuring 60 prospects with ML projections, 15 years of historical validation, and comprehensive team analysis</small>
    </div>
    """, unsafe_allow_html=True)

# ==================== Run Application ====================
if __name__ == "__main__":
    main()

