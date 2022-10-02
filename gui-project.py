import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import codecs
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar
import threading


df = pd.DataFrame(
    columns=[
        "Title",
        "Location",
        "Company",
        "Link",
        "Description",
        "Time",
        "Salary",
        "Logo",
    ]
)


def Widgets():

    search_label = Label(root, text="keyword :", pady=5, padx=5)
    search_label.grid(row=2, column=0, pady=5, padx=5)

    root.searchText = Entry(root, width=35, textvariable=search_key, font="Arial 14")
    root.searchText.grid(row=2, column=1, pady=5, padx=5, columnspan=2)

    page_label = Label(root, text="Number of pages :", pady=5, padx=5)
    page_label.grid(row=3, column=0, pady=5, padx=5)

    root.pageNum = Entry(root, width=35, textvariable=pages, font="Arial 14")
    root.pageNum.grid(row=3, column=1, pady=5, padx=5, columnspan=2)

    destination_label = Label(root, text="Destination :", pady=5, padx=9)
    destination_label.grid(row=4, column=0, pady=5, padx=5)

    root.destinationText = Entry(
        root, width=27, textvariable=download_Path, font="Arial 14"
    )
    root.destinationText.grid(row=4, column=1, pady=5, padx=5)

    browse_B = Button(
        root,
        text="Browse",
        command=Browse,
        width=10,
        relief=GROOVE,
        background="#19456B",
    )
    browse_B.grid(row=4, column=2, pady=1, padx=1)

    LinkedIn = Button(
        root,
        text="LinkedIn",
        command=startscrapLinkedIn,
        width=20,
        pady=10,
        padx=15,
        relief=GROOVE,
        font="Georgia, 13",
        background="#11698E",
        activebackground="#16C79A",
    )
    LinkedIn.grid(row=5, column=1, pady=10, padx=10)

    Wuzzuf = Button(
        root,
        text="Wuzzuf",
        command=startscrapWuzzuf,
        width=20,
        pady=10,
        padx=15,
        relief=GROOVE,
        font="Georgia, 13",
        background="#11698E",
        activebackground="#16C79A",
    )
    Wuzzuf.grid(row=6, column=1, pady=10, padx=10)


def Browse():

    download_Directory = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH", title="Path"
    )

    download_Path.set(download_Directory)


def scrapLinkedIn():
    progress = Progressbar(root, orient="horizontal", mode="determinate", length=280)
    progress.grid(row=7, column=1, pady=1, padx=1)
    key = search_key.get()
    download_Folder = download_Path.get()
    p = pages.get()
    urls = []
    global df
    for i in range(0, p):
        urls.append(
            f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={key}&amp;trk=public_jobs_jobs-search-bar_search-submit&amp;position=1&amp;pageNum=0&amp;start={i}"
        )

    for url in urls:
        r = BeautifulSoup(requests.get(url).content, "html.parser")
        jobs = r.find_all(
            "div",
            class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card",
        )
        time.sleep(3)
        for job in jobs:
            title = (
                job.find("h3", class_="base-search-card__title")
                .text.strip()
                .encode("utf-8")
            )
            title = codecs.decode(title)
            location = (
                job.find("span", class_="job-search-card__location")
                .text.strip()
                .encode("utf-8")
            )
            location = codecs.decode(location)
            company = (
                job.find("h4", class_="base-search-card__subtitle")
                .text.strip()
                .encode("utf-8")
            )
            company = codecs.decode(company)
            job_link = job.find(
                "a",
                attrs={
                    "data-tracking-control-name": "public_jobs_jserp-result_search-card"
                },
            )["href"]
            try:
                salary = (
                    job.find("span", class_="job-search-card__salary-info")
                    .text.strip()
                    .encode("utf-8")
                )
                salary = codecs.decode(salary).replace("\n", "")
            except:
                salary = "No info"
            job_r = BeautifulSoup(requests.get(job_link).content, "html.parser")
            time.sleep(3)
            try:
                description = (
                    job_r.find("div", attrs={"class": "show-more-less-html__markup"})
                    .text.strip()
                    .encode("utf-8")
                )
                description = codecs.decode(description)
            except:
                description = "No info"
            try:
                job_time = (
                    job_r.find(
                        "span", class_="posted-time-ago__text topcard__flavor--metadata"
                    )
                    .text.strip()
                    .encode("utf-8")
                )
                job_time = codecs.decode(job_time)
            except:
                job_time = "No info"
            try:
                logo = job_r.find(
                    "a",
                    attrs={"data-tracking-control-name": "public_jobs_topcard_logo"},
                ).img["data-delayed-url"]
            except:
                logo = "No info"

            df = df.append(
                {
                    "Title": title,
                    "Location": location,
                    "Company": company,
                    "Salary": salary,
                    "Link": job_link,
                    "Description": description,
                    "Logo": logo,
                    "Time": job_time,
                },
                ignore_index=True,
            )
            root.update_idletasks()
            progress["value"] += 100 * (1 / len(jobs)) / p
    download_Folder = download_Path.get()
    df.to_csv(f"{download_Folder}\jobs.csv")
    messagebox.showinfo(
        " ",
        "Done!",
    )


def scrapWuzzuf():
    progress = Progressbar(root, orient="horizontal", mode="determinate", length=280)
    progress.grid(row=7, column=1, pady=1, padx=1)
    key = search_key.get()
    download_Folder = download_Path.get()
    p = pages.get()
    global df
    urls = []
    for i in range(0, p):
        urls.append(f"https://wuzzuf.net/search/jobs/?a=navbg&q={key}&start={i}")
    for url in urls:
        headers = {
            "Connection": "keep-alive",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        }
        r = BeautifulSoup(
            requests.get(url, headers=headers, timeout=120).content, "html.parser"
        )
        jobs = r.find_all(
            "div",
            class_="css-1gatmva e1v1l3u10",
        )
        time.sleep(5)
        for job in jobs:
            job_link = f'https://wuzzuf.net{job.find("a", class_="css-o171kl")["href"]}'
            title = job.find("a", class_="css-o171kl").text.strip().encode("utf-8")
            title = codecs.decode(title)
            location = (
                job.find("span", class_="css-5wys0k").text.strip().encode("utf-8")
            )
            location = codecs.decode(location)
            company = job.find("a", class_="css-17s97q8").text.strip().encode("utf-8")
            company = codecs.decode(company).replace("-", "")

            job_r = BeautifulSoup(
                requests.get(job_link, headers=headers, timeout=120).content,
                "html.parser",
            )
            time.sleep(5)
            try:
                description = (
                    job_r.find("div", class_="css-1uobp1k").text.strip().encode("utf-8")
                )
                description = codecs.decode(description)
            except:
                description = "No info"
            try:
                job_time = (
                    job_r.find("span", class_="css-182mrdn")
                    .text.strip()
                    .encode("utf-8")
                )
                job_time = codecs.decode(job_time)
            except:
                job_time = "No info"

            df = df.append(
                {
                    "Title": title,
                    "Location": location,
                    "Company": company,
                    "Link": job_link,
                    "Description": description,
                    "Time": job_time,
                },
                ignore_index=True,
            )
            root.update_idletasks()
            progress["value"] += 100 * (1 / len(jobs)) / p
    download_Folder = download_Path.get()
    df.to_csv(f"{download_Folder}\jobs.csv")
    messagebox.showinfo(" ", "Done!")


# Using threads to solve 'unresponsive' issue


def startscrapLinkedIn():
    threading.Thread(target=scrapLinkedIn).start()


def startscrapWuzzuf():
    threading.Thread(target=scrapWuzzuf).start()


root = Tk()


root.geometry("520x300")
root.resizable(False, False)
root.title("Job scraper")
root.configure(bg="#F8F1F1")
search_key = StringVar()
download_Path = StringVar()
pages = IntVar()
pages.set(1)
Widgets()


root.mainloop()
