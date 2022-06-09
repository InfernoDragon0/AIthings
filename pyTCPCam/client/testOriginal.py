import cv2

if __name__ == "__main__":
    stream = cv2.VideoCapture(0)
    while True:
        (available, frame) = stream.read()
        if available:
            cv2.imshow('clientFrame', frame)
        else:
            break
        cv2.waitKey(1)

    cv2.destroyAllWindows()