from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

class IliaBeautyScraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    def fetch_page(self):
        """Loads the product page"""
        print("🔄 Loading product page...")
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        print("✅ Page loaded successfully.")

    def get_brand_name(self):
        """Extracts the brand name from multiple possible locations"""
        try:
            # Try extracting from meta tags
            brand_meta = self.driver.find_element(By.XPATH, "//meta[@property='og:site_name']")
            return brand_meta.get_attribute("content").strip()
        except:
            pass

        try:
            # Look for a brand section within the product page
            brand_element = self.driver.find_element(By.XPATH, "//span[contains(@class, 'brand')]")
            return brand_element.text.strip()
        except:
            pass

        return "ILIA Beauty"  # Default brand name if not found

    def get_product_name(self):
        """Extracts the product name"""
        try:
            return self.driver.find_element(By.TAG_NAME, "h1").text.strip()
        except:
            return "Product name not found."

    def get_price(self):
        """Extracts the price"""
        try:
            return self.driver.find_element(By.XPATH, "//span[@x-text='activeVariant.price_str']").text.strip()
        except:
            return "Price not found."

    def get_review_count(self):
        """Extracts the number of reviews"""
        try:
            return self.driver.find_element(By.CLASS_NAME, "oke-w-reviews-count").text.strip()
        except:
            return "Reviews count not found."

    def get_description(self):
        """Extracts the product description"""
        try:
            return self.driver.find_element(By.ID, "description_7ymy9L-accordion-panel").text.strip()
        except:
            return "Description not found."

    def scroll_to_reviews(self):
        """Scrolls to the reviews section"""
        try:
            reviews_section = self.driver.find_element(By.CLASS_NAME, "oke-reviewContent")
            self.driver.execute_script("arguments[0].scrollIntoView();", reviews_section)
            time.sleep(2)
            print("📜 Scrolled to reviews section.")
        except:
            print("⚠️ Could not scroll to reviews section.")

    def get_reviews(self):
        """Extracts reviews, including reviewer name and verified buyer status"""
        print("🔍 Fetching reviews...")
        reviews = []

        try:
            # Wait for reviews to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "oke-reviewContent"))
            )

            self.scroll_to_reviews()

            review_elements = self.driver.find_elements(By.CLASS_NAME, "oke-reviewContent")
            print(f"✅ Found {len(review_elements)} reviews.")

            for review in review_elements:
                try:
                    rating = review.find_element(By.CLASS_NAME, "oke-a11yText").text.split(" ")[1]  # Extract numeric rating
                except:
                    rating = "N/A"

                try:
                    title = review.find_element(By.CLASS_NAME, "oke-reviewContent-title").text.strip()
                except:
                    title = "No title"

                try:
                    body = review.find_element(By.CLASS_NAME, "oke-reviewContent-body").text.strip()
                except:
                    body = "No review body"

                try:
                    date = review.find_element(By.CLASS_NAME, "oke-reviewContent-date").text.strip()
                except:
                    date = "No date"

                try:
                    reviewer_name = review.find_element(By.CLASS_NAME, "oke-w-reviewer-name").text.strip()
                except:
                    reviewer_name = "Anonymous"

                try:
                    # Check if the 'verified' badge exists
                    verified_element = review.find_elements(By.CLASS_NAME, "oke-w-reviewer-verified")
                    verified = "Yes" if verified_element else "No"
                except:
                    verified = "No"

                reviews.append([reviewer_name, verified, rating, title, body, date])

            return reviews

        except Exception as e:
            print(f"❌ Error fetching reviews: {e}")
            return []

    def save_reviews(self, reviews):
        """Saves reviews to a CSV file"""
        if not reviews:
            print("⚠️ No reviews found. Skipping CSV save.")
            return
        
        try:
            with open("reviews.csv", "w", newline="", encoding="utf-8", errors="replace") as file:
                writer = csv.writer(file)
                writer.writerow(["Reviewer Name", "Verified Buyer", "Rating", "Review Title", "Review Body", "Date"])
                writer.writerows(reviews)
            print("✅ Reviews saved successfully to reviews.csv")
        except Exception as e:
            print(f"❌ Error saving reviews: {e}")

    def scrape(self):
        """Runs the full scraping process"""
        self.fetch_page()
        
        product_info = {
            "Brand Name": self.get_brand_name(),
            "Product Name": self.get_product_name(),
            "Price": self.get_price(),
            "Review Count": self.get_review_count(),
            "Description": self.get_description()
        }
        
        reviews = self.get_reviews()
        self.save_reviews(reviews)
        
        self.driver.quit()
        return product_info

# Run the scraper
if __name__ == "__main__":
    url = "https://iliabeauty.com/products/wanderlust"
    scraper = IliaBeautyScraper(url)
    product_data = scraper.scrape()
    
    print("\n✅ Reviews saved to reviews.csv")
    print("\n📌 Product Information:")
    for key, value in product_data.items():
        print(f"{key}: {value}")
