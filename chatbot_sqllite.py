import sqlite3
import re

# Common words used to check if they are keywords
common_words = ["what", "difference", 'between', "is", 'be', "a", 'an', "how", "do", "does", "in", "the", "context",
                "of", "and", "to", "for", "with", "on", "at", "by", "from", "can", "explain", "you", "are", 'I',
                'concept', 'role']


def format_answer(answer):
    """Formats the answer to make it more readable for the user"""
    char_limit = 100
    current_line = ""

    for word in answer.split():
        if len(current_line + word) <= char_limit:
            current_line += word + " "
        else:
            print(current_line.strip())
            current_line = word + " "

    if current_line:
        print(current_line.strip())


def get_answer(user_input):
    """Checks if the user input question exists in the database with defined questions and answers"""
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT answer FROM qa_pairs WHERE question = ?', (user_input.lower(),))
        result = cursor.fetchone()

        if result:
            return result[0]

        # Use the same method from [analyze mood] assignment to analyze input
        words = re.findall(r'\w+', user_input.lower())
        for word in words:
            if word in common_words:
                continue
            cursor.execute('SELECT answer FROM qa_pairs WHERE question LIKE ?', ('%' + word + '%',))
            result = cursor.fetchone()
            if result:
                return result[0]

        # If there are no keywords entered by the user in the question list,
        # check if there are any in the answer
        for word in words:
            if word in common_words:
                continue
            cursor.execute('SELECT answer FROM qa_pairs WHERE answer LIKE ?', ('%' + word + '%',))
            result = cursor.fetchone()
            if result:
                return result[0]

        return "I'm sorry, I don't have an answer for this question."

    finally:
        conn.close()


# Main loop
def main():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Hello! I'm Chatbot for AI related questions. Do you have any questions?")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    while True:
        user_input = input("Your question: ")
        # Exception handling for unexpected input
        try:
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            answer = get_answer(user_input)
            print("¨¨¨¨¨¨¨¨¨¨¨")
            print("Chatbot:")
            format_answer(answer)
            print("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨")
            print("(Enter 'exit' to end the conversation)")
        except KeyError:
            print(
                "Chatbot: Sorry, I didn't understand that. It seems that I still need to continue learning. Perhaps "
                "you can try a different question. \n(Enter 'exit' to end the conversation)")


if __name__ == "__main__":
    main()
