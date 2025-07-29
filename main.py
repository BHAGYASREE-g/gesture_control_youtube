import cv2
import mediapipe as mp
import pyautogui
import webbrowser
import time

# Open YouTube
webbrowser.open("https://www.youtube.com")
time.sleep(5)  # wait for browser to load

# MediaPipe hands setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

cap = cv2.VideoCapture(0)

def count_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4

    fingers = []

    # Thumb (compare x instead of y)
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other 4 fingers
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

last_action = None

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            finger_count = count_fingers(handLms)

            # Actions based on finger count
            if finger_count == 0 and last_action != 'mute':
                pyautogui.press("m")  # mute
                last_action = 'mute'
                print("Muted")
            elif finger_count == 1 and last_action != 'volume_up':
                pyautogui.press("volumeup")
                last_action = 'volume_up'
                print("Volume Up")
            elif finger_count == 2 and last_action != 'volume_down':
                pyautogui.press("volumedown")
                last_action = 'volume_down'
                print("Volume Down")
            elif finger_count == 5 and last_action != 'playpause':
                pyautogui.press("space")
                last_action = 'playpause'
                print("Play/Pause")
            else:
                pass

    else:
        last_action = None  # reset if no hand detected

    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
