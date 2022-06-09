import cv2

if __name__ == "__main__":
    stream = cv2.VideoCapture("rtsp://admin:amarisipc1@192.168.1.64:554/Streaming/Channels/101/")
    while True:
        (available, frame) = stream.read()
        if available:
            cv2.imshow('clientFrame', frame)
        else:
            break
        cv2.waitKey(1)

    cv2.destroyAllWindows()