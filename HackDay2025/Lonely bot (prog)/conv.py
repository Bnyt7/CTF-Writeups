import socket
import hashlib
import re
from deep_translator import GoogleTranslator

fusion_temp_celsius = 932  # Average value of 990 - 1025°C
fusion_temp_fahrenheit = 1709
fusion_temp_kelvin = 1205

# Train history years
train_electric = 1879
train_magnetic = 1979
train_vapor = 1804
train_diesel = 1925


def extract_md5_hash(data):
    match = re.search(r'/([a-f0-9]{32})/', data)
    if match:
        return match.group(1)  # Return the MD5 hash without slashes
    else:
        print("No MD5 hash found in the data!")
        return None


def crack_md5_hash(target_hash):
    with open('/usr/share/wordlists/rockyou.txt', 'r', encoding='latin-1') as f: #change to your rockyou.txt location
        for i, line in enumerate(f):
            if i >= 100:  # First 100 lines only
                break
            word = line.strip()
            md5_hash = hashlib.md5(word.encode()).hexdigest()
            if md5_hash == target_hash:
                return word
    return None

def handle_hash_cracking(data):
    # Extract MD5 hash from the data
    target_hash = extract_md5_hash(data)
    
    if target_hash:
        print(f"Extracted MD5 hash: {target_hash}")
        password = crack_md5_hash(target_hash)

        if password:
            print(f"Password found: {password}")
            return password
            
        else:
            print("Password not found in the first 100 lines of rockyou.txt.")
    else:
        print("Failed to extract the MD5 hash from the data.")


def main():
    # Server details (change to another port if slow)
    host = "challenges.hackday.fr"
    port = 41524

    # Establish connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected to the server.")

        # Helper to send data
        def send(data):
            s.sendall(data.encode())
            print(f"Sent: {data}")

        # Read all available data from the server, for some steps you have to wait a little to get the actual question
        def receive(timeout=1.0):
            data = b""
            s.settimeout(timeout)  # Set timeout
            try:
                while True:
                    chunk = s.recv(1024)
                    if not chunk:  # Connection closed
                        break
                    data += chunk
            except socket.timeout:
                pass
            decoded_data = data.decode()
            print(decoded_data)
            return decoded_data

        
        answers = [] # Store answers for later (1,2,3,4)
        bot_name ="" # Bot's name, final question
        data = receive(timeout=2.0)  # Longer timeout for initial responses
        if "Would you care to spend some time with me" in data:
            send("yes") 
            
            data = receive(timeout=1.0)

        if "Starting with the basics, the name!" in data:
            match = re.search(r"Mine is ([^\n]+)", data)
            if match:
                bot_name = match.group(1)  # Extract the bot's name
                print(f"Bot's name: {bot_name}")
            else:
                print("Bot's name not found in the data!")
            send("a") # My name
            answers.append("a")  # Store the answer
            data = receive(timeout=1.1)

        if "fusion temperature of brass" in data:
            # Respond based on the requested unit
            if "Celsius" in data or "celsius" in data:
                send(str(fusion_temp_celsius))
                answers.append(str(fusion_temp_celsius)) 
            elif "Fahrenheit" in data or "fahrenheit" in data:
                send(str(fusion_temp_fahrenheit))
                answers.append(str(fusion_temp_fahrenheit))  
            elif "Kelvin" in data or "kelvin" in data:
                send(str(fusion_temp_kelvin))
                answers.append(str(fusion_temp_kelvin))
            else:
                send(str(fusion_temp_celsius))  # Default to Celsius if not specified
                answers.append(str(fusion_temp_celsius))  # Store the answer
            data = receive(timeout=1.2)

        # First train, doesn't always work even if it's correct answer. When in doubt rerun.
        if "When was the first" in data:
            if "electric" in data:
                send(str(train_electric))
                answers.append(str(train_electric)) 
            elif "magnetic suspension" in data:
                send(str(train_magnetic))
                answers.append(str(train_magnetic))
            elif "vapor" in data:
                send(str(train_vapor))
                answers.append(str(train_vapor))
            elif "diesel" in data: #Date might not be correct, but the three others work so just rerun
                send(str(train_diesel))
                answers.append(str(train_diesel))  
            data = receive(timeout=1.5)

        if "Can't have you on this point" in data:
            # Direct matching for known encoded strings (only three different strings)
            if "SSBrbm93IG1hbnkgZW5jb2RpbmcgYmFzZXMsIGJ1dCB3aGljaCBvbmUgaSdtIHVzaW5nLi4uPyAod3JpdGUgeW91ciBhbnN3ZXIgaW4gbG93ZXJjYXNlIGxpa2UgJ2Jhc2U2NCcp" in data:
                send("base64")
                answers.append("base64") 
            elif "Ng!)(Z+9SVVQzUKWo~0{WNB_^AYx&2WpgYbVs&&NcW7y2XdrKHWguxMZ6I}XX>MmOE-pVHD0gycbY&oUZ*_7YVQzDGWpW^CZXj%LcV%*8VRL05Y-wv{ASYsBb7eL(Cn*" in data:
                send("base85")
                answers.append("base85")
            else:
                print("base32")
                send("base32")
                answers.append("base32")
            data = receive(timeout=2.0)

        if "While you wait, can you hash the previous answers" in data:
            # Concatenate all the collected answers (1,2,3,4) then hash
            concatenated_answers = ",".join(answers)  # Join all answers into one string
            print(f"Concatenated answers: {concatenated_answers}")

            if "sha1" in data:
                hash_value = hashlib.sha1(concatenated_answers.encode()).hexdigest()
            elif "sha512" in data:
                hash_value = hashlib.sha512(concatenated_answers.encode()).hexdigest()
            elif "sha256" in data:
                hash_value = hashlib.sha256(concatenated_answers.encode()).hexdigest() 
            else:
                hash_value = hashlib.md5(concatenated_answers.encode()).hexdigest()  # Default to MD5 if no other is specified

            send(hash_value)  
            data = receive(timeout=2.0)
        
        # Rock Paper Scissors
        if "Let's keep talking!" in data:
            # Parse the bot's first move
            if "P" in data:  # Bot's first move is Paper
                send("S,P")  # Respond with Scissors (S) and then Paper (P)
            elif "R" in data:  # Rock
                send("P,S")  # Paper (P) and then Scissors (S)
            elif "S" in data:  # Scissors
                send("R,P")  # Rock (R) and then Paper (P)
            data = receive(timeout=2.0)  # Wait for the bot's second move and check result
        if "My first move is " in data:
            # Same thing
            if "P" in data: 
                send("S,P") 
            elif "R" in data:  
                send("P,S")
            elif "S" in data:
                send("R,P") 
            data = receive(timeout=1.2) 
        while "My first move is " in data:
            # There will be more than one match
            if "P" in data: 
                send("S,P")
            elif "R" in data: 
                send("P,S")
            elif "S" in data: 
                send("R,P")
            data = receive(timeout=1.2)  

        # Guess the number
        if "Let's start!" in data:
            low = 0
            high = 20
            tries = 5

            guess = (low + high) // 2 #First guess : 10
            print(f"Guessing: {guess}")
            send(str(guess))

            data = receive(timeout=1.0)

            if "Oups, it's smaller than that!" in data:
                high = guess - 1
            elif "Oups, it's bigger than that!" in data:
                low = guess + 1
            else:
                print("Guessed correctly")
                # Exit the loop since the number is found

            # If did not guess in the first try, continue till you win
            if ("you found it!" not in data):
                for i in range(tries):
                    guess = (low + high) // 2  
                    print(f"Guessing: {guess}")
                    send(str(guess)) 
                    data = receive(timeout=1.0)

                    if "Oups, it's smaller than that!" in data:
                        high = guess - 1  
                    elif "Oups, it's bigger than that!" in data:
                        low = guess + 1  
                    elif "you found it!" in data:
                        break 
                    else:
                        break 
        data = receive(timeout=2.0)

        # Detect language and extract words
        match = re.search(r'translate the word /([^/]+)/ in /([^/]+)/', data)
        if match:
            word_to_translate = match.group(1)
            target_language = match.group(2)

            # Print the extracted words for verification
            print(f"Word to translate: {word_to_translate}")
            print(f"Target language: {target_language}")

            # Use the deep-translator package for the translation
            try:
                # Initialize the Google Translator from deep-translator
                translated_word = GoogleTranslator(source='auto', target=target_language.lower()).translate(word_to_translate)
                print(f"Translated word: {translated_word}")
                send(translated_word)  
                data = receive(timeout=1.0)

            except Exception as e:
                print(f"Error during translation: {e}")
        else:
            print("No valid translation request found in the input!")

        # Get a hash, find the password related to it (only the first hundred lines fro rockyou.txt)
        if "Here's the hash:" in data:       
            password = handle_hash_cracking(data)
            send(password)
            data = receive(timeout=1.2)
        # The color of Henri IV's (color) horse
        if "Wow, you're a hacker!" in data :
            answer = ""
            match = re.search(r"What's the color of Henri IV's (\w+) horse\?", data)
            if match:
                color = match.group(1)  # Extracted color
                send(color)
            data = receive(timeout=1.2)
        # Which day are we
        if "Not bad, you're not colorblind!" in data :
            if "Which day are we? (dd/mm/yyyy)" in data :
                send("26/1/2025") #Change date to today's date here , if value < 10, don't add 0 (1 instead of 01)
                data = receive(timeout=1.2)
        # What is the bot's name (very first question)
        if "Bravo, you know your calendar!" in data:
            if "my name?" in data:
                send(bot_name)
                data = receive(timeout=1.2)

if __name__ == "__main__":
    main()
