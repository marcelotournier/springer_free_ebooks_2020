import re
import csv
from urllib.request import urlopen
import concurrent.futures

def get_booklist(csvfile):
	with open(csvfile) as file:
		matrix = list(csv.reader(file))
	return matrix


def get_download_url(url):
	with urlopen(url) as link:
		page = link.readlines()
		page = [line.decode() for line in page]
	pdfs = [item for item in page if "Download this book in PDF format" in item]
	links = set([re.findall(r"/content/.*\.pdf",l)[0] for l in pdfs])
	if len(links) == 0:
		download_url = ""
	else:
		download_url = "https://link.springer.com" + list(links)[0]
	return download_url


def write_pdf(book):
	title = book[1].replace('"',"").rstrip()
	url = get_download_url(book[-1])
	if url != "":
		print("[downloading] " + book[1])
		with urlopen(url) as link:
			download = link.read()
		with open( title + '.pdf', 'wb') as file:
			file.write(download)
	else:
		print(f"[warning] {title} not downloaded")


def save_files(booklist):
	with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
		for book in booklist:
			future = executor.submit(write_pdf, book)
			

books = get_booklist('springer_free_books.csv')
print("downloading books. Please wait 20-60 Minutes, depending on your connection.")
save_files(books[1:])
