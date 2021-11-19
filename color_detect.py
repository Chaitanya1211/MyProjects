
import cv2
import requests
from colormap import rgb2hex

img = cv2.imread("login.jpg")

# declaring global variables (are used later on)
clicked = False
r = g = b = x_pos = y_pos = 0

def Convert(string):
    list1=[]
    list1[:0]=string
    list1.remove('#')
    new_hex = "".join(list1)
    return new_hex
# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    hex = rgb2hex(R, G, B)
    url = 'https://colornames.org/search/json/?hex=' + Convert(hex)
    r = requests.get(url)
    cname = r.json()['name']
    return str(cname)


# function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        #this img[] return back the BGR value of the image
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('image')
#setmouse call back : Call the required function whenever the mouse is clicked
cv2.setMouseCallback('image', draw_function)

while True:

    cv2.imshow("image", img)
    if clicked:
        #
        # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()

