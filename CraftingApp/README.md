# Eryndlyn Crafting Data Contributor Guide

Welcome! This guide will walk you through updating the crafting data for **Eryndlyn**.

You do **not** need any programming or developer experience to follow these instructions. We will walk through each step one at a time.

## What you will be doing

You will:

1. Create a GitHub account.
2. Ask an administrator for access to the Eryndlyn GitHub repository.
3. Open the Crafting App and make your changes.
4. Copy the updated JSON data.
5. Put the updated data into GitHub.
6. Submit your changes for review.
7. Run the GitHub deployment workflow after your changes have been approved.

> **Important:** Take your time and follow the steps in order. If something doesn't look like the instructions below, stop and ask an administrator for help rather than guessing.

---

# Step 1 — Create a GitHub Account

GitHub is the website we use to store and manage the Eryndlyn project.

If you already have a GitHub account, you can skip to **Step 2**.

### 1. Go to GitHub

Open:

https://github.com/

### 2. Click "Sign up"

On the GitHub homepage, click the **Sign up** button.

GitHub will ask you for some basic information, such as:

* Your email address
* A password
* A username

Follow GitHub's instructions to finish creating your account.

### 3. Verify your email address

GitHub may send you an email asking you to verify your email address.

Open that email and follow the verification instructions.

Once your account is created and your email is verified, continue to Step 2.

---

# Step 2 — Get Contributor Access

Before you can make changes to the Eryndlyn project, an administrator needs to give your GitHub account permission to contribute.

The project is located here:

https://github.com/kaitlynmurray712-coder/Eryndlyn

## Contact an administrator

Reach out to an Eryndlyn administrator and tell them:

> "I have created my GitHub account and need contributor access to the Eryndlyn repository."

Give the administrator your **GitHub username**.

### How do I find my GitHub username?

Go to:

https://github.com/

Make sure you are logged in.

Your GitHub username is the name associated with your account. It is also part of your GitHub profile URL.

For example:

```text
https://github.com/exampleusername
```

In this example, `exampleusername` is the GitHub username.

### Wait for access

An administrator will need to give your account access to the repository.

Do not continue to the next steps until the administrator confirms that you have contributor access.

---

# Step 3 — Open the Crafting App

Once you have contributor access, open the Eryndlyn Crafting App:

https://kaitlynmurray712-coder.github.io/Eryndlyn/CraftingApp/index.html

This is the website where you will make your crafting data changes.

You do **not** need to edit the website's code.

Use the controls on the page to make the changes you need.

---

# Step 4 — Update the Crafting Data

Use the Crafting App to make your changes.

Take your time and check your changes before continuing.

When you are finished, look at the **top-right corner** of the Crafting App.

You should see a button labeled:

**COPY JSON**

Click the **COPY JSON** button.

This copies the updated crafting data to your computer's clipboard.

> **Important:** Do not skip this step. The information you copy is what you will put into GitHub in the next step.

---

# Step 5 — Open the Crafting JSON File on GitHub

Now open the crafting data file in GitHub:

https://github.com/kaitlynmurray712-coder/Eryndlyn/blob/main/CraftingApp/crafting.json

You should see a file named:

```text
crafting.json
```

This file contains the crafting information used by the Eryndlyn Crafting App.

---

# Step 6 — Edit the JSON File

You need to replace the existing contents of `crafting.json` with the new JSON you copied from the Crafting App.

### 1. Find the Edit button

On the GitHub page for `crafting.json`, look for the **Edit** button.

It may look like a pencil icon.

Click it.

If you do not see an Edit button, you may not have contributor access. Contact an administrator.

### 2. Select the existing JSON

GitHub will open an editor containing the existing JSON.

Click inside the editor.

Select all of the existing text.

On Windows, you can usually do this by pressing:

```text
Ctrl + A
```

On Mac, use:

```text
Command + A
```

### 3. Delete the old JSON

Delete the selected text.

The editor should now be empty.

### 4. Paste the new JSON

Paste the JSON you copied from the Crafting App.

On Windows, you can usually paste using:

```text
Ctrl + V
```

On Mac:

```text
Command + V
```

The editor should now contain the new JSON from the Crafting App.

### 5. Check your work

Before saving anything, make sure the file contains the JSON you copied from the Crafting App.

Do not add extra text before or after the JSON.

---

# Step 7 — Create a Pull Request for Review

When you are ready to save your changes, GitHub will ask you to commit your changes.

You may see an option such as:

**Commit changes**

A **commit** is simply a saved set of changes in GitHub.

A **Pull Request**, often called a **PR**, is a request for someone else to review your changes before they become part of the main project.

## Create your commit

GitHub will provide a place to enter a description of your changes.

For example:

```text
Update crafting data
```

You can use a similar description that explains what you changed.

Then choose the option that creates your changes on a **new branch** and opens a pull request, if GitHub presents that choice.

> **Do not make changes directly to the `main` branch if GitHub gives you the option to create a new branch and pull request.**

Continue through GitHub's instructions until the Pull Request is created.

---

# Step 8 — Wait for the Pull Request to Be Reviewed

After creating the Pull Request, an administrator or project maintainer can review your changes.

You may see a page showing your Pull Request.

The page may contain information such as:

* The files you changed
* The changes you made
* Comments from reviewers
* Checks that GitHub is running

If an administrator asks you to make changes, follow their instructions.

If your Pull Request is approved and merged, your changes will become part of the project's `main` branch.

> **Do not run the deployment workflow until the administrator has confirmed that your Pull Request has been merged**, unless your project's normal process says otherwise.

---

# Step 9 — Run the Crafting Deployment

Once your Pull Request has been approved and merged, open the Eryndlyn GitHub Actions page:

https://github.com/kaitlynmurray712-coder/Eryndlyn/actions/workflows/deploy-crafting.yml

GitHub Actions is the system that performs automated tasks for the project.

For this project, it is used to deploy the updated Crafting App.

## Run the workflow

On the page, look for:

**Run workflow**

Click **Run workflow**.

GitHub may show a small menu asking which branch to run the workflow on.

Select:

```text
main
```

Then click the **Run workflow** button.

---

# Step 10 — Wait for the Deployment

After starting the workflow, GitHub will show a new workflow run.

The workflow may take a little time to finish.

You may see a status indicator showing that the workflow is:

* Running
* Successful
* Failed

Wait for the workflow to finish.

A successful workflow should indicate that the deployment completed successfully.

If the workflow fails, **do not repeatedly click "Run workflow."**

Instead, contact an administrator and provide them with the link to the failed workflow run.

---

# Step 11 — Check the Crafting App

After the deployment has completed successfully, open the Crafting App again:

https://kaitlynmurray712-coder.github.io/Eryndlyn/CraftingApp/index.html

Check that your changes are visible.

If everything looks correct, you're done!

---

# Quick Reference

Once you are familiar with the process, these are the links you will use most often.

### Crafting App

https://kaitlynmurray712-coder.github.io/Eryndlyn/CraftingApp/index.html

Use this to make and copy your crafting data.

### Crafting JSON file

https://github.com/kaitlynmurray712-coder/Eryndlyn/blob/main/CraftingApp/crafting.json

Use this to update the JSON in GitHub and create your Pull Request.

### GitHub Actions — Crafting Deployment

https://github.com/kaitlynmurray712-coder/Eryndlyn/actions/workflows/deploy-crafting.yml

Use this to manually run the crafting deployment after your changes have been merged.

### Eryndlyn GitHub Repository

https://github.com/kaitlynmurray712-coder/Eryndlyn

This is the main GitHub repository for the project.

---

# GitHub Terms You Will See

If you are new to GitHub, these terms may be unfamiliar.

| Term                  | What it means                                                                                    |
| --------------------- | ------------------------------------------------------------------------------------------------ |
| **Repository (repo)** | The project stored on GitHub.                                                                    |
| **GitHub account**    | Your personal account used to access GitHub.                                                     |
| **Contributor**       | Someone who has permission to make changes to a project.                                         |
| **File**              | A piece of information stored in the project.                                                    |
| **JSON**              | A structured format used to store the crafting data.                                             |
| **Commit**            | A saved set of changes in GitHub.                                                                |
| **Branch**            | A separate version of the project where changes can be made without immediately changing `main`. |
| **Pull Request (PR)** | A request for your changes to be reviewed and added to the project.                              |
| **Review**            | When another person checks your changes before they are merged.                                  |
| **Merge**             | Adding the approved changes into the project's main branch.                                      |
| **GitHub Actions**    | GitHub's automated system for running tasks.                                                     |
| **Workflow**          | A set of automated tasks performed by GitHub Actions.                                            |
| **Deployment**        | Publishing the updated project so people can use it.                                             |
| **`main` branch**     | The primary version of the project.                                                              |

---

# Troubleshooting

## "I can't edit the crafting.json file."

You probably do not have the required contributor permissions.

Contact an administrator and ask them to confirm that your GitHub account has contributor access to the Eryndlyn repository.

---

## "I don't see the Edit button."

Make sure you are:

1. Logged into GitHub.
2. Using the GitHub account that was given contributor access.
3. Looking at the correct repository and file.

If you still cannot see the Edit button, contact an administrator.

---

## "I don't know what to put in the JSON file."

Do not manually create or modify the JSON unless you have specifically been instructed to do so.

Go back to the Crafting App:

https://kaitlynmurray712-coder.github.io/Eryndlyn/CraftingApp/index.html

Make your changes there and click **COPY JSON**.

Then paste that copied JSON into `crafting.json`.

---

## "My Pull Request has a problem."

Contact an administrator and send them the link to your Pull Request.

Do not delete the Pull Request or make unrelated changes unless an administrator asks you to.

---

## "The GitHub Action failed."

First, make sure your Pull Request has been merged into `main`.

If it has been merged and the deployment workflow still fails, contact an administrator and send them the link to the failed workflow.

---

# You're Done!

Once:

* Your crafting changes are saved in GitHub
* Your Pull Request has been reviewed and merged
* The deployment workflow has completed successfully
* The Crafting App shows your changes

your update is complete.

Thank you for helping maintain the Eryndlyn Crafting App!
