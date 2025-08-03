import argparse
import re
from urllib.parse import urlparse
from collections import defaultdict

# 🔎 Category definitions
CATEGORIES = {
    "🧭 Travel": ["tripadvisor", "expedia", "daytripper", "airbnb", "booking", "kayak", "trivago", "google.com/maps"],
    "🎥 Media & Streaming": ["youtube", "netflix", "hulu", "reelgood", "plex", "primevideo", "real-debrid", "hbomax", "disneyplus", "crunchyroll"],
    "🛍️ Shopping": ["etsy", "amazon", "ebay", "bestbuy", "newegg", "aliexpress", "walmart", "target", "shein", "temu"],
    "📚 Learning": ["wikipedia", "coursera", "edx", "khanacademy", "udemy", "skillshare", "brilliant"],
    "⚙️ Tools": ["github", "gitlab", "replit", "jsfiddle", "codepen", "chat.openai.com", "regex101", "cloudflare"],
    "📌 Link Hubs / Bios": ["linktr.ee", "campsite.bio", "beacons.ai", "bio.site", "solo.to", "linkin.bio"],
    "📂 File Hosting / Galleries": ["bunkr", "pixeldrain", "anonfiles", "gofile", "wetransfer", "mediafire", "mega", "zippyshare", "dropbox", "drive.google"],
    "🎮 Streaming / Gaming": ["twitch", "kick", "dlive", "steam", "roblox", "epicgames", "speedrun.com"],
    "📱 Social Media": ["facebook", "instagram", "twitter", "x.com", "tiktok", "threads", "reddit", "tumblr", "snapchat"],
    "🎨 Art / Creative": ["deviantart", "artstation", "behance", "dribbble", "pixiv", "canva", "figma"],
    "🔞 Adult / Creator Platforms": [
        "onlyfans", "fansly", "manyvids", "justfor.fans", "fancentro", "nsfw",
        "stripchat", "chaturbate", "camsoda", "bongacams", "livejasmin", "myfreecams",
        "xlovecam", "camwhores", "cam4", "camversity", "flirt4free", "amateur.tv",
        "spankbang", "mym.fans", "loyalfans", "fanvue"
    ],
    "❓ Uncategorized": []
}

def categorize_url(url):
    domain = urlparse(url).netloc.lower()
    for category, keywords in CATEGORIES.items():
        if any(kw in domain for kw in keywords):
            return category
    return "❓ Uncategorized"

def extract_links_from_markdown(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    links = []
    for line in lines:
        line = line.strip()
        match = re.match(r"- \[(.*?)\]\((.*?)\)", line)
        if match:
            title, url = match.groups()
            links.append({"title": title.strip(), "url": url.strip()})
    return links

def deduplicate_links(links):
    seen = set()
    unique = []
    for link in links:
        if link['url'] not in seen:
            seen.add(link['url'])
            unique.append(link)
    return unique

def group_links_by_category(links):
    grouped = defaultdict(list)
    for link in links:
        category = categorize_url(link['url'])
        grouped[category].append(link)
    return grouped

def strip_leading_symbols(title):
    return re.sub(r"^[^a-zA-Z0-9]+", "", title).strip().lower()

def save_to_markdown(grouped, output_path):
    # Sort groups by cleaned title (ignoring emojis)
    sorted_group_names = sorted(grouped.keys(), key=strip_leading_symbols)
    sorted_grouped = {
        group: sorted(grouped[group], key=lambda l: l['title'].lower())
        for group in sorted_group_names
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        for group in sorted_group_names:
            f.write(f"## {group}\n")
            for link in sorted_grouped[group]:
                f.write(f"- [{link['title']}]({link['url']})\n")

def main():
    parser = argparse.ArgumentParser(description="Convert and categorize Tab Stash Markdown")
    parser.add_argument("input", help="Path to input Markdown file")
    parser.add_argument("output", help="Path to output Markdown file")
    args = parser.parse_args()

    raw_links = extract_links_from_markdown(args.input)
    unique_links = deduplicate_links(raw_links)
    grouped_links = group_links_by_category(unique_links)
    save_to_markdown(grouped_links, args.output)

    print("\n=== ✅ Markdown Categorizer Report ===")
    print(f"🔍 Total links found:       {len(raw_links)}")
    print(f"🚫 Duplicates removed:      {len(raw_links) - len(unique_links)}")
    print(f"✅ Unique links kept:       {len(unique_links)}")
    print(f"📦 Categories created:      {len(grouped_links)}")
    print(f"📁 Output saved to:         {args.output}")
    print("================================================\n")

if __name__ == "__main__":
    main()