# Telegram Quiz and Learning Bot with OpenAI Integration

This is a Telegram bot that leverages the OpenAI API to generate quizzes and provide learning summaries based on user input and uploaded documents. The bot supports multiple document types, including `.txt`, `.docx`, and `.pdf` files. Users can choose to either generate a quiz or learn about a specific topic.

## Features

1. **Document-Based Quiz Generation**:
   - Supports `.txt`, `.docx`, and `.pdf` files.
   - Generates multiple-choice quizzes based on the content of uploaded documents.

2. **Learning Mode**:
   - Provides a summary of a user-provided topic.
   - Offers to generate a quiz based on the summarized topic.

3. **User Interaction**:
   - Users can choose between "quiz" and "learn" modes.
   - After learning, users are prompted to generate a quiz based on the topic they just learned about.

## Prerequisites

- **Python 3.8+**
- **Telegram Bot Token** (from [BotFather](https://core.telegram.org/bots#botfather))
- **OpenAI API Key** (from [OpenAI Platform](https://platform.openai.com/))

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/telegram-quiz-learning-bot.git
   cd telegram-quiz-learning-bot
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the project directory with the following content:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```

5. **Dependencies**:
   Ensure the following libraries are installed:
   ```bash
   pip install python-telegram-bot openai python-docx PyPDF2 python-dotenv
   ```

## Usage

1. **Run the Bot**:
   ```bash
   python openaiQuiz.py
   ```

2. **Start the Bot in Telegram**:
   - Open your Telegram app.
   - Start a conversation with your bot by sending `/start`.

3. **Interact with the Bot**:
   - Type `quiz` to generate a quiz from an uploaded document.
   - Type `learn` to learn about a topic and optionally generate a quiz.

## Bot Commands

- **`/start`**: Start the bot and choose between "quiz" and "learn" modes.
- **`/cancel`**: Cancel the current operation.

## How It Works

### States

- **CHOOSING**: The initial state where the user chooses between "quiz" and "learn".
- **PROCESS_DOCUMENT**: Handles document uploads and generates quizzes.
- **LEARNING_MODE**: Summarizes the user-provided topic and asks if they want to generate a quiz.

### Functions

- **`process_document`**: Processes uploaded documents (`.txt`, `.docx`, `.pdf`) and generates a quiz.
- **`learning_mode`**: Summarizes a topic and prompts the user to generate a quiz.
- **`generate_quiz`**: Generates a multiple-choice quiz using the OpenAI API.
- **`summarize_topic`**: Summarizes a topic using the OpenAI API.

## Example Interaction

1. **Start the Bot**:
   ```
   /start
   ```
   Bot: "Hello! Do you want to 'generate a quiz' or 'learn about a topic'? Please type 'quiz' or 'learn'."

2. **Choose Learning Mode**:
   ```
   learn
   ```
   Bot: "Please send me the topic you want to learn about."

3. **Provide a Topic**:
   ```
   Artificial Intelligence
   ```
   Bot: "Summarizing the topic... Please wait."

4. **Get Summary**:
   Bot: "[Summary of Artificial Intelligence]"

   Bot: "Would you like to generate a quiz on this topic? (yes/no)"

5. **Generate Quiz**:
   ```
   yes
   ```
   Bot: "Generating quiz on the topic... Please wait."

   Bot: "[Quiz Generated Based on Topic]"

## Error Handling

- If an unsupported file type is uploaded, the bot responds with an error message.
- If the OpenAI API call fails, the bot returns an appropriate error message.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [OpenAI API](https://platform.openai.com/)
- [Python Telegram Bot Library](https://python-telegram-bot.readthedocs.io/)

## Contact

For any inquiries or support, please contact [your email or GitHub profile link].
