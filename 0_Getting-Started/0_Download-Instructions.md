These are instructions on how to download the course through github. If you have not done so already, follow the instructions video for your computer's operating system and follow along. 

1. Download the required programs for this course. There are 4 in total. Follow the links below to get your computer's operating system's version of the necessary programs.

    * [VSCode Download](https://code.visualstudio.com/download) - [Setup Video](https://code.visualstudio.com/docs/setup/setup-overview)

    * [Python Installation instructions](https://github.com/PackeTsar/Install-Python)

    * [Git Bash Installation](https://git-scm.com/downloads) 

2. Once you have downloaded these programs onto your computer, unzip one of the following videos to guide you through the installation of each program. Default settings are recommended for all installations.

    * Windows11-initial-setup-v0_1.zip

    * MacOS-initial-setup-v0_1.zip (Coming Soon)

    * Linux-initial-setup-v0_1.zip (Coming Soon)

3. Launch VSCode. If you have not already chosen a folder, look in the "File" menu at the top left of VSCode and click on "Open Folder". Then use the prompts to choose a project or documents folder that you would like to keep all of the course material in.

4. Open a Terminal inside VSCode by going to the menu in the top left corner and following File, Edit, Selection, and so on until you find Terminal. Click on it and select New Terminal.

5. Inside the terminal in the upper right hand corner, there is an icon that looks like a `+` with a "v-like" symbol next to it, which indicates that there is an associated dropdown menu. Click the dropdown-menu "v", then select "Select Default Profile". A prompt will show up at the top of your screen asking which profile you wish to choose. Click on "bash" if you are on a `macOS` or `LINUX` machine, or `GitBash` if you are on a Windows machine.<br>
**Note: If GitBash is not an option at this point, please review the Git Bash Installation and set up video instructions. Your Git Bash installation may be misconfigured.**

6. Click in the new terminal and type `git --version` to verify that `git` has been installed.

7. Type `pwd` to verify that you are in the folder that you want to install the course under.

8. Next, to download the course material, type `git clone https://github.com/vparrello/FIG-Bioinformatics-Course.git` inside your terminal.

9. Type `exit` to leave the terminal-window.

10. Use the "Open Folder" item under the "File" menu again, this time to open the course folder.

11. Launch a new terminal-window; this time,
you should see something like:

    ✅ COURSE_HOME is: /Users/yourUsername/Project/FIG-Bioinformatics-Course<br>
    🔁 Use 'cdcourse' anytime to return to this root.

* NOTE: The format for `COURSE_HOME`
may differ somewhat depending on whether you are on
`macOS`, `LINUX`, or `Windows`, as well as what folder
you installed the course under.

If you see something like the above, then congratulations &mdash; you are done with your basic setup!

12. Continue to the next document, `0_Installing-the-BV-BRC-App.md`, to install a crucial tool for this course. 
