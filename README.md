# bereal_save_memories
Python script to save all memories with side-by-side front and back images and added EXIF data

Really simple script, not mutch thought went into it. Designed to use in Windows.

Requirements:
- Python 3
- Pillow and piexif library

Steps to use:

1. Request your data straight from BeReal using the in-app form in the Help section using the following template:

In accordance with Art. 15(3) GDPR, provide me with a copy of all personal data concerning me that you are processing, including any potential pseudonymised data on me as per Article 4(5) GDPR. Please make the personal data concerning me, which I have provided to you, available to me in a structured, commonly used and machine-readable format as laid down in Article 20(1) GDPR. I include the following information necessary to identify me: username: <your username>. Thanks, <your username>

You will get a download link as an answer to your ticket in-app.

2. Unpack the zipped data to C:\bereal

*Note : Some older accounts (2021) may have a second folder named `bereal` containing jpg images. In that case just move all the jpg files to the `post` folder*

3. Place the python script next to the extracted data and run it
4. Enjoy your memories beautifully packaged and sorted by date :)
