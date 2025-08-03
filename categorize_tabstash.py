import argparse
import re
from urllib.parse import urlparse
from collections import defaultdict

# 🔎 Category definitions
CATEGORIES = {
    "💬 AI & Chatbots": [
        "chatgpt.com", "openai.com", "chat.openai.com", "poe.com", "perplexity.ai",
        "you.com", "huggingface.co"
    ],
    "📧 Email & Mail Providers": [
        "gmail.com", "mail.google.com", "outlook.com", "outlook.live.com", "hotmail.com",
        "yahoo.com", "mail.yahoo.com", "proton.me", "protonmail.com", "zoho.com", "gmx.com",
        "aol.com", "icloud.com", "mail.com", "yandex.com", "tutanota.com", "fastmail.com"
    ],
    "🔎 Search Engines": [
        "google.com", "bing.com", "duckduckgo.com", "yahoo.com", "search.yahoo.com",
        "startpage.com", "ecosia.org", "qwant.com", "brave.com", "you.com", "mojeek.com"
    ],
    "🗂️ Cloud Storage & Sync": [
        "drive.google.com", "dropbox.com", "onedrive.live.com", "mega.nz", "box.com",
        "icloud.com", "sync.com", "pcloud.com", "nextcloud.com"
    ],
    "📅 Calendar & Scheduling": [
        "calendar.google.com", "calendly.com", "icloud.com", "outlook.live.com"
    ],
    "🧠 Knowledge & Wiki": [
        "wikipedia.org", "wiktionary.org", "wikidata.org", "evernote.com", "notion.so",
        "slite.com", "obsidian.md", "roamresearch.com", "zettlr.com", "tiddlywiki.com"
    ],
    "🎓 Education & Learning": [
        "khanacademy.org", "coursera.org", "edx.org", "udemy.com", "brilliant.org",
        "academia.edu", "researchgate.net", "open.edu", "alison.com", "futurelearn.com",
        "skillshare.com"
    ],
    "🧭 Travel": [
        "tripadvisor", "expedia", "daytripper", "airbnb", "booking",
        "kayak", "trivago", "maps.google.com"
    ],
    "🎥 Media & Streaming": [
        "youtube", "netflix", "hulu", "reelgood", "plex.tv", "primevideo.com",
        "hbomax.com", "disneyplus.com", "crunchyroll.com"
    ],
    "🎞️ Streaming Tools / Indexers": [
        "real-debrid.com", "nzbgeek.info", "nzbfinder.ws", "drunkenslug.com", "dognzb.cr",
        "omgwtfnzbs.me", "nzbplanet.net", "nzb.su", "usenet-crawler.com",
        "sabnzbd.org", "nzbhydra2.org", "sonarr.tv", "radarr.video", "tautulli.com"
    ],
    "🧲 Torrents / Trackers": [
        "1337x.to", "thepiratebay.org", "rarbg.to", "nyaa.si", "fitgirl-repacks.site",
        "yts.mx", "torrentgalaxy.to", "torlock.com", "zooqle.com", "limetorrents.lol",
        "kickasstorrents.to", "skytorrents.lol"
    ],
    "🛍️ Shopping": [
        "etsy.com", "amazon.com", "ebay.com", "bestbuy.com", "newegg.com",
        "aliexpress.com", "walmart.com", "target.com", "shein.com", "temu.com"
    ],
    "⚙️ Tools": [
        "github.com", "gitlab.com", "replit.com", "jsfiddle.net", "codepen.io",
        "regex101.com", "cloudflare.com"
    ],
    "📌 Link Hubs / Bios": [
        "linktr.ee", "campsite.bio", "beacons.ai", "bio.site", "solo.to", "linkin.bio"
    ],
    "📂 File Hosting / Galleries": [
        "bunkr.is", "pixeldrain.com", "anonfiles.com", "gofile.io",
        "wetransfer.com", "mediafire.com"
    ],
    "🎮 Streaming / Gaming": [
        "twitch.tv", "kick.com", "dlive.tv", "steamcommunity.com", "roblox.com",
        "epicgames.com", "speedrun.com"
    ],
    "📱 Social Media": [
        "facebook.com", "instagram.com", "twitter.com", "x.com", "tiktok.com",
        "threads.net", "reddit.com", "tumblr.com", "snapchat.com"
    ],
    "🎨 Art / Creative": [
        "deviantart.com", "artstation.com", "behance.net", "dribbble.com",
        "pixiv.net", "canva.com", "figma.com"
    ],
    "🔞 Adult / Creator Platforms": [
        "onlyfans.com", "fansly.com", "manyvids.com", "justfor.fans", "fancentro.com", "nsfw",
        "stripchat.com", "chaturbate.com", "camsoda.com", "bongacams.com", "livejasmin.com", "myfreecams.com",
        "xlovecam.com", "camwhores.tv", "cam4.com", "camversity.com", "flirt4free.com", "amateur.tv",
        "spankbang.com", "mym.fans", "loyalfans.com", "fanvue.com"
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
