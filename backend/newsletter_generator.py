import json
from pathlib import Path

def load_content_for_month(month: str) -> dict:
    """Loads the newsletter content for a specific month from the JSON file."""
    content_path = Path(__file__).parent / "content" / "newsletter_content.json"
    with open(content_path, "r") as f:
        content = json.load(f)
    return content.get(month.lower(), {})

def generate_newsletter_html(month: str, dynamic_content: dict) -> str:
    """Generates the final HTML for the newsletter.

    Args:
        month: The month for which to generate the newsletter.
        dynamic_content: A dictionary containing the dynamic parts of the newsletter,
                         like the intro, Q&A, and nursery specials.

    Returns:
        The complete HTML string for the email.
    """
    template_path = Path(__file__).parent / "templates" / "newsletter_template.html"
    with open(template_path, "r") as f:
        html_template = f.read()

    # Fetch the static content for the month
    static_content = load_content_for_month(month)

    # Combine all content into one dictionary for easy replacement
    all_content = {
        "monthName": month.capitalize(),
        "personalIntro": dynamic_content.get("personalIntro", ""),
        "whats_blooming": static_content.get("whats_blooming", ""),
        "whats_blooming_image": static_content.get("whats_blooming_image", ""),
        "time_to_plant_veggies": static_content.get("time_to_plant", {}).get("veggies_herbs", ""),
        "time_to_plant_flowers": static_content.get("time_to_plant", {}).get("flowers_ornamentals", ""),
        "time_to_harvest": static_content.get("time_to_harvest", ""),
        "watering_wisdom": static_content.get("watering_wisdom", ""),
        "fertilizing_facts": static_content.get("fertilizing_facts", ""),
        "pest_disease_patrol": static_content.get("pest_disease_patrol", ""),
        "subscriberQuestion": dynamic_content.get("subscriberQuestion", ""),
        "subscriberAnswer": dynamic_content.get("subscriberAnswer", ""),
        "newArrivals": dynamic_content.get("newArrivals", ""),
        "monthlySpecials": dynamic_content.get("monthlySpecials", ""),
        "upcomingWorkshops": dynamic_content.get("upcomingWorkshops", ""),
    }

    # Replace all placeholders
    for key, value in all_content.items():
        html_template = html_template.replace(f"{{{{ {key} }}}}", str(value))

    return html_template
