"""
Company Ranker Module
Tier-based company reputation scoring for AI Job Agent.
Prioritizes Top 40 India + Global MNCs, suppresses unknown startups.
"""

import re
from typing import Dict, Tuple


# ============================================
# TIER 1: TOP 40 INDIA + GLOBAL MNCs (Score: 1.0)
# ============================================

TIER_1_COMPANIES = {
    # Big 4 Consulting
    "deloitte", "ey", "kpmg", "pwc",
    
    # Indian IT Giants
    "tcs", "tata consultancy", "infosys", "wipro", "hcl technologies", "tech mahindra",
    "ltimindtree", "l&t infotech", "mphasis", "persistent systems",
    
    # Global Tech Giants
    "google", "microsoft", "amazon", "apple", "meta", "facebook",
    "adobe", "ibm", "oracle", "salesforce", "sap", "cisco",
    "intel", "nvidia", "qualcomm", "vmware", "red hat",
    
    # Global Consulting
    "accenture", "capgemini", "cognizant", "genpact", "mckinsey",
    "bcg", "boston consulting", "bain", "bain & company",
    
    # Financial Services
    "jp morgan", "jpmorgan", "goldman sachs", "morgan stanley",
    "citi", "citigroup", "hsbc", "barclays", "wells fargo",
    "american express", "amex", "blackrock", "deutsche bank",
    
    # Indian Unicorns & Major Startups
    "flipkart", "swiggy", "zomato", "paytm", "phonepe", "razorpay",
    "ola", "ola electric", "meesho", "byju", "byjus", "udaan",
    "cred", "zerodha", "groww", "upstox", "dream11",
    
    # Indian Conglomerates
    "reliance", "tata", "tata group", "mahindra", "aditya birla",
    "larsen & toubro", "l&t", "godrej", "bajaj", "essar",
    
    # FMCG & Retail
    "hindustan unilever", "hul", "itc", "nestle", "britannia",
    "amazon india", "walmart", "myntra", "nykaa",
    
    # E-commerce & Logistics
    "delhivery", "porter", "dunzo", "bigbasket", "jiomart",
    
    # Fintech
    "visa", "mastercard", "rupay", "npci",
    
    # Product Companies
    "zoho", "freshworks", "postman", "browserstack", "druva",
    "hashedin", "thoughtworks", "gojek", "grab",
    
    # Telecom
    "jio", "reliance jio", "airtel", "bharti airtel", "vodafone idea",
    
    # Automotive
    "maruti suzuki", "hyundai", "tata motors", "mahindra & mahindra",
    "ola electric", "hero motocorp",
    
    # Pharma & Healthcare
    "sun pharma", "dr reddy", "cipla", "lupin", "biocon",
    "apollo hospitals", "fortis", "max healthcare", "practo",
    
    # Analytics & Data
    "mu sigma", "fractal analytics", "tiger analytics", "latentview"
}


# ============================================
# TIER 2: STRONG MID-TIER COMPANIES (Score: 0.85)
# ============================================

TIER_2_COMPANIES = {
    # Mid-tier IT Services
    "hexaware", "birlasoft", "cyient", "zensar", "sonata software",
    "mastek", "mindtree", "coforge", "intellect design",
    
    # Product Startups (Well-funded)
    "curefit", "cult.fit", "lenskart", "boat", "noise", "mamaearth",
    "wow skin science", "sugar cosmetics", "plum",
    
    # Edtech
    "unacademy", "vedantu", "toppr", "great learning", "upgrad",
    "simplilearn", "scaler", "coding ninjas", "geeksforgeeks",
    
    # Enterprise SaaS
    "clevertap", "wingify", "exotel", "netcore", "webengage",
    "darwinbox", "leena ai", "haptik", "yellow.ai",
    
    # Gaming
    "dream sports", "games24x7", "mpl", "mobile premier league",
    "winzo", "paytm first games",
    
    # Travel & Hospitality
    "oyo", "makemytrip", "mmt", "goibibo", "ixigo", "cleartrip",
    "easemytrip", "yatra",
    
    # Real Estate Tech
    "99acres", "magicbricks", "housing.com", "nobroker",
    
    # Media & Entertainment
    "hotstar", "disney+ hotstar", "sony liv", "voot", "mx player",
    "sharechat", "moj", "josh",
    
    # HealthTech
    "1mg", "pharmeasy", "netmeds", "apollo 24/7", "mfine",
    
    # Agritech
    "ninjacart", "dehaat", "agrostar", "bijak",
    
    # Logistics & Supply Chain
    "rivigo", "blackbuck", "freightwalla", "locus",
    
    # HR Tech
    "naukri", "naukri.com", "indeed india", "linkedin india",
    "shine", "monster india", "foundit",
    
    # Banking & NBFC
    "bajaj finserv", "hdfc bank", "icici bank", "axis bank",
    "kotak mahindra", "yes bank", "idfc first",
    
    # Insurance
    "policybazaar", "acko", "digit insurance", "tata aia",
    
    # Consulting (Mid-tier)
    "zs associates", "evalueserve", "wns", "wns global",
    
    # Analytics (Mid-tier)
    "edgeverve", "tredence", "affine", "absolutdata"
}


# ============================================
# COMPANY NAME NORMALIZATION
# ============================================

def normalize_company_name(company_name: str) -> str:
    """
    Normalize company name for matching.
    Removes legal suffixes, extra whitespace, special chars.
    
    Args:
        company_name: Raw company name from job posting
    
    Returns:
        Normalized lowercase company name
    """
    if not company_name or not isinstance(company_name, str):
        return ""
    
    # Convert to lowercase
    name = company_name.lower().strip()
    
    # Remove common legal suffixes
    suffixes = [
        r'\bprivate limited\b', r'\bpvt\.?\s*ltd\.?\b', r'\bpvt\b',
        r'\blimited\b', r'\bltd\.?\b', r'\bllp\b', r'\bllc\b',
        r'\binc\.?\b', r'\bcorp\.?\b', r'\bcorporation\b',
        r'\btechnologies\b', r'\btech\b', r'\bsolutions\b',
        r'\bservices\b', r'\bsoftware\b', r'\bsystems\b',
        r'\benterprises\b', r'\bgroup\b', r'\bindia\b',
        r'\bglobal\b', r'\binternational\b', r'\bworldwide\b'
    ]
    
    for suffix in suffixes:
        name = re.sub(suffix, '', name)
    
    # Remove special characters except alphanumeric and spaces
    name = re.sub(r'[^a-z0-9\s&]', ' ', name)
    
    # Normalize multiple spaces to single space
    name = re.sub(r'\s+', ' ', name).strip()
    
    return name


# ============================================
# COMPANY TIER MATCHING
# ============================================

def get_company_tier(company_name: str) -> Tuple[int, float]:
    """
    Determine company tier based on reputation.
    
    Args:
        company_name: Raw company name from job posting
    
    Returns:
        Tuple of (tier_number, company_score)
        - tier_number: 1 (top), 2 (mid), 3 (unknown)
        - company_score: 1.0 (tier 1), 0.85 (tier 2), 0.4 (tier 3)
    """
    if not company_name:
        return 3, 0.4
    
    normalized = normalize_company_name(company_name)
    
    if not normalized:
        return 3, 0.4
    
    # Check Tier 1 (exact or partial match)
    for tier1_company in TIER_1_COMPANIES:
        if tier1_company in normalized or normalized in tier1_company:
            return 1, 1.0
    
    # Check Tier 2 (exact or partial match)
    for tier2_company in TIER_2_COMPANIES:
        if tier2_company in normalized or normalized in tier2_company:
            return 2, 0.85
    
    # Default: Tier 3 (unknown startup)
    return 3, 0.4


# ============================================
# BATCH SCORING
# ============================================

def add_company_scores_to_jobs(jobs: list) -> list:
    """
    Add company_score to each job in the list.
    
    Args:
        jobs: List of job dicts
    
    Returns:
        Same list with 'company_tier', 'company_score' added
    """
    for job in jobs:
        # Extract company from job metadata
        company_name = job.get('company', '') or job.get('source', '')
        
        # Get tier and score
        tier, score = get_company_tier(company_name)
        
        # Add to job
        job['company_tier'] = tier
        job['company_score'] = score
    
    return jobs


# ============================================
# FINAL RANK CALCULATION
# ============================================

def calculate_final_rank(job: dict) -> float:
    """
    Calculate final ranking score.
    
    Formula: final_rank = 0.5 * hybrid_score + 0.5 * company_score
    
    Equal weight to skill match and company reputation.
    
    Args:
        job: Job dict with hybrid_score and company_score
    
    Returns:
        float: Final rank score (0.0 to 1.0)
    """
    hybrid_score = job.get('hybrid_score', 0.0) or 0.0
    company_score = job.get('company_score', 0.4) or 0.4
    
    # Equal weighting
    final_rank = (0.5 * hybrid_score) + (0.5 * company_score)
    
    return round(final_rank, 4)


# ============================================
# TELEGRAM ALERT FILTER
# ============================================

def should_send_telegram_alert(job: dict) -> bool:
    """
    Determine if job should trigger Telegram alert.
    
    Rule: Only Tier 1 and Tier 2 companies (company_score >= 0.85)
    
    Args:
        job: Job dict with company_score
    
    Returns:
        bool: True if alert should be sent
    """
    company_score = job.get('company_score', 0.0)
    
    # Only Tier 1 (1.0) and Tier 2 (0.85)
    return company_score >= 0.85


# ============================================
# DIAGNOSTIC / TESTING
# ============================================

def get_company_info(company_name: str) -> Dict:
    """
    Get detailed company information for debugging.
    
    Args:
        company_name: Company name to analyze
    
    Returns:
        dict with tier, score, normalized_name
    """
    normalized = normalize_company_name(company_name)
    tier, score = get_company_tier(company_name)
    
    tier_labels = {1: "Tier 1 (Top MNC)", 2: "Tier 2 (Mid-tier)", 3: "Tier 3 (Unknown)"}
    
    return {
        'original_name': company_name,
        'normalized_name': normalized,
        'tier': tier,
        'tier_label': tier_labels.get(tier, "Unknown"),
        'company_score': score,
        'telegram_alert': score >= 0.85
    }
