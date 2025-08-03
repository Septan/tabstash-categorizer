# 🧠 Tab Stash Markdown Auto-Categorizer

A Python script that takes a messy or timestamped Tab Stash Markdown export and automatically organizes all your saved links by category — no manual cleanup required.

---

## ✨ Features

- 📂 **Auto-categorizes** links by domain (e.g. YouTube → Media, GitHub → Tools)
- 🧹 **Ignores original headings** (e.g. `Saved 8/31/2023, 1:08:05 PM`)
- 📑 **Outputs clean Markdown** organized into emoji-labeled categories
- 🔢 **Alphabetically sorts** both:
  - Category groups
  - Links within each group
- 🚫 **Removes duplicate URLs**

---

## 📦 Output Example

```markdown
## ⚙️ Tools
- [Regex101](https://regex101.com)
- [py-autovod](https://github.com/0jc1/py-autovod)

## 🎥 Media & Streaming
- [YouTube](https://youtube.com)

## 🔞 Adult / Creator Platforms
- [OnlyFans](https://onlyfans.com)
```

---

## 🛠️ Installation

Clone this repo and make sure you have Python 3.7+ installed:

```bash
git clone https://github.com/yourusername/tabstash-categorizer.git
cd tabstash-categorizer
```

Install any required dependencies (just `argparse`, which is built-in):

```bash
python categorize_tabstash.py --help
```

---

## 🚀 Usage

```bash
python categorize_tabstash.py "input.md" "output.md"
```

- `input.md`: Your original exported Markdown file from Tab Stash
- `output.md`: Cleaned, categorized Markdown ready for re-import or viewing

---

## 🧠 Categories Covered

- 🎥 Media & Streaming
- ⚙️ Tools
- 📂 File Hosting / Galleries
- 📚 Learning
- 📌 Link Hubs / Bios
- 🛍️ Shopping
- 🎮 Streaming / Gaming
- 📱 Social Media
- 🔞 Adult / Creator Platforms
- ❓ Uncategorized

More domains are being added all the time. PRs welcome.

---

## 🤝 Contributing

Have more platforms you'd like to auto-categorize (e.g. niche forums or services)?  
Open a PR or submit a list — we’re happy to grow the coverage.

---

## 📄 License

MIT License
