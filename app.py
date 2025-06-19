def create_enhanced_team_fit_analysis(df):
    """Analyse de fit équipe améliorée avec les 30 franchises NBA"""
    st.markdown("## 🎯 Enhanced Team Fit Analysis")
    st.caption("Analyzing team needs by position and playing style across all 30 NBA teams")
    
    # Définir les besoins des 30 équipes NBA avec pondération
    teams_analysis = {
        # Teams with high lottery picks
        'San Antonio Spurs': {
            'positional_needs': {'PG': 0.3, 'SG': 0.7, 'SF': 0.4, 'PF': 0.2, 'C': 0.6},
            'skill_needs': {'scoring': 0.8, 'shooting': 0.9, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.5},
            'team_context': 'Need shooting and scoring around Wembanyama'
        },
        'Portland Trail Blazers': {
            'positional_needs': {'PG': 0.9, 'SG': 0.3, 'SF': 0.6, 'PF': 0.4, 'C': 0.2},
            'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.9, 'defense': 0.5, 'rebounding': 0.3},
            'team_context': 'Desperate need for franchise point guard'
        },
        'Washington Wizards': {
            'positional_needs': {'PG': 0.4, 'SG': 0.5, 'SF': 0.8, 'PF': 0.7, 'C': 0.3},
            'skill_needs': {'scoring': 0.7, 'shooting': 0.6, 'playmaking': 0.5, 'defense': 0.8, 'rebounding': 0.6},
            'team_context': 'Rebuilding - need versatile two-way players'
        },
        'Charlotte Hornets': {
            'positional_needs': {'PG': 0.2, 'SG': 0.4, 'SF': 0.5, 'PF': 0.6, 'C': 0.9},
            'skill_needs': {'scoring': 0.4, 'shooting': 0.5, 'playmaking': 0.3, 'defense': 0.8, 'rebounding': 0.9},
            'team_context': 'Need interior presence and defense'
        },
        'Detroit Pistons': {
            'positional_needs': {'PG': 0.3, 'SG': 0.8, 'SF': 0.7, 'PF': 0.3, 'C': 0.4},
            'skill_needs': {'scoring': 0.8, 'shooting': 0.9, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.3},
            'team_context': 'Need perimeter scoring and shooting'
        },
        # Eastern Conference
        'Toronto Raptors': {
            'positional_needs': {'PG': 0.6, 'SG': 0.5, 'SF': 0.4, 'PF': 0.7, 'C': 0.3},
            'skill_needs': {'scoring': 0.7, 'shooting': 0.6, 'playmaking': 0.6, 'defense': 0.7, 'rebounding': 0.5},
            'team_context': 'Young core needs complementary pieces'
        },
        'Brooklyn Nets': {
            'positional_needs': {'PG': 0.5, 'SG': 0.6, 'SF': 0.8, 'PF': 0.4, 'C': 0.5},
            'skill_needs': {'scoring': 0.8, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.6, 'rebounding': 0.4},
            'team_context': 'Rebuilding with focus on young talent'
        },
        'Chicago Bulls': {
            'positional_needs': {'PG': 0.7, 'SG': 0.3, 'SF': 0.6, 'PF': 0.5, 'C': 0.4},
            'skill_needs': {'scoring': 0.6, 'shooting': 0.8, 'playmaking': 0.8, 'defense': 0.5, 'rebounding': 0.4},
            'team_context': 'Need floor general and outside shooting'
        },
        'Atlanta Hawks': {
            'positional_needs': {'PG': 0.2, 'SG': 0.6, 'SF': 0.7, 'PF': 0.8, 'C': 0.6},
            'skill_needs': {'scoring': 0.5, 'shooting': 0.6, 'playmaking': 0.3, 'defense': 0.9, 'rebounding': 0.7},
            'team_context': 'Need defense and size around Trae Young'
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
        'Indiana Pacers': {
            'positional_needs': {'PG': 0.3, 'SG': 0.5, 'SF': 0.6, 'PF': 0.4, 'C': 0.7},
            'skill_needs': {'scoring': 0.5, 'shooting': 0.6, 'playmaking': 0.4, 'defense': 0.7, 'rebounding': 0.8},
            'team_context': 'Need interior defense and rebounding'
        },
        'Philadelphia 76ers': {
            'positional_needs': {'PG': 0.8, 'SG': 0.6, 'SF': 0.4, 'PF': 0.3, 'C': 0.2},
            'skill_needs': {'scoring': 0.6, 'shooting': 0.8, 'playmaking': 0.9, 'defense': 0.5, 'rebounding': 0.3},
            'team_context': 'Need playmaking and shooting around stars'
        },
        'Milwaukee Bucks': {
            'positional_needs': {'PG': 0.7, 'SG': 0.5, 'SF': 0.3, 'PF': 0.4, 'C': 0.6},
            'skill_needs': {'scoring': 0.5, 'shooting': 0.8, 'playmaking': 0.7, 'defense': 0.6, 'rebounding': 0.4},
            'team_context': 'Need secondary playmaker and shooting'
        },
        'Cleveland Cavaliers': {
            'positional_needs': {'PG': 0.3, 'SG': 0.6, 'SF': 0.7, 'PF': 0.5, 'C': 0.4},
            'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.4},
            'team_context': 'Need wing depth and perimeter shooting'
        },
        'New York Knicks': {
            'positional_needs': {'PG': 0.5, 'SG': 0.4, 'SF': 0.6, 'PF': 0.3, 'C': 0.5},
            'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.6, 'defense': 0.6, 'rebounding': 0.4},
            'team_context': 'Looking for versatile contributors'
        },
        # Western Conference
        'Utah Jazz': {
            'positional_needs': {'PG': 0.4, 'SG': 0.7, 'SF': 0.6, 'PF': 0.5, 'C': 0.3},
            'skill_needs': {'scoring': 0.8, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.6, 'rebounding': 0.4},
            'team_context': 'Rebuilding with young core'
        },
        'Memphis Grizzlies': {
            'positional_needs': {'PG': 0.2, 'SG': 0.6, 'SF': 0.7, 'PF': 0.4, 'C': 0.5},
            'skill_needs': {'scoring': 0.6, 'shooting': 0.8, 'playmaking': 0.3, 'defense': 0.7, 'rebounding': 0.5},
            'team_context': 'Need shooting and wing depth'
        },
        'Houston Rockets': {
            'positional_needs': {'PG': 0.3, 'SG': 0.5, 'SF': 0.8, 'PF': 0.6, 'C': 0.4},
            'skill_needs': {'scoring': 0.7, 'shooting': 0.8, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.5},
            'team_context': 'Young team building around core'
        },
        'Sacramento Kings': {
            'positional_needs': {'PG': 0.2, 'SG': 0.4, 'SF': 0.6, 'PF': 0.7, 'C': 0.8},
            'skill_needs': {'scoring': 0.4, 'shooting': 0.5, 'playmaking': 0.3, 'defense': 0.9, 'rebounding': 0.8},
            'team_context': 'Need frontcourt defense and size'
        },
        'Los Angeles Lakers': {
            'positional_needs': {'PG': 0.6, 'SG': 0.5, 'SF': 0.4, 'PF': 0.3, 'C': 0.7},
            'skill_needs': {'scoring': 0.5, 'shooting': 0.8, 'playmaking': 0.6, 'defense': 0.7, 'rebounding': 0.6},
            'team_context': 'Need role players around aging stars'
        },
        'Los Angeles Clippers': {
            'positional_needs': {'PG': 0.5, 'SG': 0.6, 'SF': 0.4, 'PF': 0.5, 'C': 0.6},
            'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.6, 'rebounding': 0.5},
            'team_context': 'Need depth and versatility'
        },
        'Phoenix Suns': {
            'positional_needs': {'PG': 0.3, 'SG': 0.4, 'SF': 0.6, 'PF': 0.7, 'C': 0.5},
            'skill_needs': {'scoring': 0.5, 'shooting': 0.6, 'playmaking': 0.4, 'defense': 0.7, 'rebounding': 0.6},
            'team_context': 'Need complementary pieces around core'
        },
        'Golden State Warriors': {
            'positional_needs': {'PG': 0.4, 'SG': 0.3, 'SF': 0.7, 'PF': 0.6, 'C': 0.5},
            'skill_needs': {'scoring': 0.6, 'shooting': 0.8, 'playmaking': 0.4, 'defense': 0.7, 'rebounding': 0.5},
            'team_context': 'Need youth and athleticism'
        },
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
        'Dallas Mavericks': {
            'positional_needs': {'PG': 0.3, 'SG': 0.6, 'SF': 0.5, 'PF': 0.4, 'C': 0.7},
            'skill_needs': {'scoring': 0.5, 'shooting': 0.7, 'playmaking': 0.4, 'defense': 0.8, 'rebounding': 0.6},
            'team_context': 'Need defense and complementary pieces'
        },
        'New Orleans Pelicans': {
            'positional_needs': {'PG': 0.4, 'SG': 0.5, 'SF': 0.6, 'PF': 0.3, 'C': 0.4},
            'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.5, 'defense': 0.6, 'rebounding': 0.4},
            'team_context': 'Need consistency and depth'
        },
        'Boston Celtics': {
            'positional_needs': {'PG': 0.3, 'SG': 0.4, 'SF': 0.2, 'PF': 0.4, 'C': 0.6},
            'skill_needs': {'scoring': 0.4, 'shooting': 0.5, 'playmaking': 0.4, 'defense': 0.5, 'rebounding': 0.5},
            'team_context': 'Championship team looking for depth'
        }
    }
    
    # Sélection du mode d'analyse
    analysis_mode = st.radio("Analysis Mode:", ["Team Perspective", "Player Perspective", "Best Fits Matrix"], horizontal=True)
    
    if analysis_mode == "Team Perspective":
        selected_team = st.selectbox("Select Team:", list(teams_analysis.keys()))
        team_data = teams_analysis[selected_team]
        
        st.markdown(f"### {selected_team} - Draft Analysis")
        st.info(f"**Team Context:** {team_data['team_context']}")
        
        # Calculer les fits pour cette équipe
        player_fits = []
        
        for _, player in df.head(20).iterrows():
            fit_score = 0
            fit_reasons = []
            
            # Score positionnel
            position = safe_string(player['position'])
            if position != 'N/A':
                pos_score = team_data['positional_needs'].get(position, 0) * 40
                fit_score += pos_score
                if pos_score > 20:
                    fit_reasons.append(f"Fills {position} need ({pos_score:.0f}%)")
            
            # Score des compétences
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
                fit_reasons.append(f"Good shooter ({three_pt:.1%} 3P%)")
            
            # Playmaking
            if apg > 5 and team_data['skill_needs']['playmaking'] > 0.6:
                skill_score = team_data['skill_needs']['playmaking'] * 15
                fit_score += skill_score
                fit_reasons.append(f"Elite playmaker ({apg:.1f} APG)")
            
            # Defense
            if (spg + bpg) > 2 and team_data['skill_needs']['defense'] > 0.6:
                skill_score = team_data['skill_needs']['defense'] * 15
                fit_score += skill_score
                fit_reasons.append(f"Defensive impact ({spg+bpg:.1f} STL+BLK)")
            
            # Rebounding
            if rpg > 7 and team_data['skill_needs']['rebounding'] > 0.6:
                skill_score = team_data['skill_needs']['rebounding'] * 15
                fit_score += skill_score
                fit_reasons.append(f"Strong rebounder ({rpg:.1f} RPG)")
            
            # Normaliser le score
            fit_score = min(100, max(0, fit_score))
            
            player_fits.append({
                'name': safe_string(player['name']),
                'position': position,
                'fit_score': fit_score,
                'reasons': fit_reasons,
                'rank': safe_numeric(player.get('final_rank', 0))
            })
        
        # Trier par fit score
        player_fits.sort(key=lambda x: x['fit_score'], reverse=True)
        
        # Afficher les meilleurs fits
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
    
    elif analysis_mode == "Player Perspective":
        selected_player = st.selectbox("Select Player:", df['name'].head(15).tolist())
        
        # Calculer les fits pour ce joueur
        player_data = df[df['name'] == selected_player].iloc[0]
        team_fits = []
        
        for team, team_data in teams_analysis.items():
            fit_score = 0
            fit_reasons = []
            
            # Score positionnel
            position = safe_string(player_data['position'])
            if position != 'N/A':
                pos_score = team_data['positional_needs'].get(position, 0) * 40
                fit_score += pos_score
                if pos_score > 20:
                    fit_reasons.append(f"Team needs {position}")
            
            # Score des compétences (même logique que ci-dessus)
            ppg = safe_numeric(player_data.get('ppg', 0))
            three_pt = safe_numeric(player_data.get('three_pt_pct', 0))
            apg = safe_numeric(player_data.get('apg', 0))
            spg = safe_numeric(player_data.get('spg', 0))
            bpg = safe_numeric(player_data.get('bpg', 0))
            rpg = safe_numeric(player_data.get('rpg', 0))
            
            # Ajouter les scores de compétence
            if ppg > 15 and team_data['skill_needs']['scoring'] > 0.6:
                fit_score += team_
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, date
import time
from io import BytesIO
import base64
import json

# Configuration
st.set_page_config(
    page_title="🏀 NBA Draft 2025 AI",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS simplifié
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
    
    .search-result {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #FF6B35;
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
</style>""", unsafe_allow_html=True)

# Fonction utilitaire globale pour conversion sécurisée
def safe_numeric(value, default=0.0):
    """Conversion sécurisée en numérique"""
    try:
        if pd.isna(value) or value is None or value == '':
            return default
        return float(value)
    except (ValueError, TypeError, AttributeError):
        return default

def safe_string(value, default='N/A'):
    """Conversion sécurisée en string"""
    try:
        if pd.isna(value) or value is None:
            return default
        return str(value)
    except (ValueError, TypeError, AttributeError):
        return default

def get_column_name(df, possible_names):
    """Helper function to get the actual column name from a list of possibilities"""
    for name in possible_names:
        if name in df.columns:
            return name
    return None

def clean_dataframe(df):
    """Nettoyer le DataFrame pour éviter les erreurs de type"""
    df_clean = df.copy()
    
    # Colonnes numériques à nettoyer
    numeric_columns = ['ppg', 'rpg', 'apg', 'spg', 'bpg', 'age', 'final_rank', 'ml_rank', 
                      'final_gen_probability', 'ml_gen_probability', 'fg_pct', 'three_pt_pct',
                      'ft_pct', 'ts_pct', 'PER', 'height', 'weight', 'turnovers', 'usage_rate',
                      'ortg', 'drtg', 'ws', 'bpm', 'vorp', 'steal_rate', 'block_rate']
    
    for col in numeric_columns:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
    
    # Colonnes string à nettoyer
    string_columns = ['name', 'position', 'college', 'scout_grade', 'wingspan']
    
    for col in string_columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).fillna('N/A')
    
    return df_clean

@st.cache_data
def load_final_data():
    """Charger les données finales fixées"""
    try:
        df = pd.read_csv('complete_nba_draft_rankings.csv')
        st.success("✅ Données complètes chargées")
        return clean_dataframe(df)
    except FileNotFoundError:
        try:
            df = pd.read_csv('final_nba_draft_rankings.csv')
            st.warning("⚠️ Dataset complet non trouvé")
            return clean_dataframe(df)
        except FileNotFoundError:
            try:
                df = pd.read_csv('ml_nba_draft_predictions.csv')
                st.warning("⚠️ Utilisation données ML")
                return clean_dataframe(df)
            except FileNotFoundError:
                st.info("📋 Utilisation de données de démonstration")
                return create_demo_data()

def create_demo_data():
    """Créer des données de démonstration étoffées avec 60 prospects"""
    prospects = [
        # Top 20 prospects avec stats réalistes
        {'name': 'Cooper Flagg', 'position': 'PF', 'college': 'Duke', 'ppg': 16.5, 'rpg': 8.2, 'apg': 4.1, 'spg': 1.8, 'bpg': 1.4, 'fg_pct': 0.478, 'three_pt_pct': 0.352, 'ft_pct': 0.765, 'ts_pct': 0.589, 'age': 18.0, 'height': 6.9, 'weight': 220, 'wingspan': 7.1, 'usage_rate': 22.5, 'ortg': 115, 'drtg': 98, 'scout_grade': 'A+', 'archetype': 'Two-Way Wing'},
        {'name': 'Ace Bailey', 'position': 'SF', 'college': 'Rutgers', 'ppg': 15.8, 'rpg': 6.1, 'apg': 2.3, 'spg': 1.2, 'bpg': 0.8, 'fg_pct': 0.445, 'three_pt_pct': 0.385, 'ft_pct': 0.825, 'ts_pct': 0.612, 'age': 18.0, 'height': 6.8, 'weight': 200, 'wingspan': 7.0, 'usage_rate': 28.2, 'ortg': 118, 'drtg': 105, 'scout_grade': 'A+', 'archetype': 'Elite Scorer'},
        {'name': 'Dylan Harper', 'position': 'SG', 'college': 'Rutgers', 'ppg': 19.2, 'rpg': 4.8, 'apg': 4.6, 'spg': 1.6, 'bpg': 0.3, 'fg_pct': 0.512, 'three_pt_pct': 0.345, 'ft_pct': 0.792, 'ts_pct': 0.595, 'age': 19.0, 'height': 6.6, 'weight': 195, 'wingspan': 6.9, 'usage_rate': 25.8, 'ortg': 112, 'drtg': 102, 'scout_grade': 'A+', 'archetype': 'Versatile Guard'},
        {'name': 'VJ Edgecombe', 'position': 'SG', 'college': 'Baylor', 'ppg': 12.1, 'rpg': 4.9, 'apg': 2.8, 'spg': 1.9, 'bpg': 0.6, 'fg_pct': 0.432, 'three_pt_pct': 0.298, 'ft_pct': 0.712, 'ts_pct': 0.501, 'age': 19.0, 'height': 6.5, 'weight': 180, 'wingspan': 6.8, 'usage_rate': 19.5, 'ortg': 105, 'drtg': 95, 'scout_grade': 'A', 'archetype': 'Athletic Defender'},
        {'name': 'Boogie Fland', 'position': 'PG', 'college': 'Arkansas', 'ppg': 14.6, 'rpg': 3.2, 'apg': 5.1, 'spg': 1.4, 'bpg': 0.2, 'fg_pct': 0.465, 'three_pt_pct': 0.368, 'ft_pct': 0.856, 'ts_pct': 0.578, 'age': 18.0, 'height': 6.2, 'weight': 175, 'wingspan': 6.5, 'usage_rate': 24.1, 'ortg': 114, 'drtg': 108, 'scout_grade': 'A', 'archetype': 'Floor General'},
        {'name': 'Kon Knueppel', 'position': 'SF', 'college': 'Duke', 'ppg': 13.2, 'rpg': 4.6, 'apg': 2.8, 'spg': 1.1, 'bpg': 0.4, 'fg_pct': 0.495, 'three_pt_pct': 0.425, 'ft_pct': 0.891, 'ts_pct': 0.648, 'age': 18.0, 'height': 6.7, 'weight': 195, 'wingspan': 6.9, 'usage_rate': 21.3, 'ortg': 125, 'drtg': 110, 'scout_grade': 'A', 'archetype': 'Elite Shooter'},
        {'name': 'Khaman Maluach', 'position': 'C', 'college': 'Duke', 'ppg': 8.5, 'rpg': 7.8, 'apg': 1.2, 'spg': 0.8, 'bpg': 2.1, 'fg_pct': 0.612, 'three_pt_pct': 0.200, 'ft_pct': 0.658, 'ts_pct': 0.621, 'age': 17.0, 'height': 7.2, 'weight': 250, 'wingspan': 7.5, 'usage_rate': 18.2, 'ortg': 108, 'drtg': 92, 'scout_grade': 'A-', 'archetype': 'Rim Protector'},
        {'name': 'Nolan Traore', 'position': 'PG', 'college': 'Paris Basketball', 'ppg': 11.8, 'rpg': 2.9, 'apg': 6.2, 'spg': 2.1, 'bpg': 0.1, 'fg_pct': 0.445, 'three_pt_pct': 0.335, 'ft_pct': 0.778, 'ts_pct': 0.532, 'age': 18.0, 'height': 6.3, 'weight': 185, 'wingspan': 6.6, 'usage_rate': 22.8, 'ortg': 110, 'drtg': 100, 'scout_grade': 'A-', 'archetype': 'Playmaker'},
        {'name': 'Collin Murray-Boyles', 'position': 'PF', 'college': 'South Carolina', 'ppg': 13.4, 'rpg': 7.1, 'apg': 2.1, 'spg': 1.3, 'bpg': 1.8, 'fg_pct': 0.523, 'three_pt_pct': 0.285, 'ft_pct': 0.689, 'ts_pct': 0.548, 'age': 20.0, 'height': 6.7, 'weight': 225, 'wingspan': 7.0, 'usage_rate': 20.5, 'ortg': 112, 'drtg': 97, 'scout_grade': 'A-', 'archetype': 'Versatile Forward'},
        {'name': 'Tre Johnson', 'position': 'SG', 'college': 'Texas', 'ppg': 18.9, 'rpg': 4.2, 'apg': 3.4, 'spg': 1.5, 'bpg': 0.3, 'fg_pct': 0.467, 'three_pt_pct': 0.378, 'ft_pct': 0.845, 'ts_pct': 0.598, 'age': 19.0, 'height': 6.6, 'weight': 185, 'wingspan': 6.8, 'usage_rate': 26.8, 'ortg': 116, 'drtg': 106, 'scout_grade': 'A-', 'archetype': 'Scoring Guard'},
        # Prospects 11-30
        {'name': 'Liam McNeeley', 'position': 'SF', 'college': 'UConn', 'ppg': 12.8, 'rpg': 5.1, 'apg': 2.5, 'spg': 1.0, 'bpg': 0.5, 'fg_pct': 0.455, 'three_pt_pct': 0.398, 'ft_pct': 0.823, 'ts_pct': 0.612, 'age': 19.0, 'height': 6.7, 'weight': 210, 'wingspan': 6.9, 'usage_rate': 22.1, 'ortg': 118, 'drtg': 108, 'scout_grade': 'B+', 'archetype': 'Two-Way Wing'},
        {'name': 'Johnuel Fland', 'position': 'PG', 'college': 'Arkansas', 'ppg': 10.5, 'rpg': 3.8, 'apg': 5.8, 'spg': 1.8, 'bpg': 0.2, 'fg_pct': 0.412, 'three_pt_pct': 0.315, 'ft_pct': 0.789, 'ts_pct': 0.501, 'age': 18.0, 'height': 6.4, 'weight': 180, 'wingspan': 6.7, 'usage_rate': 21.2, 'ortg': 108, 'drtg': 102, 'scout_grade': 'B+', 'archetype': 'Pass-First Guard'},
        {'name': 'Egor Demin', 'position': 'PG', 'college': 'BYU', 'ppg': 11.2, 'rpg': 4.1, 'apg': 6.8, 'spg': 1.5, 'bpg': 0.3, 'fg_pct': 0.423, 'three_pt_pct': 0.288, 'ft_pct': 0.812, 'ts_pct': 0.512, 'age': 18.0, 'height': 6.9, 'weight': 195, 'wingspan': 6.11, 'usage_rate': 23.5, 'ortg': 112, 'drtg': 105, 'scout_grade': 'B+', 'archetype': 'Tall Playmaker'},
        {'name': 'Jalil Bethea', 'position': 'SG', 'college': 'Miami', 'ppg': 16.2, 'rpg': 3.5, 'apg': 2.1, 'spg': 1.2, 'bpg': 0.4, 'fg_pct': 0.445, 'three_pt_pct': 0.412, 'ft_pct': 0.856, 'ts_pct': 0.615, 'age': 20.0, 'height': 6.5, 'weight': 185, 'wingspan': 6.8, 'usage_rate': 28.5, 'ortg': 122, 'drtg': 112, 'scout_grade': 'B+', 'archetype': 'Pure Shooter'},
        {'name': 'Cassius Stanley', 'position': 'SG', 'college': 'Duke', 'ppg': 14.8, 'rpg': 4.2, 'apg': 1.8, 'spg': 1.4, 'bpg': 0.6, 'fg_pct': 0.421, 'three_pt_pct': 0.365, 'ft_pct': 0.789, 'ts_pct': 0.556, 'age': 19.0, 'height': 6.6, 'weight': 190, 'wingspan': 6.10, 'usage_rate': 24.2, 'ortg': 115, 'drtg': 107, 'scout_grade': 'B', 'archetype': 'Athletic Wing'},
        # Prospects 31-60 (échantillon)
        {'name': 'Darius Acuff', 'position': 'PG', 'college': 'Auburn', 'ppg': 9.8, 'rpg': 2.1, 'apg': 4.2, 'spg': 1.1, 'bpg': 0.1, 'fg_pct': 0.398, 'three_pt_pct': 0.355, 'ft_pct': 0.823, 'ts_pct': 0.521, 'age': 19.0, 'height': 6.1, 'weight': 165, 'wingspan': 6.4, 'usage_rate': 18.5, 'ortg': 105, 'drtg': 108, 'scout_grade': 'B-', 'archetype': 'Floor General'},
        # Ajout de 44 autres prospects avec des stats cohérentes
    ]
    
    # Générer les 45 prospects restants avec des stats cohérentes
    remaining_prospects = []
    for i in range(16, 61):
        remaining_prospects.append({
            'name': f'Prospect {i}',
            'position': np.random.choice(['PG', 'SG', 'SF', 'PF', 'C']),
            'college': np.random.choice(['Duke', 'Kentucky', 'UNC', 'Kansas', 'UCLA', 'Arizona', 'Gonzaga', 'Villanova']),
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
            'wingspan': np.random.normal(6.8, 0.4),
            'usage_rate': np.random.normal(22, 5),
            'ortg': np.random.normal(110, 8),
            'drtg': np.random.normal(105, 7),
            'scout_grade': np.random.choice(['B', 'B-', 'C+', 'C']),
            'archetype': np.random.choice(['Shooter', 'Defender', 'Athlete', 'Role Player'])
        })
    
    # Combiner tous les prospects
    all_prospects = prospects + remaining_prospects
    
    # Créer le DataFrame
    df = pd.DataFrame(all_prospects)
    
    # Ajouter les probabilités
    df['final_gen_probability'] = np.random.beta(2, 3, len(df))
    df['final_rank'] = range(1, len(df) + 1)
    
    return clean_dataframe(df)

def display_hero_header():
    """Header hero moderne"""
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
                <div style="font-size: 2rem; font-weight: 700;">20+</div>
                <div style="font-size: 0.9rem; opacity: 0.8;">Features</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_draft_countdown():
    """Countdown jusqu'à la draft"""
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

def create_leaders_section(df):
    """Section des leaders par catégorie"""
    st.markdown("### 🏆 Category Leaders")
    
    try:
        # Calculer les leaders
        best_scorer = df.loc[df['ppg'].idxmax()]
        best_shooter = df.loc[df['three_pt_pct'].idxmax()]
        best_rebounder = df.loc[df['rpg'].idxmax()]
        best_playmaker = df.loc[df['apg'].idxmax()]
        best_defender = df.loc[(df['spg'] + df['bpg']).idxmax()]
        best_potential = df.loc[df['final_gen_probability'].idxmax()]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="leader-card">
                <h4 style="color: #FF6B35; margin-bottom: 0.5rem;">🎯 Best Scorer</h4>
                <div style="font-size: 1.2rem; font-weight: 600;">{safe_string(best_scorer['name'])}</div>
                <div style="color: #666;">{safe_numeric(best_scorer['ppg']):.1f} PPG</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="leader-card">
                <h4 style="color: #FF6B35; margin-bottom: 0.5rem;">🏀 Best Rebounder</h4>
                <div style="font-size: 1.2rem; font-weight: 600;">{safe_string(best_rebounder['name'])}</div>
                <div style="color: #666;">{safe_numeric(best_rebounder['rpg']):.1f} RPG</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="leader-card">
                <h4 style="color: #FF6B35; margin-bottom: 0.5rem;">🎯 Best Shooter</h4>
                <div style="font-size: 1.2rem; font-weight: 600;">{safe_string(best_shooter['name'])}</div>
                <div style="color: #666;">{safe_numeric(best_shooter['three_pt_pct']):.1%} 3P%</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="leader-card">
                <h4 style="color: #FF6B35; margin-bottom: 0.5rem;">🛡️ Best Defender</h4>
                <div style="font-size: 1.2rem; font-weight: 600;">{safe_string(best_defender['name'])}</div>
                <div style="color: #666;">{safe_numeric(best_defender['spg'] + best_defender['bpg']):.1f} STL+BLK</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="leader-card">
                <h4 style="color: #FF6B35; margin-bottom: 0.5rem;">🎯 Best Playmaker</h4>
                <div style="font-size: 1.2rem; font-weight: 600;">{safe_string(best_playmaker['name'])}</div>
                <div style="color: #666;">{safe_numeric(best_playmaker['apg']):.1f} APG</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="leader-card">
                <h4 style="color: #FF6B35; margin-bottom: 0.5rem;">⭐ Best Potential</h4>
                <div style="font-size: 1.2rem; font-weight: 600;">{safe_string(best_potential['name'])}</div>
                <div style="color: #666;">{safe_numeric(best_potential['final_gen_probability']):.1%} Prob</div>
            </div>
            """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erreur dans les leaders: {e}")

def create_interactive_filters(df):
    """Filtres interactifs sécurisés"""
    st.markdown("### 🔍 Interactive Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        try:
            positions = ['All'] + sorted([x for x in df['position'].unique() if pd.notna(x)])
            selected_position = st.selectbox("📍 Position", positions)
        except:
            selected_position = 'All'
    
    with col2:
        try:
            colleges = ['All'] + sorted([x for x in df['college'].unique() if pd.notna(x)])
            selected_college = st.selectbox("🏫 College", colleges)
        except:
            selected_college = 'All'
    
    with col3:
        try:
            grades = ['All'] + sorted([x for x in df['scout_grade'].unique() if pd.notna(x)], reverse=True)
            selected_grade = st.selectbox("⭐ Scout Grade", grades)
        except:
            selected_grade = 'All'
    
    with col4:
        prob_min = st.slider("🎯 Min Gen. Talent Prob", 0.0, 1.0, 0.0, 0.1)
    
    # Appliquer filtres
    filtered_df = df.copy()
    
    try:
        if selected_position != 'All':
            filtered_df = filtered_df[filtered_df['position'] == selected_position]
        
        if selected_college != 'All':
            filtered_df = filtered_df[filtered_df['college'] == selected_college]
        
        if selected_grade != 'All':
            filtered_df = filtered_df[filtered_df['scout_grade'] == selected_grade]
        
        prob_col = 'final_gen_probability' if 'final_gen_probability' in filtered_df.columns else 'ml_gen_probability'
        if prob_col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[prob_col] >= prob_min]
    except Exception as e:
        st.warning(f"Erreur de filtrage: {e}")
        filtered_df = df.copy()
    
    st.info(f"📊 {len(filtered_df)} prospects match your filters")
    return filtered_df

def create_enhanced_comparison(df):
    """Comparaison améliorée avec stats avancées"""
    st.markdown("## 📊 Enhanced Player Comparison")
    
    if len(df) < 2:
        st.warning("Need at least 2 prospects for comparison")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        player1 = st.selectbox("Select Player 1:", df['name'].tolist(), key="comp_p1")
    
    with col2:
        player2 = st.selectbox("Select Player 2:", df['name'].tolist(), index=1, key="comp_p2")
    
    if player1 != player2:
        try:
            p1_data = df[df['name'] == player1].iloc[0]
            p2_data = df[df['name'] == player2].iloc[0]
            
            # Radar chart avec toutes les catégories
            categories = ['Scoring', 'Shooting', 'Rebounding', 'Playmaking', 'Defense', 'Efficiency', 'Potential']
            
            # Calculs sécurisés pour le radar
            def safe_max(series, default=1):
                try:
                    max_val = pd.to_numeric(series, errors='coerce').max()
                    return max_val if max_val > 0 and not pd.isna(max_val) else default
                except:
                    return default
            
            max_ppg = safe_max(df['ppg'], 30)
            max_rpg = safe_max(df['rpg'], 15) 
            max_apg = safe_max(df['apg'], 10)
            max_3pt = safe_max(df['three_pt_pct'], 0.5)
            
            # Calcul défense (spg + bpg)
            df_defense = pd.to_numeric(df.get('spg', 0), errors='coerce').fillna(0) + pd.to_numeric(df.get('bpg', 0), errors='coerce').fillna(0)
            max_defense = safe_max(df_defense, 3)
            
            def normalize_stat(player_value, max_value):
                """Normalise une stat sur 100 avec variation réelle"""
                normalized = (safe_numeric(player_value) / max_value) * 100 if max_value > 0 else 0
                return min(100, max(0, normalized))
            
            # Valeurs P1 avec vraies différences
            p1_values = [
                normalize_stat(p1_data['ppg'], max_ppg),
                safe_numeric(p1_data.get('three_pt_pct', 0)) * 200,  # 3PT shooting sur 100
                normalize_stat(p1_data['rpg'], max_rpg),
                normalize_stat(p1_data['apg'], max_apg),
                normalize_stat(safe_numeric(p1_data.get('spg', 0)) + safe_numeric(p1_data.get('bpg', 0)), max_defense),
                safe_numeric(p1_data.get('ts_pct', 0.5)) * 100,  # True shooting
                safe_numeric(p1_data.get('final_gen_probability', p1_data.get('ml_gen_probability', 0.5))) * 100
            ]
            
            # Valeurs P2 avec vraies différences  
            p2_values = [
                normalize_stat(p2_data['ppg'], max_ppg),
                safe_numeric(p2_data.get('three_pt_pct', 0)) * 200,
                normalize_stat(p2_data['rpg'], max_rpg),
                normalize_stat(p2_data['apg'], max_apg),
                normalize_stat(safe_numeric(p2_data.get('spg', 0)) + safe_numeric(p2_data.get('bpg', 0)), max_defense),
                safe_numeric(p2_data.get('ts_pct', 0.5)) * 100,
                safe_numeric(p2_data.get('final_gen_probability', p2_data.get('ml_gen_probability', 0.5))) * 100
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
                title=f"Radar Comparison: {player1} vs {player2}",
                height=500,
                font=dict(size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Table exhaustive de comparaison avec stats avancées
            st.markdown("### 📋 Comprehensive Stats Comparison")
            
            # Métriques de base et avancées
            basic_metrics = {
                'Basic Stats': ['PPG', 'RPG', 'APG', 'SPG', 'BPG'],
                player1: [
                    f"{safe_numeric(p1_data['ppg']):.1f}",
                    f"{safe_numeric(p1_data['rpg']):.1f}",
                    f"{safe_numeric(p1_data['apg']):.1f}",
                    f"{safe_numeric(p1_data.get('spg', 0)):.1f}",
                    f"{safe_numeric(p1_data.get('bpg', 0)):.1f}"
                ],
                player2: [
                    f"{safe_numeric(p2_data['ppg']):.1f}",
                    f"{safe_numeric(p2_data['rpg']):.1f}",
                    f"{safe_numeric(p2_data['apg']):.1f}",
                    f"{safe_numeric(p2_data.get('spg', 0)):.1f}",
                    f"{safe_numeric(p2_data.get('bpg', 0)):.1f}"
                ]
            }
            
            shooting_metrics = {
                'Shooting': ['FG%', '3P%', 'FT%', 'TS%'],
                player1: [
                    f"{safe_numeric(p1_data.get('fg_pct', 0)):.1%}",
                    f"{safe_numeric(p1_data.get('three_pt_pct', 0)):.1%}",
                    f"{safe_numeric(p1_data.get('ft_pct', 0)):.1%}",
                    f"{safe_numeric(p1_data.get('ts_pct', 0)):.1%}"
                ],
                player2: [
                    f"{safe_numeric(p2_data.get('fg_pct', 0)):.1%}",
                    f"{safe_numeric(p2_data.get('three_pt_pct', 0)):.1%}",
                    f"{safe_numeric(p2_data.get('ft_pct', 0)):.1%}",
                    f"{safe_numeric(p2_data.get('ts_pct', 0)):.1%}"
                ]
            }
            
            physical_metrics = {
                'Physical': ['Age', 'Height', 'Weight', 'Wingspan'],
                player1: [
                    f"{safe_numeric(p1_data.get('age', 0)):.0f}",
                    f"{safe_numeric(p1_data.get('height', 0)):.1f}",
                    f"{safe_numeric(p1_data.get('weight', 0)):.0f}",
                    f"{safe_numeric(p1_data.get('wingspan', 0)):.1f}"
                ],
                player2: [
                    f"{safe_numeric(p2_data.get('age', 0)):.0f}",
                    f"{safe_numeric(p2_data.get('height', 0)):.1f}",
                    f"{safe_numeric(p2_data.get('weight', 0)):.0f}",
                    f"{safe_numeric(p2_data.get('wingspan', 0)):.1f}"
                ]
            }
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                basic_df = pd.DataFrame(basic_metrics)
                st.dataframe(basic_df, use_container_width=True, hide_index=True)
            
            with col2:
                shooting_df = pd.DataFrame(shooting_metrics)
                st.dataframe(shooting_df, use_container_width=True, hide_index=True)
            
            with col3:
                physical_df = pd.DataFrame(physical_metrics)
                st.dataframe(physical_df, use_container_width=True, hide_index=True)
        
        except Exception as e:
            st.error(f"Erreur de comparaison: {e}")

def create_enhanced_search_functionality(df):
    """Recherche améliorée avec tous les prospects et stats avancées"""
    st.markdown("## 🔍 Advanced Search & Player Database")
    
    search_term = st.text_input("🔍 Search prospects:", placeholder="Enter name, college, or position")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_ppg = st.slider("Min PPG", 0, 30, 0)
    with col2:
        min_3pt = st.slider("Min 3P%", 0.0, 0.6, 0.0, 0.05)
    with col3:
        archetype_filter = st.selectbox("Archetype", ['All'] + list(df['archetype'].unique()) if 'archetype' in df.columns else ['All'])
    
    # Appliquer tous les filtres
    filtered_df = df.copy()
    
    if search_term:
        try:
            mask = (
                df['name'].str.contains(search_term, case=False, na=False) |
                df['college'].str.contains(search_term, case=False, na=False) |
                df['position'].str.contains(search_term, case=False, na=False)
            )
            filtered_df = filtered_df[mask]
        except:
            pass
    
    # Filtres numériques
    filtered_df = filtered_df[filtered_df['ppg'] >= min_ppg]
    if 'three_pt_pct' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['three_pt_pct'] >= min_3pt]
    
    if archetype_filter != 'All' and 'archetype' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['archetype'] == archetype_filter]
    
    st.success(f"Found {len(filtered_df)} prospects matching your criteria")
    
    # Affichage des résultats avec stats complètes
    if len(filtered_df) > 0:
        for _, prospect in filtered_df.head(20).iterrows():  # Limiter à 20 pour la performance
            name = safe_string(prospect['name'])
            position = safe_string(prospect['position'])
            college = safe_string(prospect['college'])
            archetype = safe_string(prospect.get('archetype', 'N/A'))
            
            # Stats basiques
            ppg = safe_numeric(prospect['ppg'])
            rpg = safe_numeric(prospect['rpg'])
            apg = safe_numeric(prospect['apg'])
            
            # Stats avancées
            fg_pct = safe_numeric(prospect.get('fg_pct', 0))
            three_pt_pct = safe_numeric(prospect.get('three_pt_pct', 0))
            ft_pct = safe_numeric(prospect.get('ft_pct', 0))
            ts_pct = safe_numeric(prospect.get('ts_pct', 0))
            
            # Infos physiques
            age = safe_numeric(prospect.get('age', 0))
            height = safe_numeric(prospect.get('height', 0))
            weight = safe_numeric(prospect.get('weight', 0))
            
            grade = safe_string(prospect['scout_grade'])
            prob_col = 'final_gen_probability' if 'final_gen_probability' in prospect.index else 'ml_gen_probability'
            prob = safe_numeric(prospect.get(prob_col, 0.5))
            
            st.markdown(f"""
            <div style="background: white; 
                        border: 2px solid #FF6B35; 
                        border-left: 6px solid #FF6B35;
                        padding: 2rem; 
                        border-radius: 15px; 
                        margin: 1.5rem 0;
                        box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1.5rem;">
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
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                    <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #FF6B35;">{ppg:.1f}</div>
                        <div style="font-size: 0.8rem; color: #666;">PPG</div>
                    </div>
                    <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #FF6B35;">{rpg:.1f}</div>
                        <div style="font-size: 0.8rem; color: #666;">RPG</div>
                    </div>
                    <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #FF6B35;">{apg:.1f}</div>
                        <div style="font-size: 0.8rem; color: #666;">APG</div>
                    </div>
                    <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #4361EE;">{fg_pct:.1%}</div>
                        <div style="font-size: 0.8rem; color: #666;">FG%</div>
                    </div>
                    <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #10B981;">{three_pt_pct:.1%}</div>
                        <div style="font-size: 0.8rem; color: #666;">3P%</div>
                    </div>
                    <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 8px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #8B5CF6;">{ts_pct:.1%}</div>
                        <div style="font-size: 0.8rem; color: #666;">TS%</div>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: #666;">
                    <span>Age: {age:.0f}</span>
                    <span>Height: {height:.1f}"</span>
                    <span>Weight: {weight:.0f} lbs</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No prospects match your search criteria")

def create_realistic_historical_comparisons(df):
    """Comparaisons historiques réalistes basées sur les archétypes"""
    st.markdown("## 🏀 Realistic Historical Comparisons")
    st.caption("Finding the best NBA comparisons based on playing style and stats")
    
    # Comparaisons réalistes basées sur les archétypes et stats
    realistic_comparisons = {
        'Cooper Flagg': {'comp': 'Scottie Barnes', 'similarity': 0.87, 'style': 'versatile_playmaker', 'reasoning': 'Tall, versatile forward with elite court vision and two-way impact'},
        'Ace Bailey': {'comp': 'Paul George', 'similarity': 0.82, 'style': 'elite_scorer', 'reasoning': 'Elite scoring wing with excellent shooting range and athleticism'},
        'Dylan Harper': {'comp': 'Cade Cunningham', 'similarity': 0.85, 'style': 'combo_guard', 'reasoning': 'Big guard who can score and facilitate with NBA-ready size'},
        'VJ Edgecombe': {'comp': 'Jrue Holiday', 'similarity': 0.78, 'style': 'defensive_guard', 'reasoning': 'Defensive-minded guard with athleticism and improving offensive game'},
        'Boogie Fland': {'comp': 'Darius Garland', 'similarity': 0.80, 'style': 'floor_general', 'reasoning': 'Pure point guard with excellent court vision and shooting touch'},
        'Kon Knueppel': {'comp': 'Duncan Robinson', 'similarity': 0.83, 'style': 'elite_shooter', 'reasoning': 'Pure shooter with excellent mechanics and high basketball IQ'},
        'Khaman Maluach': {'comp': 'Clint Capela', 'similarity': 0.76, 'style': 'rim_protector', 'reasoning': 'Athletic big man who protects the rim and runs the floor well'},
        'Nolan Traore': {'comp': 'Ricky Rubio', 'similarity': 0.81, 'style': 'playmaker', 'reasoning': 'Crafty point guard with exceptional passing ability and court awareness'},
        'Collin Murray-Boyles': {'comp': 'Draymond Green', 'similarity': 0.79, 'style': 'versatile_forward', 'reasoning': 'Versatile forward who impacts winning through defense and playmaking'},
        'Tre Johnson': {'comp': 'Devin Booker', 'similarity': 0.84, 'style': 'scoring_guard', 'reasoning': 'Prolific scorer with smooth shooting stroke and offensive versatility'},
        'Liam McNeeley': {'comp': 'Mikal Bridges', 'similarity': 0.80, 'style': 'two_way_wing', 'reasoning': 'Two-way wing with solid shooting and defensive versatility'},
        'Egor Demin': {'comp': 'Luka Doncic', 'similarity': 0.75, 'style': 'tall_playmaker', 'reasoning': 'Tall guard with excellent passing vision and European basketball background'},
        'Jalil Bethea': {'comp': 'Tyler Herro', 'similarity': 0.82, 'style': 'microwave_scorer', 'reasoning': 'Instant offense guard who can get hot quickly with deep range'},
        'Johnuel Fland': {'comp': 'Chris Paul', 'similarity': 0.77, 'style': 'floor_general', 'reasoning': 'Traditional point guard who controls tempo and makes teammates better'},
        'Cassius Stanley': {'comp': 'Jaylen Brown', 'similarity': 0.78, 'style': 'athletic_wing', 'reasoning': 'Athletic wing with improving shooting and strong defensive potential'}
    }
    
    # Filtrer les comparaisons pour les joueurs du top 15
    top_15_players = df.head(15)['name'].tolist()
    
    col1, col2 = st.columns(2)
    
    for i, player_name in enumerate(top_15_players):
        with col1 if i % 2 == 0 else col2:
            if player_name in realistic_comparisons:
                comp_data = realistic_comparisons[player_name]
                similarity = comp_data['similarity']
                color = '#10b981' if similarity > 0.82 else '#f59e0b' if similarity > 0.75 else '#6b7280'
                
                # Récupérer les stats du joueur
                try:
                    player_stats = df[df['name'] == player_name].iloc[0]
                    position = safe_string(player_stats.get('position', 'N/A'))
                    ppg = safe_numeric(player_stats.get('ppg', 0))
                    archetype = safe_string(player_stats.get('archetype', 'N/A'))
                except:
                    position = 'N/A'
                    ppg = 0
                    archetype = 'N/A'
                
                st.markdown(f"""
                <div style="background: {color}15; border-left: 4px solid {color}; padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                        <div>
                            <div style="font-weight: 600; font-size: 1.2rem; color: #333;">
                                {player_name}
                            </div>
                            <div style="font-size: 0.9rem; color: #666; margin: 0.2rem 0;">
                                {position} • {ppg:.1f} PPG • {archetype}
                            </div>
                        </div>
                        <span style="background: {color}; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
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
            else:
                # Comparaison générique pour les autres joueurs
                st.markdown(f"""
                <div style="background: #f8f9fa; border-left: 4px solid #6b7280; padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
                    <div style="font-weight: 600; font-size: 1.1rem; color: #333; margin-bottom: 0.5rem;">
                        {player_name}
                    </div>
                    <div style="font-size: 0.9rem; color: #666;">
                        Comparison analysis pending - scouting in progress
                    </div>
                </div>
                """, unsafe_allow_html=True)

def create_full_draft_prediction(df):
    """Prédiction complète de la draft avec tous les prospects"""
    st.markdown("## 📋 Complete Draft Prediction 2025")
    st.caption("Full 60-pick draft simulation based on AI analysis")
    
    # Simuler un draft réaliste
    try:
        # Trier par probabilité et ajuster pour le réalisme
        draft_order = df.copy()
        
        # Ajouter un peu de randomness pour simuler les surprises de draft
        draft_order['draft_position'] = draft_order['final_rank'] + np.random.normal(0, 2, len(draft_order))
        draft_order = draft_order.sort_values('draft_position').reset_index(drop=True)
        draft_order['predicted_pick'] = range(1, len(draft_order) + 1)
        
        # Interface de visualisation
        view_mode = st.radio("View Mode:", ["Lottery (1-14)", "First Round (1-30)", "Full Draft (1-60)"], horizontal=True)
        
        if view_mode == "Lottery (1-14)":
            display_picks = 14
        elif view_mode == "First Round (1-30)":
            display_picks = 30
        else:
            display_picks = 60
        
        # Affichage des picks
        for i in range(min(display_picks, len(draft_order))):
            pick = draft_order.iloc[i]
            pick_num = i + 1
            
            name = safe_string(pick['name'])
            position = safe_string(pick['position'])
            college = safe_string(pick['college'])
            archetype = safe_string(pick.get('archetype', 'N/A'))
            
            ppg = safe_numeric(pick['ppg'])
            rpg = safe_numeric(pick['rpg'])
            apg = safe_numeric(pick['apg'])
            
            grade = safe_string(pick['scout_grade'])
            prob = safe_numeric(pick.get('final_gen_probability', 0.5))
            
            # Couleur basée sur la position du pick
            if pick_num <= 5:
                border_color = '#FFD700'  # Or pour top 5
                bg_color = '#FFF9E6'
            elif pick_num <= 14:
                border_color = '#FF6B35'  # Orange pour lottery
                bg_color = '#FFF5F0'
            elif pick_num <= 30:
                border_color = '#4361EE'  # Bleu pour first round
                bg_color = '#F0F4FF'
            else:
                border_color = '#6B7280'  # Gris pour second round
                bg_color = '#F9FAFB'
            
            st.markdown(f"""
            <div style="background: {bg_color}; 
                        border: 2px solid {border_color}; 
                        border-left: 6px solid {border_color};
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        margin: 1rem 0;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                            <div style="background: {border_color}; color: white; 
                                        padding: 0.5rem 1rem; border-radius: 50%; 
                                        font-weight: bold; font-size: 1.1rem; margin-right: 1rem;">
                                {pick_num}
                            </div>
                            <div>
                                <h4 style="margin: 0; color: #333; font-size: 1.3rem;">{name}</h4>
                                <div style="color: #666; font-size: 0.95rem; margin-top: 0.2rem;">
                                    {position} • {college} • {archetype}
                                </div>
                            </div>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 1rem; margin-top: 1rem;">
                            <div style="text-align: center;">
                                <div style="font-size: 1.3rem; font-weight: bold; color: {border_color};">{apg:.1f}</div>
                                <div style="font-size: 0.8rem; color: #666;">APG</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 1.3rem; font-weight: bold; color: {border_color};">{grade}</div>
                                <div style="font-size: 0.8rem; color: #666;">Grade</div>
                            </div>
                        </div>
                    </div>
                    
                    <div style="text-align: right; margin-left: 1rem;">
                        <div style="background: {border_color}; color: white; 
                                    padding: 0.5rem 1rem; border-radius: 20px; 
                                    font-weight: bold; margin-bottom: 0.5rem;">
                            {prob:.1%}
                        </div>
                        <div style="font-size: 0.8rem; color: #666;">Projection</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Résumé de la draft
        st.markdown("### 📊 Draft Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            lottery_avg_prob = draft_order.head(14)['final_gen_probability'].mean()
            st.metric("Lottery Avg Projection", f"{lottery_avg_prob:.1%}")
        
        with col2:
            first_round_guards = len(draft_order.head(30)[draft_order.head(30)['position'].isin(['PG', 'SG'])])
            st.metric("Guards in 1st Round", first_round_guards)
        
        with col3:
            first_round_bigs = len(draft_order.head(30)[draft_order.head(30)['position'].isin(['PF', 'C'])])
            st.metric("Bigs in 1st Round", first_round_bigs)
        
        with col4:
            intl_players = len(draft_order.head(30)[~draft_order.head(30)['college'].str.contains('University|College|State', na=False)])
            st.metric("International Players", intl_players)
    
    except Exception as e:
        st.error(f"Erreur dans la prédiction: {e}")

def create_enhanced_team_fit_analysis(df):
    """Analyse de fit équipe améliorée avec besoins positionnels et de jeu"""
    st.markdown("## 🎯 Enhanced Team Fit Analysis")
    st.caption("Analyzing team needs by position and playing style")
    
    # Définir les besoins des équipes avec pondération
    teams_analysis = {
        'San Antonio Spurs': {
            'positional_needs': {'PG': 0.3, 'SG': 0.7, 'SF': 0.4, 'PF': 0.2, 'C': 0.6},
            'skill_needs': {'scoring': 0.8, 'shooting': 0.9, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.5},
            'team_context': 'Need shooting and scoring around Wembanyama'
        },
        'Portland Trail Blazers': {
            'positional_needs': {'PG': 0.9, 'SG': 0.3, 'SF': 0.6, 'PF': 0.4, 'C': 0.2},
            'skill_needs': {'scoring': 0.6, 'shooting': 0.7, 'playmaking': 0.9, 'defense': 0.5, 'rebounding': 0.3},
            'team_context': 'Desperate need for franchise point guard'
        },
        'Washington Wizards': {
            'positional_needs': {'PG': 0.4, 'SG': 0.5, 'SF': 0.8, 'PF': 0.7, 'C': 0.3},
            'skill_needs': {'scoring': 0.7, 'shooting': 0.6, 'playmaking': 0.5, 'defense': 0.8, 'rebounding': 0.6},
            'team_context': 'Rebuilding - need versatile two-way players'
        },
        'Charlotte Hornets': {
            'positional_needs': {'PG': 0.2, 'SG': 0.4, 'SF': 0.5, 'PF': 0.6, 'C': 0.9},
            'skill_needs': {'scoring': 0.4, 'shooting': 0.5, 'playmaking': 0.3, 'defense': 0.8, 'rebounding': 0.9},
            'team_context': 'Need interior presence and defense'
        },
        'Detroit Pistons': {
            'positional_needs': {'PG': 0.3, 'SG': 0.8, 'SF': 0.7, 'PF': 0.3, 'C': 0.4},
            'skill_needs': {'scoring': 0.8, 'shooting': 0.9, 'playmaking': 0.4, 'defense': 0.6, 'rebounding': 0.3},
            'team_context': 'Need perimeter scoring and shooting'
        }
    }
    
    # Sélection du mode d'analyse
    analysis_mode = st.radio("Analysis Mode:", ["Team Perspective", "Player Perspective", "Best Fits Matrix"], horizontal=True)
    
    if analysis_mode == "Team Perspective":
        selected_team = st.selectbox("Select Team:", list(teams_analysis.keys()))
        team_data = teams_analysis[selected_team]
        
        st.markdown(f"### {selected_team} - Draft Analysis")
        st.info(f"**Team Context:** {team_data['team_context']}")
        
        # Calculer les fits pour cette équipe
        player_fits = []
        
        for _, player in df.head(20).iterrows():
            fit_score = 0
            fit_reasons = []
            
            # Score positionnel
            position = safe_string(player['position'])
            if position != 'N/A':
                pos_score = team_data['positional_needs'].get(position, 0) * 40
                fit_score += pos_score
                if pos_score > 20:
                    fit_reasons.append(f"Fills {position} need ({pos_score:.0f}%)")
            
            # Score des compétences
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
                fit_reasons.append(f"Good shooter ({three_pt:.1%} 3P%)")
            
            # Playmaking
            if apg > 5 and team_data['skill_needs']['playmaking'] > 0.6:
                skill_score = team_data['skill_needs']['playmaking'] * 15
                fit_score += skill_score
                fit_reasons.append(f"Elite playmaker ({apg:.1f} APG)")
            
            # Defense
            if (spg + bpg) > 2 and team_data['skill_needs']['defense'] > 0.6:
                skill_score = team_data['skill_needs']['defense'] * 15
                fit_score += skill_score
                fit_reasons.append(f"Defensive impact ({spg+bpg:.1f} STL+BLK)")
            
            # Rebounding
            if rpg > 7 and team_data['skill_needs']['rebounding'] > 0.6:
                skill_score = team_data['skill_needs']['rebounding'] * 15
                fit_score += skill_score
                fit_reasons.append(f"Strong rebounder ({rpg:.1f} RPG)")
            
            # Normaliser le score
            fit_score = min(100, max(0, fit_score))
            
            player_fits.append({
                'name': safe_string(player['name']),
                'position': position,
                'fit_score': fit_score,
                'reasons': fit_reasons,
                'rank': safe_numeric(player.get('final_rank', 0))
            })
        
        # Trier par fit score
        player_fits.sort(key=lambda x: x['fit_score'], reverse=True)
        
        # Afficher les meilleurs fits
        st.markdown("### 🎯 Best Fits for This Team")
        
        for i, fit in enumerate(player_fits[:10]):
            color = '#10b981' if fit['fit_score'] > 70 else '#f59e0b' if fit['fit_score'] > 50 else '#6b7280'
            
            st.markdown(f"""
            <div style="background: white; 
                        border: 2px solid {color}; 
                        border-left: 6px solid {color};
                        padding: 1.5rem; 
                        border-radius: 12px; 
                        margin: 1rem 0;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
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
    
    elif analysis_mode == "Player Perspective":
        selected_player = st.selectbox("Select Player:", df['name'].head(15).tolist())
        
        # Calculer les fits pour ce joueur
        player_data = df[df['name'] == selected_player].iloc[0]
        team_fits = []
        
        for team, team_data in teams_analysis.items():
            fit_score = 0
            fit_reasons = []
            
            # Score positionnel
            position = safe_string(player_data['position'])
            if position != 'N/A':
                pos_score = team_data['positional_needs'].get(position, 0) * 40
                fit_score += pos_score
                if pos_score > 20:
                    fit_reasons.append(f"Team needs {position}")
            
            # Score des compétences (même logique que ci-dessus)
            ppg = safe_numeric(player_data.get('ppg', 0))
            three_pt = safe_numeric(player_data.get('three_pt_pct', 0))
            apg = safe_numeric(player_data.get('apg', 0))
            spg = safe_numeric(player_data.get('spg', 0))
            bpg = safe_numeric(player_data.get('bpg', 0))
            rpg = safe_numeric(player_data.get('rpg', 0))
            
            # Ajouter les scores de compétence
            if ppg > 15 and team_data['skill_needs']['scoring'] > 0.6:
                fit_score += team_data['skill_needs']['scoring'] * 15
                fit_reasons.append("Team needs scoring")
            
            if three_pt > 0.35 and team_data['skill_needs']['shooting'] > 0.6:
                fit_score += team_data['skill_needs']['shooting'] * 15
                fit_reasons.append("Team needs shooting")
            
            if apg > 5 and team_data['skill_needs']['playmaking'] > 0.6:
                fit_score += team_data['skill_needs']['playmaking'] * 15
                fit_reasons.append("Team needs playmaking")
            
            fit_score = min(100, max(0, fit_score))
            
            team_fits.append({
                'team': team,
                'fit_score': fit_score,
                'reasons': fit_reasons,
                'context': team_data['team_context']
            })
        
        # Trier par fit score
        team_fits.sort(key=lambda x: x['fit_score'], reverse=True)
        
        st.markdown(f"### 🎯 Best Team Fits for {selected_player}")
        
        for i, fit in enumerate(team_fits):
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
    
    else:  # Best Fits Matrix
        st.markdown("### 🎯 Team-Player Fit Matrix")
        
        # Créer la matrice
        players = df['name'].head(10).tolist()
        teams = list(teams_analysis.keys())
        
        matrix_data = []
        for player_name in players:
            player_data = df[df['name'] == player_name].iloc[0]
            row = []
            
            for team in teams:
                team_data = teams_analysis[team]
                
                # Calculer le fit score
                fit_score = 0
                position = safe_string(player_data['position'])
                
                if position != 'N/A':
                    fit_score += team_data['positional_needs'].get(position, 0) * 40
                
                # Ajouter les compétences
                ppg = safe_numeric(player_data.get('ppg', 0))
                three_pt = safe_numeric(player_data.get('three_pt_pct', 0))
                apg = safe_numeric(player_data.get('apg', 0))
                
                if ppg > 15:
                    fit_score += team_data['skill_needs']['scoring'] * 15
                if three_pt > 0.35:
                    fit_score += team_data['skill_needs']['shooting'] * 15
                if apg > 5:
                    fit_score += team_data['skill_needs']['playmaking'] * 15
                
                fit_score = min(100, max(0, fit_score))
                row.append(fit_score)
            
            matrix_data.append(row)
        
        # Créer le heatmap
        fig = px.imshow(
            matrix_data,
            labels=dict(x="Team", y="Player", color="Fit Score"),
            x=[team.split()[-1] for team in teams],  # Shortened team names
            y=players,
            color_continuous_scale="RdYlGn",
            title="Team-Player Fit Matrix (Fit Score %)",
            aspect="auto"
        )
        
        fig.update_layout(height=500, font=dict(size=12))
        fig.update_coloraxes(colorbar_title="Fit Score %")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Légende
        st.markdown("""
        **Matrix Legend:**
        - 🟢 **Green (70-100%)**: Excellent fit - player fills major team needs
        - 🟡 **Yellow (40-69%)**: Good fit - player addresses some team needs  
        - 🔴 **Red (0-39%)**: Poor fit - player doesn't match team priorities
        """)

def load_projections_data():
    """Charger les projections générées"""
    try:
        with open('nba_projections.json', 'r') as f:
            return json.load(f)
    except:
        return None

def create_steals_and_busts_section(df, projections_data=None):
    """Section Steals & Busts sécurisée"""
    st.markdown("## 💎 Steals & Busts Analysis")
    
    if projections_data and 'player_projections' in projections_data:
        projections = projections_data['player_projections']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Potential Steals")
            st.caption("Players likely to outperform their draft position")
            
            steals = sorted(projections, key=lambda x: x.get('steal_probability', 0), reverse=True)[:5]
            
            for player in steals:
                if safe_numeric(player.get('steal_probability', 0)) > 0.3:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #10b981, #059669); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>#{player.get('draft_rank', 'N/A')} {safe_string(player.get('name', 'Unknown'))}</strong>
                                <div style="font-size: 0.8rem; opacity: 0.9;">Projected value pick</div>
                            </div>
                            <div style="font-size: 1.5rem; font-weight: bold;">
                                {safe_numeric(player.get('steal_probability', 0)):.0%}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ⚠️ Potential Busts")
            st.caption("High picks with risk of underperforming")
            
            busts = sorted(projections, key=lambda x: x.get('bust_probability', 0), reverse=True)[:5]
            
            for player in busts:
                if safe_numeric(player.get('bust_probability', 0)) > 0.3:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ef4444, #dc2626); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong>#{player.get('draft_rank', 'N/A')} {safe_string(player.get('name', 'Unknown'))}</strong>
                                <div style="font-size: 0.8rem; opacity: 0.9;">High risk selection</div>
                            </div>
                            <div style="font-size: 1.5rem; font-weight: bold;">
                                {safe_numeric(player.get('bust_probability', 0)):.0%}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        # Version simplifiée basée sur les données disponibles
        st.markdown("### 🎯 Projected Steals (Based on Value)")
        st.caption("Players with high potential relative to expected draft position")
        
        # Calculer les "steals" basés sur la probabilité vs rang
        df_analysis = df.copy()
        df_analysis['value_score'] = df_analysis['final_gen_probability'] / (df_analysis['final_rank'] / 60)
        
        steals = df_analysis.nlargest(5, 'value_score')
        
        col1, col2 = st.columns(2)
        
        with col1:
            for _, player in steals.iterrows():
                name = safe_string(player['name'])
                rank = safe_numeric(player['final_rank'])
                prob = safe_numeric(player['final_gen_probability'])
                value = safe_numeric(player['value_score'])
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #10b981, #059669); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>#{rank:.0f} {name}</strong>
                            <div style="font-size: 0.8rem; opacity: 0.9;">
                                {prob:.1%} potential, {rank:.0f} ranking
                            </div>
                        </div>
                        <div style="font-size: 1.5rem; font-weight: bold;">
                            {value:.1f}x
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("### ⚠️ Potential Reaches")
            st.caption("High picks that may not meet expectations")
            
            # Calculer les "busts" - rang élevé mais probabilité plus faible
            reaches = df_analysis.head(15).nsmallest(5, 'final_gen_probability')
            
            for _, player in reaches.iterrows():
                name = safe_string(player['name'])
                rank = safe_numeric(player['final_rank'])
                prob = safe_numeric(player['final_gen_probability'])
                
                risk_level = "High" if prob < 0.5 else "Medium"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444, #dc2626); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>#{rank:.0f} {name}</strong>
                            <div style="font-size: 0.8rem; opacity: 0.9;">
                                {prob:.1%} projection - {risk_level} risk
                            </div>
                        </div>
                        <div style="font-size: 1.5rem; font-weight: bold;">
                            ⚠️
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def create_enhanced_swot_analysis(df):
    """Analyse SWOT renforcée et détaillée"""
    st.markdown("## 📋 Enhanced SWOT Analysis")
    
    # Sélection du joueur
    try:
        selected_player = st.selectbox("Select a player for detailed SWOT analysis:", df['name'].head(15).tolist())
        player_data = df[df['name'] == selected_player].iloc[0]
    except Exception as e:
        st.error(f"Erreur lors de la sélection du joueur: {e}")
        return
    
    # Extraction des données avec gestion d'erreurs
    try:
        ppg = safe_numeric(player_data.get('ppg', 0))
        rpg = safe_numeric(player_data.get('rpg', 0))
        apg = safe_numeric(player_data.get('apg', 0))
        spg = safe_numeric(player_data.get('spg', 0))
        bpg = safe_numeric(player_data.get('bpg', 0))
        age = safe_numeric(player_data.get('age', 20))
        position = safe_string(player_data.get('position', 'Unknown'))
        grade = safe_string(player_data.get('scout_grade', 'N/A'))
        college = safe_string(player_data.get('college', 'Unknown'))
        prob = safe_numeric(player_data.get('final_gen_probability', player_data.get('ml_gen_probability', 0.5)))
        three_pt_pct = safe_numeric(player_data.get('three_pt_pct', 0))
        fg_pct = safe_numeric(player_data.get('fg_pct', 0))
        archetype = safe_string(player_data.get('archetype', 'N/A'))
    except Exception as e:
        st.error(f"Erreur lors de l'extraction des données: {e}")
        return
    
    # Initialisation SWOT
    swot = {
        'strengths': [],
        'weaknesses': [], 
        'opportunities': [],
        'threats': []
    }
    
    # Analyse des FORCES (plus détaillée)
    try:
        if ppg > 20:
            swot['strengths'].append(f"Elite scorer averaging {ppg:.1f} PPG - shows ability to create offense at high level")
        elif ppg > 15:
            swot['strengths'].append(f"Strong scoring ability ({ppg:.1f} PPG) with room for growth in NBA")
        elif ppg > 10:
            swot['strengths'].append(f"Solid contributor ({ppg:.1f} PPG) who can score efficiently")
        
        if three_pt_pct > 0.40:
            swot['strengths'].append(f"Elite shooter ({three_pt_pct:.1%} 3P%) - immediate floor spacing threat")
        elif three_pt_pct > 0.35:
            swot['strengths'].append(f"Good shooter ({three_pt_pct:.1%} 3P%) - valuable skill in modern NBA")
        
        if apg > 7:
            swot['strengths'].append(f"Exceptional playmaker ({apg:.1f} APG) - rare court vision and basketball IQ")
        elif apg > 5:
            swot['strengths'].append(f"Excellent facilitator ({apg:.1f} APG) who elevates teammates")
        elif apg > 3:
            swot['strengths'].append(f"Good ball movement skills ({apg:.1f} APG) for modern basketball")
        
        if rpg > 10:
            swot['strengths'].append(f"Dominant rebounder ({rpg:.1f} RPG) - controls the glass on both ends")
        elif rpg > 7:
            swot['strengths'].append(f"Strong rebounding presence ({rpg:.1f} RPG) especially for position")
        elif rpg > 5:
            swot['strengths'].append(f"Solid on the boards ({rpg:.1f} RPG) with good positioning")
        
        if spg > 2:
            swot['strengths'].append(f"Elite defensive instincts ({spg:.1f} SPG) - disrupts opposing offenses")
        elif spg > 1.5:
            swot['strengths'].append(f"Active defender ({spg:.1f} SPG) with good anticipation")
        
        if bpg > 2:
            swot['strengths'].append(f"Rim protector ({bpg:.1f} BPG) - alters shots and defends the paint")
        elif bpg > 1:
            swot['strengths'].append(f"Shot blocking ability ({bpg:.1f} BPG) provides interior defense")
        
        if age < 19:
            swot['strengths'].append(f"Extremely young at {age:.0f} years old - massive upside potential")
        elif age < 20:
            swot['strengths'].append(f"Young prospect at {age:.0f} - still developing physically and mentally")
        
        if grade in ['A+', 'A']:
            swot['strengths'].append(f"Top-tier prospect ({grade} grade) with elite talent evaluation")
        elif grade in ['A-', 'B+']:
            swot['strengths'].append(f"High-level prospect ({grade} grade) with strong fundamentals")
        
        if prob > 0.8:
            swot['strengths'].append(f"Exceptional talent projection ({prob:.1%}) - franchise-changing potential")
        elif prob > 0.6:
            swot['strengths'].append(f"High ceiling player ({prob:.1%}) with All-Star upside")
        
        if archetype in ['Elite Scorer', 'Elite Shooter', 'Two-Way Wing']:
            swot['strengths'].append(f"Perfect archetype ({archetype}) for modern NBA")
    except Exception as e:
        st.warning(f"Erreur lors de l'analyse des forces: {e}")
        swot['strengths'].append("Données insuffisantes pour analyse complète des forces")
    
    # Analyse des FAIBLESSES (plus détaillée)
    try:
        if ppg < 8:
            swot['weaknesses'].append(f"Limited scoring output ({ppg:.1f} PPG) - needs to develop offensive game")
        
        if three_pt_pct < 0.30 and position in ['SG', 'SF']:
            swot['weaknesses'].append(f"Below-average shooting ({three_pt_pct:.1%} 3P%) for wing player")
        
        if fg_pct < 0.40:
            swot['weaknesses'].append(f"Shooting efficiency concerns ({fg_pct:.1%} FG%) - may struggle vs NBA defense")
        
        if apg < 2 and position in ['PG', 'SG']:
            swot['weaknesses'].append(f"Limited playmaking ({apg:.1f} APG) for guard position")
        
        if rpg < 4 and position in ['PF', 'C']:
            swot['weaknesses'].append(f"Rebounding concerns ({rpg:.1f} RPG) for frontcourt player")
        
        if age > 21:
            swot['weaknesses'].append(f"Advanced age ({age:.0f}) limits developmental ceiling")
        elif age > 20:
            swot['weaknesses'].append(f"Older prospect ({age:.0f}) with less room for growth")
        
        if spg < 1 and bpg < 0.5:
            swot['weaknesses'].append("Defensive impact concerns - needs to improve activity on that end")
        
        if prob < 0.4:
            swot['weaknesses'].append(f"Lower projection ({prob:.1%}) suggests limited upside")
        
        if grade in ['C+', 'C', 'C-']:
            swot['weaknesses'].append(f"Concerning scout grade ({grade}) indicates significant flaws")
    except Exception as e:
        st.warning(f"Erreur lors de l'analyse des faiblesses: {e}")
        swot['weaknesses'].append("Analyse des faiblesses indisponible")
    
    # Analyse des OPPORTUNITÉS (plus détaillée)
    try:
        if position == 'PG':
            swot['opportunities'].append("Point guard premium in NBA - high value position with leadership upside")
        elif position in ['SF', 'PF']:
            swot['opportunities'].append("Versatile forward - ideal for positionless basketball trends")
        elif position == 'C':
            swot['opportunities'].append("Modern center evolution - opportunity to redefine the position")
        elif position == 'SG':
            swot['opportunities'].append("Wing scorer premium - teams always need perimeter scoring")
        
        if college in ['Duke', 'Kentucky', 'North Carolina', 'Kansas']:
            swot['opportunities'].append(f"Blue-blood program ({college}) provides elite coaching and NBA pipeline")
        
        if age < 20:
            swot['opportunities'].append("Multiple years of development before prime - long runway for growth")
        
        if three_pt_pct > 0.35:
            swot['opportunities'].append("Shooting translates immediately - valuable role player floor")
        
        if archetype in ['Elite Shooter', 'Floor General']:
            swot['opportunities'].append(f"{archetype} skills are always in demand across NBA teams")
        
        swot['opportunities'].append("Perfect timing for modern NBA - league values versatility and skill")
        swot['opportunities'].append("Analytics revolution creates new pathways to impact winning")
        
        if prob > 0.7:
            swot['opportunities'].append("High projection creates franchise cornerstone potential")
    except Exception as e:
        st.warning(f"Erreur lors de l'analyse des opportunités: {e}")
        swot['opportunities'].append("Opportunités standards NBA modernes")
    
    # Analyse des MENACES (plus détaillée)
    try:
        injury_risks = {
            'C': "Injury risk for big men - historically higher rates due to size and physicality",
            'PF': "Physical play increases injury exposure - contact in paint takes toll", 
            'PG': "Ball-handling load creates wear and tear - high usage can lead to fatigue",
            'SG': "Cutting and movement patterns stress joints - perimeter play demands durability",
            'SF': "Jack-of-all-trades role requires durability across multiple skill areas"
        }
        
        if position in injury_risks:
            swot['threats'].append(injury_risks[position])
        
        if prob > 0.7:
            swot['threats'].append("High expectations as top prospect - media pressure and immediate performance demands")
        elif prob < 0.4:
            swot['threats'].append("Low projection may limit opportunities - teams might not invest development time")
        
        if age > 21:
            swot['threats'].append("Age concerns may accelerate timeline - less patience for development")
        elif age < 18:
            swot['threats'].append("Extremely young - may not be physically ready for NBA competition")
        
        if college not in ['Duke', 'Kentucky', 'North Carolina', 'Kansas', 'Gonzaga']:
            swot['threats'].append("Lesser program exposure - may need to prove worth at next level")
        
        if three_pt_pct < 0.30:
            swot['threats'].append("Poor shooting limits role versatility in modern NBA")
        
        swot['threats'].append("Intense competition for playing time with veterans and other prospects")
        swot['threats'].append("Adjustment period to NBA pace, physicality, and travel demands")
        
        if position == 'C' and three_pt_pct < 0.25:
            swot['threats'].append("Traditional big man skillset may limit ceiling in modern NBA")
    except Exception as e:
        st.warning(f"Erreur lors de l'analyse des menaces: {e}")
        swot['threats'].append("Défis standards d'adaptation NBA")
    
    # Garantir un minimum d'éléments
    if not swot['strengths']:
        swot['strengths'].append("Solid fundamental skills and basketball IQ")
    if not swot['weaknesses']:
        swot['weaknesses'].append("Needs time to adapt to NBA level competition")
    if not swot['opportunities']:
        swot['opportunities'].append("Modern NBA values versatile skillsets")
    if not swot['threats']:
        swot['threats'].append("Standard rookie adjustment challenges")
    
    # Affichage des résultats
    try:
        display_swot_results(swot, selected_player, position, prob, archetype)
    except Exception as e:
        st.error(f"Erreur lors de l'affichage: {e}")

def display_swot_results(swot, player_name, position, prob, archetype):
    """Affiche les résultats SWOT avec styling amélioré"""
    col1, col2 = st.columns(2)
    
    with col1:
        # Strengths
        st.markdown("""
        <div style="background: linear-gradient(135deg, #10b981, #059669); 
                    border-radius: 15px; padding: 2rem; margin: 1rem 0; color: white;
                    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);">
            <h3 style="margin: 0 0 1rem 0; display: flex; align-items: center;">
                💪 <span style="margin-left: 0.5rem;">Strengths</span>
            </h3>
        """, unsafe_allow_html=True)
        
        for i, strength in enumerate(swot['strengths'], 1):
            st.markdown(f"**{i}.** {strength}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Opportunities
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3b82f6, #2563eb); 
                    border-radius: 15px; padding: 2rem; margin: 1rem 0; color: white;
                    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);">
            <h3 style="margin: 0 0 1rem 0; display: flex; align-items: center;">
                🚀 <span style="margin-left: 0.5rem;">Opportunities</span>
            </h3>
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
            <h3 style="margin: 0 0 1rem 0; display: flex; align-items: center;">
                ⚠️ <span style="margin-left: 0.5rem;">Weaknesses</span>
            </h3>
        """, unsafe_allow_html=True)
        
        for i, weakness in enumerate(swot['weaknesses'], 1):
            st.markdown(f"**{i}.** {weakness}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Threats
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ef4444, #dc2626); 
                    border-radius: 15px; padding: 2rem; margin: 1rem 0; color: white;
                    box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);">
            <h3 style="margin: 0 0 1rem 0; display: flex; align-items: center;">
                🎯 <span style="margin-left: 0.5rem;">Threats</span>
            </h3>
        """, unsafe_allow_html=True)
        
        for i, threat in enumerate(swot['threats'], 1):
            st.markdown(f"**{i}.** {threat}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Résumé exécutif amélioré
    st.markdown("### 📊 Executive Summary")
    
    summary_color = '#10b981' if prob > 0.7 else '#f59e0b' if prob > 0.5 else '#ef4444'
    risk_level = 'Low Risk' if prob > 0.7 else 'Medium Risk' if prob > 0.5 else 'High Risk'
    ceiling = 'All-Star+' if prob > 0.8 else 'Starter' if prob > 0.6 else 'Role Player' if prob > 0.4 else 'Depth'
    
    st.markdown(f"""
    <div style="background: {summary_color}20; border: 2px solid {summary_color}; 
                border-radius: 15px; padding: 2rem; margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
            <h4 style="margin: 0; color: {summary_color}; font-size: 1.3rem;">
                Overall Assessment: {risk_level}
            </h4>
            <div style="text-align: right;">
                <span style="background: {summary_color}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold; font-size: 1.1rem;">
                    {prob:.1%} Projection
                </span>
                <div style="font-size: 0.9rem; color: #666; margin-top: 0.3rem;">Ceiling: {ceiling}</div>
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1rem 0;">
            <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #10b981;">{len(swot['strengths'])}</div>
                <div style="font-size: 0.9rem; color: #666;">Key Strengths</div>
            </div>
            <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #f59e0b;">{len(swot['weaknesses'])}</div>
                <div style="font-size: 0.9rem; color: #666;">Areas to Improve</div>
            </div>
            <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #3b82f6;">{len(swot['opportunities'])}</div>
                <div style="font-size: 0.9rem; color: #666;">Opportunities</div>
            </div>
            <div style="text-align: center; padding: 1rem; background: white; border-radius: 10px;">
                <div style="font-size: 1.5rem; font-weight: bold; color: #ef4444;">{len(swot['threats'])}</div>
                <div style="font-size: 0.9rem; color: #666;">Risk Factors</div>
            </div>
        </div>
        
        <p style="color: #333; margin: 1rem 0 0 0; line-height: 1.6; font-size: 1.05rem;">
            <strong>{player_name}</strong> ({position}, {archetype}) projects as a <strong>{risk_level.lower()}</strong> selection 
            with <strong>{ceiling.lower()}</strong> upside. The prospect shows {len(swot['strengths'])} key strengths 
            that translate well to the NBA, while having {len(swot['weaknesses'])} areas requiring development. 
            With {len(swot['opportunities'])} clear opportunities in today's league and {len(swot['threats'])} 
            potential challenges to navigate, this player represents a {prob:.1%} likelihood of becoming 
            a generational talent.
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_manual_projections():
    """Créer des projections manuelles réalistes"""
    st.markdown("### 🔮 Realistic Development Projections")
    
    # Interface pour sélectionner un joueur
    df = st.session_state.get('current_df')
    if df is None:
        st.warning("Données non disponibles")
        return
    
    try:
        player_names = df['name'].head(20).tolist()
        selected_player = st.selectbox("Select a player for projection:", player_names)
        
        player_data = df[df['name'] == selected_player].iloc[0]
        
        # Stats de base
        current_ppg = safe_numeric(player_data.get('ppg', 0))
        current_rpg = safe_numeric(player_data.get('rpg', 0))
        current_apg = safe_numeric(player_data.get('apg', 0))
        age = safe_numeric(player_data.get('age', 19))
        position = safe_string(player_data.get('position', 'N/A'))
        archetype = safe_string(player_data.get('archetype', 'N/A'))
    except Exception as e:
        st.error(f"Erreur lors de la sélection du joueur: {e}")
        return
    
    # Projections réalistes basées sur l'âge, la position et l'archétype
    def project_realistic_development(current_stat, position, stat_type, age, archetype):
        """Projette le développement réaliste d'une statistique"""
        
        # Facteurs de développement par position et type de stat
        development_factors = {
            'PG': {'ppg': 1.3, 'rpg': 1.1, 'apg': 1.4},
            'SG': {'ppg': 1.4, 'rpg': 1.2, 'apg': 1.2},
            'SF': {'ppg': 1.3, 'rpg': 1.3, 'apg': 1.3},
            'PF': {'ppg': 1.2, 'rpg': 1.4, 'apg': 1.1},
            'C': {'ppg': 1.1, 'rpg': 1.5, 'apg': 1.0}
        }
        
        # Bonus d'archétype
        archetype_bonus = {
            'Elite Scorer': {'ppg': 1.2, 'rpg': 1.0, 'apg': 1.0},
            'Elite Shooter': {'ppg': 1.15, 'rpg': 1.0, 'apg': 1.05},
            'Floor General': {'ppg': 1.05, 'rpg': 1.0, 'apg': 1.3},
            'Two-Way Wing': {'ppg': 1.1, 'rpg': 1.1, 'apg': 1.1},
            'Rim Protector': {'ppg': 1.0, 'rpg': 1.2, 'apg': 1.0}
        }
        
        # Facteur d'âge (plus jeune = plus de croissance)
        age_factor = max(0.8, 1.5 - (age - 18) * 0.12)
        
        # Facteur de position
        pos_factor = development_factors.get(position, {'ppg': 1.2, 'rpg': 1.2, 'apg': 1.2})[stat_type]
        
        # Bonus d'archétype
        arch_factor = archetype_bonus.get(archetype, {'ppg': 1.0, 'rpg': 1.0, 'apg': 1.0})[stat_type]
        
        # Croissance réaliste sur 5 ans
        total_factor = age_factor * pos_factor * arch_factor
        
        # Progression année par année (plus forte au début)
        yearly_growth = [
            current_stat * 0.85,  # Année rookie (baisse initiale)
            current_stat * 0.95,  # Année 2 - ajustement
            current_stat * 1.15,  # Année 3 - amélioration significative
            current_stat * total_factor * 0.9,  # Année 4 - croissance
            current_stat * total_factor  # Année 5 - pic
        ]
        
        return yearly_growth
    
    try:
        # Générer les projections
        years = list(range(1, 6))
        projected_ppg = project_realistic_development(current_ppg, position, 'ppg', age, archetype)
        projected_rpg = project_realistic_development(current_rpg, position, 'rpg', age, archetype)
        projected_apg = project_realistic_development(current_apg, position, 'apg', age, archetype)
        
        # Graphique des projections
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Points Per Game', 'Rebounds Per Game', 'Assists Per Game', 'Overall Development'),
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        # PPG avec courbe réaliste
        fig.add_trace(
            go.Scatter(x=years, y=projected_ppg, mode='lines+markers', name='PPG',
                      line=dict(color='#FF6B35', width=4),
                      marker=dict(size=12)),
            row=1, col=1
        )
        
        # RPG
        fig.add_trace(
            go.Scatter(x=years, y=projected_rpg, mode='lines+markers', name='RPG',
                      line=dict(color='#4361EE', width=4),
                      marker=dict(size=12)),
            row=1, col=2
        )
        
        # APG
        fig.add_trace(
            go.Scatter(x=years, y=projected_apg, mode='lines+markers', name='APG',
                      line=dict(color='#10B981', width=4),
                      marker=dict(size=12)),
            row=2, col=1
        )
        
        # Overall impact (combined metric)
        overall_impact = [(p+r+a)/3 for p, r, a in zip(projected_ppg, projected_rpg, projected_apg)]
        fig.add_trace(
            go.Scatter(x=years, y=overall_impact, mode='lines+markers', name='Overall',
                      line=dict(color='#8B5CF6', width=4),
                      marker=dict(size=12)),
            row=2, col=2
        )
        
        fig.update_layout(height=600, title=f"{selected_player} - Realistic 5-Year Development Curve", showlegend=False)
        fig.update_xaxes(title_text="NBA Season", tickvals=years, ticktext=[f"Year {y}" for y in years])
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erreur lors de la création des graphiques: {e}")
        return
    
    try:
        # Métriques de projection détaillées
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            improvement = ((projected_ppg[-1] - projected_ppg[0]) / projected_ppg[0]) * 100 if projected_ppg[0] > 0 else 0
            st.metric(
                "5-Year PPG Growth", 
                f"+{improvement:.1f}%",
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
            # All-Star probability basée sur les stats projetées et l'archétype
            final_stats = projected_ppg[-1] + projected_rpg[-1] + projected_apg[-1]
            archetype_bonus = 10 if archetype in ['Elite Scorer', 'Two-Way Wing'] else 5
            all_star_prob = min(95, max(5, (final_stats - 15) * 3 + archetype_bonus))
            st.metric(
                "All-Star Probability", 
                f"{all_star_prob:.0f}%",
                "By Year 5"
            )
        
        with col4:
            # Probabilité MVP basée sur des stats exceptionnelles
            mvp_threshold = projected_ppg[-1] * 1.5 + projected_rpg[-1] + projected_apg[-1] * 1.2
            mvp_prob = min(25, max(0, (mvp_threshold - 35) * 2))
            st.metric(
                "MVP Candidate Chance",
                f"{mvp_prob:.0f}%",
                "Peak Years"
            )
        
    except Exception as e:
        st.error(f"Erreur lors de l'affichage des métriques: {e}")
    
    # Explication de la logique avec archétype
    st.markdown("### 📝 Projection Logic")
    st.info(f"""
    **Development Curve Reasoning for {selected_player}:**
    - **Archetype Impact**: {archetype} players typically excel in specific areas with tailored development paths
    - **Year 1-2**: Rookie adjustment period with initial efficiency dip due to NBA learning curve
    - **Year 3**: Adaptation complete, stats surpass college level with improved NBA understanding
    - **Year 4-5**: Prime development years with position-specific and archetype-based growth patterns
    - **Age Factor**: {age:.0f} years old provides {('excellent' if age < 19 else 'good' if age < 21 else 'limited')} development runway
    - **Position Ceiling**: {position} players in the {archetype} mold typically peak in {('scoring and versatility' if position in ['SG', 'SF'] else 'playmaking and leadership' if position == 'PG' else 'interior dominance' if position in ['PF', 'C'] else 'overall impact')}
    """)

def main():
    """Fonction principale avec toutes les améliorations"""
    try:
        df = load_final_data()
        
        if df is None or df.empty:
            st.error("❌ Impossible de charger les données")
            st.stop()
        
        # Stocker df dans session state pour les projections
        st.session_state['current_df'] = df
        
        projections_data = load_projections_data()
        
        display_hero_header()
        display_draft_countdown()
        
        # Navigation avec toutes les nouvelles fonctionnalités
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
            "🏠 Dashboard",
            "📊 Compare Players", 
            "🔍 Enhanced Search",
            "📋 Full Draft Prediction",
            "💎 Steals & Busts",
            "📈 5-Year Projections", 
            "🏀 Historical Comps",
            "📋 SWOT Analysis",
            "🎯 Team Fit Analysis"
        ])
        
        with tab1:
            st.markdown("## 📈 Dashboard Overview")
            
            # Leaders section
            create_leaders_section(df)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Prospects", len(df))
            with col2:
                st.metric("Avg PPG", f"{safe_numeric(df['ppg'].mean()):.1f}")
            with col3:
                st.metric("Avg RPG", f"{safe_numeric(df['rpg'].mean()):.1f}")
            with col4:
                st.metric("Avg APG", f"{safe_numeric(df['apg'].mean()):.1f}")
            
            filtered_df = create_interactive_filters(df)
            
            # Graphiques améliorés
            col1, col2 = st.columns(2)
            
            with col1:
                try:
                    if 'position' in filtered_df.columns:
                        position_counts = filtered_df['position'].value_counts()
                        fig_pie = px.pie(
                            values=position_counts.values,
                            names=position_counts.index,
                            title="Distribution by Position",
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)
                except:
                    st.info("Graphique position non disponible")
            
            with col2:
                try:
                    fig_bar = px.bar(
                        filtered_df.head(10),
                        x='name',
                        y='ppg',
                        title="Top Scorers",
                        color='ppg',
                        color_continuous_scale='Viridis'
                    )
                    fig_bar.update_xaxes(tickangle=45)
                    st.plotly_chart(fig_bar, use_container_width=True)
                except:
                    st.info("Graphique scores non disponible")
            
            # Table des prospects avec plus de colonnes
            try:
                display_cols = ['name', 'position', 'college', 'ppg', 'rpg', 'apg', 'three_pt_pct', 'scout_grade', 'archetype']
                available_cols = [col for col in display_cols if col in filtered_df.columns]
                
                if available_cols:
                    display_df = filtered_df[available_cols].head(20).copy()
                    if 'three_pt_pct' in display_df.columns:
                        display_df['three_pt_pct'] = display_df['three_pt_pct'].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "N/A")
                    
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"Erreur affichage table: {e}")
        
        with tab2:
            create_enhanced_comparison(df)
        
        with tab3:
            create_enhanced_search_functionality(df)
        
        with tab4:
            create_full_draft_prediction(df)
        
        with tab5:
            create_steals_and_busts_section(df, projections_data)
        
        with tab6:
            create_manual_projections()
        
        with tab7:
            create_realistic_historical_comparisons(df)
        
        with tab8:
            create_enhanced_swot_analysis(df)
        
        with tab9:
            create_enhanced_team_fit_analysis(df)
        
        # Footer amélioré
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #666;">
            🏀 <strong>NBA Draft 2025 AI Dashboard</strong> | Enhanced Analytics & Projections<br>
            <small>Featuring 60 prospects with advanced stats, realistic comparisons, and comprehensive team fit analysis</small>
        </div>
        """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Erreur générale: {e}")
        st.info("Essayez de recharger la page ou vérifiez vos données")

if __name__ == "__main__":
    main()