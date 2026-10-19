import os
import re
import pandas as pd
import folium
from folium.plugins import MarkerCluster


def clean_coordinate(coord_str, is_lat=True):
    """Automatically extracts and identifies Kenya coordinates regardless of their column order."""
    if pd.isna(coord_str) or str(coord_str).strip() == "":
        return None
    try:
        # Find all decimal or whole numbers in the text string
        numbers = re.findall(r'[-+]?\d*\.\d+|\d+', str(coord_str))
        if len(numbers) < 2:
            return None

        val1 = float(numbers[0])
        val2 = float(numbers[1])

        # Automatically assign based on Kenya's geographic boundaries
        if is_lat:
            if -5.0 <= val1 <= 5.0:
                return val1
            elif -5.0 <= val2 <= 5.0:
                return val2
        else:
            if 33.0 <= val1 <= 42.0:
                return val1
            elif 33.0 <= val2 <= 42.0:
                return val2
        return None
    except:
        return None


def get_marker_color(agency):
    """Assigns custom visual mapping colors based on the facility managing agency."""
    agency_lower = str(agency).lower()
    if 'ministry' in agency_lower or 'public' in agency_lower or 'government' in agency_lower:
        return 'green'  # Public Sector / MoH
    elif 'faith' in agency_lower or 'christian' in agency_lower or 'church' in agency_lower or 'mission' in agency_lower:
        return 'blue'  # Faith-Based / Mission
    elif 'ngo' in agency_lower or 'non-gov' in agency_lower or 'foundation' in agency_lower:
        return 'orange'  # NGOs / Non-Profits
    elif 'private' in agency_lower or 'clinic' in agency_lower:
        return 'cadetblue'  # Private Entities
    return 'red'  # Others / Unknown


def process_healthcare_map():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Using your working absolute path
    csv_path = r'C:\Users\Hp\Downloads\Health Map.csv'
    output_html = os.path.join(base_dir, 'kenya_facilities_map.html')

    print("📖 Loading your healthcare facilities dataset...")
    if not os.path.exists(csv_path):
        print(f"❌ Could not find file at: {csv_path}")
        return

    # Load dataset as an Excel file to handle the hidden spreadsheet structure safely
    try:
        df = pd.read_excel(csv_path)
    except Exception as e:
        print(f"❌ Failed to parse the spreadsheet structure: {e}")
        return


    print("🧹 Parsing spatial geolocation coordinates...")
    target_col = 'Geolocation' if 'Geolocation' in df.columns else \
    [c for c in df.columns if 'geolocation' in c.lower()][0]

    # Swapping the extraction positions to match your file's coordinate arrangement
    df['Latitude'] = df[target_col].apply(lambda x: clean_coordinate(x, is_lat=True))
    df['Longitude'] = df[target_col].apply(lambda x: clean_coordinate(x, is_lat=False))

    clean_df = df.dropna(subset=['Latitude', 'Longitude'])
    print(f"✅ Successfully mapped {len(clean_df)} out of {len(df)} facilities!")

    # --- PORTFOLIO ANALYSIS INSIGHTS ---
    county_col = 'County' if 'County' in clean_df.columns else [c for c in clean_df.columns if 'county' in c.lower()][0]
    const_col = 'Consituency' if 'Consituency' in clean_df.columns else \
    [c for c in clean_df.columns if 'const' in c.lower()][0]

    print("\n📊 [Insight 1] --- HEALTH FACILITY COUNT BY COUNTY (TOP 10) ---")
    print(clean_df[county_col].value_counts().head(10))

    print("\n🏢 [Insight 2] --- HIGHEST CONCENTRATION OF FACILITIES BY CONSTITUENCY ---")
    const_counts = clean_df[const_col].value_counts().head(10)
    print(const_counts)

    # --- MAP COMPILATION WITH AGENCY COLOR-CODING ---
    print("\n🗺️ Crafting your interactive color-coded geographic map layout...")
    kenya_map = folium.Map(location=[0.0236, 37.9062], zoom_start=6.5)
    marker_cluster = MarkerCluster(name="Health Facilities Hub").add_to(kenya_map)

    name_col = 'Facility Type NAME' if 'Facility Type NAME' in clean_df.columns else 'Facility Type Name'

    for idx, row in clean_df.iterrows():
        agency_name = row.get('Agency', 'Unknown')
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 220px;">
            <h4 style="margin: 0 0 5px 0; color: #2c3e50;">{row.get(name_col, 'Facility')}</h4>
            <hr style="margin: 5px 0;">
            <b>County:</b> {row.get(county_col, 'N/A')}<br>
            <b>Constituency:</b> {row.get(const_col, 'N/A')}<br>
            <b>Managing Agency:</b> {agency_name}<br>
            <b>Type:</b> {row.get('facility type', 'N/A')}
        </div>
        """

        # Color-code dynamically based on Managing Agency value
        color = get_marker_color(agency_name)

        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color=color, icon='plus', prefix='fa')
        ).add_to(marker_cluster)

    kenya_map.save(output_html)
    print(f"\n🎉 Map compiled perfectly! File saved to: {output_html}")
    print("👉 Refresh your browser tab to see the updated interactive color-coded map!")


if __name__ == '__main__':
    process_healthcare_map()

