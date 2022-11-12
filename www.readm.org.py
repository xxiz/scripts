# To get your manga id head over to https://readm.org/ and search for your manga then copy the manga ID from the URL
# Example: https://readm.org/manga/one-piece/ -> Manga ID: one-piece
# So to download One Piece chapter's 510-520 you would do the following:
# python3 readm.py one-piece 1:1000

# NOTE: This scripts is multithreaded so it takes a while initally to propogate all chapter URLs
# NOTE: I reccomend downloading ~100 chapters at a time to avoid getting rate limited, although I have not experienced it

import concurrent.futures, os, sys, shutil, requests, time, zipfile
from tarfile import CompressionError
from http.client import CannotSendRequest
from bs4 import BeautifulSoup

BASE_URL = "https://readm.org"
SAVE_DIRECTORY = os.getcwd() + "\\manga"
READ_MANGA_URL = "https://readm.org/manga/{}/{}/all-pages"
USAGE = "Usage: python3 {} <manga> <chapter> or python3 {} <manga> <start chapter>:<end chapter>"

def create_comic_archive(manga_id, chapter_number):
    save_dir = f"{SAVE_DIRECTORY}\\{manga_id}"
    content_dir = f"{save_dir}\\{chapter_number}"
    try:
        with zipfile.ZipFile(f"{save_dir}\\{chapter_number}.cbz", 'w') as zip_file:
            for item in os.listdir(content_dir):
                zip_file.write(os.path.join(content_dir, item), item)
            
            print(f"Created comic archive for ch.{chapter_number}")
    except Exception as e:
        print(f"ERROR - Cannot create comic archive for ch.{chapter_number}")
        raise CompressionError

def remove_temp_folder(save_dir):
    shutil.rmtree(save_dir)

def has_chapter_been_downloaded(manga, chapter):
    # CBZ File Check
    if os.path.exists(f"{SAVE_DIRECTORY}\\{manga}\\{chapter}.cbz"):
        return True
    
    # Download Folder Check
    if os.path.exists(f"{SAVE_DIRECTORY}\\{manga}\\{chapter}"):
        if len(os.listdir(f"{SAVE_DIRECTORY}\\{manga}\\{chapter}")) > 0:
            return False
    return False

def download_manga_chapter(manga_id, chapter_number):

    save_dir = f"{SAVE_DIRECTORY}\\{manga_id}\\{chapter_number}"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    html_content = requests.get(READ_MANGA_URL.format(manga_id, chapter_number)).text
    soup = BeautifulSoup(html_content, 'html.parser')

    i = 1
    manga_panels = soup.find_all('img', class_='img-responsive scroll-down')
    # print("Found {} panels for ch.{}".format(len(manga_panels), chapter_number))

    for panel in manga_panels:
        
        download_url = BASE_URL + panel['src']
        save_path = f"{SAVE_DIRECTORY}\\{manga_id}\\{chapter_number}\\panel_{i}.jpg"

        if os.path.exists(save_path):
            print(f"ERROR - Panel # {i} already exists for ch.{chapter_number}, skipping...")
            i += 1
            continue

        try:
            r = requests.get(download_url).content
            with open(save_path, 'wb') as f:
                f.write(r)
            i += 1
        except:
            print(f"ERROR - Cannot download Panel # {i} ch.{chapter_number}")
            i += 1
            raise CannotSendRequest
    

    create_comic_archive(manga_id, chapter_number)
    
    try:
        remove_temp_folder(save_dir)
    except:
        print(f"ERROR - Cannot remove temp folder for ch.{chapter_number}")
        raise OSError

    print(f"Downloaded {manga_id} ch.{chapter_number} ({i} panels)")

if __name__ == "__main__":

    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print(USAGE.format(sys.argv[0], sys.argv[0]))
        exit(1)
    
    try:
        if ":" in sys.argv[2]:
            manga = sys.argv[1]
            start_chapter, end_chapter = sys.argv[2].split(":")
            
            start_chapter = int(start_chapter)
            end_chapter = int(end_chapter)

            if start_chapter > end_chapter:
                print("Start chapter cannot be greater than end chapter")
                exit(1)
            
            # First run to see if manga folder is already created
            if not os.path.exists(os.getcwd() + f"\\manga"):
                os.mkdir(os.getcwd() + f"\\manga")

            # Create the working directory for the manga if it doesn't exist
            if not os.path.exists(os.getcwd() + f"\\manga\\{manga}"):
                os.mkdir(os.getcwd() + f"\\manga\\{manga}")

            start_time = time.time()

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for chapter in range(start_chapter, end_chapter + 1):
                    if not has_chapter_been_downloaded(manga, chapter):
                        futures.append(executor.submit(download_manga_chapter, manga_id=manga, chapter_number=chapter))
                    else:
                        print("Chapter {} already downloaded".format(chapter))
        
        else:
            manga = sys.argv[1]
            chapter = sys.argv[2]
            if not has_chapter_been_downloaded(manga, chapter):
                download_manga_chapter(manga, chapter)
            else:
                print("Chapter {} already downloaded".format(chapter))
    except Exception as e:
        print(USAGE)
        exit(1)