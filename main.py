from pytube import YouTube, Search, Stream
import csv

qualities = [320, 160, 128, 70, 50]


def get_audio_and_link(request, download_limit=1000, download_audio=False):
    f = open(f"results_{request}.csv", "w", encoding="utf8", newline='')
    csv_f = csv.writer(f)
    s = Search(request)
    count = 0

    while len(s.results) < download_limit:
        try:
            s.get_next_results()
        except:
            print(f"Got first {len(s.results)} for {request}!")
            f.write(f"# Got first {len(s.results)} for {request}\n")
            break

    csv_f.writerow(['Naslov', 'URL', 'filename'])
    r: YouTube
    for ind in range(len(s.results)):
        r = s.results[ind]
        # For each we want the url and audio file
        if download_audio:
            downloaded = False
            for q in qualities:
                if r.streams.filter(abr=f"{q}kbps", only_audio=True):
                    clip = r.streams.filter(abr=f"{q}kbps", only_audio=True)[0]
                    clip: Stream
                    extension = clip.default_filename.split(".")[-1]
                    clip.download(filename=f"{count}.{extension}")
                    csv_f.writerow([r.title, r.watch_url])
                    f.flush()
                    print(f"Downloaded {r.watch_url}")
                    downloaded = True
                    count += 1
                    break
            if not downloaded:
                print(r.watch_url)
        else:
            csv_f.writerow([r.title, r.watch_url, f'{ind:>05d}.mp3'])
    f.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_audio_and_link("slovenska otroška glasba", download_audio=False)
    get_audio_and_link("slovenske otroške", download_audio=False)
    get_audio_and_link("slovenske mladinske pesmi", download_audio=False)
