# DevExpert Slack Bot

This is a Python-based **AI Slack Bot** using the [OpenAI GPT-4](https://platform.openai.com/docs/models/gpt-4) model and MySQL for storing conversation data. The bot listens for mentions in a Slack channel and generates AI responses using OpenAI's API. All conversation data is then saved to a MySQL database.

## Dependencies

- Python 3.6 or later
- [OpenAI](https://github.com/openai/openai)
- [slack-bolt](https://github.com/slackapi/bolt-python) and [slack-sdk](https://github.com/slackapi/python-slack-sdk) Python libraries
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/) Python library
- [python-dotenv](https://pypi.org/project/python-dotenv/) Python library
- [SlackApi](https://api.slack.com/apps)

## Creating a Slack API App and Configuration

To create a Slack API App and configure the necessary settings, follow these steps:

1. Go to the [Slack API website](https://api.slack.com/apps) and sign in to your Slack account.

2. Click the **Create New App** button.

3. Choose a name for your app and select the workspace you want to develop it in, then click the **Create App** button.

4. Enable the **Event Subscriptions** feature in the app settings:

   a. Click on **Event Subscriptions** in the left sidebar.

   b. Toggle the **Enable Events** switch on.

   c. Enter the **Request URL** (you will provide this later, after deploying your bot).

   d. Scroll down to **Subscribe to bot events**, click **Add Bot User Event**, and add the following bot user event: `app_mention`.

5. Add the necessary OAuth Scopes:

   a. Click on **OAuth & Permissions** in the left sidebar.

   b. Scroll down to the **Bot Token Scopes** section and click the **Add an OAuth Scope** button.

   c. Add the following OAuth scopes: `app_mentions:read`, `chat:write`, and `users:read`.

6. Install the app to your workspace:

   a. Scroll up to the **Install App** section and click the **Install App to Workspace** button.

   b. Authorize the app in the prompted window.

7. Retrieve your app's tokens:

   a. After installing the app, you will be redirected to the **OAuth & Permissions** page.

   b. Copy the **Bot User OAuth Token** (starts with `xoxb-`) and paste it into your `.env` file as the value for `SLACK_BOT_TOKEN`.

   c. Copy the **App Token** (starts with `xapp-`) and paste it into your `.env` file as the value for `SLACK_APP_TOKEN`.

8. Set up a public-facing server or a tunneling service like [ngrok](https://ngrok.com/) to expose your bot's server to the internet, which is needed for Slack events to reach your bot.

9. Once your bot is running and your server is publicly accessible, go back to the **Event Subscriptions** settings on the Slack API website and update the **Request URL** with your bot's public URL followed by the endpoint path, e.g., `https://your-public-url.com/slack/events`.

10. Save your changes, and your Slack API app should now be configured and ready to use with the AI Slack Bot.

## Setting Up the Database and Server

To set up the MySQL database and server, follow these steps:

### MySQL Database Setup

1. Install MySQL Server on your machine, or use a cloud-based MySQL service. For installation instructions, refer to the [official MySQL documentation](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/).

2. Create a new MySQL database and user for the AI Slack Bot:

   a. Log in to your MySQL server using the command line or a GUI tool such as MySQL Workbench or phpMyAdmin.

   b. Run the following SQL command to create a new database (replace `your_database_name` with the desired name):

   ```
   CREATE DATABASE your_database_name;
   ```

   c. Run the following SQL command to create a new user and grant them privileges to the newly created database (replace `your_user_name`, `your_password`, and `your_database_name` with the appropriate values):

   ```
   CREATE USER 'your_user_name'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON your_database_name.* TO 'your_user_name'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. Create the `conversations` table in your MySQL database:

   a. Run the following SQL command to create the `conversations` table:

   ```sql
   CREATE TABLE conversations (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id VARCHAR(255) NOT NULL,
       user_input TEXT NOT NULL,
       ai_response TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

## Installation

1. Fork the repository and clone it:

```bash
git clone https://github.com/yourusername/ai-slack-bot.git
cd ai-slack-bot
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the template.env file to a new file named .env and update the values with your credentials:

```bash
cp template.env .env
```

4. Replace the placeholders with your actual credentials:

```bash
SLACK_APP_TOKEN=<My-SLACK_APP_TOKEN>
SLACK_BOT_TOKEN=<My-SLACK_BOT_TOKEN>
OPENAI_API_KEY=<My-OPENAI_API_KEY>
MYSQL_HOST=<MYSQL_HOST>
MYSQL_USER=<MYSQL_USER>
MYSQL_PASSWORD=<MYSQL_PASSWORD>
MYSQL_DATABASE=<MYSQL_DATABASE>
```

5. Run the bot:

```bash
python main.py
```
