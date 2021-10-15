import sys
import requests
from lxml import html

def download(url: str, filename: str):
    if not len(filename.split(".")) > 1:
        filename = filename + ".mp4"
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print("[+] Download completed!")
    return filename

def parse_link(url: str):
    final_url = ""
    r = requests.get(url)
    tree = html.fromstring(r.text)
    element = tree.xpath("/html/body/a[@class=\"download_url\"]/@onclick")[0]

    for char in element[element.index("h")::]:
        if char == "'":
            break
        final_url += char

    print("[*] link parsed!")
    return final_url

def check_youtube_url(url: str):
    valid = True
    splitted = url.split("&")
    for word in splitted:
        if word.split("=")[0] == "list":
            valid = False

    return valid

def parse_youtube_link(url: str):
    final_url = ""
    video_code = ""
    base_url = "https://api.tubemp3.biz/video/{0}"

    if not check_youtube_url(url):
        print("[-] Url is a playlist url, make sure to pass a video url instead!")
        sys.exit(-1)

    for a in url[url.index("=")::]:
        if a == "=":
            continue
        video_code += a

    final_url = base_url.format(video_code)
    print("[*] Youtube link parsed!")
    return final_url

def usage() -> None:
    print("[*] Usage: \n")
    print(f"[*] python3 {sys.argv[0]} <VIDEO URL> <OUTPUT FILENAME>\n")

def main() -> None:
    if not len(sys.argv) > 1:
        usage()
        return

    youtube_link = str(sys.argv[1])
    filename = str(sys.argv[2])
    parsed_youtube_link = parse_youtube_link(youtube_link)
    parsed_link = parse_link(parsed_youtube_link)
    filename = download(parsed_link, filename)
    print(f"[+] Open '{filename}'")

if __name__ == '__main__':
    main()
