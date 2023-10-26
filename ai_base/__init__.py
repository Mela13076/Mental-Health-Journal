import random

happy_sentences = ["Congratulations on your well-deserved success! You've earned it.",
                   "You've worked so hard for this achievement, and now it's time to celebrate!",
                   "Well done! Your dedication and determination have paid off.",
                   "This accomplishment is a testament to your talent and commitment. Bravo!",
                   "You've reached a new milestone, and I couldn't be happier for you.",
                   "You make the impossible look easy. Congratulations on your outstanding performance.",
                   "Your success is an inspiration to us all. Keep up the great work!",
                   "Wishing you continued success and even greater achievements in the future.",
                   "You've proven once again that hard work and perseverance lead to greatness.",
                   "The world is a better place with your talent and accomplishments. Congratulations!"]
cheer_up_sentences = ["Don't worry; tough times don't last forever, but tough people do!",
                      "You've got the strength to overcome any obstacle that comes your way.",
                      "Every day is a fresh start, a new chance to make things better.",
                      "Remember, even in the darkest clouds, there's a silver lining waiting for you.",
                      "You're capable of achieving amazing things, and I believe in you.",
                      "Happiness is just around the corner; keep going, and you'll find it.",
                      "Life's challenges are opportunities in disguise, and you're well-equipped to seize them.",
                      "Your smile can brighten someone's day, including your own. So, keep smiling!",
                      "Surround yourself with positivity, and you'll attract even more good vibes.",
                      "You're not alone; there are people who care about you and are here to support you."]
anxious_sentences = ["Take a deep breath and remember that you're stronger than your anxiety.",
                     "Anxiety is just a passing cloud; it will soon give way to clearer skies.",
                     "You are not alone in this. I'm here to support you through your anxious moments.",
                     "It's okay to feel anxious; it's a normal human emotion. Be kind to yourself.",
                     "Try to focus on the present moment, and let go of worries about the future.",
                     "Imagine a place or memory that brings you peace, and take yourself there mentally.",
                     "Remember, you've overcome anxious moments before, and you will do it again.",
                     "Reach out to someone you trust and share your feelings. You don't have to go through this alone.",
                     "Engage in a calming activity, like deep breathing, meditation, or a soothing walk.",
                     "This too shall pass, and brighter, calmer days are ahead. You've got this!"]
neutral_sentences = ["Okay!",
                     "That\'s interesting!",
                     "I see!",
                     "Awesome! What else?",
                     "Alright!",
                     "Let\'s make some progress!",
                     "That's a fascinating point. Can you elaborate a bit further?",
                     "It's great to have this conversation with you; I'm learning a lot.",
                     "I'm intrigued by your experiences. Could you share more details?",
                     "Let's delve deeper into this. What do you think are the key factors at play?"]
other_sentences = ["Today is a beautiful day, filled with sunshine and smiles.",
                   "I just received some fantastic news that made my day.",
                   "Happiness is a choice, and I choose to be happy every day.",
                   "Spending time with loved ones always brings joy to my heart.",
                   "The laughter of children playing is a melody that warms the soul.",
                   "I'm grateful for the little things in life that bring me happiness.",
                   "Sunsets by the beach are a reminder of life's simple, beautiful moments.",
                   "Achieving your goals and dreams can fill your heart with pure happiness.",
                   "A warm hug from a friend can turn a gloomy day into a bright one.",
                   "Kindness is the key to a happier world, and I'm spreading it every day."]


def get_ai_answer(input_string, mood):
    mood = mood.lower()
    if mood == 'happy':
        return random.choice(happy_sentences)
    elif mood == 'sad':
        return random.choice(cheer_up_sentences)
    elif mood == 'anxious':
        return random.choice(anxious_sentences)
    elif mood == 'neutral':
        return random.choice(neutral_sentences)
    else:
        return random.choice(other_sentences)


if __name__ == '__main__':
    print('This is the AI package.')
