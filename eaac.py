from bs4 import BeautifulSoup
import urllib.request
import colorama


def main():
    resp = urllib.request.urlopen("http://eaac.info")
    soup = BeautifulSoup(
        resp,  "html.parser", from_encoding=resp.info().get_param('charset')

    )
    links = soup.find_all('a', href=True)
    unique_links = []
    generate_links = [
        unique_links.append([link.text, link['href']]) for link in links if link['href']
        not in ['#', 'http://www.yootheme.com'] and [link.text, link['href']] not in unique_links
    ]

    # Check existing homepage links, write new ones and compare
    try:
        f = open('files/homepage_links.txt', 'r')
        old_text = f.read()
        f.close()
    except FileNotFoundError:
        old_text = 'no existing file'

    f = open('files/homepage_links.txt', 'w')
    new_text = ''
    for link in unique_links:
        text_to_write = '{}: {}\n'.format(link[0], link[1])
        new_text += text_to_write
    f.write(new_text)
    f.close()

    if old_text == 'no existing file':
        print(colorama.Fore.CYAN + 'New file homepage_links.txt created.')
        for link in unique_links:
            compare_link_text(link)
    elif new_text != old_text:
        print(colorama.Fore.RED + "Home page links have changed")
        # if homepage links have changed, check content of all links
        for link in unique_links:
            compare_link_text(link)
    else:
        # if homepage links have not changed, just check content of timetable link
        print(
            colorama.Fore.GREEN + "Home page links have not changed; "
                                  "checking content of Timetable link only")
        for link in unique_links:
            if link[0] == "2015 TIMETABLE":
                compare_link_text(link)


def compare_link_text(link):
    filename = '{}.txt'.format('_'.join(link[0].split(' ')))
    try:
        f = open('files/{}'.format(filename), 'r')
        old_link_text = f.read()
        f.close()
    except FileNotFoundError:
        old_link_text = 'no existing file'

    f = open('files/{}'.format(filename), 'w')
    resp = urllib.request.urlopen(link[1])
    soup = BeautifulSoup(
        resp,  "html.parser", from_encoding=resp.info().get_param('charset')
    )
    new_link_text = soup.find('body').get_text()

    f.write(new_link_text)
    f.close()

    if old_link_text == 'no existing file':
        print(colorama.Fore.CYAN + 'New file {} created for "{} - {}"'. format(
            filename, link[0], link[1]
        ))
    elif old_link_text.splitlines() != new_link_text.splitlines():
        print(colorama.Fore.RED + 'Content of link "{} - {}" has changed (file {})'.format(
            link[0], link[1], filename
        ))
    else:
        print(colorama.Fore.GREEN + 'Checked content of link "{} - {}"; no change'.format(
            link[0], link[1]
        ))

if __name__ == '__main__':
    colorama.init()
    main()
    colorama.deinit()
