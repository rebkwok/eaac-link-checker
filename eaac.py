from bs4 import BeautifulSoup
import urllib.request
import colorama
import smtplib
import os
from email.mime.text import MIMEText
from email.parser import Parser


def main():

    changed = False
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

    msg = []

    if old_text == 'no existing file':
        nofile_msg = 'New file homepage_links.txt created.'
        print(colorama.Fore.CYAN + nofile_msg)
        msg += [nofile_msg]
        changed = True
        for link in unique_links:
            new_msg, _ = compare_link_text(link)
            msg += new_msg
    elif new_text != old_text:
        print(colorama.Fore.RED + "Home page links have changed")
        changed = True
        # if homepage links have changed, check content of all links
        for link in unique_links:
            new_msg, _ = compare_link_text(link)
            msg += new_msg
    else:
        # if homepage links have not changed, just check content of timetable link
        nochange_msg = "Home page links have not changed; " \
                       "checking content of Timetable link only"
        print(colorama.Fore.GREEN + nochange_msg)
        msg += [nochange_msg]

        for link in unique_links:
            if link[0] == "2015 TIMETABLE":
                new_msg, changed_link = compare_link_text(link)
                msg += new_msg
                changed = changed_link

    from_email = 'coderebk@gmail.com'
    to_email = ['rebkwok@gmail.com', 'rebkwok@yahoo.co.uk']
    subject = '**{}** EAAC link checker'.format(
        'CHANGED' if changed else 'NO CHANGE'
    )

    email_msg = MIMEText('\n'.join(msg))
    email_msg['From'] = from_email
    email_msg['Subject'] = subject

    if changed:
        email_msg['To'] = ', '.join(to_email)
    else:
        email_msg['To'] = 'rebkwok@gmail.com'
    username = 'coderebk@gmail.com'
    password = os.environ.get('EMAIL_PASSWORD', '')

    if password:
        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(from_email, to_email, email_msg.as_string())
        server.quit()
    else:
        print("No email password found!")


def compare_link_text(link):
    msg = []
    changed = False
    filename = '{}.txt'.format('_'.join(link[0].split(' ')))
    try:
        f = open('files/{}'.format(filename), 'r')
        old_link_text = f.read()
        f.close()
    except FileNotFoundError:
        old_link_text = 'no existing file'
        filename = 'temp.txt'

    f = open('files/{}'.format(filename), 'w')
    resp = urllib.request.urlopen(link[1])
    soup = BeautifulSoup(
        resp,  "html.parser", from_encoding=resp.info().get_param('charset')
    )
    new_link_text = soup.find('body').get_text()

    f.write(new_link_text)
    f.close()

    if old_link_text == 'no existing file':
        changed = True
        newfile_msg = 'CHANGED: New link "{} - {}"; written to temp.txt; NOTE: add new file {}'.format(
            link[0], link[1], '{}.txt'.format('_'.join(link[0].split(' ')))
        )
        print(colorama.Fore.CYAN + newfile_msg)
        msg.append(newfile_msg)
    elif old_link_text.splitlines() != new_link_text.splitlines():
        changed = True
        linkmsg = 'CHANGED: content of link "{} - {}")'.format(
            link[0], link[1]
        )
        print(colorama.Fore.RED + linkmsg)
        msg.append(linkmsg)
    else:
        linkmsg = 'No change: content of link "{} - {}"'.format(
            link[0], link[1]
        )
        print(colorama.Fore.GREEN + linkmsg)
        msg.append(linkmsg)

    return msg, changed

if __name__ == '__main__':
    colorama.init()
    main()
    colorama.deinit()