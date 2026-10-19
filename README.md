# 🇰🇪 Spatial Analysis & Infrastructure Mapping of Kenyan Healthcare Facilities

An end-to-end data engineering and geospatial analysis pipeline built entirely in **Python** using **PyCharm**. This project opens, cleans, structures, and visualizes an administrative healthcare dataset of **6,762 facilities** across Kenya, transforming raw location metadata into an interactive geographic intelligence dashboard.

---

## 🛠️ Data Engineering & Robustness Framework
Real-world regional public health datasets are notoriously unstructured. This pipeline implements several programmatic safeguards to cleanly ingest malformed spreadsheet structures:

* **Format Agnostic Ingestion:** Bypasses memory allocation failures and `Buffer overflow` text tokenization errors by natively decoding binary structures using the `openpyxl` engine.
* **Algorithmic Spatial Self-Correction:** Implements an advanced regular expression parser that automatically identifies latitude and longitude indices by validating real-world bounding boxes for Kenya (Lat: `-5.0 to 5.0`, Lon: `33.0 to 42.0`). This dynamically corrects flipped data columns without losing database rows.
* **Encoding & Quote Resiliency:** Uses `latin1` code pages and explicit quoting overrides (`quoting=3`) to safely parse text files containing unmatched quotation marks or local geographic annotations.

---

## 📊 Infrastructure Insights & Core Findings

The pipeline successfully mapped **4,862 high-confidence facility coordinates** after dropping entries with missing or corrupted spatial data, uncovering significant distribution insights:

### 1. Regional Density Leaders (Top 10 Counties)
The data shows that healthcare facility footprints are densely clustered across several high-population counties, led by Western, Coastal, and Eastern representations:
1. **Kakamega** (219 facilities)
2. **Kilifi** (208 facilities)
3. **Makueni** (191 facilities)
4. **Meru** (189 facilities)
5. **Kisii** (184 facilities)
6. *Remaining Top 10:* Nakuru (181), Murang'a (171), Nairobi (170), Kiambu (166), and Nyeri (141).

### 2. Micro-Level Clustering (Top 10 Constituencies)
When drilling past county boundaries into specific constituencies, the script revealed highly concentrated localized medical footprints. **Shinyalu Constituency** leads the country in overall numbers:

| Constituency | County Context | Active Facility Count |
| :--- | :--- | :---: |
| **Shinyalu** | Kakamega | **219** |
| **Kaloleni** | Kilifi | **208** |
| **Kibwezi West** | Makueni | **191** |
| **North ImentI** | Meru | **189** |
| **Nyaribari Chache** | Kisii | **184** |
| **Subukia** | Nakuru | **181** |
| **Mathioya** | Murang'a | **171** |
| **Kamukunji** | Nairobi | **170** |
| **Gatundu North** | Kiambu | **166** |
| **Kieni** | Nyeri | **141** |

---

## 🗺️ Visual Map Architecture & Color-Coding Schema
The generated file `kenya_facilities_map.html` groups facilities using **Marker Clustering matrices** to prevent browser lag. To show structural operational dependencies at a glance, individual pins are dynamically color-coded by their managing **Agency**:

* 🟢 **Green Markers:** Public Sector infrastructure (Ministry of Health / County Government).
* 🔵 **Blue Markers:** Mission and Faith-Based facilities (Church groups / Christian Health Associations).
* 🟠 **Orange Markers:** Non-Governmental Organizations (NGOs and Non-Profits).
* 🌐 **Cadet Blue Markers:** Private sectors, local medical centers, and private clinics.
