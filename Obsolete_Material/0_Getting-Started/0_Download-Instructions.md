These are instructions on how to download the course through github. If you have not done so already, follow the instructions video for your computer's operating system and follow along. 

1. Download the required programs for this course. There are 4 in total. Follow the links below to get your computer's operating system's version of the necessary programs.

    * [VSCode Download](https://code.visualstudio.com/download) - [Setup Video](https://code.visualstudio.com/docs/setup/setup-overview)
    * [Python Installation instructions](https://github.com/PackeTsar/Install-Python) 
    * [Git Bash Installation](https://git-scm.com/downloads) 

2. Once you have downloaded these programs onto your computer, unzip one of the following videos to guide you through the installation of each program. Default settings are recommended for all installations.

    * Windows11-initial-setup-v0_1.zip
    * MacOS-initial-setup-v0_1.zip (Comming Soon)
    * Linux-initial-setup-v0_1.zip (Coming Soon)

3. Launch VSCode. If you have not already chosen a folder, look in the "File" menu at the top left of VSCode and click on "Open Folder". Then use the prompts to choose a project or documents folder that you would like to keep all of the course material in.

4. Open a Terminal inside VSCode by going to the menu in the top left corner and following File, Edit, Selection, and so on until you find Terminal. Click on it and select New Terminal.

5. Inside the terminal in the upper right hand corner, there is an icon of a + and a dropdown menu. Click inside the dropdown menu and select "Select Default Profile". A prompt will show up at the top of your screen asking which profile you wish to choose. Click on GitBash.
    **Note: If GitBash is not an option at this point, please review the Git Bash Installation and set up video instructions. Your Git Bash installation may be misconfigured

6. Click in the new terminal and type `git --version` to verify your git bash installation.

7. Next to download the course material, type `git clone https://github.com/vparrello/FIG-Bioinformatics-Course.git` inside your terminal.

8. Once that finishes, type `git branch ` and then your name. This will be the name of your branch.  

9. Next type `git checkout ` and then the name of your branch. This creates a personal copy of the material for you.

git branch --set-upstream-to=origin/master <branch>

10. You are done with your basic setup! Continue to the next document to install a crucial tool for this course. 

## Creating a Persistent Environment Variable

In this course, we will be calling programs from the command line. This tool requires that you are in a specific directory, or location, to call those programs in a way that the computer can find them. To make this easier, we are going to create an environment configuration file that contains a variable, or a shortcut, that points to the Course directory. This way you will have a shortcut command that ensures you start each exercise in the same location. This file is called `.bashrc` and is located in your home directory to make sure you can access it from any terminal. 

1. Open a terminal in VSCode.

2. Use `pwd` to find out where you are:
    ```bash
    pwd
    ```
    You should get a path that looks similar to this:
    ```
    /Users/joeshmoe/Documents/FIG-Bioinformatics-Course
    ```
    Ensure the path ends with `FIG-Bioinformatics-Course`. If it does not, close your VSCode and reopen it inside the `FIG-Bioinformatics-Course` directory from your File Explorer. Remember this path as you will need to copy and paste it into the `.bashrc` file in step 4.

3. Open the `.bashrc` file in your home directory using Visual Studio Code:
    ```bash
    code ~/.bashrc
    ```
    If the file does not exist, this command will create it. It will then open a new window in VSCode in which you can insert your information.

4. Add the following lines to the `.bashrc` file to set the `COURSE_DIR` variable and navigate instructions to the course directory: BE SURE TO REPLACE THE PATH WITH YOUR OWN PATH FROM STEP 2.
    ```bash
    # Set the course directory environment variable
    export COURSE_DIR="/Users/joeshmoe/Documents/FIG-Bioinformatics-Course"

    # Automatically navigate to the course directory
    cd $COURSE_DIR
    ```

5. Save the file in Visual Studio Code by clicking on `File` > `Save` or using the shortcut `Ctrl + S` (Windows/Linux) or `Cmd + S` (macOS). It is now safe to close the other window of VSCode.

6. Apply the changes immediately by sourcing the `.bashrc` file in the terminal:
    ```bash
    source ~/.bashrc
    ```

7. Check to make sure that the .bashrc file worked by typing `echo $COURSE_DIR` in the terminal. It should return the path to the Course directory and should match the same print out you had when you used `pwd`. If these are different, start over from step 2 and ensure that you have used the correct path. If you get a `404 file not found` error, then you should go back to step 3 and recreate the .bashrc file.

