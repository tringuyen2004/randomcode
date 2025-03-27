from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def parse_number(number_str):
    """Converts formatted numbers (e.g., '358,813') to integers safely."""
    try:
        return int(number_str.replace(',', ''))
    except ValueError:
        return 0  # Return 0 if parsing fails

def get_active_users(mode, pages=5):
    """Scrapes active user count for a given game mode from osu! rankings."""

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    total_players = 0

    try:
        for page in range(1, pages + 1):
            url = f"https://osu.ppy.sh/rankings/{mode}/country?page={page}"
            driver.get(url)

            # Wait until the table is present (max 10s timeout)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody tr'))
                )
            except Exception as e:
                print(f"Timeout or error loading page {page}: {e}")
                continue  # Skip to next page

            print(f"\n--- Page {page} ---")
            rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')

            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if len(cells) >= 3:
                    rank = cells[0].text.strip()
                    country = cells[1].text.strip()
                    active_users_str = cells[2].text.strip()
                    active_users = parse_number(active_users_str)
                    total_players += active_users
                    print(f"{rank} | {country} | {active_users_str}")

    finally:
        driver.quit()  # Ensure the browser is closed

    return total_players

if __name__ == "__main__":
    while True:
        mode = input("Enter mode (osu, taiko, fruits, mania): ").strip().lower()
    
        if mode not in ["osu", "taiko", "fruits", "mania"]:
            print("Invalid mode! Please enter one of: osu, taiko, fruits, mania")
        else:
            total_players = get_active_users(mode)
            print("\n===============================")
            print(f"Total Active Users: {total_players:,}")
            print("===============================")
