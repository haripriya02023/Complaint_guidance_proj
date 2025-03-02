import kivy
kivy.require("2.0.0")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
import webbrowser

# Complaint Data (DO NOT CHANGE)
complaint_data = {
    "Women & Child Rights": {
        "Child Labour": {"portals": ["https://pencil.gov.in", "https://nhrc.nic.in"], "helplines": ["1098", "1800-11-5533"], "image": "images/child_labour.webp"},
        "Women Harassment": {"portals": ["https://ncw.nic.in"], "helplines": ["1091"], "image": "images/women_harassment.webp"},
        "Child Marriage": {"portals": ["https://childlineindia.org"], "helplines": ["1098"], "image": "images/child_marriage.webp"},
        "Female Foeticide": {"portals": ["https://ncpcr.gov.in"], "helplines": ["1098"], "image": "images/female_foeticide.webp"},
        "Sexual Harassment at Workplace": {"portals": ["https://shebox.nic.in"], "helplines": ["181"], "image": "images/sexual_harassment_workplace.webp"}
    },
    "Senior Citizen Rights": {
        "Elder Abuse": {"portals": ["https://socialjustice.nic.in"], "helplines": ["14567"], "image": "images/elder_abuse.webp"},
        "Pension Issues": {"portals": ["https://pensionersportal.gov.in"], "helplines": ["1800-180-5325"], "image": "images/pension_issues.webp"}
    },
    "Environmental Issues": {
        "Pollution Complaint": {"portals": ["https://cpcb.nic.in"], "helplines": ["1800-11-0601"], "image": "images/pollution_complaint.webp"},
        "Deforestation": {"portals": ["https://moef.gov.in"], "helplines": ["+91-11-24695235"], "image": "images/deforestation.webp"}
    },
    "Public Safety & Traffic Violations": {
        "Traffic Violations": {"portals": ["https://trafficpolice.nic.in"], "helplines": ["100"], "image": "images/traffic_violations.webp"},
        "Hit & Run Cases": {"portals": ["https://morth.nic.in"], "helplines": ["1073"], "image": "images/hit_and_run.webp"}
    },
    "Corruption & Government Services": {
        "Bribery & Corruption": {"portals": ["https://cvc.gov.in"], "helplines": ["1800-11-0180"], "image": "images/bribery.webp"},
        "Delayed Services": {"portals": ["https://pgportal.gov.in"], "helplines": ["1800-11-0031"], "image": "images/delayed_services.webp"}
    },
    "Consumer Rights": {
        "Consumer Fraud": {"portals": ["https://consumerhelpline.gov.in"], "helplines": ["1800-11-4000"], "image": "images/consumer_fraud.webp"},
        "Fake Products": {"portals": ["https://consumerhelpline.gov.in"], "helplines": ["14404"], "image": "images/fake_product.webp"}
    },
    "Human Rights Violations": {
        "Human Trafficking": {"portals": ["https://nhrc.nic.in"], "helplines": ["112"], "image": "images/human_trafficking.webp"},
        "Bonded Labour": {"portals": ["https://labour.gov.in"], "helplines": ["1800-11-0039"], "image": "images/bonded_labour.webp"}
    },
    "Cyber Crimes": {
        "Online Fraud": {"portals": ["https://cybercrime.gov.in"], "helplines": ["155260"], "image": "images/online_fraud.webp"},
        "Social Media Harassment": {"portals": ["https://cybercrime.gov.in"], "helplines": ["1930"], "image": "images/socialmedia_harassment.webp"}
    },
    "Education & Student Rights": {
        "Ragging Complaint": {"portals": ["https://antiragging.in"], "helplines": ["1800-180-5522"], "image": "images/ragging.webp"},
        "Scholarship Issues": {"portals": ["https://scholarships.gov.in"], "helplines": ["0120-6619540"], "image": "images/scholarship_issues.webp"}
    },
    "Discrimination": {
        "Caste Discrimination": {"portals": ["https://nhrc.nic.in", "https://socialjustice.gov.in"], "helplines": ["1800-11-8888"], "image": "images/caste_discrimination.webp"},
        "Regional Discrimination": {"portals": ["https://nhrc.nic.in", "https://mib.gov.in"], "helplines": ["1800-11-9222"], "image": "images/regional_discrimination.webp"},
        "LGBTQ+ Discrimination": {"portals": ["https://transgender.dosje.gov.in", "https://nhrc.nic.in"], "helplines": ["181", "112"], "image": "images/lgbtq+_discrimination.webp"}
    }
}


# Home Screen
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        layout.add_widget(Label(text="Complaint Categories", font_size=24))
        
        # Create buttons for each category
        for category in complaint_data.keys():
            btn = Button(text=category, size_hint_y=None, height=50, background_color=(0.4, 0.7, 1, 1))
            btn.bind(on_release=self.go_to_category)
            layout.add_widget(btn)
        
        self.add_widget(layout)

    def go_to_category(self, instance):
        self.manager.current = "category"
        self.manager.get_screen("category").load_subcategories(instance.text)

# Category Screen
class CategoryScreen(Screen):
    def load_subcategories(self, category):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        layout.add_widget(Label(text=f"{category} Issues", font_size=22))
        
        for subcategory in complaint_data[category].keys():
            btn = Button(text=subcategory, size_hint_y=None, height=50, background_color=(1, 0.5, 0.5, 1))
            btn.bind(on_release=lambda btn, sub=subcategory: self.go_to_details(sub))
            layout.add_widget(btn)

        back_btn = Button(text="Back", size_hint_y=None, height=50, background_color=(0.5, 0.5, 0.5, 1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'home'))

        layout.add_widget(back_btn)

        self.add_widget(layout)

    def go_to_details(self, subcategory):
        self.manager.current = "details"
        self.manager.get_screen("details").update_details(subcategory)

# Details Screen
class DetailsScreen(Screen):
    def update_details(self, subcategory):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Get the subcategory details
        data = next((complaint_data[c][subcategory] for c in complaint_data if subcategory in complaint_data[c]), None)

        if data:
            # Display Image
            if "image" in data and data["image"]:
                img = Image(source=data["image"], size_hint=(1, 0.5))
                layout.add_widget(img)
            
            # Complaint Portals
            for portal in data["portals"]:
                btn = Button(text=portal, size_hint_y=None, height=40, background_color=(0.9, 0.8, 0.98, 1))
                btn.bind(on_release=lambda btn, url=portal: webbrowser.open(url))
                layout.add_widget(btn)

            # Helpline Numbers
            for helpline in data["helplines"]:
                layout.add_widget(Label(text=f"Helpline: {helpline}", size_hint_y=None, height=30))

        # Back Button
        back_btn = Button(text="Back", size_hint_y=None, height=40, background_color=(0.5, 0.5, 0.5, 1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'category'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

# Screen Manager
class ComplaintApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(CategoryScreen(name="category"))
        sm.add_widget(DetailsScreen(name="details"))
        return sm

# Run the App
if __name__ == "__main__":
    ComplaintApp().run()
