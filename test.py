import cv2
import random
import time
import mediapipe as mp

# Initialize the webcam
cap = cv2.VideoCapture(0)

# List of text choices
text_choices = ["ask Kars for a Candy", "community service", "go code", "keep playing ping pong until you win one game",  "you won 10 intra dollars", "Do 10 push ups now ", "just be grateful today", "you won 10 black hole days", "do ft_split in less than 10 minutes and get a t-shirt"]

# Display each text for 0.1 seconds (adjust as needed)
display_duration = 0.1
word_display_duration = 5  # Duration to display the chosen word
home_screen_duration = 5  # Duration for the home screen message

# Initialize MediaPipe Hand object
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# State variables
current_state = "home_screen"  # Indicates the current state of the program
chosen_word = ""  # Stores the chosen word when iteration is stopped
state_start_time = time.time()  # Start time for the current state
word_index = 0

# Futura font for displaying text
font_path = cv2.FONT_HERSHEY_DUPLEX
big_font_scale = 2
small_font_scale = 1

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Get the dimensions of the frame
    height, width, _ = frame.shape
    
    current_time = time.time()
    elapsed_time = current_time - state_start_time
    
    if current_state == "home_screen":
        # Display the "To Start : Raise 1 Hand" message on the home screen
        message_line1 = "To Start : Raise 1 Hand"
        message_line2 = "To Stop: Raise Second Hand"
        
        text_size = cv2.getTextSize(message_line1, font_path, big_font_scale, 2)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2 - 50
        
        cv2.putText(frame, message_line1, (text_x, text_y), font_path, big_font_scale, (0, 255, 255), 2, cv2.LINE_AA)
        
        text_size = cv2.getTextSize(message_line2, font_path, big_font_scale, 2)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2 + 50
        
        cv2.putText(frame, message_line2, (text_x, text_y), font_path, big_font_scale, (0, 255, 255), 2, cv2.LINE_AA)
        
        # Detect hands in the frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        # If one hand is raised, move to word iteration state
        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 1:
            current_state = "word_iteration"
            state_start_time = current_time
    elif current_state == "word_iteration":
        if elapsed_time > display_duration:
            # Move to the next word after the display duration
            word_index += 1
            if word_index >= len(text_choices):
                word_index = 0  # Reset index for continuous iteration
            state_start_time = current_time
        
        # Get the current word to display
        current_text = text_choices[word_index]
        
        # Display the current word
        text_size = cv2.getTextSize(current_text, font_path, big_font_scale, 2)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2
        cv2.putText(frame, current_text, (text_x, text_y), font_path, big_font_scale, (255, 0, 255), 2, cv2.LINE_AA)
        
        # Detect both hands raised to move to chosen word state
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
            current_state = "chosen_word"
            chosen_word = current_text
            state_start_time = current_time
    elif current_state == "chosen_word":
        # Display the chosen word
        text_size = cv2.getTextSize(chosen_word, font_path, big_font_scale, 2)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2
        cv2.putText(frame, chosen_word, (text_x, text_y), font_path, big_font_scale, (0, 255, 0), 2, cv2.LINE_AA)
        
        # After 5 seconds, move to home screen state
        if elapsed_time > word_display_duration:
            current_state = "home_screen"
            state_start_time = current_time
    
    cv2.imshow('Text Overlay', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()