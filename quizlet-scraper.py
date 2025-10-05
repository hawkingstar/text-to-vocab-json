from playwright.sync_api import sync_playwright
import json

def scrape_quizlet(url, output_file="quizlet_vocab.json"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        print(page.content()[:2000])


        # Grab the __NEXT_DATA__ script without waiting for visibility
        script = page.query_selector("script#__NEXT_DATA__").inner_text()
        data = json.loads(script)

        terms_data = data["props"]["pageProps"]["set"]["terms"]

        vocab = [
            {"latin": t["word"], "english": t["definition"], "audio": "https:totallyareallinktotheaudio"}
            for t in terms_data
        ]

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(vocab, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(vocab)} terms to {output_file}")
        browser.close()


if __name__ == "__main__":
    scrape_quizlet("https://quizlet.com/338142/stage-3-flash-cards/")
