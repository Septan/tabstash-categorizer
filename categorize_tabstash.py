import argparse
import re
from urllib.parse import urlparse
from collections import defaultdict

# 🔎 Category definitions
CATEGORIES = {
    '💬 AI & Chatbots': [
        'chatgpt.com', 'huggingface.co', 'openai.com', 'openwebui.com',
        'perplexity.ai', 'poe.com', 'whiskit.ai', 'you.com',
    ],
    '📧 Email & Mail Providers': [
        'aol.com', 'fastmail.com', 'gmail.com', 'gmx.com',
        'hotmail.com', 'icloud.com', 'mail.com', 'outlook.com',
        'proton.me', 'protonmail.com', 'tutanota.com', 'yahoo.com',
        'yandex.com', 'zoho.com',
    ],
    '🔎 Search Engines': [
        'bing.com', 'brave.com', 'duckduckgo.com', 'ecosia.org',
        'google.com', 'mojeek.com', 'qwant.com', 'startpage.com',
    ],
    '🗂️ Cloud Storage & Sync': [
        'backblaze.com', 'box.com', 'dropbox.com', 'ente.io',
        'filen.io', 'goodsync.com', 'internxt.com', 'mega.io',
        'mega.nz', 'myairbridge.com', 'nextcloud.com', 'pcloud.com',
        'sync.com',
    ],
    '📅 Calendar & Scheduling': [
        'calendly.com',
    ],
    '🧠 Knowledge & Wiki': [
        'archive.org', 'blockstack.org', 'bookmarkninja.com', 'evernote.com',
        'notion.so', 'obsidian.md', 'raindrop.io', 'roamresearch.com',
        'slite.com', 'tiddlywiki.com', 'wikidata.org', 'wikipedia.org',
        'wiktionary.org', 'zettlr.com',
    ],
    '🎓 Education & Learning': [
        'abcmouse.com', 'academia.edu', 'alison.com', 'brilliant.org',
        'coursera.org', 'edx.org', 'futurelearn.com', 'khanacademy.org',
        'networkchuck.com', 'open.edu', 'oxforddictionaries.com', 'researchgate.net',
        'skillshare.com', 'teachable.com', 'thebiblestudies.fun', 'thinkthroughmath.com',
        'udemy.com',
    ],
    '🧭 Travel': [
        'airbnb.com', 'booking.com', 'daytripper.com', 'expedia.com',
        'kayak.com', 'tripadvisor.com', 'trivago.com',
    ],
    '🎥 Media & Streaming': [
        'amcplus.com', 'bfi.org.uk', 'braflix.so', 'broadwaypixels.com',
        'cinefilhd.org', 'cinemaz.to', 'cineverse.com', 'cmt.com',
        'criticker.com', 'crunchyroll.com', 'cultpix.com', 'discoveryplus.com',
        'disneyplus.com', 'dxdhd.com', 'emby.media', 'episode-alert.com',
        'fandango.com', 'fubo.tv', 'fullmoondirect.com', 'fullmoonfeatures.com',
        'hbomax.com', 'hulu.com', 'kinox.to', 'letterboxd.com',
        'max.com', 'mediux.pro', 'movielens.org', 'movieparadise.org',
        'netflix.com', 'nobodyhome.tv', 'onlinedigitaldownloads.com', 'opendub.org',
        'opensubtitles.com', 'opensubtitles.org', 'paramountplus.com', 'peacocktv.com',
        'playon.tv', 'plex.tv', 'plexguide.com', 'pluto.tv',
        'primevideo.com', 'psa.pm', 'psarips.eu', 'psarips.in',
        'reelgood.com', 'retrocrush.tv', 'retroflix.club', 'roku.com',
        'rottentomatoes.com', 'samsungtvplus.com', 'scener.com', 'setvnow.com',
        'shout-tv.com', 'shudder.com', 'sling.com', 'stremio.com',
        'tastedive.com', 'themoviedb.org', 'theposterdb.com', 'thetvdb.com',
        'trakt.tv', 'tubitv.com', 'tvtime.com', 'vidguard.to',
        'vimeo.com', 'vudu.com', 'watchertv.com', 'youtube.com',
    ],
    '🎞️ Streaming Tools / Indexers': [
        'alldebrid.com', 'cocoleech.com', 'debrid-file.com', 'debrid-link.com',
        'debrid-link.fr', 'dognzb.cr', 'drunkenslug.com', 'fastusenet.org',
        'leechpremium.link', 'linkifier.com', 'newjds.com', 'newsgroup.ninja',
        'newshosting.com', 'notifiarr.com', 'nzb.cat', 'nzb.su',
        'nzbfinder.ws', 'nzbforyou.com', 'nzbgeek.info', 'nzbgrabit.org',
        'nzbgrabit.xyz', 'nzbhydra2.org', 'nzbndx.com', 'nzbnoob.com',
        'nzbplanet.net', 'nzbstars.com', 'omgwtfnzbs.me', 'orionoid.com',
        'prem.link', 'premiumgrab.com', 'premiumize.me', 'proleech.link',
        'radarr.video', 'real-debrid.com', 'sabnzbd.org', 'seedit4.me',
        'sonarr.tv', 'tautulli.com', 'torbox.app', 'uploadedpremiumlink.net',
        'usenet-crawler.com', 'vnz-leech.com',
    ],
    '🧲 Torrents / Trackers': [
        '1337x.to', '3dtorrents.org', 'abnzb.com', 'aither.cc',
        'alpharatio.cc', 'animebytes.tv', 'animetorrents.me', 'animetosho.org',
        'ansktracker.net', 'arenabg.com', 'asiancinema.me', 'asiandvdclub.org',
        'audiobookbay.is', 'audiobookbay.nl', 'back-ups.me', 'bakabt.me',
        'bird-hd.info', 'blutopia.xyz', 'btschool.net', 'cgpeers.com',
        'cgpeers.to', 'cheggit.me', 'chilebt.com', 'dascene.net',
        'datascene.net', 'datascene.xyz', 'demonoid.is', 'devil-torrents.pl',
        'dimeadozen.org', 'dnoid.pw', 'filelist.io', 'fitgirl-repacks.site',
        'gingadaddy.com', 'hd-bits.com', 'hd-space.org', 'hd4free.xyz',
        'hdcenter.net', 'hdme.eu', 'homeporntorrents.club', 'iptorrents.com',
        'iptorrents.me', 'israbox.pro', 'kickasstorrents.to', 'layer13.net',
        'limetorrents.lol', 'mdan.org', 'mousebits.com', 'myanonamouse.net',
        'nbtorrents.com', 'nethd.org', 'ninjacentral.co.za', 'nyaa.si',
        'orpheus.network', 'pussytorrents.org', 'qxr.pw', 'rarbg.to',
        'revolutiontt.me', 'revott.me', 'rutracker.org', 'sceneaccess.eu',
        'scenenzbs.com', 'scenepalace.info', 'skytorrents.lol', 'thepiratebay.org',
        'torlock.com', 'torrentday.com', 'torrentday.it', 'torrentdb.net',
        'torrentgalaxy.to', 'torrenting.com', 'torrenting.me', 'torrentleech.me',
        'torrentleech.org', 'torrentshack.me', 'torrentsurf.net', 'torrminatorr.com',
        'worldofp2p.net', 'wtfnzb.pw', 'wtftrackr.xyz', 'x265.club',
        'xtorrenty.org', 'xtremebytes.net', 'xtremewrestlingtorrents.net', 'yts.mx',
        'zooqle.com',
    ],
    '🛍️ Shopping': [
        'adobe.com', 'aliexpress.com', 'amazon.com', 'apple.com',
        'asetek.com', 'bestbuy.com', 'blueapron.com', 'camel.com',
        'cheapjoes.com', 'cricketwireless.com', 'cvs.com', 'dbrand.com',
        'dollargeneral.com', 'dollarshaveclub.com', 'ebay.com', 'etsy.com',
        'evga.com', 'gamersupps.gg', 'gearbest.com', 'gearbest.ma',
        'heb.com', 'jadebloom.com', 'lootcrate.com', 'mall-simulator.tools',
        'mtailor.com', 'mycommerce.com', 'newegg.com', 'onkyo4k.com',
        'petco.com', 'planttherapy.com', 'pureformulas.com', 'razer.com',
        'samsclub.com', 'shein.com', 'squaretrade.com', 'staples.com',
        'steelseries.com', 'target.com', 'temu.com', 'vitacost.com',
        'walmart.com', 'xiaomi.com',
    ],
    '⚙️ Tools': [
        'able.style', 'adalo.com', 'ashampoo.com', 'atlassian.net',
        'autocode.com', 'bitdefender.com', 'bitsum.com', 'cloudinary.com',
        'codepen.io', 'comodo.com', 'corel.com', 'deepl.com',
        'docker.com', 'dvdfab.cn', 'getoutfox.com', 'github.com',
        'gitlab.com', 'heroku.com', 'ifttt.com', 'integromat.com',
        'intelx.io', 'iosgods.com', 'jdownloader.org', 'jsfiddle.net',
        'macrium.com', 'malwarebytes.com', 'mcebuddy2x.com', 'pcpartpicker.com',
        'picbackman.com', 'poikosoft.com', 'regex101.com', 'replit.com',
        'speechify.com', 'stardock.com', 'symless.com', 'topazlabs.com',
        'tria.ge', 'uptimerobot.com', 'userbenchmark.com', 'videos.com',
        'vidiq.com', 'xmarks.com',
    ],
    '📌 Link Hubs / Bios': [
        'beacons.ai', 'bio.site', 'campsite.bio', 'linkin.bio',
        'linktr.ee', 'odesli.co', 'solo.to',
    ],
    '📂 File Hosting / Galleries': [
        'abyss.to', 'anonfiles.com', 'bunkr.cr', 'bunkr.is',
        'bunkr.la', 'bunkrr.su', 'byse.sx', 'catbox.moe',
        'cyberdrop.cr', 'cyberdrop.me', 'cyberfile.me', 'doodrive.com',
        'doodstream.com', 'filedropper.com', 'filefactory.com', 'filegarden.com',
        'filemoon.sx', 'filemoon.to', 'filepost.io', 'freeimage.host',
        'fromsmash.com', 'gofile.io', 'imagebam.com', 'imgbash.com',
        'imgbox.com', 'imgur.com', 'krakenfiles.com', 'kwik.cx',
        'letsupload.io', 'letsupload.org', 'mediafire.com', 'mirrorace.com',
        'mirrorace.org', 'mirrored.to', 'mp4upload.com', 'multifilemirror.com',
        'multiup.io', 'multiup.org', 'photobucket.com', 'pixeldrain.com',
        'postimages.org', 'rapidgator.net', 'rarefile.net', 'rips.cc',
        'sltube.org', 'streamtape.to', 'turboimagehost.com', 'upfile.online',
        'uploadboy.com', 'upvid.co', 'userscloud.com', 'veev.to',
        'void.to', 'vudeo.co', 'wetransfer.com', 'yourupload.com',
        'zippyshare.cloud',
    ],
    '🎮 Streaming / Gaming': [
        'arcgames.com', 'astats.nl', 'backloggery.com', 'battle.net',
        'bethesda.net', 'blankos.com', 'caffeine.tv', 'callofduty.com',
        'callofwar.com', 'cdkeys.com', 'chrono.gg', 'dailyindiegame.com',
        'division2map.com', 'dlive.tv', 'dovetailgames.com', 'emuparadise.me',
        'epicgames.com', 'escapefromtarkov.com', 'fanatical.com', 'fortnite.gg',
        'fruitlab.com', 'g2a.com', 'gaijin.net', 'game-debate.com',
        'gamebillet.com', 'gameloft.com', 'gamersgate.com', 'gamesessions.com',
        'gamevox.com', 'garena.sg', 'gog.com', 'greenmangaming.com',
        'grouvee.com', 'hellhades.com', 'horsereality.com', 'howlongtobeat.com',
        'hoyolab.com', 'hoyoverse.com', 'humblebundle.com', 'ign.com',
        'itch.io', 'kick.com', 'kinguin.net', 'legacygames.com',
        'mmobomb.com', 'mythical.games', 'neopets.com', 'nexusmods.com',
        'nitrotype.com', 'nvidia.com', 'origin.com', 'palia.com',
        'pgsharp.com', 'plarium.com', 'playatlas.com', 'playscrabble.com',
        'playspellbreak.com', 'playstation.com', 'playvalorant.com', 'pogo.com',
        'pokemon.com', 'relic.com', 'rf4game.com', 'riotgames.com',
        'roblox.com', 'rockstargames.com', 'scrabulizer.com', 'sliver.tv',
        'sonyentertainmentnetwork.com', 'speedrun.com', 'spigotmc.org', 'square-enix.com',
        'steamcommunity.com', 'stream-recorder.com', 'streamray.com', 'thegamerlobby.com',
        'thesimsresource.com', 'thetrackernetwork.com', 'trovo.live', 'truckersmp.com',
        'trucksbook.eu', 'twitch.tv', 'ubisoft.com', 'utomik.com',
        'voidu.com', 'warframe.com', 'wbgames.com', 'wizards.com',
        'wolfire.com', 'yuplay.com',
    ],
    '📱 Social Media': [
        'discord.com', 'discordapp.com', 'facebook.com', 'forumotion.com',
        'groups.io', 'imvu.com', 'instagram.com', 'line.me',
        'loforo.com', 'minds.com', 'myspace.com', 'pinterest.com',
        'pixelfed.social', 'proboards.com', 'reddit.com', 'skype.com',
        'snapchat.com', 'snoopreport.com', 'socialmediagirls.com', 'starngage.com',
        'threads.net', 'tiktok.com', 'trillian.im', 'tumblr.com',
        'twitter.com', 'x.com',
    ],
    '🎨 Art / Creative': [
        'artstation.com', 'behance.net', 'canva.com', 'coloringbliss.com',
        'coverlabs.io', 'deviantart.com', 'dreamstime.com', 'dribbble.com',
        'dungeonfog.com', 'eyeem.com', 'fanart.tv', 'fantart.tv',
        'figma.com', 'gumroad.com', 'picsart.com', 'pixiv.net',
    ],
    '🔞 Adult / Creator Platforms': [
        'adult-cinema-network.net', 'amateur.tv', 'amateuralbum.net', 'archivebate.com',
        'bdsmlr.com', 'bongacams.com', 'bootytape.com', 'cam4.com',
        'cambro.tv', 'camclips.cc', 'camhub.cc', 'camsavexx.com',
        'camsoda.com', 'camvault.xyz', 'camversity.com', 'camwhores.tv',
        'camwhores.video', 'camwhoreshd.com', 'candfans.jp', 'chaturbate.com',
        'chaturbetter.com', 'chaturfier.com', 'cherrykiss.org', 'cloudbate.com',
        'colombialady.com', 'coomer.party', 'coomer.su', 'fancentro.com',
        'fansly.com', 'fanvue.com', 'fapello.com', 'flirt4free.com',
        'gelbooru.com', 'haijiao.com', 'highwebmedia.com', 'hqcollect.net',
        'instabang.com', 'justfor.fans', 'leaker.me', 'leaker.tv',
        'livecamrips.com', 'livejasmin.com', 'loveagain.com', 'loyalfans.com',
        'lpsg.com', 'manyvids.com', 'myfreecams.com', 'mym.fans',
        'nudography.com', 'onlyfans.com', 'onlysimps.lol', 'pimpandhost.com',
        'recu.me', 'recurbate.com', 'sexy-egirls.com', 'sexyforums.com',
        'simpcity.cr', 'simpcity.su', 'sleazemovies.com', 'sorrymother.video',
        'spankbang.com', 'streamate.com', 'stripchat.com', 'sweetsext.com',
        'theoriginalcandid.com', 'truecandid.com', 'xlovecam.com',
    ],
    '💳 Finance & Payments': [
        'affirm.com', 'airtm.com', 'bitrefill.com', 'capitalone.com',
        'coinbase.com', 'exchangerate-api.com', 'globalcashcard.com', 'id.me',
        'oobit.com', 'paxful.com', 'paypal.com', 'privacy.com',
        'remitly.com', 'venmo.com', 'westernunion.com', 'wise.com',
        'worldremit.com', 'xe.com',
    ],
    '🔐 Security & Privacy': [
        'abine.com', 'airvpn.org', 'firefox.com', 'goldenfrog.com',
        'ipvanish.com', 'kroll.com', 'krollmonitoring.com', 'lastpass.com',
        'privateinternetaccess.com', 'privatevpn.com', 'simplelogin.io', 'spamguardapp.com',
        'vyprvpn.com',
    ],
    '🖥️ Hosting / Domains / Self-Hosting': [
        'airspy.us', 'bytesized-hosting.com', 'cloudflare.com', 'cybrancee.com',
        'heracle.net', 'herokuapp.com', 'hoshi.cfd', 'lifx.com',
        'mariushosting.com', 'namecheap.com', 'openweathermap.org', 'parsec.app',
        'pogdigital.com', 'porkbun.com', 'rapidseedbox.com', 'seedbox.io',
        'shoutcast.com', 'synology.com', 'synology.me', 'tal0ne.co.uk',
        'teamviewer.com', 'ubi.com', 'ui.com', 'vpshostingservice.co',
        'vultr.com', 'xirvik.com', 'zap-hosting.com',
    ],
    '❤️ Health & Fitness': [
        'athenahealth.com', 'dentalsleepsolutions.com', 'eclinicalweb.com', 'entrykeyid.com',
        'firstopinionapp.com', 'garmin.com', 'ifit.com', 'lincare.com',
        'lincareportal.com', 'mapmywalk.com', 'myfitnesspal.com', 'myhealthone.com',
        'mystrength.com', 'resmed.com', 'superiorhealthplan.com',
    ],
    '🎵 Music & Audio': [
        '8tracks.com', 'audials.com', 'broadcastify.com', 'cdbaby.com',
        'chartmetric.com', 'chartmetric.io', 'cliggo.com', 'deezer.com',
        'discogs.com', 'ear-play.com', 'earplay.com', 'fullmixmusic.org',
        'ibroadcast.com', 'jamendo.com', 'last.fm', 'losslessmusics.org',
        'metabrainz.org', 'musebootlegs.com', 'musicbrainz.org', 'musicroamer.com',
        'napster.com', 'nationalradiodata.com', 'qobuz.com', 'radioreference.com',
        'siriusxm.com', 'songswave.com', 'soundsnap.com', 'symfonium.app',
        'tidal.com', 'universalproductionmusic.com', 'yetanothermusicserver.top',
    ],
    '📖 Books / Anime / Reading': [
        'androidmovie.ru', 'anidb.net', 'anidl.org', 'anilist.co',
        'animea.net', 'animeftw.tv', 'animegrimoire.moe', 'animekaizoku.com',
        'animekayo.com', 'animelliure.net', 'animeout.xyz', 'animeultima.eu',
        'animez.to', 'hi10anime.com', 'kametsu.com', 'kawaii.su',
        'krdl.moe', 'myanimelist.net', 'papercraftermagazine.co.uk', 'place4books.uk',
        'wizardingworld.com',
    ],
    '📰 News / Reviews / Reference': [
        'bhg.com', 'consumerreports.org', 'foxnews.com', 'funtrivia.com',
        'melissa.com', 'mvgroup.org', 'recordsfinder.com', 'spokeo.com',
        'streetrx.com', 'thekrazycouponlady.com', 'whitepages.com',
    ],
    '💰 Deals / Rewards / Surveys': [
        '2captcha.com', 'azcaptcha.com', 'bidbag.us', 'bidslammer.com',
        'clickworker.com', 'coupons.com', 'esnipe.com', 'gg2u.org',
        'gixen.com', 'goofbid.com', 'grab8.com', 'groupees.com',
        'hideout.co', 'ibotta.com', 'loots.com', 'nielsen.com',
        'selly.gg', 'sharewareonsale.com', 'streetpricer.com', 'swagbucks.com',
        'timebucks.com', 'usedprice.com',
    ],
    '🗨️ Communities & Forums': [
        'ablackweb.com', 'cracked.io', 'dirtywarez.com', 'geek-hub.com.au',
        'gfxnews.org', 'leakedbb.com', 'lolz.live', 'mobilism.org',
        'nulled.to', 'nulledbb.com', 'piracy.su', 'piracy.vip',
        'raidforums.com', 'rin.ru', 'sharebb.me', 'sharemania.us',
        'snahp.eu', 'snahp.it', 'srrdb.com', 'teamos-hkrg.com',
        'teamos.xyz', 'tehparadox.net', 'undernet.org', 'warez-v3.org',
        'warezforums.com',
    ],
    '🏠 Home / Food / Lifestyle': [
        'doordash.com', 'gofundme.com', 'havenly.com', 'planetzero.me',
        'plotaroute.com', 'reciperr.com', 'tacobell.com', 'texastripe.com',
        'whole-dog-journal.com',
    ],
    '🛠️ Productivity / Business': [
        'cloudresearch.com', 'dasan.co', 'datanodes.to', 'fedex.com',
        'freshdesk.com', 'goshippo.com', 'joinflyp.com', 'observanow.com',
        'pirateship.com', 'smartreceipts.co', 'take-me-to.space', 'togetherprice.com',
        'twilio.com', 'ups.com', 'usps.com',
    ],
    '⚖️ Government / Public Services': [
        'texas.gov', 'yourtexasbenefits.com',
    ],
    '🎲 Gambling / Betting': [
        'betonline.ag', 'icmpoker.com', 'ignitioncasino.eu', 'partypoker.com',
        'pokerstars.com',
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
